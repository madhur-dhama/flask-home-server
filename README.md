# 🧩 Flask Home Server

A **lightweight local file server** built with Flask for Linux.  
Browse, upload, download, delete, and organize your files — all from your web browser.  
Works entirely **offline** on your **local Wi-Fi**, perfect for quick file sharing between your **laptop and phone**.

---

## 🚀 Features

- 📂 Browse files & folders  
- ⬆️ Upload files (up to **15 GB**)  
- ⬇️ Download directly from the browser  
- 🗑️ Delete files or folders  
- 🪄 Create new folders  
- 📱 Mobile-friendly interface  
- ⚡ Works locally — no internet required  
- 🧰 Single-file app (`app.py`)

---

## ⚙️ How It Works

Runs a small **Flask web server** that serves the `~/FileShare` folder.  
You can manage your files through a clean, web-based interface accessible from any device on your Wi-Fi.

---

## 🛠️ Setup

### 1. Clone this repo
```bash
git clone https://github.com/madhur-dhama/flask-home-server.git
```

### 2. Install dependencies
```bash
python -m venv venv
source ~/venv/bin/activate
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

**Examples:**
- LAN: `http://192.168.0.105:8000`
- Wi-Fi: `http://192.168.0.208:8000`

---

## ▶️ Quick Start (next time)
```bash
source ~/venv/bin/activate
python app.py
```

---

## 📁 Shared Folder

All files are stored in:
```
~/FileShare
```

---

## 🧑‍💻 Tech Stack

- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS, JS  
- **Platform:** Linux  
- **Storage:** Local filesystem  

---

## ⚠️ Note

- Designed for **local use only**.  
- **No authentication** — avoid using on public or untrusted networks.

---

## 🏁 License

Licensed under the **MIT License** — free to use, modify, and share.

---

## ✨ Author

**Madhur Dhama**  
Built for simple, offline file sharing using Flask + Linux.
