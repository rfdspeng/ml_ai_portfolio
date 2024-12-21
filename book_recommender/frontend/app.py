import streamlit as st
import httpx
import json
import asyncio
from uuid import uuid4
import os

stream = False

async def get_assistant_response(userquery: dict[str, str]) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(os.getenv("BACKEND_ENDPOINT", "http://localhost:8000/chat/"), json=userquery)
        response.raise_for_status()
        return response.json()["response"]

st.title("Welcome to the bookstore!")

# Initialize session_state
if "userid" not in st.session_state:
    st.session_state.userid = str(uuid4())
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# First time in the bookstore
if st.session_state.messages == []:
    with st.spinner("..."):
        userquery = {"userid": st.session_state.userid, "message": ""}
        response = asyncio.run(get_assistant_response(userquery))

    with st.chat_message("assistant"):
        if not stream:
            st.markdown(response)
        else:
            response = st.write_stream(response)
            # assistant.messages_list.append({"role": "assistant", "content": response})

    st.session_state.messages.append({"role": "assistant", "content": response})

# This expression assigns the user's input to prompt and checks that it's not None
if prompt := st.chat_input("Your turn"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("..."):
        userquery = {"userid": st.session_state.userid, "message": prompt}
        response = asyncio.run(get_assistant_response(userquery))

    with st.chat_message("assistant"):
        if not stream:
            st.markdown(response)
        else:
            response = st.write_stream(response)
            # assistant.messages_list.append({"role": "assistant", "content": response})

    st.session_state.messages.append({"role": "assistant", "content": response})