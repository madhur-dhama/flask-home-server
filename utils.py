"""
Utility functions for the Flask Home Server
"""
import os
import pathlib
import datetime
from config import SHARED_DIR, MAX_CONTENT_LENGTH

def human_size(n):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if n < 1024.0:
            return f"{n:3.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"

def get_safe_path(subpath=''):
    """Prevent directory traversal and return safe path"""
    if subpath:
        requested = os.path.normpath(os.path.join(SHARED_DIR, subpath))
        if not requested.startswith(SHARED_DIR):
            return SHARED_DIR
        return requested
    return SHARED_DIR

def list_files(current_path):
    """List files and folders with metadata"""
    p = pathlib.Path(current_path)
    items = []
    for entry in sorted(p.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        stat = entry.stat()
        rel_path = os.path.relpath(entry, SHARED_DIR)
        items.append({
            'name': entry.name,
            'path': rel_path,
            'is_file': entry.is_file(),
            'size': human_size(stat.st_size) if entry.is_file() else '',
            'mtime': datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    return items

def get_breadcrumbs(current_path):
    """Generate breadcrumbs for navigation"""
    rel_path = os.path.relpath(current_path, SHARED_DIR)
    if rel_path == '.':
        return []
    breadcrumbs = []
    cumulative = ''
    for part in rel_path.split(os.sep):
        cumulative = os.path.join(cumulative, part) if cumulative else part
        breadcrumbs.append({'name': part, 'path': cumulative})
    return breadcrumbs

def get_directory_size(path):
    """Recursively calculate total directory size"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)
    except Exception:
        pass
    return total

def get_free_space():
    """Return remaining space based on MAX_CONTENT_LENGTH"""
    used = get_directory_size(SHARED_DIR)
    free = MAX_CONTENT_LENGTH - used
    return max(free, 0)