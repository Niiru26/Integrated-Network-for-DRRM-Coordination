# utils/local_storage.py
import streamlit as st
import os
import json
from datetime import datetime
from supabase import create_client

def save_file(file_path, content):
    # implementation...
    
def delete_file(file_path):
    # implementation...
    
def get_file_size(file_path):
    # implementation...
    
def file_exists(file_path):
    # implementation...


def get_supabase_client():
    """Get Supabase client from session state"""
    if 'supabase_client' not in st.session_state:
        supabase_url = st.secrets["SUPABASE_URL"]
        supabase_key = st.secrets["SUPABASE_KEY"]
        st.session_state.supabase_client = create_client(supabase_url, supabase_key)
    return st.session_state.supabase_client


# =============================================================================
# LOCAL STORAGE FUNCTIONS (for files saved on local computer)
# =============================================================================

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)
    return path


def get_storage_path(category, subcategory=None, filename=None):
    """Get full storage path for a file"""
    path = os.path.join("local_storage", category)
    if subcategory:
        path = os.path.join(path, subcategory)
    ensure_directory(path)
    if filename:
        return os.path.join(path, filename)
    return path


def save_file(uploaded_file, category, subcategory=None, custom_name=None):
    """Save uploaded file to local storage"""
    if not uploaded_file:
        return None
    
    # Generate filename
    if custom_name:
        filename = custom_name
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
    
    # Get storage path
    file_path = get_storage_path(category, subcategory, filename)
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def delete_file(file_path):
    """Delete a file from local storage"""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False


def file_exists(file_path):
    """Check if file exists"""
    return os.path.exists(file_path) if file_path else False


def get_file_size(file_path):
    """Get file size in human-readable format"""
    if not file_path or not os.path.exists(file_path):
        return "0 B"
    return format_file_size(os.path.getsize(file_path))


def get_file_info(file_path):
    """Get file information"""
    if not file_path or not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    return {
        "size": get_file_size(file_path),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
    }


def get_storage_usage():
    """Get total storage usage"""
    total_size = 0
    if os.path.exists("local_storage"):
        for root, dirs, files in os.walk("local_storage"):
            for f in files:
                file_path = os.path.join(root, f)
                total_size += os.path.getsize(file_path)
    return format_file_size(total_size)


def format_file_size(size_bytes):
    """Format file size in human-readable format"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# =============================================================================
# CLOUD STORAGE FUNCTIONS (Supabase Storage - shared across all users)
# =============================================================================

def save_file_to_cloud(uploaded_file, folder, filename=None):
    """Save uploaded file to Supabase Storage (cloud)"""
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