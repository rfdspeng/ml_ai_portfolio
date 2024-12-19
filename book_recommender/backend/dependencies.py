from fastapi import Depends, Request
from typing import Annotated
from backend.models.retriever import BookRetriever
from backend.routers.chat import UserQuery
from qdrant_client.models import ScoredPoint

async def get_bookretriever(request: Request) -> BookRetriever:
    return request.app.state.bookretriever

async def retrieve(retriever: Annotated[BookRetriever, Depends(get_bookretriever)], query: UserQuery = Depends()) -> list[ScoredPoint]:
    search_results = retriever.retrieve(query)
    return search_results

# async def retrieve(query: str, retriever: Annotated[BookRetriever, Depends(get_bookretriever)]) -> list[ScoredPoint]:
#     search_results = retriever.retrieve(query)
#     return search_results

# async def retrieve(query: UserQuery = Depends(), retriever: Annotated[BookRetriever, Depends(get_bookretriever)]) -> list[ScoredPoint]:
#     search_results = retriever.retrieve(query)
#     return search_results