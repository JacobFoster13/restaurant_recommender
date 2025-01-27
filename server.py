import os
import time
import streamlit as st
from backend import setup_model, generate_response, connect_users

def stream(response):
    for word in response.split():
        yield word + ' '
        time.sleep(0.03)

st.title("Dallas Restaurant Recommender")

@st.cache_resource()
def get_retriever():
    return setup_model()

retriever = get_retriever()

@st.cache_resource()
def get_user_db():
    return connect_users()

db = get_user_db()

# with st.container(border=True):
if 'chat' not in st.session_state:
    st.session_state.chat = []

for chat in st.session_state.chat:
    with st.chat_message(chat['role']):
        st.markdown(chat['content'])

if prompt := st.chat_input("What can I help you with?"):
    st.session_state.chat.append(
        {
            'role': 'user', 
            'content' : prompt
        }
    )

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = generate_response(prompt, retriever)
        st.write_stream(stream(response.content))
    
    st.session_state.chat.append(
        {
            'role': 'assistant',
            'content': response.content
        }
    )

print(st.session_state)

