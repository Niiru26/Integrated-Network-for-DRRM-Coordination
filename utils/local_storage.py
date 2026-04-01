# utils/local_storage.py
import streamlit as st
import os
from datetime import datetime
from supabase import create_client

def get_supabase_client():
    """Get Supabase client from session state"""
    if 'supabase_client' not in st.session_state:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        st.session_state.supabase_client = create_client(supabase_url, supabase_key)
    return st.session_state.supabase_client


def save_file_to_cloud(uploaded_file, folder, filename=None):
    """Save uploaded file to Supabase Storage"""
    if not uploaded_file:
        return None
    
    client = get_supabase_client()
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
    
    # Full path in bucket
    file_path = f"{folder}/{filename}"
    
    try:
        # Upload to Supabase Storage
        client.storage.from_("indc_files").upload(
            file_path,
            uploaded_file.getvalue(),
            {"content-type": uploaded_file.type}
        )
        
        # Get public URL
        public_url = client.storage.from_("indc_files").get_public_url(file_path)
        
        return {
            "path": file_path,
            "url": public_url,
            "filename": filename,
            "original_name": uploaded_file.name,
            "size": len(uploaded_file.getvalue()),
            "uploaded_at": datetime.now().isoformat()
        }
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return None


def delete_file_from_cloud(file_path):
    """Delete file from Supabase Storage"""
    if not file_path:
        return False
    
    client = get_supabase_client()
    
    try:
        client.storage.from_("indc_files").remove([file_path])
        return True
    except Exception as e:
        print(f"Delete failed: {e}")
        return False


def get_file_url(file_path):
    """Get public URL for a file"""
    if not file_path:
        return None
    
    client = get_supabase_client()
    return client.storage.from_("indc_files").get_public_url(file_path)


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if not size_bytes:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"