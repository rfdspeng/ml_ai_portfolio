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
        # Decode request
        try:
            decodedEvent = json.loads(event["body"])
            userid = decodedEvent["userid"]
            message = decodedEvent["message"]
        except (KeyError, json.JSONDecodeError) as e:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid request body", "details": str(e)})
            }

        credentials = dict(dotenv_values(".env"))
        retriever = BookRetriever(credentials, collection_name="best-book-ever", top_k=5)
        assistant = BookAssistant(credentials["OPENAI_API_KEY"])

        try:
            query = UserQuery(userid=userid, message=message)
            search_results = await retrieve(query, retriever)
            response = await assistant.respond(user_query=message, search_results=search_results, stream=False)
        except Exception as e:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Internal server error", "details": str(e)})
            }
        
        return {
            "statusCode": 200,
            "body": json.dumps({"response": response})
        }
    
    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Path not found"})
    }