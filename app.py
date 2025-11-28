"""
Flask Home Server - Main Application
Run: python app.py
"""
import sys
sys.dont_write_bytecode = True

import os
import logging
import werkzeug
import tempfile
from flask import Flask, render_template, send_from_directory, request, jsonify
from werkzeug.utils import secure_filename

from config import SHARED_DIR, TEMP_DIR, HOST, PORT, MAX_CONTENT_LENGTH, SECRET_KEY
from utils import human_size, get_safe_path, list_files, get_breadcrumbs, get_free_space

# Logging Setup
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Initialize Directories
os.makedirs(SHARED_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.environ['TMPDIR'] = TEMP_DIR
tempfile.tempdir = TEMP_DIR 

# Flask Configuration
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = SECRET_KEY
werkzeug.serving.WSGIRequestHandler.protocol_version = "HTTP/1.1"

@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    current_path = get_safe_path(subpath)
    files = list_files(current_path)
    
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
    full_path = get_safe_path(filepath)
    return send_from_directory(
        os.path.dirname(full_path),
        os.path.basename(full_path),
        as_attachment=True
    )

@app.route('/delete/<path:filepath>', methods=['POST'])
def delete(filepath):
    try:
        full_path = get_safe_path(filepath)
        os.remove(full_path)
        logger.info(f"Deleted: {filepath}")
        return jsonify({'success': True})
    except Exception as e:
        logger.exception(f"Delete error: {filepath}")
        return jsonify({'success': False, 'error': f'{type(e).__name__}: {str(e)}'}), 500

@app.route('/storage-check', methods=['POST'])
def storage_check():
    try:
        data = request.get_json()
        upload_size = data.get('size', 0)
        free = get_free_space()
        return jsonify({'available': free > upload_size, 'free': free})
    except Exception as e:
        logger.exception("Storage check error")
        return jsonify({'available': False, 'free': 0, 'error': f'{type(e).__name__}: {str(e)}'}), 400

@app.route('/upload', methods=['POST'])
def upload():
    try:
        current_subpath = request.form.get('current_path', '')
        upload_dir = get_safe_path(current_subpath)
        files = request.files.getlist('files')
        if files:
            # Handle normal small files
            for f in files:
                if f.filename:
                    f.save(os.path.join(upload_dir, secure_filename(f.filename)))
                    logger.info(f"Saved (small): {f.filename}")
        else:
            # Handle large streamed file
            file_name = request.headers.get('X-Filename')
            safe_name = secure_filename(file_name)
            final_path = os.path.join(upload_dir, safe_name)
            with open(final_path, 'wb') as f:
                while chunk := request.stream.read(1024*1024):  # 1 MB chunks
                    f.write(chunk)
            logger.info(f"Saved (stream): {safe_name}")
        return jsonify({'success': True})

    except Exception as e:
        logger.exception("Upload error")
        return jsonify({'error': f'{type(e).__name__}: {e}'}), 500

if __name__ == '__main__':
    logger.info(f"Serving: {SHARED_DIR}")
    logger.info(f"Access: http://<your-ip>:{PORT}")
    app.run(host=HOST, port=PORT, threaded=True, debug=False)