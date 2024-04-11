import json
import os
from typing import Dict, Any

import boto3
import urllib3
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain_community.chat_models import BedrockChat
from langchain_community.retrievers import AmazonKnowledgeBasesRetriever

http = urllib3.PoolManager()
bedrock_runtime = boto3.client('bedrock-runtime')
load_dotenv('.env')
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')


def knowledge(query: str) -> Dict[str, Any]:
    try:
        llm = BedrockChat(
            model_id="anthropic.claude-v2:1",
            model_kwargs={
                "temperature": 0
            }
        )

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
        print(query)
        # TODO: streamで返す？
        return qa.invoke(query)
    except Exception as e:
        print(e)


def is_slack_retry(event: Dict[str, Any]) -> bool:
    request_header = event["headers"]
    keys = request_header.keys()
    return "x-slack-retry-num" in keys and "x-slack-retry-reason" in keys and request_header[
        "x-slack-retry-reason"] == "http_timeout"


def lambda_handler(event: Dict[str, Any], context):
    if (is_slack_retry(event)):
        return {
            'statusCode': 200,
            'body': {
                'message': 'No need to resend'
            }
        }
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
    input_text = body["event"]["text"]
    print("-------debug: input_text--------")
    print(input_text)
    res = knowledge(input_text)
    msg = {
        "channel": "#general",
        "username": "",
        "text": f"{res['result']}",
        "icon_emoji": ""
    }

    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST', WEB_HOOK_URL, body=encoded_msg)
    print({
        "message": f"{res}",
        "status_code": resp.status,
        "response": resp.data
    })

# r = knowledge("西さんについて教えてください。回答はマークダウン記法をで出力してください。")
# print(r['result'])
