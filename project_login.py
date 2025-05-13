from tkinter import *
from tkinter import messagebox
import sqlite3 as sql
import hashlib,os,sys

#to convert relative into absolute path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = Tk()
root.title("BOOK BUFFET")
root.iconbitmap(resource_path("images\\library.ico"))

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.resizable(False, False)


img = PhotoImage(file=resource_path("images\\imgback1.png"))  # Background image
lb0 = Label(root, image=img)
lb0.place(x=0, y=0, relwidth=1, relheight=1)

# Frame for login form
frm = Frame(root, width=520, height=350, bg="black")
frm.place(relx=0.5, rely=0.5, anchor="center")  # Centering the frame

# Admin logo
logo = PhotoImage(file=resource_path("images\\admin.png"))
logolbl = Label(frm, image=logo, bg="black")
logolbl.grid(row=0, column=0, columnspan=3, pady=15)

# Username label and entry
unameImg = PhotoImage(file=resource_path("images\\user.png"))
username = Label(frm, image=unameImg, text="ENTER USERNAME:", font=("Arial 15 bold"), compound="left", bg="black", fg="white", bd=5)
username.grid(row=1, column=0, padx=10, pady=20)

# Username Entry
userEntry = Entry(frm, bd=5, font=("Arial 15 bold"))
userEntry.insert(0, "Enter Username")
userEntry.grid(row=1, column=1, padx=10, pady=20)
userEntry.bind("<FocusIn>", lambda event: clear_placeholder_user())

def clear_placeholder_user():
    if userEntry.get() == "Enter Username":
        userEntry.delete(0, END)

# Password label and entry
passImg = PhotoImage(file=resource_path("images\\password.png"))
password = Label(frm, image=passImg, text="ENTER PASSWORD:", font=("Arial 15 bold"), compound="left", bg="black", fg="white", bd=5)
password.grid(row=2, column=0, padx=10, pady=20)

passEntry = Entry(frm, show="*", bd=5, font=("Arial 15 bold"))
passEntry.grid(row=2, column=1, padx=10, pady=20)

# Show Password checkbox
show_var = IntVar()
show_pass = Checkbutton(frm, text="Show Password", font=("Arial 10 bold"), bg="black", fg="white",activebackground="black", 
                        activeforeground="white",variable=show_var, command=lambda: toggle_password())
show_pass.grid(row=2, column=2, sticky="w", padx=5)

# Reset button
resetImg = PhotoImage(file=resource_path("images\\reset.png"))
reset = Button(frm, text="RESET", background="red", font=("Arial 15 bold"), bd=5, activebackground="red", activeforeground="black",
               cursor="hand2", command=lambda: clear(), image=resetImg, compound="left")
reset.grid(row=3, column=0, padx=10, pady=10)

# Login button
loginImg = PhotoImage(file=resource_path("images\\log.png"))
login = Button(frm, text="LOGIN", background="green", font=("Arial 15 bold"), bd=5, activebackground="green", activeforeground="black",
               cursor="hand2", command=lambda: log(), image=loginImg, compound="left")
login.grid(row=3, column=1,columnspan=2, padx=10, pady=10)

# Register button
register = Button(frm, text="REGISTER", background="blue", font=("Arial 15 bold"), bd=5, activebackground="blue", activeforeground="white",
                  cursor="hand2", command=lambda: register_new(), compound="left")
register.grid(row=4, column=0, columnspan=3, pady=10)

# ===== Functions =====
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def log():
    uid = userEntry.get()
    pid = passEntry.get()
    dbadmin = sql.connect(resource_path("admin.db"))
    cur = dbadmin.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS UserLogin(User_id TEXT, Password TEXT)")
        cur.execute("SELECT * FROM UserLogin WHERE User_id=?", (uid,))
        record = cur.fetchone()
        hashed = hash_pass(pid)
        if uid == "" or pid == "":
            messagebox.showwarning("Warning", "Please fill out all required details!")
        elif record and record[1] == hashed:
            messagebox.showinfo("Success", "Login successful!")
            root.destroy()
            import dashboard
        else:
            messagebox.showerror("Error", "Invalid username or password!")
            clear()
    except Exception as e:
        messagebox.showerror("Database Error", f"SQLite error: {e}")
    finally:
        cur.close()
        dbadmin.close()

def clear():
    userEntry.delete(0, END)
    passEntry.delete(0, END)

def toggle_password():
    if show_var.get():
        passEntry.config(show="")  # Show password
    else:
        passEntry.config(show="*")  # Hide password

def register_new():
    new_user = userEntry.get()
    new_pass = passEntry.get()
    if not new_user or not new_pass or new_user == "Enter Username":
        messagebox.showwarning("Warning", "Please enter both username and password to register!")
        return

    dbadmin = sql.connect(resource_path("admin.db"))
    cur = dbadmin.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS UserLogin(User_id TEXT, Password TEXT)")
        cur.execute("SELECT * FROM UserLogin WHERE User_id=?", (new_user,))
        record = cur.fetchone()
        if record:
            messagebox.showerror("Error", "Username already exists! Please choose another.")
        else:
            #store  password in hashed form for security
            hashed = hash_pass(new_pass)
            cur.execute("INSERT INTO UserLogin(User_id, Password) VALUES(?, ?)", (new_user, hashed))
            dbadmin.commit()
            messagebox.showinfo("Success", "Registration successful! You can now login.")
            clear()
    except Exception as e:
        messagebox.showerror("Database Error", f"SQLite error: {e}")
    finally:
        cur.close()
        dbadmin.close()

# BIND ENTER KEY TO LOGIN FUNCTION
root.bind('<Return>', lambda event: log())
root.mainloop()
