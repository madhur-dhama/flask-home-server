📁 Flask File Server

A simple Flask-based local file server for Linux that lets you browse, upload, download, delete, and manage files directly from your web browser.
Runs entirely on your local network — no internet required.

🚀 Features

📂 Browse files and folders

⬆️ Upload files (supports large uploads up to 15 GB)

⬇️ Download files directly from the browser

🗑️ Delete files or folders

🪄 Create new folders

📱 Mobile-friendly UI — access from your phone or tablet

💻 Works fully offline on your local Wi-Fi

⚡ Single Python script — lightweight and easy to run

🧠 How It Works

This project starts a Flask web server on your Linux system that serves a folder named shared/.
When running, it provides a clean, responsive web interface to manage those files from any device on the same network.

🛠️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/flask-file-server.git
cd flask-file-server

2. Install dependencies

Make sure Python 3 and Flask are installed:

pip install flask

3. Run the server
python3 app.py

4. Access from browser

Open this link on your laptop or phone (same Wi-Fi):

http://<your-local-ip>:8000


You’ll see a file browser interface where you can upload or download files.

📁 Default Folder

All files are served from a directory named shared/ in the project root.
If it doesn’t exist, it will be created automatically.

You can change the folder path by editing this line in app.py:

SHARED_DIR = os.path.abspath("shared")

⚙️ Configuration
Setting	Description	Default
PORT	Web server port	8000
HOST	Network host	0.0.0.0 (all devices)
SHARED_DIR	Folder to serve	shared/
MAX_CONTENT_LENGTH	Max upload size	15 GB
🧩 Example Use Cases

Share files between your Linux laptop and Android phone

Use as a temporary LAN file drop for your local network

Access and manage large files without USB drives or cables

🧑‍💻 Tech Stack

Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript

Platform: Linux

Storage: Local filesystem

⚠️ Notes

Designed for local use only — there’s no authentication by default.

Avoid using it on public networks without adding authentication or HTTPS.

🏁 License

This project is open-source under the MIT License — feel free to use, modify, and share it.

✨ Author

Madhur Dhama
📍 Built for learning and personal LAN file sharing convenience.
