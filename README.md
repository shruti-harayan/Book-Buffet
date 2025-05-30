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

---

## 🧑‍💻 Technologies Used

| Technology   | Purpose                      |
|--------------|-------------------------------|
| **Python 3.11** | Core programming language  |
| **Tkinter**     | GUI Toolkit                 |
| **SQLite3**     | Local DB for books & members |
| **pandas, numpy** | Data manipulation        |
| **matplotlib**  | Charts (bar, line)          |
| **FPDF**        | Export to PDF               |
| **Pillow (PIL)**| Image/icon handling         |

---

## 🚀 How to Run

### 🟢 Option 1: From Executable (Recommended for Users)

1. Go to [Releases](https://github.com/yourusername/BookBuffet/releases)
2. Download `BookBuffet_v1.0.zip`
3. Extract the ZIP
4. Double-click `project_login.exe`

✅ You're in!

> 📁 Databases and required Excel files are bundled inside the ZIP

---

### 🧑‍💻 Option 2: From Source (For Developers)

```bash
git clone https://github.com/yourusername/BookBuffet.git
cd BookBuffet
pip install -r requirements.txt
python project_login.py
```

🔐 Default Login
---
Username:  admin	
Password:  shruti

Or click the Register button to create your own account.

🔏 License
---
This project is licensed under the MIT License. Feel free to use, modify, and share!


🙋‍♀️ Author
---
Developed by Shruti Harayan

Made with ❤️ using Python + Tkinter
