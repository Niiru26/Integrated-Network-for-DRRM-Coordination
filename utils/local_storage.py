# utils/local_storage.py
import os
import json
from datetime import datetime

def save_file(file_path, content):
    """Save file to local storage"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
    return True

def delete_file(file_path):
    """Delete file from local storage"""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def get_file_size(file_path):
    """Get file size in bytes"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0

def file_exists(file_path):
    """Check if file exists"""
    return os.path.exists(file_path)

def get_file_info(file_path):
    """Get file information including name, size, modified date"""
    if os.path.exists(file_path):
        stat = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "path": file_path
        }
    return None

def save_file_to_cloud(file_path, content):
    """Save file to cloud (Supabase) - placeholder"""
    return save_file(file_path, content)

def delete_file_from_cloud(file_path):
    """Delete file from cloud - placeholder"""
    return delete_file(file_path)

def get_file_url(file_path):
    """Get file URL - placeholder"""
    return file_path if os.path.exists(file_path) else None

def list_files(directory):
    """List all files in a directory"""
    if os.path.exists(directory):
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return []