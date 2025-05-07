// lib/bedrock-chatbot-stack.ts
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as s3deploy from 'aws-cdk-lib/aws-s3-deployment';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as origins from 'aws-cdk-lib/aws-cloudfront-origins';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import * as path from 'path';
import * as cr from 'aws-cdk-lib/custom-resources';
import * as logs from 'aws-cdk-lib/aws-logs';

export interface BedrockChatbotStackProps extends cdk.StackProps {
  modelId?: string;
}

export class BedrockChatbotStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: BedrockChatbotStackProps) {
    super(scope, id, props);

    const modelId = props?.modelId || 'us.amazon.nova-lite-v1:0';

    // Cognito User Poolの作成
    const userPool = new cognito.UserPool(this, 'ChatbotUserPool', {
      userPoolName: 'chatbot-user-pool',
      selfSignUpEnabled: true,
      signInAliases: {
        email: true,
        username: false,
      },
      standardAttributes: {
        email: {
          required: true,
          mutable: true,
        },
      },
      autoVerify: {
        email: true,
      },
      passwordPolicy: {
        minLength: 8,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: false,
      },
      accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
    });

    // User Pool Clientの作成
    const userPoolClient = new cognito.UserPoolClient(this, 'ChatbotUserPoolClient', {
      userPool,
      authFlows: {
        userPassword: true,
        userSrp: true,
      },
      generateSecret: false,
      oAuth: {
        flows: {
          implicitCodeGrant: true,
          authorizationCodeGrant: true,
        },
        scopes: [cognito.OAuthScope.EMAIL, cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE],
        callbackUrls: ['http://localhost:3000'],
      },
      readAttributes: new cognito.ClientAttributes().withStandardAttributes({
        email: true,
        emailVerified: true,
        phoneNumber: true,
        fullname: true,
      }),
      writeAttributes: new cognito.ClientAttributes().withStandardAttributes({
        email: true,
        phoneNumber: true,
        fullname: true,
      }),
    });

    // S3バケットの作成
    const websiteBucket = new s3.Bucket(this, 'WebsiteBucket', {
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      cors: [
        {
          allowedHeaders: ['*'],
          allowedMethods: [
            s3.HttpMethods.GET,
            s3.HttpMethods.HEAD,
          ],
          allowedOrigins: ['*'],
          maxAge: 3000,
        },
      ],
    });

