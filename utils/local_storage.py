# utils/local_storage.py
import os
import json
import shutil
from datetime import datetime
from pathlib import Path

# Base storage directory
BASE_STORAGE_DIR = "local_storage"

def get_storage_path(subfolder=""):
    """Get storage path for files"""
    if subfolder:
        path = os.path.join(BASE_STORAGE_DIR, subfolder)
    else:
        path = BASE_STORAGE_DIR
    os.makedirs(path, exist_ok=True)
    return path

def save_file(file_path, content, mode='w'):
    """Save file to local storage"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, mode) as f:
        f.write(content)
    return True

def save_binary_file(file_path, content):
    """Save binary file to local storage"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as f:
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

def read_file(file_path):
    """Read file content"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read()
    return None

def read_binary_file(file_path):
    """Read binary file content"""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return f.read()
    return None

def create_backup(file_path, backup_dir="backups"):
    """Create a backup of a file"""
    if os.path.exists(file_path):
        backup_path = get_storage_path(backup_dir)
        backup_file = os.path.join(backup_path, f"{os.path.basename(file_path)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(file_path, backup_file)
        return backup_file
    return None

def restore_backup(backup_file, target_path):
    """Restore a backup file"""
    if os.path.exists(backup_file):
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        shutil.copy2(backup_file, target_path)
        return True
    return False

def get_all_files(directory, extension=None):
    """Get all files in a directory, optionally filtered by extension"""
    files = []
    if os.path.exists(directory):
        for f in os.listdir(directory):
            file_path = os.path.join(directory, f)
            if os.path.isfile(file_path):
                if extension is None or f.endswith(extension):
                    files.append(file_path)
    return files