# 🧩 Flask Home Server

A **lightweight local file server** built with Flask for Linux. Browse, upload, download, and delete files — all from your web browser. Works entirely **offline** on your **local Wi-Fi**, perfect for quick file sharing between your **PC and phone**.

---

## 🚀 Features

- 📂 **Browse files & folders** with breadcrumb navigation
- ⬆️ **Upload multiple files** with real-time progress tracking
- ⬇️ **Download files** directly to your device
- 🗑️ **Delete files** with confirmation dialog
- 💾 **Storage quota enforcement** - prevents uploads when full
- 📊 **Live upload progress** with time remaining estimates
- 🎨 **Modern dark/light theme** (auto-detects system preference)
- ⚡ **Works locally** — no internet required
- 📱 **Mobile-friendly** responsive design

---

## 🛠️ Setup

### 1. Clone this repo
```bash
git clone https://github.com/madhurdhama/flask-home-server.git
cd flask-home-server
```

### 2. Install dependencies
```bash
python3 -m venv ~/ve_flask
source ~/ve_flask/bin/activate
pip install flask
```

### 3. Run the server
```bash
python3 app.py
```

### 4. Access from any device on your network

Open in your browser: `http://<your-ip>:8000`

**Example:** `http://192.168.0.10:8000`

**To find your IP address:**
```bash
ip a | grep 'inet '
```

---

## ▶️ Quick Start (subsequent runs)
```bash
source ~/ve_flask/bin/activate
python3 app.py
```

---

## 📁 Directory Structure
```
~/FileShare/          # All shared files (auto-created)
~/.tmp/               # Temporary upload staging (auto-created)
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
    └── index.html         # File browser interface
```

---

## 🧑‍💻 Tech Stack

- **Backend:** Flask + Python 3
- **Frontend:** Vanilla JavaScript
- **Styling:** CSS3 with CSS variables for theming
- **Icons:** Font Awesome 6
- **Platform:** Linux (tested on Arch)
- **Storage:** Local filesystem with quota management
- **Server:** Werkzeug development server (HTTP/1.1)

---

## ⚠️ Security Notice

- Designed for **local network use only**
- **No authentication** — anyone on your Wi-Fi can access files
- **Do not expose** to public networks or the internet
- Use only on **trusted networks**
- Consider adding authentication for multi-user environments
