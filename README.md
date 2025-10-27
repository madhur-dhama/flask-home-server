# 🧩 Flask Home Server

A **lightweight local file server** built with Flask for Linux.  
Browse, upload, download, and stream your files — all from your web browser.  
Works entirely **offline** on your **local Wi-Fi**, perfect for quick file sharing between your **pc and phone**.

---

## 🚀 Features

- 📂 **Browse files & folders**
- ⬆️ **Upload multiple files**
- ⬇️ **Download**
- 🎵 **Stream audio files**
- 🎬 **Stream video files** 
- 🎮 **Built-in media player**
- 💾 **Storage space monitoring**
- 📊 **Upload progress tracking**
- 🎨 **Modern dark theme** 
- ⚡ **Works locally — no internet required**

---

## ⚙️ How It Works

Runs a small **Flask web server** that serves the `~/FileShare` folder.  
You can manage your files through a clean, web-based interface accessible from any device on your Wi-Fi.

Files are organized in folders, with full support for nested directory structures. The server handles large file uploads using chunked transfers and provides real-time progress feedback.

---

## 🛠️ Setup

### 1. Clone this repo
```bash
git clone https://github.com/madhur-dhama/flask-home-server.git
cd flask-home-server
```

### 2. Install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install flask
```

### 3. Run the server 
```bash
python app.py
```

### 4. Access it on your phone or another device
Open in your browser:
```
http://<your-ip>:8000
```

**Examples:** - `http://192.168.0.51:8000`

**To find your IP address:**
```bash
hostname -i
```

---

## ▶️ Quick Start (next time)
```bash
source venv/bin/activate
python app.py
```

---

## 📁 Directory Structure

```
~/FileShare/          # All shared files (auto-created)
~/.tmp/               # Temporary upload directory (auto-created)
flask-home-server/
├── app.py            # Main Flask application
├── config.py         # Configuration settings
├── utils.py          # Helper functions
├── static/
│   ├── css/
│   │   ├── style.css      # Main stylesheet
│   │   └── all.min.css    # Font Awesome icons
│   └── js/
│       └── app.js         # Frontend JavaScript
└── templates/
    ├── index.html         # File browser interface
    └── player.html        # Media player interface
```

---

## 🧑‍💻 Tech Stack

- **Backend:** Flask (Python 3)
- **Frontend:** HTML5, CSS3, JavaScript
- **Icons:** Font Awesome
- **Platform:** Linux 
- **Storage:** Local filesystem
- **Server:** Werkzeug (Flask development server)

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
HOST = '0.0.0.0'                    # Listen on all interfaces
PORT = 8000                          # Server port
MAX_CONTENT_LENGTH = 100 * 1024³    # 100GB upload limit
SHARED_DIR = "~/FileShare"          # Shared folder location
TEMP_DIR = "~/.tmp"                 # Temporary upload directory
```

---

## 📊 Storage Limits

- **Maximum file size:** 100 GB per file
- **Total storage:** Limited by your disk space
- **Upload capacity:** Multiple files simultaneously
- **Storage tracking:** Real-time free space display in header

---

## ⚠️ Security Notice

- Designed for **local network use only**
- **No authentication** — anyone on your Wi-Fi can access files
- **Do not expose** to public networks or the internet
- Use only on **trusted networks**
- Consider adding authentication for multi-user environments