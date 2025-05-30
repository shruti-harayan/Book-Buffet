📖 Book Buffet – Library Management System
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Desktop-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

A standalone, full-featured **desktop app** built with Python (Tkinter) for managing a library's books, members, reports, and backups — no internet required.

---

## ✅ Features

- 📘 **Book Management** – Add, update, delete, and search books
- 👤 **Member Management** – Register, update, delete library members
- 🔄 **Issue & Return** – Manage book transactions with auto quantity updates
- 📈 **Graphical Reports** – Bar & line charts (matplotlib)
- 💾 **Backup** – Export data to CSV and PDF
- 🔐 **Secure Login** – Admin login + new user registration
- 🧩 **SQLite3 Database** – Lightweight, local storage (offline)
---

## 🖼️ Screenshots

> 📌 Upload screenshots to `/images/screenshots/` and embed them like:

![Login Page](images/screenshots/login.png)
![Dashboard](images/screenshots/dashboard.png)


🧑‍💻 Technologies Used
Python 3.11	Core language
Tkinter	GUI Toolkit
SQLite3	Database for books & members
pandas, numpy	Data manipulation
matplotlib	Chart generation
FPDF	PDF export
PIL (Pillow)	Image support

🚀 How to Run
Download BookBuffet_v1.0.zip from Releases

Extract the ZIP

Run project_login.exe

You're in! 🎉

💻 From Source

git clone https://github.com/yourusername/BookBuffet.git
cd BookBuffet
pip install -r requirements.txt
python project_login.py

🔑 Default Login
Username	Password
admin	shruti

Or use the Register button to create a new user.

🗂️ Project Structure
BookBuffet/
├── images/                  # All icons & images
├── backup_folder/           # Created during backup
├── BookDB.db                # Books database
├── MemDB.db                 # Members database
├── admin.db                 # Admin login credentials
├── Existing Book.xlsx       # Used in report generation
├── dashboard.py             # Main GUI
├── project_login.py         # Entry point
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

📄 License
This project is licensed under the MIT License.
Feel free to use, adapt, and improve it.

👤 Author
Shruti H.

Made with ❤️ using Python + Tkinter
