# 🧩 Flask Home Server

A **lightweight Flask-based Home server** for Linux that lets you **browse, upload, download, delete, and organize files** right from your web browser.  
Works entirely offline — perfect for sharing files between your **laptop and phone** on the same Wi-Fi network.


## 🚀 Features

- 📂 Browse files and folders  
- ⬆️ Upload files (up to **15 GB**)  
- ⬇️ Download directly via browser  
- 🗑️ Delete files or folders  
- 🪄 Create new folders  
- 📱 Mobile-friendly interface  
- ⚡ Works locally — no internet required  
- 🧰 Single-file app (just run `app.py`)


## ⚙️ How It Works

The app starts a **Flask web server** that shares a folder named `shared/`.  
When running, it provides a clean browser interface to manage files over your local network.


## 🛠️ Setup

### 1. Clone this repository
```bash
git clone https://github.com/madhur-dhama/flask-file-server.git
cd flask-file-server
```

### 2. Install dependencies
```bash
pip install flask
```

### 3. Run the app
```bash
python3 app.py
```

### 4. Access on your phone or another device
Find your local IP:
```bash
hostname -i
```

Then open this in your browser:
```
http://<your-ip>:8000
```
Example: 
`http://192.168.105:8000` - if connected with lan
`http://192.168.208:8000` - if connected with wireless

## 📁 Default Folder

Files are served from the folder:
```
shared/
```
It’s created automatically.  
You can change it by editing:
```python
SHARED_DIR = os.path.abspath("shared")
```


## ⚙️ Configuration

| Option | Description | Default |
|:--------|:-------------|:---------|
| `PORT` | Server port | `8000` |
| `HOST` | Listen address | `0.0.0.0` |
| `SHARED_DIR` | Shared folder path | `shared/` |
| `MAX_CONTENT_LENGTH` | Max upload size | `15 GB` |


## 🧠 Use Cases

- Quick file transfer between **Linux and mobile**  
- Offline file sharing on **local Wi-Fi**  
- Temporary LAN file drop for your home or office  


## 🧑‍💻 Tech Stack

- **Backend:** Flask (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Platform:** Linux  
- **Storage:** Local filesystem  


## ⚠️ Note

- This is designed for **local use only**.  
- There’s **no authentication** — don’t use it on public networks.  


## 🏁 License

Licensed under the **MIT License** — free to use, modify, and share.  


## ✨ Author

**Madhur Dhama**  
Built for easy offline file sharing using Flask and Linux.  
