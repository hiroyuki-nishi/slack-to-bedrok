import json
import os
from typing import Dict, Any

import boto3
import urllib3
from botocore.exceptions import NoCredentialsError
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
    try:
        request_header = event["headers"]
        keys = request_header.keys()
        return "x-slack-retry-num" in keys and "x-slack-retry-reason" in keys and request_header[
            "x-slack-retry-reason"] == "http_timeout"
    except KeyError as e:
        return e


def output_file_to_s3(file_name: str):
    try:
        bucket_name = 'your_bucket_name'
        content = "This is a sample text file content."
        s3 = boto3.client('s3')
        s3.upload_file(file_name, 'output', file_name)

        # テキストファイルの作成と書き込み
        with open(file_name, 'w') as file:
            file.write(content)

        # ファイルをS3にアップロード
        s3.upload_file(file_name, bucket_name, file_name)

        print(f"File '{file_name}' successfully uploaded to S3 bucket '{bucket_name}'.")

        # 署名付きURLの生成
        signed_url = s3.generate_presigned_url('get_object',
                                               Params={'Bucket': bucket_name, 'Key': file_name},
                                               ExpiresIn=3600)  # URLの有効期限は1時間

        print(f"Signed URL to download the file: {signed_url}")
    except FileNotFoundError:
        print("Error: The file was not found.")
    except NoCredentialsError:
        print("Error: Credentials not available.")


def lambda_handler(event: Dict[str, Any], context):
    try:
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
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': {
                'message': 'Internal Server Error'
            }
        }


# r = knowledge("簡単なマークダウンファイルを作成してください")
# print(r['result'])
output_file_to_s3('output.txt')
