import os
from openai import OpenAI
from qdrant_client import QdrantClient



class retriever:
    def __init__(self, collection_name, top_k=5):
        self.openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.qdrant_client = QdrantClient(
            url=os.environ["QDRANT_URL"],
            api_key=os.environ["QDRANT_API_KEY"],
        )
        self.collection_name = collection_name
        self.top_k = top_k # number of entries to retrieve

    def _embed_(self, user_query):
        response = self.openai_client.embeddings.create(input=user_query, model="text-embedding-ada-002")
        return response.data[0].embedding

    def retrieve(self, user_query):
        self.user_query = user_query
        self.query_vector = self._embed_(self, user_query)

        self.search_results = self.qdrant_client.search(
            collection_name = self.collection_name,
            query_vector = self.query_vector,
            limit = self.top_k,
        )

        hits = []
        for hdx, hit in enumerate(self.search_results):
            hitstr = f"Result #{hdx} \\n \
                        Title: {hit.payload["title"]} \\n \
                        Author: {hit.payload["author"]} \\n \
                        Description: \\n \
                        {hit.payload["description"]}"
            
            hits.append(hitstr)
        
        return "\\n\\n".join(hits)