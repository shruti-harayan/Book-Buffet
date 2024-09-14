from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

root=Tk()
root.title("BOOK BUFFET")
root.iconbitmap("images\\library.ico")
root.geometry('1530x800+0+0')
root.resizable(False, False)
img=PhotoImage(file="images\\imgback1.png")  #adds background image
lb0=Label(root,image=img).pack()

frm=Frame(root,width=520,height=350,bg="black")     #creating a frame
frm.place(x=500,y=270)

logo=PhotoImage(file="images\\admin.png")               #admin logo
logolbl=Label(frm,image=logo,compound='center',bg="black")
logolbl.grid(row=0,column=0,columnspan=2,pady=15)

#label and entry field for username
unameImg=PhotoImage(file="images\\user.png")
username=Label(frm,image=unameImg,text="ENTER USERNAME:",font=("Arial 15 bold"),compound="left",bg="black",fg="white",bd=5)
username.grid(row=1,column=0,padx=10,pady=20)

userEntry=Entry(frm,bd=5,font=("Arial 15 bold"))
userEntry.insert(0,"Enter Username")
userEntry.grid(row=1,column=1,padx=10,pady=20)

#label and entry field for password
passImg=PhotoImage(file="images\\password.png")
password=Label(frm,image=passImg,text="ENTER PASSWORD:",font=("Arial 15 bold"),compound="left",bg="black",fg="white",bd=5)
password.grid(row=2,column=0,padx=10,pady=20)

passEntry=Entry(frm,show="*",bd=5,font=("Arial 15 bold"))
passEntry.grid(row=2,column=1,padx=10,pady=20)

# reset button
resetImg=PhotoImage(file="images\\reset.png")
reset=Button(frm,text="RESET",background="red",font=("Arial 15 bold"),bd=5,activebackground="red",activeforeground="black",
             cursor="hand2",command=lambda:clear(),image=resetImg,compound="left")
reset.grid(row=3,column=0,padx=10,pady=20)

#login button
loginImg=PhotoImage(file="images\\log.png")
login=Button(frm,text="LOGIN",background="green",font=("Arial 15 bold"),bd=5,activebackground="green",activeforeground="black",
             cursor="hand2",command=lambda:log(),image=loginImg,compound="left")
login.grid(row=3,column=1,padx=10,pady=20)

def log():
    uid=userEntry.get()
    pid=passEntry.get()
    dbadmin=sql.connect("admin.db")
    cur=dbadmin.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS UserLogin(User_id TEXT,Password TEXT)")
        cur.execute("SELECT * FROM UserLogin WHERE User_id=?", (uid,))
        record=cur.fetchone()
        if uid == "" or pid == "":
            messagebox.showwarning("Warning","Please fill out require details!!")   
        elif record and record[1]==pid:
            messagebox.showinfo("success","Login successfully......")
            root.destroy()
            import dashboard
        else:
            messagebox.showerror("Error","Please enter correct credentials")
            clear()
    except Exception as e:
            messagebox.showinfo("Database Error", f"SQLite error: {e}")
    finally:
        cur.close()
        dbadmin.close()
def clear():
        userEntry.delete(0,END)
        passEntry.delete(0,END)

root.mainloop()