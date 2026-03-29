# utils/local_storage.py
import os
import shutil
from datetime import datetime
import streamlit as st
import mimetypes

# Base path for local storage
BASE_STORAGE_PATH = "local_storage"

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    os.makedirs(path, exist_ok=True)
    return path

def get_storage_path(category, subcategory=None, filename=None):
    """Get full storage path for a file"""
    path = os.path.join(BASE_STORAGE_PATH, category)
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
        original_name = uploaded_file.name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{original_name}"
    
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
    
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def get_file_type(file_path):
    """Get file type/MIME type"""
    if not file_path or not os.path.exists(file_path):
        return "Unknown"
    
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if mime_type.startswith('image/'):
            return "Image"
        elif mime_type.startswith('application/pdf'):
            return "PDF"
        elif mime_type.startswith('application/msword'):
            return "Word Document"
        elif mime_type.startswith('application/vnd.openxmlformats-officedocument'):
            return "Office Document"
        elif mime_type.startswith('text/'):
            return "Text"
    
    ext = file_path.split('.')[-1].upper() if '.' in file_path else "Unknown"
    return f"{ext} File"

def get_file_info(file_path):
    """Get file information"""
    if not file_path or not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    return {
        "size": get_file_size(file_path),
        "size_bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
        "type": get_file_type(file_path)
    }

def list_files(category, subcategory=None, extensions=None):
    """List files in a storage directory"""
    path = get_storage_path(category, subcategory)
    
    if not os.path.exists(path):
        return []
    
    files = []
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            # Check extension filter
            if extensions:
                ext = filename.split('.')[-1].lower()
                if ext not in extensions:
                    continue
            
            files.append({
                "name": filename,
                "path": file_path,
                "size": get_file_size(file_path),
                "modified": datetime.fromtimestamp(os.path.getmtime(file_path))
            })
    
    return sorted(files, key=lambda x: x["modified"], reverse=True)

def get_storage_usage():
    """Get total storage usage"""
    total_size = 0
    if os.path.exists(BASE_STORAGE_PATH):
        for root, dirs, files in os.walk(BASE_STORAGE_PATH):
            for f in files:
                file_path = os.path.join(root, f)
                total_size += os.path.getsize(file_path)
    
    return get_file_size(total_size)