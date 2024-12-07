import os
from openai import OpenAI
from qdrant_client import QdrantClient
import sys



class BookRetriever:
    def __init__(self, collection_name, top_k=5):
        self.llm_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.vectordb_client = QdrantClient(
            url=os.environ["QDRANT_URL"],
            api_key=os.environ["QDRANT_API_KEY"],
        )
        self.collection_name = collection_name
        self.top_k = top_k # number of entries to retrieve

    def _embed_(self, user_query):
        response = self.llm_client.embeddings.create(input=user_query, model="text-embedding-ada-002")
        return response.data[0].embedding

    def retrieve(self, user_query):
        self.user_query = user_query
        self.query_vector = self._embed_(user_query)

        self.search_results = self.vectordb_client.search(
            collection_name = self.collection_name,
            query_vector = self.query_vector,
            limit = self.top_k,
        )
        return self.search_results

class BookAssistant:
    def __init__(self, system_message="You are a bookstore assistant assisting customers with finding a book to read that fits their preferences.", model="gpt-3.5-turbo"):
        self.llm_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.messages_list = [{"role": "system", "content": system_message}]
        self.model = model
    
    def _search_results_to_context_(self, search_results):
        hits = []
        for hdx, hit in enumerate(search_results):
            title = hit.payload.get("title", "Unknown title")
            author = hit.payload.get("author", "Unknown author")
            description = hit.payload.get("description", "No description available.")
            genres = hit.payload.get("genres", "Unknown genre")

            # Truncate descriptor for brevity
            if len(description) > 150:
                description = description[:150] + "..."

            # Format hit information
            hitstr = (
                f"Result #{hdx + 1}:\n"
                f"Title: {title}\n"
                f"Author: {author}\n"
                f"Description: {description}\n"
                f"Genres: {genres}\n"
            )
            hits.append(hitstr)

        # Combine all hits into a single string
        context = "\n".join(hits)
        return context

    def respond(self, user_query="", search_results=[]):
        if search_results != []: # if search results aren't empty, append them to the user query
            self.search_results = search_results
            context = self._search_results_to_context_(search_results)
            content = (
                f"User message: {user_query}\n"
                f"Related books in stock:\n---\n"
                f"{context}"
            )
            self.messages_list.append({"role": "user", "content": content})
            
        elif user_query != "": # if search results are empty, use the user query directly
            self.messages_list.append({"role": "user", "content": user_query})

        else: # if there is no user query (e.g. upon first loading the application)
            "Do nothing." 

        # Response
        response = self.llm_client.chat.completions.create(
            messages = self.messages_list,
            model = self.model,
        )

        output = response.choices[0].message.content
        self.messages_list.append({"role": "assistant", "content": output})

        return output

def main(collection_name):
    retriever = BookRetriever(collection_name)
    chatbot = BookAssistant()
    print(chatbot.respond())
    user_query = "Hello! Do you have any fantasy books featuring dragons?"
    search_results = retriever.retrieve(user_query)
    print(chatbot.respond(user_query, search_results))

if __name__ == "__main__":
    collection_name = sys.argv[1] if len(sys.argv) > 1 else "best-book-ever"
    main(collection_name)