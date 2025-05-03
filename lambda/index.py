import json
import os
# import boto3 # Bedrockを使わないのでコメントアウト
import re
import urllib.request # 追加: HTTPリクエスト用
from botocore.exceptions import ClientError


# Lambda コンテキストからリージョンを抽出する関数
def extract_region_from_arn(arn):
    # ARN 形式: arn:aws:lambda:region:account-id:function:function-name
    match = re.search('arn:aws:lambda:([^:]+):', arn)
    if match:
        return match.group(1)
    return "us-east-1"  # デフォルト値

# グローバル変数としてクライアントを初期化（初期値）
# bedrock_client = None # Bedrockを使わないのでコメントアウト

# モデルID
# MODEL_ID = os.environ.get("MODEL_ID", "us.amazon.nova-lite-v1:0") # Bedrockを使わないのでコメントアウト

def lambda_handler(event, context):
    try:
        # コンテキストから実行リージョンを取得し、クライアントを初期化
        # global bedrock_client # Bedrockを使わないのでコメントアウト
        # if bedrock_client is None: # Bedrockを使わないのでコメントアウト
        #     region = extract_region_from_arn(context.invoked_function_arn) # Bedrockを使わないのでコメントアウト
        #     bedrock_client = boto3.client('bedrock-runtime', region_name=region) # Bedrockを使わないのでコメントアウト
        #     print(f"Initialized Bedrock client in region: {region}") # Bedrockを使わないのでコメントアウト

        print("Received event:", json.dumps(event))

        # Cognitoで認証されたユーザー情報を取得
        user_info = None
        if 'requestContext' in event and 'authorizer' in event['requestContext']:
            user_info = event['requestContext']['authorizer']['claims']
            print(f"Authenticated user: {user_info.get('email') or user_info.get('cognito:username')}")

        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])

        print("Processing message:", message)
        # print("Using model:", MODEL_ID) # Bedrockを使わないのでコメントアウト

        # 会話履歴を使用
        messages = conversation_history.copy()

        # ユーザーメッセージを追加
        messages.append({
            "role": "user",
            "content": message
        })

        # --- ここからBedrock呼び出し部分をコメントアウト ---
        # Nova Liteモデル用のリクエストペイロードを構築
        # 会話履歴を含める
        # bedrock_messages = []
        # for msg in messages:
        #     if msg["role"] == "user":
        #         bedrock_messages.append({
        #             "role": "user",
        #             "content": [{"text": msg["content"]}]
        #         })
        #     elif msg["role"] == "assistant":
        #         bedrock_messages.append({
        #             "role": "assistant",
        #             "content": [{"text": msg["content"]}]
        #         })

        # invoke_model用のリクエストペイロード
        # request_payload = {
        #     "messages": bedrock_messages,
        #     "inferenceConfig": {
        #         "maxTokens": 512,
        #         "stopSequences": [],
        #         "temperature": 0.7,
        #         "topP": 0.9
        #     }
        # }

        # print("Calling Bedrock invoke_model API with payload:", json.dumps(request_payload))

        # invoke_model APIを呼び出し
        # response = bedrock_client.invoke_model(
        #     modelId=MODEL_ID,
        #     body=json.dumps(request_payload),
        #     contentType="application/json"
        # )

        # レスポンスを解析
        # response_body = json.loads(response['body'].read())
        # print("Bedrock response:", json.dumps(response_body, default=str))

        # 応答の検証
        # if not response_body.get('output') or not response_body['output'].get('message') or not response_body['output']['message'].get('content'):
        #     raise Exception("No response content from the model")

        # アシスタントの応答を取得
        # assistant_response = response_body['output']['message']['content'][0]['text']
        # --- Bedrock呼び出し部分ここまで ---

        # --- ここから自作API呼び出し部分を追加 ---
        api_url = "https://5bc5-34-125-197-63.ngrok-free.app" # あなたのngrok URL
        # FastAPIが受け付けるリクエストボディ形式に合わせてください (例: {"text": message})
        api_request_data = {"text": message}
        api_request_body = json.dumps(api_request_data).encode('utf-8')

        print(f"Calling custom API at {api_url} with body: {api_request_data}")

        req = urllib.request.Request(
            api_url,
            data=api_request_body,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as res:
                if res.status == 200:
                    api_response_body = json.loads(res.read().decode('utf-8'))
                    print(f"Custom API response: {api_response_body}")
                    # FastAPIが返す応答のキー名に合わせてください (例: 'generated_text', 'response'など)
                    assistant_response = api_response_body.get('response', "応答を取得できませんでした。") # 仮のキー名: 'response'
                else:
                     print(f"API Error: Status {res.status}")
                     assistant_response = f"APIエラーが発生しました (ステータス: {res.status})。"

        except urllib.error.URLError as e:
            print(f"URLError: {e.reason}")
            assistant_response = f"APIへの接続に失敗しました: {e.reason}"
        except Exception as e:
            print(f"An error occurred during API call: {e}")
            assistant_response = f"API呼び出し中に予期せぬエラーが発生しました: {e}"
        # --- 自作API呼び出し部分ここまで ---


        # アシスタントの応答を会話履歴に追加
        messages.append({
            "role": "assistant",
            "content": assistant_response
        })

        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": messages
            })
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        } 