    // CloudFront Distribution
    const distribution = new cloudfront.Distribution(this, 'Distribution', {
      defaultBehavior: {
        origin: new origins.S3Origin(websiteBucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
        allowedMethods: cloudfront.AllowedMethods.ALLOW_GET_HEAD_OPTIONS,
        cachedMethods: cloudfront.CachedMethods.CACHE_GET_HEAD_OPTIONS,
        compress: true,
      },
      defaultRootObject: 'index.html',
      errorResponses: [
        {
          httpStatus: 403,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
        },
        {
          httpStatus: 404,
          responseHttpStatus: 200,
          responsePagePath: '/index.html',
        },
      ],
      enableIpv6: true,
    });

    // CloudFront URLをユーザープールクライアントのコールバックURLに追加
    userPoolClient.node.addDependency(distribution);
    
    const cfnUserPoolClient = userPoolClient.node.defaultChild as cognito.CfnUserPoolClient;
    cfnUserPoolClient.callbackUrLs = [
      `https://${distribution.distributionDomainName}`,
      'http://localhost:3000',
    ];

    // Lambda実行ロールを作成
    const lambdaRole = new iam.Role(this, 'ChatLambdaRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
      ]
    });

    // Bedrockへのアクセス権限を追加
    lambdaRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'bedrock:InvokeModel',
        'bedrock:InvokeModelWithResponseStream'
      ],
      resources: ['*']
    }));

    // Lambda function
    const chatFunction = new lambda.Function(this, 'ChatFunction', {
      runtime: lambda.Runtime.PYTHON_3_10,
      handler: 'index.lambda_handler',
      code: lambda.Code.fromAsset(path.join(__dirname, '../lambda')),
      timeout: cdk.Duration.seconds(30),
      memorySize: 128,
      role: lambdaRole,
      environment: {
        MODEL_ID: modelId,
      },
    });

    // 明示的な依存関係を追加
    const cfnChatFunction = chatFunction.node.defaultChild as lambda.CfnFunction;
    const cfnLambdaRole = lambdaRole.node.defaultChild as iam.CfnRole;
    cfnChatFunction.addDependsOn(cfnLambdaRole);

    // API Gateway with Cognito Authorizer
    const api = new apigateway.RestApi(this, 'ChatbotApi', {
      restApiName: 'Bedrock Chatbot API',
      description: 'API for Bedrock Converse chatbot',
      defaultCorsPreflightOptions: {
        allowOrigins: apigateway.Cors.ALL_ORIGINS,
        allowMethods: apigateway.Cors.ALL_METHODS,
        allowHeaders: ['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'X-Amz-Security-Token'],
        allowCredentials: true,
      },
    });

    // Cognito Authorizer
    const authorizer = new apigateway.CognitoUserPoolsAuthorizer(this, 'ChatbotAuthorizer', {
      cognitoUserPools: [userPool],
    });

    const chatResource = api.root.addResource('chat');
    chatResource.addMethod('POST', new apigateway.LambdaIntegration(chatFunction), {
      authorizer,
      authorizationType: apigateway.AuthorizationType.COGNITO,
    });

    // 設定生成用のLambdaロールを作成
    const configGeneratorRole = new iam.Role(this, 'ConfigGeneratorRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
      managedPolicies: [
        iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
      ]
    });
    
    // S3とCloudFrontへのアクセス権限を追加
    configGeneratorRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        's3:GetObject',
        's3:PutObject'
      ],
      resources: [
        `${websiteBucket.bucketArn}/*`
      ]
    }));
    
    configGeneratorRole.addToPolicy(new iam.PolicyStatement({
      actions: [
        'cloudfront:CreateInvalidation'
      ],
      resources: ['*']
    }));
    
    // 設定生成用のLambda関数
    const configGeneratorFunction = new lambda.Function(this, 'ConfigGeneratorFunction', {
      runtime: lambda.Runtime.NODEJS_18_X,
      handler: 'index.handler',
      role: configGeneratorRole,
      code: lambda.Code.fromInline(`
        // AWS SDK v3 のインポート
        const { S3Client, GetObjectCommand, PutObjectCommand } = require('@aws-sdk/client-s3');
        const { CloudFrontClient, CreateInvalidationCommand } = require('@aws-sdk/client-cloudfront');
        const fs = require('fs');
        const path = require('path');
        const https = require('https');
        const url = require('url');
        
        exports.handler = async (event, context) => {
          console.log('Event:', JSON.stringify(event, null, 2));
          
          try {
            if (event.RequestType === 'Delete') {
              return await sendResponse(event, context, 'SUCCESS');
            }
            
            const {
              WebsiteBucketName,
              ApiEndpoint,
              UserPoolId,
              UserPoolClientId,
              Region,
              FrontendSourcePath,
              CloudFrontDistributionId
            } = event.ResourceProperties;
            
            // S3クライアントの初期化
            const s3Client = new S3Client({ region: Region });
            
            // 設定ファイルの内容を作成
            const configContent = {
              REACT_APP_API_ENDPOINT: ApiEndpoint,
              REACT_APP_USER_POOL_ID: UserPoolId,
              REACT_APP_USER_POOL_CLIENT_ID: UserPoolClientId,
              REACT_APP_REGION: Region
            };
            
            // config.jsファイルを作成
            const configJsContent = \`
              window.REACT_APP_CONFIG = {
                apiEndpoint: "\${ApiEndpoint}",
                userPoolId: "\${UserPoolId}",
                userPoolClientId: "\${UserPoolClientId}",
                region: "\${Region}"
              };
            \`;
            
            // config.jsファイルをS3にアップロード
            await s3Client.send(new PutObjectCommand({
              Bucket: WebsiteBucketName,
              Key: 'config.js',
              Body: configJsContent,
              ContentType: 'application/javascript'
            }));
            console.log('Uploaded config.js to S3');
            
            // index.htmlを取得して修正
            try {
              const indexHtmlResponse = await s3Client.send(new GetObjectCommand({
                Bucket: WebsiteBucketName,
                Key: 'index.html'
              }));
              
              // StreamをStringに変換
              const bodyContents = await streamToString(indexHtmlResponse.Body);
              let indexHtml = bodyContents;
              
              // config.jsを読み込むスクリプトタグを追加
              if (!indexHtml.includes('config.js')) {
                indexHtml = indexHtml.replace('</head>', '<script src="/config.js"></script></head>');
                
                // 修正したindex.htmlをアップロード
                await s3Client.send(new PutObjectCommand({
                  Bucket: WebsiteBucketName,
                  Key: 'index.html',
                  Body: indexHtml,
                  ContentType: 'text/html'
                }));
                console.log('Modified and uploaded index.html');
              }
            } catch (error) {
              console.log('Error processing index.html:', error);
              // index.htmlが見つからない場合は無視
            }
            
            // CloudFrontキャッシュの無効化
            if (CloudFrontDistributionId) {
              const cloudfrontClient = new CloudFrontClient({ region: Region });
              await cloudfrontClient.send(new CreateInvalidationCommand({
                DistributionId: CloudFrontDistributionId,
                InvalidationBatch: {
                  CallerReference: Date.now().toString(),
                  Paths: {
                    Quantity: 2,
                    Items: ['/index.html', '/config.js']
                  }
                }
              }));
              console.log('Created CloudFront invalidation');
            }
            
            return await sendResponse(event, context, 'SUCCESS');
          } catch (error) {
            console.error('Error:', error);
            return await sendResponse(event, context, 'FAILED', { Error: error.message });
          }
        };
        
        // StreamをStringに変換するヘルパー関数
        async function streamToString(stream) {
          return new Promise((resolve, reject) => {
            const chunks = [];
            stream.on('data', (chunk) => chunks.push(chunk));
            stream.on('end', () => resolve(Buffer.concat(chunks).toString('utf-8')));
            stream.on('error', reject);
          });
        }
        
        async function sendResponse(event, context, status, data = {}) {
          const responseBody = {
            Status: status,
            Reason: data.Error || 'See CloudWatch logs for details',
            PhysicalResourceId: context.logStreamName,
            StackId: event.StackId,
            RequestId: event.RequestId,
            LogicalResourceId: event.LogicalResourceId,
            Data: data
          };
          
          console.log('Sending response:', JSON.stringify(responseBody));
          
          return new Promise((resolve, reject) => {
            const parsedUrl = url.parse(event.ResponseURL);
            const options = {
              hostname: parsedUrl.hostname,
              port: 443,
              path: parsedUrl.path,
              method: 'PUT',
              headers: {
                'Content-Type': '',
                'Content-Length': Buffer.byteLength(JSON.stringify(responseBody))
              }
            };
            
            const req = https.request(options, (res) => {
              console.log(\`Response status code: \${res.statusCode}\`);
              resolve();
            });
            
            req.on('error', (error) => {
              console.error('Error sending response:', error);
              reject(error);
            });
            
            req.write(JSON.stringify(responseBody));
            req.end();
          });
        }
      `),
      timeout: cdk.Duration.minutes(5),
      memorySize: 512,
      environment: {
        NODE_OPTIONS: '--enable-source-maps',
      },
    });
    
    // 明示的な依存関係を追加
    const cfnConfigFunction = configGeneratorFunction.node.defaultChild as lambda.CfnFunction;
    const cfnConfigRole = configGeneratorRole.node.defaultChild as iam.CfnRole;
    cfnConfigFunction.addDependsOn(cfnConfigRole);
    
    // カスタムリソースプロバイダー
    const configProvider = new cr.Provider(this, 'ConfigProvider', {
      onEventHandler: configGeneratorFunction,
      logRetention: logs.RetentionDays.ONE_DAY,
    });
    
    // カスタムリソース
    const configResource = new cdk.CustomResource(this, 'ConfigResource', {
      serviceToken: configProvider.serviceToken,
      properties: {
        WebsiteBucketName: websiteBucket.bucketName,
        ApiEndpoint: `${api.url}chat`,
        UserPoolId: userPool.userPoolId,
        UserPoolClientId: userPoolClient.userPoolClientId,
        Region: this.region,
        FrontendSourcePath: '../frontend/build',
        CloudFrontDistributionId: distribution.distributionId,
        // 変更があった場合に再実行されるようにタイムスタンプを追加
        Timestamp: new Date().toISOString(),
      },
    });
    
    // S3デプロイメントの後に設定を生成するように依存関係を設定
    const websiteDeployment = new s3deploy.BucketDeployment(this, 'DeployWebsite', {
      sources: [s3deploy.Source.asset(path.join(__dirname, '../frontend/build'))],
      destinationBucket: websiteBucket,
      distribution,
      distributionPaths: ['/*'],
    });
    
    // 依存関係を設定
    configResource.node.addDependency(websiteDeployment);

    // Outputs
    new cdk.CfnOutput(this, 'CloudFrontURL', {
      value: `https://${distribution.distributionDomainName}`,
      description: 'The URL of the CloudFront distribution',
    });

    new cdk.CfnOutput(this, 'ApiGatewayURL', {
      value: api.url,
      description: 'The URL of the API Gateway endpoint',
    });

    new cdk.CfnOutput(this, 'ModelId', {
      value: modelId,
      description: 'The Bedrock model ID being used',
    });

    new cdk.CfnOutput(this, 'UserPoolId', {
      value: userPool.userPoolId,
      description: 'The ID of the Cognito User Pool',
    });

    new cdk.CfnOutput(this, 'UserPoolClientId', {
      value: userPoolClient.userPoolClientId,
      description: 'The ID of the Cognito User Pool Client',
    });
  }
}