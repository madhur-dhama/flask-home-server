"""
Flask Home Server - Main Application
Run: python app.py
"""
import sys
sys.dont_write_bytecode = True  # Prevent __pycache__ creation

import os
import logging
import tempfile
import werkzeug
from flask import (Flask, render_template, send_from_directory, request, redirect, url_for, flash)
from werkzeug.utils import secure_filename

from config import SHARED_DIR, TEMP_DIR, HOST, PORT, MAX_CONTENT_LENGTH, SECRET_KEY
from utils import (human_size, get_safe_path, list_files, get_breadcrumbs, get_directory_size, get_free_space, get_media_type)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
tempfile.tempdir = TEMP_DIR
os.environ['TMPDIR'] = TEMP_DIR

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = SECRET_KEY

# Increase Werkzeug limits for large file uploads
werkzeug.serving.WSGIRequestHandler.protocol_version = "HTTP/1.1"

@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    """List files and directories"""
    current_path = get_safe_path(subpath)
    files = list_files(current_path)
    breadcrumbs = get_breadcrumbs(current_path)
    storage_left = human_size(get_free_space())
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 50
    total_files = len(files)
    total_pages = (total_files + per_page - 1) // per_page
    start, end = (page - 1) * per_page, (page - 1) * per_page + per_page
    files_paginated = files[start:end]

    return render_template(
        'index.html',
        files=files_paginated,
        count=total_files,
        breadcrumbs=breadcrumbs,
        current_subpath=subpath,
        storage_left=storage_left,
        page=page,
        total_pages=total_pages
    )

@app.route('/download/<path:filepath>')
def download(filepath):
    """Download file"""
    full_path = get_safe_path(filepath)
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/stream/<path:filepath>')
def stream(filepath):
    """Stream file inline"""
    full_path = get_safe_path(filepath)
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename, as_attachment=False)

@app.route('/play/<path:filepath>')
def play(filepath):
    """Play audio or video in browser"""
    full_path = get_safe_path(filepath)
    if not os.path.exists(full_path):
        flash('File not found')
        return redirect(url_for('browse'))

    filename = os.path.basename(full_path)
    media_type = get_media_type(filename)
    if not media_type:
        flash('Unsupported media format')
        return redirect(url_for('browse'))

    return render_template(
        'player.html',
        filepath=filepath,
        filename=filename,
        media_type=media_type
    )

@app.route('/upload', methods=['POST'])
def upload():
    """Handle uploads"""
    try:
        logger.info(f"Upload request received. Content-Length: {request.content_length}")
        current_path = request.form.get('current_path', '')
        upload_dir = get_safe_path(current_path)

        free_space = get_free_space()
        if free_space <= 0:
            flash('Storage is full! Cannot upload files.')
            return redirect(f'/browse/{current_path}' if current_path else '/')

        if request.content_length and request.content_length > free_space:
            flash(f'Not enough storage! Available: {human_size(free_space)}, '
                  f'Upload size: {human_size(request.content_length)}')
            return redirect(f'/browse/{current_path}' if current_path else '/')

        if 'files' not in request.files:
            flash('No files selected')
            return redirect(f'/browse/{current_path}' if current_path else '/')

        files = request.files.getlist('files')
        uploaded = []

        for file in files:
            if not file.filename:
                continue
            filename = secure_filename(file.filename)
            dest = os.path.join(upload_dir, filename)

            # Handle duplicates
            base, ext = os.path.splitext(dest)
            counter = 1
            while os.path.exists(dest):
                dest = f"{base}_{counter}{ext}"
                counter += 1

            logger.info(f"Saving: {filename} -> {dest}")
            file.save(dest)
            uploaded.append(filename)

        if uploaded:
            msg = f'Uploaded: {uploaded[0]}' if len(uploaded) == 1 else f'Uploaded {len(uploaded)} files'
            flash(msg)
        else:
            flash('No files were uploaded')

        return redirect(f'/browse/{current_path}' if current_path else '/')
    except Exception as e:
        logger.exception("Upload error")
        flash(f'Upload error: {e}')
        current_path = request.form.get('current_path', '')
        return redirect(f'/browse/{current_path}' if current_path else '/')

if __name__ == '__main__':
    logger.info(f"Serving folder: {SHARED_DIR}")
    logger.info(f"Open on phone: http://<your-ip>:{PORT}")
    logger.info(f"Max upload size: {human_size(MAX_CONTENT_LENGTH)}")
    app.run(host=HOST, port=PORT, threaded=True, debug=False)