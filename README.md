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

✅ Add, update, delete, and search books
📚 Issue and return books with automatic quantity updates
👥 Member registration and management
📊 Graphical reports (Bar & Line charts using matplotlib)
📂 Backup to CSV & PDF with one click
🔒 Login system with registration support
💾 Local SQLite3 database (no internet required)
🖼️ Uses FPDF, PIL, pandas, numpy, and Tkinter widgets

---

## 🖼️ Screenshots (Add Yours)

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
📦 Executable (Recommended)
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





A full-featured, standalone desktop application built using Tkinter, SQLite, and Python, designed for managing library operations like book issuance, returns, member registration, backups, and reporting.

✅ This project is compiled into a .exe file and is available as a downloadable release for easy access.

🔧 Features


📦 How to Use (For Users)
🔽 Download & Run
Visit the Releases Page
Download the latest ZIP (e.g. BookBuffet_v1.0.zip)
Extract the zip file
Double-click on project_login.exe to launch the app 🚀
🗂️ Databases and required Excel files are included in the ZIP

🧑‍💻 Technologies Used
Python 3.11
Tkinter (GUI)
SQLite3 (Databases)
Pandas, NumPy
matplotlib (Charts)
FPDF (PDF backup)
Pillow (PIL for image handling)

🔗 Dependencies
Install them via: pip install -r requirements.txt

flaticon.com for free images: .png or .ico file

🛠️ Developer Setup
📁 Project Structure
Book-Buffet/
│
├── images/                  # All icons/images used in the app
├── backup_folder/           # Auto-generated on first backup
├── BookDB.db                # Main book database
├── MemDB.db                 # Member data
├── admin.db                 # Login credentials
├── Existing Book.xlsx       # Excel export (used in reports)
├── project_login.py         # Entry point to the app
├── dashboard.py             # Main dashboard UI
├── README.md

📝 Additional Notes
The application uses ensure_writable_db() internally to make databases writable when compiled as .exe
All local file paths are managed via sys._MEIPASS to ensure compatibility in PyInstaller
Installer can be created using Inno Setup or you can use the provided .exe directly

🔐 Default Admin Login
Username: admin	   
Password: shruti
you cal also register a new user

Running from source:
git clone https://github.com/your-username/BookBuffet.git
cd BookBuffet
pip install -r requirements.txt
python project_login.py
