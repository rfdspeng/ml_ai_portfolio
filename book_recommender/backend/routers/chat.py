from fastapi import APIRouter, Depends
# from fastapi.responses import StreamingResponse
from asyncio import Lock
from typing import Annotated
from pydantic import BaseModel
from backend.models import BookAssistant, UserQuery
from backend.dependencies import retrieve
from qdrant_client.models import ScoredPoint
from dotenv import dotenv_values

router = APIRouter()

bookassistants = {}
assistant_locks = {}

def get_or_create_assistant(userid: int) -> BookAssistant:
    if userid not in bookassistants:
        llm_api_key = dict(dotenv_values(".env"))["OPENAI_API_KEY"]
        bookassistants[userid] = BookAssistant(llm_api_key)
    return bookassistants[userid]

@router.post("/")
async def chat(query: UserQuery, search_results: Annotated[list[ScoredPoint] | None, Depends(retrieve)]) -> dict[str, str]:
    userid = query.userid
    message = query.message

    # If multiple requests for the same userid come in, this can create a race condition for bookassistants and bookassistants[userid]
    # We want to lock down these resources so only one request has access at any given time
    async with assistant_locks.setdefault(userid, Lock()): # create a new lock for this userid if it doesn't exist and store in assistant_locks
        bookassistants[userid] = get_or_create_assistant(userid)
        response = await bookassistants[userid].respond(user_query=message, search_results=search_results, stream=False) # asynchronous chat completion

    return {"response": response}

# @router.post("/")
# async def chat(query: UserQuery) -> dict[str, str]:
#     userid = query.userid
#     message = query.message

#     return {f"{userid}": message}

"""
async def get_or_create_assistant(userid: int) -> BookAssistant:
    if userid not in bookassistants:
        async with assistant_locks.setdefault(userid, Lock()):
            if userid not in bookassistants:
                bookassistants[userid] = BookAssistant(llm_api_key)
    return bookassistants[userid]

@router.post("/")
async def chat(query: UserQuery, search_results: Annotated[list[ScoredPoint], Depends(retrieve)]):
    userid = query.userid
    message = query.message

    bookassistants[userid] = await get_or_create_assistant(userid)
    response = bookassistants[userid].respond(user_query=message, search_results=search_results, stream=True)

    return StreamingResponse(response, media_type="text/event-stream")
"""

"""
def get_or_create_assistant(userid: int) -> BookAssistant:
    if userid not in bookassistants:
        bookassistants[userid] = BookAssistant(llm_api_key)
    return bookassistants[userid]

@router.post("/")
async def chat(query: UserQuery, search_results: Annotated[list[ScoredPoint], Depends(retrieve)]) -> dict[str, str]:
    userid = query.userid
    message = query.message
    lock = Lock()

    await lock.acquire()
    try:
        bookassistants[userid] = get_or_create_assistant(userid)
        response = await bookassistants[userid].respond(user_query=message, search_results=search_results, stream=False)
    finally:
        lock.release()

    return {"response", response}
"""