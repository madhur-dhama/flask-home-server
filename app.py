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
from flask import (Flask, render_template, send_from_directory, request, jsonify)
from werkzeug.utils import secure_filename

from config import (SHARED_DIR, TEMP_DIR, HOST, PORT, MAX_CONTENT_LENGTH, SECRET_KEY)
from utils import (human_size, get_safe_path, list_files, get_breadcrumbs, get_free_space)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
tempfile.tempdir = TEMP_DIR
os.environ['TMPDIR'] = TEMP_DIR

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = SECRET_KEY

werkzeug.serving.WSGIRequestHandler.protocol_version = "HTTP/1.1"

@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    """List files and directories"""
    current_path = get_safe_path(subpath)
    files = list_files(current_path)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 50
    start = (page - 1) * per_page
    
    return render_template(
        'index.html',
        files=files[start:start + per_page],
        count=len(files),
        breadcrumbs=get_breadcrumbs(current_path),
        current_subpath=subpath,
        storage_left=human_size(get_free_space()),
        page=page,
        total_pages=(len(files) + per_page - 1) // per_page
    )

@app.route('/download/<path:filepath>')
def download(filepath):
    """Download file"""
    full_path = get_safe_path(filepath)
    return send_from_directory(
        os.path.dirname(full_path),
        os.path.basename(full_path),
        as_attachment=True
    )

@app.route('/delete/<path:filepath>', methods=['POST'])
def delete(filepath):
    """Delete file"""
    try:
        full_path = get_safe_path(filepath)
        
        if not os.path.exists(full_path):
            logger.warning(f"Delete failed - not found: {filepath}")
            return jsonify({'success': False}), 404
        
        if not os.path.isfile(full_path):
            logger.warning(f"Delete failed - is folder: {filepath}")
            return jsonify({'success': False}), 400
        
        os.remove(full_path)
        logger.info(f"Deleted: {filepath}")
        return jsonify({'success': True})
            
    except Exception as e:
        logger.exception(f"Delete error: {filepath}")
        return jsonify({'success': False}), 500

@app.route('/upload', methods=['POST'])
def upload():
    """Handle uploads - reject if quota exceeded"""
    try:
        if 'files' not in request.files:
            return jsonify({'error': 'No files'}), 400

        files = request.files.getlist('files')
        upload_dir = get_safe_path(request.form.get('current_path', ''))
        
        uploaded = 0
        
        for file in files:
            if not file.filename:
                continue
            
            # Check quota
            file.seek(0, 2)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > get_free_space():
                logger.warning(f"Rejected {file.filename} - quota exceeded")
                continue
            
            # Handle duplicates
            filename = secure_filename(file.filename)
            base, ext = os.path.splitext(filename)
            dest = os.path.join(upload_dir, filename)
            counter = 1
            while os.path.exists(dest):
                dest = os.path.join(upload_dir, f"{base}_{counter}{ext}")
                counter += 1

            # Save file
            file.save(dest)
            uploaded += 1
            logger.info(f"Saved: {os.path.basename(dest)}")

        return jsonify({'success': True, 'count': uploaded})

    except Exception as e:
        logger.exception("Upload error")
        return jsonify({'error': 'Upload failed'}), 500

if __name__ == '__main__':
    logger.info(f"Serving: {SHARED_DIR}")
    logger.info(f"Access: http://<your-ip>:{PORT}")
    logger.info(f"Max upload: {human_size(MAX_CONTENT_LENGTH)}")
    app.run(host=HOST, port=PORT, threaded=True, debug=False)