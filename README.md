# slack-to-bedrok
Slack sends a message to AWS bedrok.

# 概要

SlackのメッセージをAWSのBedrokに送信するLambda関数です。

# 構成

- python3.12

# ステップ 1: 仮想環境の作成
まず、Lambda関数で使用するPythonパッケージを分離するために、仮想環境を作成します。これにより、システム全体にインストールされているパッケージとの競合を避けることができます。

## Python 3.xがインストールされていることを確認
```
python3 --version
```

## 仮想環境の作成
```
python3 -m venv venv
```

## 仮想環境のアクティベート
```
source venv/bin/activate
```


# ステップ 2: 必要なパッケージのインストール
仮想環境内で、langchainを含む必要なPythonパッケージをインストールします。必要に応じて、その他の依存関係もここでインストールします。

## langchain とその他必要なパッケージのインストール
```
pip install -r requirements.txt

# 書き出す場合
pip freeze > requirements.txt
```

# ステップ 3: Lambda関数のデプロイ

Lambda関数をデプロイするために、AWS CLIを使用します。AWS
CLIがインストールされていない場合は、[こちら](https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-install.html)
の手順に従ってインストールしてください。

## ビルド

```
sam build
sam deploy --guided
```

## デプロイ

ビルドが成功したら、アプリケーションをAWSにデプロイします。
初めてデプロイする場合は、以下のコマンドを実行してデプロイプロセスをガイドします。

このコマンドは、デプロイに関する一連の質問を行い、その設定をsamconfig.tomlに保存します。
後続のデプロイでは、sam deployを直接実行するだけで済みます。

```
# 初回
sam deploy --guided

# 次回から
sam deploy
```
