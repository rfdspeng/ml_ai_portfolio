import json
from dotenv import dotenv_values
from models import BookRetriever, BookAssistant, UserQuery
from qdrant_client.models import ScoredPoint

CHAT_PATH = "/chat"

async def retrieve(query: UserQuery, retriever: BookRetriever) -> list[ScoredPoint] | None:
    if query.message == "":
        return None
    
    search_results = await retriever.retrieve(query.message)
    return search_results

async def lambda_handler(event, context):
    if event["rawPath"] == CHAT_PATH:
        decodedEvent = json.loads(event["body"])
        userid = decodedEvent["userid"]
        message = decodedEvent["message"]
        query = UserQuery(userid=userid, message=message)

        credentials = dict(dotenv_values(".env"))

        retriever = BookRetriever(credentials, collection_name="best-book-ever", top_k=5)
        assistant = BookAssistant(credentials["OPENAI_API_KEY"])

        search_results = await retrieve(query, retriever)
        response = await assistant.respond(user_query=message, search_results=search_results, stream=False)
        print(response)
        return {"response": response}