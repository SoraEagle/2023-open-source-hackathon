import streamlit as st
from streamlit.components.v1 import html

DEFAULT_SELECT_VALUE = "Select repository"
MODEL_NAME = "gpt-3.5-turbo-16k"


def initialize_session():
    if not "initialized" in st.session_state:
        st.session_state["initialized"] = True
        st.session_state["repo_name"] = DEFAULT_SELECT_VALUE
        st.session_state["user_name"] = ""
        st.session_state["repo_url"] = ""
        st.session_state["visitied_list"] = []
        st.session_state["messages"] = []
        st.session_state["chat_memory"] = None


def handling_user_change():
    st.session_state["repo_name"] = DEFAULT_SELECT_VALUE
    st.session_state["repo_url"] = ""
