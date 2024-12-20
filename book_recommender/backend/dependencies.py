from fastapi import Depends, Request
from typing import Annotated
from backend.models import BookRetriever, UserQuery
from qdrant_client.models import ScoredPoint

# 1 instance of BookRetriever per application, defined in app lifespan and stored in app.state.bookretriever
async def get_bookretriever(request: Request) -> BookRetriever:
    return request.app.state.bookretriever

# Apparently UserQuery = Depends() signals to FastAPI that it should look at the dependent function for UserQuery object
async def retrieve(query: UserQuery, retriever: Annotated[BookRetriever, Depends(get_bookretriever)]) -> list[ScoredPoint] | None:
    if query.message == "":
        return None
    
    search_results = await retriever.retrieve(query.message)
    return search_results