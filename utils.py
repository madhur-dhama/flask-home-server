"""
Utility functions for the Flask Home Server
"""
import os
import pathlib
import datetime
from config import SHARED_DIR, STORAGE_QUOTA

def human_size(n):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def get_safe_path(subpath=''):
    requested = os.path.normpath(os.path.join(SHARED_DIR, subpath))
    return requested if requested.startswith(SHARED_DIR) else SHARED_DIR

def list_files(current_path):
    items = []
    for entry in sorted(pathlib.Path(current_path).iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        stat = entry.stat()
        items.append({
            'name': entry.name,
            'path': os.path.relpath(entry, SHARED_DIR),
            'is_file': entry.is_file(),
            'size': human_size(stat.st_size) if entry.is_file() else '',
            'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    return items

def get_breadcrumbs(current_path):
    rel_path = os.path.relpath(current_path, SHARED_DIR)
    if rel_path == '.':
        return []
    breadcrumbs = []
    cumulative = ''
    for part in rel_path.split(os.sep):
        cumulative = os.path.join(cumulative, part) if cumulative else part
        breadcrumbs.append({'name': part, 'path': cumulative})
    return breadcrumbs

def get_free_space():
    used = sum(f.stat().st_size for f in pathlib.Path(SHARED_DIR).rglob('*') if f.is_file())
    return max(STORAGE_QUOTA - used, 0)