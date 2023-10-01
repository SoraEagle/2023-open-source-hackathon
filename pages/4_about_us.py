import requests
import streamlit as st
import pandas as pd
from common import *
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="The Team",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="auto"
)

st.sidebar.header("About the project")
def load_lottieurl(url: str ):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_url_hello = "https://lottie.host/19223a39-36e6-4231-b509-912a9965b8f9/xTdcZRz7xz.json"

lottie_hello = load_lottieurl(lottie_url_hello)







df = pd.DataFrame(
    {
        "GitHub": [
            "https://github.com/kagemni",
            "https://github.com/prettyXD",
            "https://github.com/soraEagle",
            "https://github.com/jer8miah",
        ]
    },
    index=["Knights", "Rex", "Sora", "Jeremiah"],
)


def make_clickable(link):
    text = link.split("/")[-1]
    return f'<a target="_blank" href="{link}">{text}</a>'


df["GitHub"] = df["GitHub"].apply(make_clickable)
df = df.to_html(escape=False)
st.sidebar.write(df, unsafe_allow_html=True)


#tab1 = st.tabs(["ENGLISH"])

#selected_tab = st.sidebar.selectbox("Select Tab", ["Project"])

st.markdown("# Git scraper : GitHub Chatbot🤖\n")
#if selected_tab == "Project":
with st.container():
    col1, col2 = st.columns([3,1.5])
    with col1:
        

        st.write(
            """
            Created mainly with the help of Python, ChatGPT, and MongoDB, this is an GitHub web scraper,
            where an user can search for GitHub repositories they would like to look into, and
            ChatGPT would explain the repository to them.
            """
            )

        #st.markdown("## ??")
        #st.write(
        #    """
        #    biography
        #    """
        #)
        st.markdown("## Open Source *:blue[Hack]:grey[fest]* ")
        st.write(
                """
                The inspiration for our project came from the **Event Description** for the :rainbow[MLH] **Open Source Hackfest**, which was to make a project that "_promotes the principle of sharing knowledge for the benefit of the wider community_".
When the team thought about it, we all agreed that, pairing ChatGPT with an web scraper and database would do _just that_!
                """
        )
        st.markdown("\n")
        st.markdown("## Features")
        st.markdown(
            """
            - Summarization of the user's GitHub page.
            - Visualization of the chosen repository's file structure
            - Provides  code analysis 
         """
        )

with col2:
    st_lottie(lottie_hello, key="hello", height=675)
