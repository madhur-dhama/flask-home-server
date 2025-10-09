"""
Utility functions for the Flask Home Server
"""
import os
import pathlib
import datetime
from config import SHARED_DIR

def human_size(n):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return f"{n:3.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"

def is_media_file(filename):
    """Check if file is audio or video"""
    ext = os.path.splitext(filename)[1].lower()
    media_exts = ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac', '.opus',
                  '.mp4', '.webm', '.ogv', '.mkv', '.avi', '.mov', '.m4v']
    return ext in media_exts

def get_safe_path(subpath=''):
    """Get a safe path within SHARED_DIR, preventing directory traversal"""
    if subpath:
        requested = os.path.normpath(os.path.join(SHARED_DIR, subpath))
        if not requested.startswith(SHARED_DIR):
            return SHARED_DIR
        return requested
    return SHARED_DIR

def list_files(current_path):
    """List all files and folders in the current path"""
    p = pathlib.Path(current_path)
    items = []
    
    for entry in sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        stat = entry.stat()
        rel_path = os.path.relpath(entry, SHARED_DIR)
        
        items.append({
            'name': entry.name,
            'path': rel_path,
            'is_file': entry.is_file(),
            'is_media': is_media_file(entry.name) if entry.is_file() else False,
            'size': human_size(stat.st_size) if entry.is_file() else '',
            'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return items

def get_breadcrumbs(current_path):
    """Generate breadcrumb navigation"""
    rel_path = os.path.relpath(current_path, SHARED_DIR)
    if rel_path == '.':
        return []
    
    parts = rel_path.split(os.sep)
    breadcrumbs = []
    cumulative = ''
    
    for part in parts:
        cumulative = os.path.join(cumulative, part) if cumulative else part
        breadcrumbs.append({'name': part, 'path': cumulative})
    
    return breadcrumbs