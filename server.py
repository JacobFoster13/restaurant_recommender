import os
import time
import streamlit as st
from utils import generate_title
from login_register import check_user, register_new_user
from backend import setup_model, generate_response, connect_users, save_chat, load_chats

def stream(response):
    for word in response.split():
        yield word + ' '
        time.sleep(0.03)

st.set_page_config(page_title="Dallas Restaurants", layout="wide")
st.title("Dallas Restaurant Recommender")

@st.cache_resource()
def get_retriever():
    return setup_model()

retriever = get_retriever()

@st.cache_resource()
def get_db():
    return connect_users()

db = get_db()

if 'email' not in st.session_state:
    st.session_state.email = False

if 'display_login' not in st.session_state:
    st.session_state.display_login = False

if 'chat' not in st.session_state:
    st.session_state.chat = []

if 'chat_id' not in st.session_state:
    st.session_state.chat_id = None

if not st.session_state.email:
    if st.button("Login / Sign-Up"):
        st.session_state.display_login = not st.session_state.display_login
        st.rerun()

if st.session_state.display_login and not st.session_state.email:
    st.markdown("### Welcome! Login to Dallas Restaurant Recs!")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("Login"):
            email = st.text_input("Your Email")
            password = st.text_input("Password", type='password')
            submit = st.form_submit_button("Log In")

            if submit:
                valid = check_user(email, password, db)
                if valid:
                    st.session_state.email = email
                    st.session_state.display_login = False
                    st.success("Welcome back!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    with tab2:
        with st.form("New User Registration"):
            new_email = st.text_input("Enter your email address")
            new_password = st.text_input("Choose your password", type='password')
            confirm = st.text_input("Confirm your password", type='password')
            submit_register = st.form_submit_button("Register")
            
            if submit_register:
                if new_password != confirm:
                    st.error("Passwords do not match.")
                elif register_new_user(new_email, new_password, db):
                    st.success("Welcome to Dallas Restaurant Recs! Thanks for joining!")
                    st.session_state.email = new_email
                    st.session_state.display_login = False
                    st.rerun()
                else:
                    st.error("This email is already in use. Log in or register with a different email.")

if st.session_state.email:
    st.sidebar.header("Chat History")
    user_chats = load_chats(st.session_state.email, db)

    for i, chat in enumerate(user_chats):
        if st.sidebar.button(f"{chat.get('title', 'Untitled Chat')}"):
            st.session_state.chat = chat['messages']
            st.session_state.chat_id = chat['_id']
            st.rerun()

    if st.sidebar.button("Start New Chat"):
        st.session_state.chat = []
        st.session_state.chat_id = None
        st.rerun()

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

    if st.session_state.email:
        if not st.session_state.chat_id:
            title = generate_title(prompt)
        else:
            title = None

        save_chat(
            st.session_state.email,
            st.session_state.chat,
            db, 
            st.session_state.chat_id,
            title
        )

print(st.session_state)

