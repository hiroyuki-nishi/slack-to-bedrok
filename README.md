# slack-to-bedrok
Slack sends a message to AWS bedrok.

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
source mylambdaenv/bin/activate
```


# ステップ 2: 必要なパッケージのインストール
仮想環境内で、langchainを含む必要なPythonパッケージをインストールします。必要に応じて、その他の依存関係もここでインストールします。

## langchain とその他必要なパッケージのインストール
```
pip install -r requirements.txt

# 書き出す場合
pip freeze > requirements.txt
```

