import json
import os

import boto3
import urllib3
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import BedrockChat
from langchain.retrievers import AmazonKnowledgeBasesRetriever

http = urllib3.PoolManager()


bedrock_runtime = boto3.client('bedrock-runtime')
load_dotenv('.env')
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')


def knowledge(name: str):
    try:
        llm = BedrockChat(
            model_id="anthropic.claude-v2:1",
            model_kwargs={
                "temperature": 0
            }
        )

        print('--------debug: knowledge id--------')
        print(KNOWLEDGE_BASE_ID)
        retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=KNOWLEDGE_BASE_ID,
            retrieval_config={
                "vectorSearchConfiguration": {
                    "numberOfResults": 4
                }
            }
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type='stuff',
            retriever=retriever,
            verbose=True
        )
        query = f"{name}さんについて教えてください"
        print(query)
        result = qa.run(query)
        # TODO: streamで返す？
        return result
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    print('---------START---------')
    print(event)
    body = json.loads(event['body'])

    # Slackイベントの検証
    # Slackにこのchallenge値を返すことで、エンドポイントの検証を行います。
    if "challenge" in body:
        challenge = body['challenge']
        return {
            "statusCode": 200,
            "body": json.dumps({"challenge": challenge})
        }
    # lambdaからSlackに返答するためのWebHookURL
    print('--------START: knowledge--------')
    res = knowledge('西')
    print('--------END: knowledge--------')
    msg = {
        "channel": "#general",
        "username": "",
        "text": f"${res}",
        "icon_emoji": ""
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    print('--------START: REQUEST--------')
    resp = http.request('POST', WEB_HOOK_URL, body=encoded_msg)
    print('--------END: REQUEST--------')
    print({
        "message": f"{res}",
        "status_code": resp.status,
        "response": resp.data
    })
