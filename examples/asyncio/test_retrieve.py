from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import ScoredPoint
import sys
import os
import asyncio

class BookRetriever:
    def __init__(self, credentials: dict, collection_name: str, top_k: int=5):
        self.llm_client = AsyncOpenAI(api_key=credentials["OPENAI_API_KEY"])
        self.vectordb_client = AsyncQdrantClient(
            url=credentials["QDRANT_URL"],
            api_key=credentials["QDRANT_API_KEY"],
        )
        self.collection_name = collection_name
        self.top_k = top_k # number of entries to retrieve

    async def _embed_(self, user_query: str) -> list:
        response = await self.llm_client.embeddings.create(input=user_query, model="text-embedding-ada-002")
        return response.data[0].embedding

    # async def retrieve(self, user_query: str) -> list[ScoredPoint]:
    #     self.user_query = user_query
    #     self.query_vector = await self._embed_(user_query)

    #     self.search_results = await self.vectordb_client.search( # await
    #         collection_name = self.collection_name,
    #         query_vector = self.query_vector,
    #         limit = self.top_k,
    #     )
    #     return self.search_results
    
    async def retrieve(self, user_query: str) -> list[ScoredPoint]:
        # Generate the embedding for the user's query
        query_vector = await self._embed_(user_query)

        # Perform the vector search and return results
        search_results = await self.vectordb_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=self.top_k,
        )
        return search_results
    
    async def close(self) -> None:
        await self.vectordb_client.close()

collection_name = "best-book-ever"
credentials = {"QDRANT_URL": os.getenv("QDRANT_URL"),
               "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY"),
               "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")}

retriever = BookRetriever(credentials, collection_name)

async def main():
    results = await asyncio.gather(retriever.retrieve("Do you have any fantasy books featuring dragons?"),
                                   retriever.retrieve("Do you have any memoirs by Asian-American authors?"),
                                   retriever.retrieve("Do you have any history books about South African apartheid?"))
    await retriever.close()
    return results

r1, r2, r3 = asyncio.run(main())

print("r1")
for hdx, hit in enumerate(r1):
    title = hit.payload.get("title", "Unknown title")
    print(title)
print("")

print("r2")
for hdx, hit in enumerate(r2):
    title = hit.payload.get("title", "Unknown title")
    print(title)
print("")

print("r3")
for hdx, hit in enumerate(r3):
    title = hit.payload.get("title", "Unknown title")
    print(title)
print("")