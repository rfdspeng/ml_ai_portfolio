from fastapi import APIRouter, Depends
# from fastapi.responses import StreamingResponse
from asyncio import Lock
from typing import Annotated
from pydantic import BaseModel
from backend.models.assistant import BookAssistant
from backend.dependencies import retrieve
from qdrant_client.models import ScoredPoint

class UserQuery(BaseModel):
    userid: int
    message: str

router = APIRouter()

bookassistants = {}
assistant_locks = {}

async def get_or_create_assistant(userid: int) -> BookAssistant:
    if userid not in bookassistants:
        bookassistants[userid] = await BookAssistant(llm_api_key)
    return bookassistants[userid]

@router.post("/")
async def chat(query: UserQuery, search_results: Annotated[list[ScoredPoint], Depends(retrieve)]) -> dict[str, str]:
    userid = query.userid
    message = query.message

    # If multiple requests for the same userid come in, this can create a race condition for bookassistants and bookassistants[userid]
    # We want to lock down these resources so only one request has access at any given time
    async with assistant_locks.setdefault(userid, Lock()): # create a new lock for this userid if it doesn't exist
        bookassistants[userid] = await get_or_create_assistant(userid)
        response = await bookassistants[userid].respond(user_query=message, search_results=search_results, stream=False)

    return {"response", response}

async def get_or_create_assistant(userid: int) -> BookAssistant:
    if userid not in bookassistants:
        bookassistants[userid] = BookAssistant(llm_api_key)
    return bookassistants[userid]

@router.post("/")
async def chat(query: UserQuery, search_results: Annotated[list[ScoredPoint], Depends(retrieve)]) -> dict[str, str]:
    userid = query.userid
    message = query.message

    # Ensure a lock exists for this userid
    lock = assistant_locks.setdefault(userid, Lock())

    # Lock the entire critical section for this userid
    async with lock:
        # Get or create the assistant
        assistant = await get_or_create_assistant(userid)

        # Generate a response (assistant state is modified here)
        response = await assistant.respond(
            user_query=message,
            search_results=search_results,
            stream=False
        )

    return {"response": response}

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