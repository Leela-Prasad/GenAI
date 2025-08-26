import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
open_ai_key = os.environ["OPENAI_API_KEY"]

client = OpenAI()


def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0):
    response1 = client.responses.create(model=model,
                                        input=messages,
                                        temperature=temperature)

    return response1.output[0].content[0].text


st.title("Chatbot with Streamlit")

prompt = st.chat_input("write something...")

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = get_completion_from_messages(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)


