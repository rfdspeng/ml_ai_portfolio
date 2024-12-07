import streamlit as st
from agents import BookRetriever, BookAssistant
# import os
# import time
# import random

# def response_generator():
#     response = random.choice(
#         [
#             "Hello there! How can I assist you today?",
#             "Hi, human! Is there anything I can help you with?",
#             "Do you need help?",
#         ]
#     )

#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)

st.title("Welcome to the bookstore!")

# Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# Initialize session_state
if "retriever" not in st.session_state:
    collection_name = "best-book-ever"
    st.session_state["retriever"] = BookRetriever(st.secrets.credentials, collection_name)
    st.session_state["assistant"] = BookAssistant(st.secrets.credentials["OPENAI_API_KEY"])
    st.session_state.messages = [] # I don't want to use assistant.messages_list since it exposes the search results from the retriever

# Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

retriever = st.session_state["retriever"]
assistant = st.session_state["assistant"]

# Display chat messages from history on app rerun
# Skip first message since it's the system message
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# First time in the bookstore
if st.session_state.messages == []:
    welcome = assistant.respond(stream=False)
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# This expression assigns the user's input to prompt and checks that it's not None
if prompt := st.chat_input("Your turn"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    search_results = retriever.retrieve(prompt)
    # response = assistant.respond(prompt, search_results)
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    stream = assistant.respond(prompt, search_results, stream=True)
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # with st.chat_message("user"):
    #     st.markdown(prompt)
    # st.session_state.messages.append({"role": "user", "content": prompt})

    # response = f"Echo: {prompt}"
    # with st.chat_message("assistant"):
    #     st.markdown(response)
    # st.session_state.messages.append({"role": "assistant", "content": response})

    # with st.chat_message("assistant"):
    #     response = st.write_stream(response_generator())
    # st.session_state.messages.append({"role": "assistant", "content": response})