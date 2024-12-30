import streamlit as st
from agents import BookRetriever, BookAssistant
# import os
# import time
# import random

st.title("Welcome to the bookstore!")

stream = True

assistant = BookAssistant(st.secrets.credentials["OPENAI_API_KEY"])
response = assistant.respond(stream=stream)

with st.chat_message("assistant"):
    response_text = st.write_stream(response)

# st.write(response)

# response_txt = ""
# for chunk in response:
#     if chunk.choices[0].delta.content is not None:
#         response_txt = response_txt + chunk.choices[0].delta.content

# st.write(response_txt)
# myiter = []
# with st.chat_message("assistant"):
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             st.markdown(chunk.choices[0].delta.content)
#             myiter = myiter.append(chunk.choices[0].delta.content)

# myiter = iter(myiter)

