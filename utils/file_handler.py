"""
File handling utilities for uploads
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Base upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file, subfolder=""):
    """Save uploaded file to disk"""
    if uploaded_file is None:
        return None
    
    save_dir = os.path.join(UPLOAD_DIR, subfolder)
    os.makedirs(save_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(save_dir, safe_filename)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def read_uploaded_file(uploaded_file):
    """Read and parse uploaded file based on type"""
    if uploaded_file is None:
        return None
    
    file_ext = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_ext == 'csv':
            return pd.read_csv(uploaded_file)
        elif file_ext in ['xlsx', 'xls']:
            return pd.read_excel(uploaded_file)
        elif file_ext == 'json':
            return pd.read_json(uploaded_file)
        elif file_ext in ['txt', 'md']:
            return uploaded_file.read().decode('utf-8')
        else:
            return uploaded_file.read()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

def get_file_info(file_path):
    """Get information about a saved file"""
    if not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    return {
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'created': datetime.fromtimestamp(stat.st_ctime),
        'name': os.path.basename(file_path)
    }