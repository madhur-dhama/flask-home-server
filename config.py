"""
Configuration settings for the Flask Home Server
"""
import os

# Server configuration
HOST = '0.0.0.0'
PORT = 8000

# Directory configuration
SHARED_DIR = os.path.join(os.path.expanduser("~"), "FileShare")
TEMP_DIR = os.path.join(os.path.expanduser("~"), ".tmp")

# Upload configuration
ALLOWED_EXTENSIONS = None  # None = allow all types
MAX_CONTENT_LENGTH = 100 * 1024 * 1024 * 1024  # 15 GiB upload limit

# Security
SECRET_KEY = 'local-secret-change-if-needed'
