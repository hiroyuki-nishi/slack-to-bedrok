import os

import boto3
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.chat_models import BedrockChat
from langchain.retrievers import AmazonKnowledgeBasesRetriever

bedrock_runtime = boto3.client('bedrock-runtime')
load_dotenv('.env')
KNOWLEDGE_BASE_ID = os.getenv('KNOWLEDGE_BASE_ID')


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
    # parser = argparse.ArgumentParser(description="Chatbot")
    # parser.add_argument("--about", type=str, default="西")
    # name = parser.parse_args()
    # langchainを使用した処理をここに記述
    # この例では、受け取ったイベントの内容をそのまま返します
    print('--------START: knowledge--------')
    res = knowledge('西')
    print('--------END: knowledge--------')
    return {
        'statusCode': 200,
        'body': res
    }