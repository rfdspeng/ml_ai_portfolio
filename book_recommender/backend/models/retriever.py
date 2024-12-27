from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import ScoredPoint

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
    
    async def retrieve(self, user_query: str) -> list[ScoredPoint]:
        query_vector = await self._embed_(user_query)

        search_results = await self.vectordb_client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=self.top_k,
        )
        return search_results
    
    async def close(self) -> None:
        await self.vectordb_client.close()