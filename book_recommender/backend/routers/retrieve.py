from fastapi import APIRouter, Depends
from backend import dependencies
from backend.models.retriever import BookRetriever
from backend.routers.chat import UserQuery
from typing import Annotated
from qdrant_client.models import ScoredPoint

# router = APIRouter()

# @router.get("/")
# async def retrieve(query: UserQuery = Depends(), retriever: Annotated[BookRetriever, Depends(dependencies.get_bookretriever)]) -> list[ScoredPoint]:
#     search_results = retriever.retrieve(query)
#     return search_results