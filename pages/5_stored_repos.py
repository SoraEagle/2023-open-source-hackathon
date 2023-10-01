import streamlit as st
import requests
import pymongo
from pymongo import MongoClient 
from datetime import datetime
import base64
from common import *
from io import BytesIO
from anytree import RenderTree
from streamlit_agraph import agraph, Node, Edge, Config
from streamlit_agraph.config import Config
from githubqa.get_info_from_api import github_api_call, get_repo_list, get_avatar_info
from PIL import Image

DEFAULT_SELECT_VALUE = "Select a Repo"

st.set_page_config(page_title="Stored Repositories (by Date)")

# MongoDB configuration
mongo_host = '127.0.0.1'
mongo_port = 27017
mongo_db_name = 'github-scraper'

client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db_name]
collection = db['github_repos']

# Commented out the GitHub User and GitHub Repository input fields
# github_username = st.text_input("GitHub User")
# repo_name = st.text_input("GitHub Repository")

st.sidebar.title("`Git Scraper")
st.session_state["user_name"] = st.sidebar.text_input(
    "GitHub Username:",
    key="github_user_input",
    placeholder="input GitHub username",
    value=st.session_state["user_name"],
    on_change=handling_user_change,
)

# Sidebar Select Repo + User Avatar layout
if st.session_state["user_name"]:
    user_name = st.session_state["user_name"]
    repo_list_tuple = get_repo_list(user_name)  # Remove [0]
    repo_list = list(repo_list_tuple)  # Convert the tuple to a list
    user_info = get_avatar_info(user_name)
    if repo_list:  # Check if the returned value is not empty
        repo_list = [DEFAULT_SELECT_VALUE] + repo_list
        if st.session_state["repo_name"] not in repo_list:
            st.session_state["repo_name"] = repo_list[0]  # Set to the first item as a fallback
        st.session_state["repo_name"] = st.sidebar.selectbox(
            f"Select {user_name}'s repository",
            repo_list,
            key="repo_select"
        )
        if st.session_state["repo_name"] != DEFAULT_SELECT_VALUE:
            st.session_state[
                "repo_url"
            ] = f"https://github.com/{st.session_state['user_name']}/{st.session_state['repo_name']}"
        avatar_url = user_info["avatar_url"]
        image_response = requests.get(avatar_url)
        image = Image.open(BytesIO(image_response.content)).resize((250, 250))
        st.sidebar.image(
            image, use_column_width="always", caption=f"{user_name}'s profile"
        )
    else:
        st.error("Invalid username.")

if st.button("Fetch Repository"):
    github_username = st.session_state["user_name"]
    repo_name = st.session_state["repo_name"]
    
    if github_username and repo_name:
        github_repo_url = f'https://api.github.com/repos/{github_username}/{repo_name}'  # Fetch info only for the selected repo
        response = requests.get(github_repo_url)

        if response.status_code == 200:
            repo_data = response.json()

            # Store GitHub repositories with additional information
            repositories = []

            repo_count = 0

            for repo in repo_data[:100]:
                repo_name = repo["name"]
                repo_url = repo["html_url"]

                last_accessed_response = requests.get(f'https://api.github.com/repos/{github_username}/{repo_name}/commits/master')

                if last_accessed_response.status_code == 200:
                    last_accessed_data = last_accessed_response.json()
                    if last_accessed_data:
                        last_accessed_date = datetime.strptime(
                            last_accessed_data[0]['commit']['committer']['date'],
                            "%Y-%m-%dT%H:%M:%SZ"
                        ).strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        last_accessed_date = "N/A"
                else:
                    last_accessed_date = "N/A"

                cleaned_data = {
                    "Name": repo_name,
                    "GitHub Link": repo_url,
                    "GitHub User": github_username,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Last Accessed": last_accessed_date,
                }

                repositories.append(cleaned_data)

                repo_count += 1

            # Insert data into MongoDB
            collection.insert_many(cleaned_data)
            st.success("Data Saved")
        else:
            st.error("Failed to fetch GitHub data")

# Retrieve data from MongoDB
retrieved_data = list(collection.find({}))

if retrieved_data:
    st.write("Data retrieved")

    fields_excluded = [
        "fork", "forks_url", "keys_url", "collaborators_url", "teams_url", "hooks_url",
        "issue_events_url", "events_url", "assignees_url", "branches_url", "tags_url",
        "blobs_url", "git_tags_url", "git_refs_url", "trees_url", "statuses_url",
        "languages_url", "stargazers_url", "contributors_url", "subscribers_url",
        "subscription_url", "commits_url", "git_commits_url", "comments_url",
        "issue_comment_url", "contents_url", "compare_url", "merges_url",
        "archive_url", "downloads_url", "issues_url", "pulls_url", "milestones_url",
        "notifications_url", "labels_url", "releases_url", "deployments_url",
        "created_at", "updated_at", "pushed_at", "git_url", "ssh_url", "clone_url",
        "svn_url", "homepage", "size", "stargazers_count", "watchers_count",
        "language", "has_issues", "has_projects", "has_downloads", "has_wiki",
        "has_pages", "has_discussions", "forks_count", "mirror_url", "archived",
        "disabled", "open_issues_count", "license", "allow_forking", "is_template",
        "web_commit_signoff_required", "topics", "forks", "open_issues",
        "default_branch", "_id", "id", "node_id", "owner", "visibility", "watchers", "Name", "url","private"

    ]
    if retrieved_data:
        rearranged_columns = ["GitHub User", "GitHub Link", "Name"] + [col for col in retrieved_data[0] if col not in ["GitHub User", "GitHub Link", "Name"]]
    else:
        rearranged_columns = []  
    cleaned_retrieved_data = [{key: value for key, value in item.items() if key not in fields_excluded} for item in retrieved_data]
    # Display data in a table
    st.table(cleaned_retrieved_data)

    if len(cleaned_retrieved_data) > 100:

        cleaned_retrieved_data.sort(key=lambda x: x["Date"])

        oldest_repo = cleaned_retrieved_data[0]

        collection.delete_one({"Name": oldest_repo["Name"]})
        st.success(f"Deleted the oldest repository")
else:
    st.info("No data received")