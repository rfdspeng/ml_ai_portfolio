from fastapi import Depends, Request
from typing import Annotated
from backend.models import BookRetriever, UserQuery
from qdrant_client.models import ScoredPoint

# 1 instance of BookRetriever per application, defined in app lifespan and stored in app.state.bookretriever
async def get_bookretriever(request: Request) -> BookRetriever:
    return request.app.state.bookretriever

async def retrieve(query: UserQuery, retriever: Annotated[BookRetriever, Depends(get_bookretriever)]) -> list[ScoredPoint] | None:
    if query.message == "":
        return None
    
    search_results = await retriever.retrieve(query.message)
    return search_results