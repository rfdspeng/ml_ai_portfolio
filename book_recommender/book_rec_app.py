import streamlit as st
# from models.agents import BookRetriever, BookAssistant
import os
from openai import OpenAI
from qdrant_client import QdrantClient
import sys

stream = True

class BookRetriever:
    def __init__(self, credentials, collection_name, top_k=5):
        self.llm_client = OpenAI(api_key=credentials["OPENAI_API_KEY"])
        self.vectordb_client = QdrantClient(
            url=credentials["QDRANT_URL"],
            api_key=credentials["QDRANT_API_KEY"],
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
    def __init__(self, llm_api_key, system_message="You are a bookstore assistant assisting customers with finding a book to read that fits their preferences.", model="gpt-3.5-turbo"):
        self.llm_client = OpenAI(api_key=llm_api_key)
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

    def respond(self, user_query="", search_results=[], stream=False):
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
            pass

        # Response
        response = self.llm_client.chat.completions.create(
            messages = self.messages_list,
            model = self.model,
            stream = stream,
        )

        if not stream:
            output = response.choices[0].message.content
            self.messages_list.append({"role": "assistant", "content": output})
            return output
        else:
            # output = ""
            # for chunk in response:
            #     if chunk.choices[0].delta.content is not None:
            #         output = output + chunk.choices[0].delta.content
            # self.messages_list.append({"role": "assistant", "content": output})
            return response

st.title("Welcome to the bookstore!")

# Initialize session_state
if "retriever" not in st.session_state:
    collection_name = "best-book-ever"
    st.session_state["retriever"] = BookRetriever(st.secrets.credentials, collection_name)
    st.session_state["assistant"] = BookAssistant(st.secrets.credentials["OPENAI_API_KEY"])
    st.session_state.messages = [] # I don't want to use assistant.messages_list since it exposes the search results from the retriever

retriever = st.session_state["retriever"]
assistant = st.session_state["assistant"]

# Display chat messages from history on app rerun
# Skip first message since it's the system message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# First time in the bookstore
if st.session_state.messages == []:
    with st.spinner("..."):
        welcome = assistant.respond(stream=stream)
    with st.chat_message("assistant"):
        if not stream:
            st.markdown(welcome)
            response = welcome
        else:
            response = st.write_stream(welcome)
            assistant.messages_list.append({"role": "assistant", "content": response})

    st.session_state.messages.append({"role": "assistant", "content": response})

# This expression assigns the user's input to prompt and checks that it's not None
if prompt := st.chat_input("Your turn"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("..."):
        search_results = retriever.retrieve(prompt)
        # response = assistant.respond(prompt, search_results)
        # with st.chat_message("assistant"):
        #     st.markdown(response)
        response = assistant.respond(prompt, search_results, stream=stream)
    with st.chat_message("assistant"):
        if not stream:
            st.markdown(response)
        else:
            response = st.write_stream(response)
            assistant.messages_list.append({"role": "assistant", "content": response})

    st.session_state.messages.append({"role": "assistant", "content": response})