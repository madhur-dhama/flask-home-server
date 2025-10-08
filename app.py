"""
Flask Home Server - Main Application
Run: python app.py
"""
import sys
sys.dont_write_bytecode = True  # Prevent __pycache__ creation

from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile

from utils import human_size, get_safe_path, list_files, get_breadcrumbs
from config import SHARED_DIR, PORT, HOST, MAX_CONTENT_LENGTH, TEMP_DIR

# Setup temp directory
os.makedirs(TEMP_DIR, exist_ok=True)
tempfile.tempdir = TEMP_DIR
os.environ['TMPDIR'] = TEMP_DIR
print(f"Using temp directory: {TEMP_DIR}")

# Create shared directory in HOME
os.makedirs(SHARED_DIR, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['MAX_FORM_MEMORY_SIZE'] = MAX_CONTENT_LENGTH
app.secret_key = 'local-secret-change-if-needed'

print(f"Serving files from: {SHARED_DIR}")

# Routes
@app.route('/')
@app.route('/browse/')
@app.route('/browse/<path:subpath>')
def browse(subpath=''):
    current_path = get_safe_path(subpath)
    files = list_files(current_path)
    breadcrumbs = get_breadcrumbs(current_path)
    return render_template('index.html', 
                         files=files, 
                         count=len(files), 
                         breadcrumbs=breadcrumbs, 
                         current_subpath=subpath)

@app.route('/download/<path:filepath>')
def download(filepath):
    full_path = get_safe_path(filepath)
    directory = os.path.dirname(full_path)
    filename = os.path.basename(full_path)
    return send_from_directory(directory, filename, as_attachment=True)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        print(f"Upload request received. Content-Length: {request.content_length}")
        
        current_path = request.form.get('current_path', '')
        upload_dir = get_safe_path(current_path)
        
        print(f"Upload directory: {upload_dir}")
        
        if 'files' not in request.files:
            print("No files in request")
            flash('No files selected')
            return redirect(f'/browse/{current_path}' if current_path else '/')
        
        files = request.files.getlist('files')
        print(f"Number of files: {len(files)}")
        uploaded = []
        
        for file in files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            dest = os.path.join(upload_dir, filename)
            print(f"Saving: {filename} to {dest}")
            
            file.save(dest)
            uploaded.append(filename)
            print(f"Saved: {filename}")
        
        if uploaded:
            msg = f'Uploaded: {uploaded[0]}' if len(uploaded) == 1 else f'Uploaded {len(uploaded)} files'
            flash(msg)
        else:
            flash('No files were uploaded')
        
        print(f"Upload complete. Uploaded {len(uploaded)} files")
        return redirect(f'/browse/{current_path}' if current_path else '/')
    except Exception as e:
        print(f"Upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Upload error: {str(e)}')
        current_path = request.form.get('current_path', '')
        return redirect(f'/browse/{current_path}' if current_path else '/')

@app.route('/delete/<path:filepath>', methods=['POST'])
def delete(filepath):
    try:
        import shutil
        full_path = get_safe_path(filepath)
        
        if not os.path.exists(full_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            shutil.rmtree(full_path)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/create_folder', methods=['POST'])
def create_folder():
    try:
        current_path = request.form.get('current_path', '')
        folder_name = request.form.get('folder_name', '').strip()
        
        if not folder_name:
            flash('Folder name cannot be empty')
            return redirect(f'/browse/{current_path}' if current_path else '/')
        
        safe_name = secure_filename(folder_name)
        base_dir = get_safe_path(current_path)
        folder_path = os.path.join(base_dir, safe_name)
        
        if os.path.exists(folder_path):
            flash(f'Folder "{safe_name}" already exists')
        else:
            os.makedirs(folder_path)
            flash(f'Created folder: {safe_name}')
        
        return redirect(f'/browse/{current_path}' if current_path else '/')
    except Exception as e:
        flash(f'Error creating folder: {str(e)}')
        current_path = request.form.get('current_path', '')
        return redirect(f'/browse/{current_path}' if current_path else '/')

if __name__ == '__main__':
    print(f"Serving folder: {SHARED_DIR}")
    print(f"Open on phone: http://<your-ip>:{PORT}")
    print(f"Max upload size: 15 GB")
    
    # Increase Werkzeug limits for large file uploads
    import werkzeug
    werkzeug.serving.WSGIRequestHandler.protocol_version = "HTTP/1.1"
    
    app.run(host=HOST, port=PORT, threaded=True, debug=False)
