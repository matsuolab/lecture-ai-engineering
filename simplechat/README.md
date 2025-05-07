# Bedrock Chatbot with Cognito Authentication

Amazon Bedrock を使用したチャットボットアプリケーションで、Amazon Cognito による認証機能を備えています。

## 機能

- Amazon Bedrock の LLM モデル（Nova Lite または micro）を使用したチャット機能
- Amazon Cognito によるユーザー認証
- API Gateway による安全な API アクセス
- CloudFront + S3 によるフロントエンドホスティング
- AWS CDK を使用したインフラのコード化

## アーキテクチャ

![Architecture Diagram](./architecture.png)

## 前提条件

- [Node.js](https://nodejs.org/) (v14 以上)
- [AWS CLI](https://aws.amazon.com/cli/) (設定済み)
- [AWS CDK](https://aws.amazon.com/cdk/) (v2)
- [Python](https://www.python.org/) (v3.9 以上)

## セットアップ手順


### 重要: Bedrockモデルアクセス許可の設定

このアプリケーションを使用するには、AWS Bedrockのモデルへのアクセス許可が必要です。
以下の手順でモデルアクセスを有効にしてください：

1. AWS Managementコンソールにログイン
2. Amazon Bedrockサービスが利用可能なリージョンに移動
3. 左側のナビゲーションから「モデルアクセス」を選択
4. 使用するモデル（例：us.amazon.nova-lite-v1:0）の横にあるチェックボックスをオンにする
5. 画面下部の「次へ」ボタンをクリックし、内容を確認の上、「送信」をクリックする

* Cross Region Inferenceが有効となっているリージョンを推奨します。
* アクセス許可がない状態で環境をセットアップした場合、チャットボットは500エラーを返します。


### 1. リポジトリのクローン

```
git clone https://github.com/keisskaws/simplechat
cd simplechat
```

### 2. CDK プロジェクトの依存関係 && フロントエンドのビルド
```
npm install
```

### 3. AWS アカウントのブートストラップ（初回のみ）
```
npx cdk bootstrap
```

### 4. CDK スタックのデプロイ
```
npx cdk deploy
```

### 5. アプリケーションへのアクセス
デプロイ出力に表示された CloudFront URL にアクセスしてアプリケーションを使用します。

使用方法
CloudFront URL にアクセスします
「サインアップ」をクリックして新しいアカウントを作成します
登録したメールアドレスに送信された確認コードを入力します
ログイン後、チャットインターフェースが表示されます
メッセージを入力して Amazon Bedrock モデルと対話します
カスタマイズ
別の Bedrock モデルの使用
bin/bedrock-chatbot.ts ファイルを編集して、使用するモデルを変更できます：

```
typescript 

new BedrockChatbotStack(app, 'BedrockChatbotStack', {
  modelId: 'us.amazon.nova-micro-v1:0',
  // ...
});
```


### フロントエンドのカスタマイズ
フロントエンドのコードは frontend/src ディレクトリにあります。React コンポーネントを編集してカスタマイズできます。



### クリーンアップ
プロジェクトのリソースを削除するには以下のコマンドを実行します


```
npx cdk destroy
```


### トラブルシューティング
# API 呼び出しエラー
Cognito トークンが正しく設定されているか確認してください
API Gateway の CORS 設定が正しいか確認してください
CloudWatch Logs で Lambda 関数のログを確認してください

# 認証エラー
ユーザープールの設定を確認してください
フロントエンドの環境変数が正しく設定されているか確認してください
