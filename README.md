📖 Book Buffet – Library Management System
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Desktop-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

A full-featured, standalone desktop application built using Tkinter, SQLite, and Python, designed for managing library operations like book issuance, returns, member registration, backups, and reporting.

✅ This project is compiled into a .exe file and is available as a downloadable release for easy access.

🔧 Features
✅ Add, update, delete, and search books
📚 Issue and return books with automatic quantity updates
👥 Member registration and management
📊 Graphical reports (Bar & Line charts using matplotlib)
📂 Backup to CSV & PDF with one click
🔒 Login system with registration support
💾 Local SQLite3 database (no internet required)
🖼️ Uses FPDF, PIL, pandas, numpy, and Tkinter widgets

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
