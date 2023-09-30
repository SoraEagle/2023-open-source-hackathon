import streamlit as st
import pandas as pd
from common import *

st.set_page_config(page_title="The Team")

st.sidebar.header("About the project")

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


tab1 = st.tabs(["ENGLISH"])

with tab1:
    st.markdown("# Git scraper : GitHub Chatbot\n")

    st.write(
        """
       who knws
        """
    )

    st.markdown("## ??")
    st.write(
        """
       biography
        """
    )
    st.markdown("## Hackathon ")
    st.write(
        """
        did it for a hackathon
        """
    )
    st.markdown("\n")
    st.markdown("## Features")
    st.markdown(
        """
        featuresss
        """
    )
