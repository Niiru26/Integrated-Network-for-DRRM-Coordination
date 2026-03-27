# utils/github_backup.py
import requests
import streamlit as st
import json

def create_github_gist(files, description, is_public=False):
    """
    Create a GitHub Gist backup of your project state
    
    Args:
        files: Dictionary of filename -> content
        description: Description of the gist
        is_public: Whether the gist is public
    """
    # You'll need a GitHub token
    # Store it in st.secrets["GITHUB_TOKEN"]
    
    token = st.secrets.get("GITHUB_TOKEN")
    if not token:
        return "GitHub token not configured. Add GITHUB_TOKEN to secrets."
    
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Format files for Gist API
    gist_files = {}
    for filename, content in files.items():
        gist_files[filename] = {"content": content}
    
    data = {
        "description": description,
        "public": is_public,
        "files": gist_files
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        gist_url = response.json()["html_url"]
        return f"Backup created: {gist_url}"
    else:
        return f"Failed: {response.status_code} - {response.text}"

def backup_to_github(chat_part, summary, key_files):
    """Backup the current state to GitHub Gist"""
    description = f"INDC App - {chat_part} - {summary[:50]}..."
    return create_github_gist(key_files, description, is_public=False)