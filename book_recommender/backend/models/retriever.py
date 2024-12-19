from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import ScoredPoint

class BookRetriever:
    def __init__(self, credentials: dict, collection_name: str, top_k: int=5):
        self.llm_client = OpenAI(api_key=credentials["OPENAI_API_KEY"]) # AsyncOpenAI
        self.vectordb_client = QdrantClient(
            url=credentials["QDRANT_URL"],
            api_key=credentials["QDRANT_API_KEY"],
        )
        self.collection_name = collection_name
        self.top_k = top_k # number of entries to retrieve

    # async
    def _embed_(self, user_query: str) -> list:
        response = self.llm_client.embeddings.create(input=user_query, model="text-embedding-ada-002") # await
        return response.data[0].embedding

    # async
    def retrieve(self, user_query: str) -> list[ScoredPoint]:
        self.user_query = user_query
        self.query_vector = self._embed_(user_query)

        self.search_results = self.vectordb_client.search( # await
            collection_name = self.collection_name,
            query_vector = self.query_vector,
            limit = self.top_k,
        )
        return self.search_results
    
    def close(self) -> None:
        self.vectordb_client.close()