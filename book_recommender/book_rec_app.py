import streamlit as st
from agents import BookRetriever, BookAssistant
# import os
# import time
# import random

st.title("Welcome to the bookstore!")

stream = False

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
    welcome = assistant.respond(stream=stream)
    with st.chat_message("assistant"):
        if not stream:
            st.markdown(welcome)
            response = welcome
        else:
            response = st.write_stream(welcome)
            # st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# This expression assigns the user's input to prompt and checks that it's not None
if prompt := st.chat_input("Your turn"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
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
    st.session_state.messages.append({"role": "assistant", "content": response})