import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import os,re,webbrowser,csv,sys,subprocess
from datetime import datetime,timedelta
from tkinter.ttk import Combobox
import numpy as np, matplotlib.pyplot as plt,pandas as pd, sqlite3 as sql
from fpdf import FPDF
from datetime import datetime
from PIL import Image, ImageTk

month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
y = list(range(2023, 2040))
d = list(range(1, 32))

#to convert relative into absolute path
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.title("BOOK BUFFET")
root.iconbitmap(resource_path('images\\library.ico'))

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Set the geometry to full screen
root.geometry(f"{screen_width}x{screen_height}+0+0")
root.resizable(False, False)
root.configure(bg="white")

#Header with moving text
def move_text():
    if header_label.winfo_exists():
        current = header_label.cget("text")
        new = current[1:] + current[0]
        header_label.config(text=new)
        root.after(200, move_text)

header_frame = tk.Frame(root, bg="blue")
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="!!! WELCOME ADMIN !!!", font=("arial", 20, "bold"), fg="white", bg="blue")
header_label.pack(side=tk.LEFT, padx=10)
move_text()

#funtion to display date and time
def update_datetime():
    if time_label.winfo_exists():
        now = datetime.now()
        time_label.config(text=f"Time: {now.strftime('%H:%M:%S')}")
        date_label.config(text=f"Date: {now.strftime('%d/%m/%Y')}  ")
        root.after(1000, update_datetime)

time_label = tk.Label(header_frame, font=("arial", 16, "bold"), fg="white", bg="blue")
time_label.pack(side=tk.RIGHT, padx=10)
date_label = tk.Label(header_frame, font=("arial", 16, "bold"), fg="white", bg="blue")
date_label.pack(side=tk.RIGHT)
update_datetime()

#function to refresh the treeview
def refresh():
    #to change the bg color of row based on even/odd number of row  or low stock 
    book_tree.tag_configure('oddrow',background="white")
    book_tree.tag_configure('evenrow',background="lightblue")
    book_tree.tag_configure("lowstock", background="salmon")
    #clear the treeview
    book_tree.delete(*book_tree.get_children())

    dbbook=sql.connect(resource_path("BookDB.db"))
    cur = dbbook.cursor()
    cur.execute("SELECT * FROM Book")
    records=cur.fetchall()
    for index, record in enumerate(records):
        tags = []
        if int(record[4]) <= 5:
            tags.append("lowstock")
        else:
            tags.append("evenrow" if index % 2 == 0 else "oddrow")

        book_tree.insert("", "end", values=record, tags=tags)
        
    dbbook.commit()
    cur.close()
    dbbook.close()

#function to add new book to the database
def add_book():
    popup = Toplevel(root)
    popup.title("Add Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")   #set background color

    global backbtnImg,book_idImg,book_idLabel,book_titleLabel,book_titleImg,book_authorImg,book_authorLabel,book_priceImg
    global book_priceLabel,book_quantityImg,book_quantityLabel,addbookLabel,clear
    #clear all the fields
    def clear():
        book_idEntry.delete(0,END)
        book_titleEntry.delete(0,END)
        book_authorEntry.delete(0,END)
        book_priceEntry.delete(0,END)
        book_quantityEntry.delete(0,END)

    #destroy the popup window
    def destry():
       popup.destroy()

    #validity check for title and author name does not contain numbers or special symbol other than those specified
    def is_valid_name(name):
        return bool(re.fullmatch(r"[A-Za-z .'?+]+", name.strip()))

    #add new book entry in the database
    def addnewbook():        
        global book_id,title,author,price,quantity,dbbook,cur
        book_id=book_idEntry.get()
        title=book_titleEntry.get()
        author=book_authorEntry.get()
        price=book_priceEntry.get()
        quantity=book_quantityEntry.get()

        dbbook=sql.connect(resource_path("BookDB.db"))
        cur=dbbook.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS Book(
            Book_ID TEXT,Title TEXT,Author TEXT,
            Price INT,Quantity INT)
             """)
        try:
            # Check if the book already exists
            cur.execute("SELECT * FROM Book WHERE Book_ID=?",(book_id,))
            query=cur.fetchone()
            if query:
                messagebox.showwarning("Warning","A Book with same ID already exist!!!!")
            else:
                q='INSERT INTO Book VALUES(?,?,?,?,?)'
                value=(book_id,title,author,int(price),int(quantity))
                cur.execute(q,value)
                dbbook.commit()
                messagebox.showinfo("success","Book Added Successfully!!!")
                book_tree.insert("","end",values=(value[0], value[1], value[2], value[3], value[4]) ) #update the treeview after adding new values
                refresh()           #refresh the treeview after adding new values
                clear()
        except Exception as e:
            messagebox.showerror("ERROR", f"Something went wrong:\n{e}")
        cur.close()
        dbbook.close()
    
    def add():
        title = book_titleEntry.get()
        author = book_authorEntry.get()
    
        if (book_idEntry.get().strip() == "" or 
            title.strip() == "" or 
            book_authorEntry.get().strip() == "" or 
            book_priceEntry.get().strip() == "" or 
            book_quantityEntry.get().strip() == ""):
            messagebox.showwarning("Warning", "Please fill out all the details!!")
        elif not is_valid_name(title):
            messagebox.showwarning("Invalid Input", "Please enter a valid book title (letters and spaces only).")
        elif not is_valid_name(author):
            messagebox.showwarning("Invalid Input", "Please enter a valid author name (letters and spaces only).")
        else:
            addnewbook()
    
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#heading
    addbookLabel=Label(popup,text="ADD BOOK",anchor="center",bg="blue",width=60,fg="white",font=("Arial 14 bold"))
    addbookLabel.grid(row=0,column=1,sticky="nsew")
#book_id label
    book_idImg=PhotoImage(file=resource_path("images\\book_id.png"))
    book_idLabel=Label(popup,text="    BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_idImg,compound="left",bd=4)
    book_idLabel.grid(row=1,column=1,rowspan=1,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=1,padx=10,pady=10,sticky="s")

#book title label
    book_titleImg=PhotoImage(file=resource_path("images\\book_title.png"))
    book_titleLabel=Label(popup,text="    TITLE: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_titleImg,compound="left",bd=4)
    book_titleLabel.grid(row=2,column=1,sticky="w")
#book title entry box
    book_titleEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_titleEntry.insert(0,"Enter Book Name")
    book_titleEntry.grid(row=2,column=1,padx=10,pady=10,sticky="s")

#book Author label
    book_authorImg=PhotoImage(file=resource_path("images\\book_author.png"))
    book_authorLabel=Label(popup,text="    AUTHOR: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_authorImg,compound="left",bd=4)
    book_authorLabel.grid(row=3,column=1,sticky="w")
#book title entry box
    book_authorEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_authorEntry.insert(0,"Enter Author Name")
    book_authorEntry.grid(row=3,column=1,padx=10,pady=10,sticky="s")

#book Price label
    book_priceImg=PhotoImage(file=resource_path("images\\book_price.png"))
    book_priceLabel=Label(popup,text="    PRICE: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_priceImg,compound="left",bd=4)
    book_priceLabel.grid(row=4,column=1,sticky="w")
#book Price entry box
    book_priceEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_priceEntry.insert(0,"Enter Book Price")
    book_priceEntry.grid(row=4,column=1,padx=10,pady=10,sticky="s")

#book Quantity label
    book_quantityImg=PhotoImage(file=resource_path("images\\book_quantity.png"))
    book_quantityLabel=Label(popup,text="    QUANTITY: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_quantityImg,compound="left",bd=4)
    book_quantityLabel.grid(row=5,column=1,sticky="w")
#book Quantity entry box
    book_quantityEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_quantityEntry.insert(0,"Enter Book Quantity")
    book_quantityEntry.grid(row=5,column=1,padx=10,pady=10,sticky="s")
  
#add button
    addbtn=Button(popup,text="ADD",background="green",font=("Arial 14 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:add())
    addbtn.grid(row=1,column=1,pady=20,sticky="e")
#reset button
    reset=Button(popup,text="CLEAR",background="red",font=("Arial 14 bold"),bd=5,activebackground="red",activeforeground="black"
                 ,cursor="hand2",command=clear,width=10)
    reset.grid(row=2,column=1,pady=20,sticky="e")


#function for updating book details
def update_book():
    popup = Toplevel(root)
    popup.title("Update Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    global updatebookLabel,backbtnImg,book_id,book_idEntry,book_idImg
    def destry():
        popup.destroy()
        backbtnImg.config()

    def updt():
        up = Toplevel(popup)
        up.title('Edit Book')
        up.geometry("800x400+530+300")
        up.resizable(False,False)
        up.config(bg="yellow")
        
        def reset():
            book_idEntry.delete(0,END)
            book_titleEntry.delete(0,END)
            book_authorEntry.delete(0,END)
            book_priceEntry.delete(0,END)
            book_quantityEntry.delete(0,END)

        def savefunc():
            global book_id,title,author,price,quantity,existing_book
            new_book_id=book_idEntry.get()
            title=book_titleEntry.get()
            author=book_authorEntry.get()
            price=book_priceEntry.get()
            quantity=book_quantityEntry.get()

            if not book_id or not title or not author or not price or not quantity:
                messagebox.showwarning("Warning","Please fill out all the details!!!!")
                return  # Do not continue
            else: 
                try:
                    confirm = messagebox.askyesno("Confirm Update", "Are you sure you want to update this book's details?")
                    if confirm:
                        cur.execute("UPDATE Book SET Book_ID=?,Title=?,Author=?,Price=?,Quantity=? WHERE Book_ID=?",
                            (new_book_id, title, author, price, quantity, book_id))
                        dbbook.commit()
                        messagebox.showinfo("SUCCESS", "Details updated successfully!")
                        viewbook()  # Refresh the TreeView
                        up.destroy()
                        cur.close()
                        dbbook.close()
                    else:
                        messagebox.showinfo("Cancelled", "Update cancelled.")
                        up.destroy()  # Close the edit popup if user cancels
                except sql.Error as e:
                    messagebox.showerror("ERROR", f"SQLite error: {e}")
           
#heading text
        lb1=Label(up,text="Update Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
        lb1.grid(row=0,column=0,sticky="nsew")
#Update book_id Label
        book_idLabel=Label(up,text="    BOOK ID: ",font=("Arial 12 bold"),bg="yellow",bd=4)
        book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#Update book_id entry box
        book_idEntry=Entry(up,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        book_idEntry.grid(row=1,column=0,padx=10,pady=15,sticky="n")
#Update book title label
        book_titleLabel=Label(up,text="    TITLE: ",font=("Arial 12 bold"),bd=4,bg="yellow")
        book_titleLabel.grid(row=2,column=0,padx=20,pady=10,sticky="w")
#Update book title entry box
        book_titleEntry=Entry(up,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        book_titleEntry.grid(row=2,column=0,padx=10,pady=10,sticky="n")
#Update book Author label
        book_authorLabel=Label(up,text="    AUTHOR: ",font=("Arial 12 bold"),bg="yellow",bd=4)
        book_authorLabel.grid(row=3,column=0,padx=20,pady=10,sticky="w")
#Update book title entry box
        book_authorEntry=Entry(up,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        book_authorEntry.grid(row=3,column=0,padx=10,pady=10,sticky="n")
#Update book Price label
        book_priceLabel=Label(up,text="    PRICE: ",font=("Arial 12 bold"),bg="yellow",bd=4)
        book_priceLabel.grid(row=4,column=0,padx=20,pady=10,sticky="w")
#Update book Price entry box
        book_priceEntry=Entry(up,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        book_priceEntry.grid(row=4,column=0,padx=10,pady=10,sticky="n")
#Update book Quantity label
        book_quantityLabel=Label(up,text="    QUANTITY: ",font=("Arial 12 bold"),bg="yellow",bd=4)
        book_quantityLabel.grid(row=5,column=0,padx=20,pady=10,sticky="w")
#Update book Quantity entry box
        book_quantityEntry=Entry(up,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        book_quantityEntry.grid(row=5,column=0,padx=10,pady=10,sticky="n")
#clear button
        clearbtn=Button(up,text="clear",bd=5,font=("Arial 12 bold"),background="red",width=10,command=lambda:reset(),
                    activebackground="red",activeforeground="black")
        clearbtn.grid(row=6,column=0,pady=10,sticky="n")      
#save button
        save=Button(up,text="SAVE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:savefunc())
        save.grid(row=6,column=0,pady=10,padx=30,sticky="w")

        try:
            dbbook=sql.connect(resource_path("BookDB.db"))
            cur=dbbook.cursor()
            cur.execute("SELECT * FROM Book WHERE Book_ID=?",(book_id,))
            value = cur.fetchone()
            if value is not None:
                book_idEntry.insert(0,value[0])
                book_titleEntry.insert(0,value[1])
                book_authorEntry.insert(0,value[2])
                book_priceEntry.insert(0,value[3])
                book_quantityEntry.insert(0,value[4])
        except sql.Error as e:
            print(f"SQLite error: {e}")
        up.mainloop()

    def check():
            global existing_book,book_id
            book_id=book_idEntry.get()
            dbbook=sql.connect(resource_path("BookDB.db"))
            cur=dbbook.cursor()
            #check if book already exist
            cur.execute("SELECT * FROM Book WHERE Book_ID=?",(book_id,))
            existing_book=cur.fetchone()
            if existing_book:
                book_id=existing_book[0]
                updt()
            elif book_id=="":
                messagebox.showwarning("Warning","Please provide a value !!")
            else:
                messagebox.showwarning("Warning","Book does not exists in database!!!")

#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#heading
    updatebookLabel=Label(popup,text="UPDATE BOOK",anchor="center",bg="blue",width=60,fg="white",font=("Arial 14 bold"))
    updatebookLabel.grid(row=0,column=1,sticky="nsew")
    #book_id label
    book_idImg=PhotoImage(file=resource_path("images\\book_id.png"))
    book_idLabel=Label(popup,text="  BOOK ID:",font=("Arial 12 bold"),bg="#b9f8f8",image=book_idImg,compound="left",bd=4)
    book_idLabel.grid(row=1,column=1,rowspan=2,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=1,padx=5,pady=20,sticky="s")
#submit button
    submitbtn=Button(popup,text="SUBMIT",background="green",font=("Arial 14 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:check())
    submitbtn.grid(row=1,column=1,pady=20,sticky="e")

#User interface to add new member
def add_new_member():
    popup = Toplevel(root)
    popup.title("Add new member")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    global member_idLabel,member_nameLabel,member_emailLabel,member_yearLabel,member_courseLabel
    global member_idEntry,member_nameEntry,member_emailEntry,member_yearEntry,member_courseEntry
    global backbtnImg,member_idImg,member_nameImg,member_emailImg,member_yearImg,member_courseImg
    def clear():
        member_idEntry.delete(0,END)
        member_nameEntry.delete(0,END)
        member_emailEntry.delete(0,END)
        member_yearEntry.delete(0,END)
        member_courseEntry.delete(0,END)
    def destry():
        popup.destroy()

#heading label
    lb1=Label(popup,text="Add New Member",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#member_id label
    member_idImg=PhotoImage(file=resource_path("images\\mem_id.png"))
    member_idLabel=Label(popup,text=" Enter Member ID:",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_idImg,compound="left")
    member_idLabel.grid(row=1,column=0,padx=20,pady=5,sticky="w")
#member_id entry box
    member_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.insert(0,"Enter Member ID")
    member_idEntry.grid(row=1,column=0,padx=10,pady=5,sticky="s")

#member_name label
    member_nameImg=PhotoImage(file=resource_path("images\\mem_name.png"))
    member_nameLabel=Label(popup,text=" Enter Member Name:",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_nameImg,compound="left")
    member_nameLabel.grid(row=2,column=0,padx=10,pady=5,sticky="w")
#member_name entry box
    member_nameEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_nameEntry.insert(0,"Enter Member Name")
    member_nameEntry.grid(row=2,column=0,padx=10,pady=5,sticky="s")

#member email label
    member_emailImg=PhotoImage(file=resource_path("images\\mem_email.png"))
    member_emailLabel=Label(popup,text="  Enter Email ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_emailImg,compound="left")
    member_emailLabel.grid(row=3,column=0,padx=20,pady=5,sticky="w")
#member_email entry box
    member_emailEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_emailEntry.insert(0,"Enter Email ID")
    member_emailEntry.grid(row=3,column=0,padx=10,pady=5,sticky="s")

#member year of studying label
    member_yearImg=PhotoImage(file=resource_path("images\\mem_year.png"))
    member_yearLabel=Label(popup,text="Enter year of studying: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_yearImg,compound="left")
    member_yearLabel.grid(row=4,column=0,padx=20,pady=5,sticky="w")
#member year of studying entry box
    member_yearEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_yearEntry.insert(0,"Enter Year of studying")
    member_yearEntry.grid(row=4,column=0,padx=10,pady=5,sticky="s")

#member select course label
    member_courseImg=PhotoImage(file=resource_path("images\\mem_course.png"))
    member_courseLabel=Label(popup,text="  Enter Course Name: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_courseImg,compound="left")
    member_courseLabel.grid(row=5,column=0,padx=20,pady=5,sticky="w")
#member select course entry box
    member_courseEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_courseEntry.insert(0,"Enter Course Name")
    member_courseEntry.grid(row=5,column=0,padx=10,pady=5,sticky="s")

#save button
    save=Button(popup,text="SAVE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:addnewmember())
    save.grid(row=1,column=1,pady=20,sticky="w")
#reset button
    reset=Button(popup,text="CLEAR",background="red",font=("Arial 14 bold"),bd=5,activebackground="red",activeforeground="black"
                 ,cursor="hand2",command=lambda:clear(),width=10)
    reset.grid(row=2,column=1,pady=20,sticky="w")

#update new member in database
def addnewmember():
    global mem_id,mem_name,year,email,course
    mem_id=member_idEntry.get()
    mem_name=member_nameEntry.get()
    email=member_emailEntry.get()
    year=member_yearEntry.get()
    course=member_courseEntry.get()

    #validation to check member name and course name
    def is_valid_name(name):
        return bool(re.fullmatch(r"[A-Za-z ]+",name.strip()))
    
    #validation to check email ID
    def is_valid_email(e):
        pattern = r"^[A-Za-z0-9._]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.fullmatch(pattern,e.strip()))

    if not mem_id or not mem_name or not email or not year or not course:
        messagebox.showwarning("Warning","Please fill out require details!!")
        return

    dbmemb=sql.connect(resource_path("MemDB.db"))
    cur=dbmemb.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS member(Member_ID INT,Member_Name TEXT,Email TEXT,Year INT,Course TEXT)
             """)
    try:
        mem_id = int(mem_id)
        year = int(year)
        if not 1 <= year <= 4:
            messagebox.showwarning("Warning", "Year should be between 1 and 4!!")
            return
    except ValueError:
        messagebox.showwarning("Warning", "ID and Year should be integer values!!")
        return
          
    try:
        cur.execute("SELECT * FROM member WHERE Member_ID=?",(mem_id,))
        existing_member = cur.fetchone()
        if existing_member:
            messagebox.showwarning("Warning", f"Member with ID {mem_id} already exists!")
        elif not is_valid_email(email):
            messagebox.showwarning("Invalid Input", "Please enter a valid email(Eg:xyz12@gmail.com)")
        elif not is_valid_name(course):
            messagebox.showwarning("Invalid Input", "Please enter a valid course name.")
        elif not is_valid_name(mem_name):
            messagebox.showwarning("Invalid Input", "Please enter a valid member name.")
        else:
            cur.execute("INSERT INTO member(Member_ID,Member_Name,Email,Year,Course) VALUES(?,?,?,?,?)",(mem_id,mem_name,email,year,course))
            dbmemb.commit()
            messagebox.showinfo("SUCCESS", "Member Added Successfully!!!!!")
    except sql.Error as e:
        messagebox.showerror("ERROR", f"SQLite error: {e}")
    cur.close()
    dbmemb.close()

#to delete existing book from the database
def delete_book():
    popup = Toplevel(root)
    popup.title("Delete Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    global book_idEntry,book_idImg,backbtnImg
    def destry():
        popup.destroy()
        
    #delete book from database
    def delfunc():
        global book_id
        book_id=book_idEntry.get()
        dbbook=sql.connect(resource_path("BookDB.db"))
        cur=dbbook.cursor()
        # Check if book_id is not empty
        if book_id=="":
            messagebox.showwarning("Warning", "Please enter Book ID.")
            return
        cur.execute("SELECT * FROM Book WHERE Book_id=?",(book_id,))
        result=cur.fetchone()
        if not result:
            messagebox.showwarning("Warning","Book Does Not Exist")
            return
        else:
            try:
                response=messagebox.askyesno("CONFIRM","Do you really want to Delete this book !!!")
                # Take action based on user's response
                if response:
                    cur.execute("DELETE FROM Book WHERE Book_id=?",(book_id,))    
                    dbbook.commit()
                    messagebox.showinfo("SUCCESS", "Book deleted successfully!!!")
                    # update the TreeView 
                    refresh()
                else:
                    messagebox.showinfo("INFO", "Deletion canceled.")
            except sql.Error as e:
                messagebox.showerror("ERROR", f"SQLite error: {e}")
        cur.close()
        dbbook.close()

#heading label
    lb1=Label(popup,text="Delete Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=destry)
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file=resource_path("images\\book_id.png"))
    book_idLabel=Label(popup,text="   Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=book_idImg,compound="left")
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")
#submit button
    submit=Button(popup,text="DELETE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=delfunc)
    submit.grid(row=2,column=0,pady=10,padx=30,sticky="s")

#to search existing book details
def search_book():
    global backbtnImg, book_idImg
    popup = Toplevel(root)
    popup.title("Search Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    result_window = None  # Reference to the result window

    def perform_search():
        nonlocal result_window
        book_id = book_idEntry.get().strip()
        if not book_id:
            messagebox.showwarning("Warning", "Please enter Book ID!!")
            return

        dbbook = sql.connect(resource_path("BookDB.db"))
        cur = dbbook.cursor()
        try:
            cur.execute("SELECT * FROM Book WHERE Book_ID=?", (book_id,))
            book_data = cur.fetchone()

            if not book_data:
                messagebox.showwarning("Error", "Book does not exist!!!")
                return

            # Destroy previous result window if already opened
            if result_window and result_window.winfo_exists():
                result_window.destroy()

            # Create result window
            result_window = Toplevel(popup)
            result_window.title("Search Result")
            result_window.geometry("500x300+600+380")
            result_window.configure(bg="yellow")

            Label(result_window, text="Book Found!", font=("Arial 14 bold"), bg="blue", fg="white", width=30).pack(pady=10)

            details_labels = ["Book_ID", "Title", "Author", "Price", "Quantity"]
            for i, attribute in enumerate(details_labels):
                Label(result_window, text=f"{attribute}: {book_data[i]}", font=("Arial 12 bold"), bg="yellow").pack(anchor="w", padx=20, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
        finally:
            cur.close()
            dbbook.close()

    def destry():
        popup.destroy()
        if result_window and result_window.winfo_exists():
            result_window.destroy()

    # === UI Elements ===
    Label(popup, text="Search Book", font=("Arial 14 bold"), bd=5, bg="blue", fg="white", width=60).grid(row=0, column=0, sticky="nsew")

    backbtnImg = PhotoImage(file=resource_path("images\\backbtn.png"))
    Button(popup, text=" BACK", image=backbtnImg, font=("Arial 12 bold"), compound="left", bd=5, command=destry).grid(row=0, column=0, sticky="w")

    book_idImg = PhotoImage(file=resource_path("images\\book_id.png"))
    Label(popup, text=" Enter BOOK ID: ", font=("Arial 12 bold"), bg="#b9f8f8", bd=4, image=book_idImg, compound="left").grid(row=1, column=0, padx=20, pady=10, sticky="w")

    book_idEntry = Entry(popup, bd=5, font=("Arial 12 bold"), fg="blue", width=30)
    book_idEntry.insert(0, "Enter Book ID")
    book_idEntry.grid(row=1, column=0, padx=10, pady=10, sticky="s")

    Button(popup, text="SEARCH", background="green", font=("Arial 12 bold"), bd=5, activebackground="green",
           activeforeground="black", cursor="hand2", width=10, command=perform_search).grid(row=2, column=0, pady=10, padx=30, sticky="s")

#return book
def return_book():
    popup = Toplevel(root)
    popup.title("Return Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    global retrn,backbtnImg,book_idImg,member_idImg,return_dateImg
    def destry():
        popup.destroy()

#heading label
    lb1=Label(popup,text="Return Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file=resource_path("images\\book_id.png"))
    book_idLabel=Label(popup,text="Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=book_idImg)
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")
#member_id label
    member_idImg=PhotoImage(file=resource_path("images\\mem_id.png"))
    member_idLabel=Label(popup,text="Enter Member ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=member_idImg)
    member_idLabel.grid(row=2,column=0,padx=20,pady=10,sticky="w")
#member_id entry box
    member_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.insert(0,"Enter Member ID")
    member_idEntry.grid(row=2,column=0,padx=10,pady=10,sticky="s")
#return date label
    return_dateImg=PhotoImage(file=resource_path("images\\return_date.png"))
    return_dateLabel=Label(popup,text="Return Date: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=return_dateImg)
    return_dateLabel.grid(row=3,column=0,padx=20,pady=10,sticky="w")
#return date combobox
    # Combobox for year, month, and date
    return_year = Combobox(popup, values=y, width=5, font=("Arial 11 bold"), justify="center", state="readonly")
    return_month = Combobox(popup, values=month, width=10, font=("Arial 11 bold"), justify="center", state="readonly")
    return_date = Combobox(popup, width=5, font=("Arial 11 bold"), justify="center", state="readonly")

    return_year.place(x=200, y=185)
    return_month.place(x=270, y=185)
    return_date.place(x=360, y=185)

    # Set today's date initially
    now = datetime.now()
    return_year.set(now.year)
    return_month.set(month[now.month - 1])

#return button
    returnbtn=Button(popup,text="RETURN",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:returnfunc())
    returnbtn.grid(row=4,column=0,pady=10,padx=30,sticky="n")
    
#auto updates date so user can select only valid dates for specific month(eg. 30th for april,31st for dec.)
    def update_days(event=None):
        selected_month = return_month.get()
        selected_year = int(return_year.get())

        if selected_month in ("April", "June", "September", "November"):
            days = list(range(1, 31))  # 30 days
        elif selected_month == "February":
            # Check for leap year
            if (selected_year % 4 == 0 and selected_year % 100 != 0) or (selected_year % 400 == 0):
                days = list(range(1, 30))  # 29 days
            else:
                days = list(range(1, 29))  # 28 days
        else:
            days = list(range(1, 32))  # 31 days

        return_date['values'] = days
        if int(return_date.get() or 0) > len(days):
            return_date.set(days[-1])
        else:
            if not return_date.get():
                return_date.set(1)  # Default to 1st if nothing selected

    return_month.bind("<<ComboboxSelected>>", update_days)
    return_year.bind("<<ComboboxSelected>>", update_days)

    # Call once initially
    update_days()


#to calculate fine on late return
    def fine(book_id, member_id, expected_return_date_str):
        dbmemb=sql.connect(resource_path("MemDB.db"))
        cursor=dbmemb.cursor()
        try:
            # Convert string dates to datetime objects
            expected_return_date = datetime.strptime(expected_return_date_str, "%Y-%m-%d")
            actual_return_date = datetime(int(return_year.get()), month.index(return_month.get()) + 1, int(return_date.get()))

            # Calculate fine
            if actual_return_date > expected_return_date:
                days_late = (actual_return_date - expected_return_date).days
                calculated_fine = days_late * 2  # fine_rate_per_day
                confirm_fine = messagebox.askyesno("Calculate Fine", f"Calculate fine for {days_late} days late?")
                if confirm_fine:
                    messagebox.showinfo("Fine Calculation", f"Fine for {days_late} days late: Rs. {calculated_fine}")
                    # Delete the record from the database after calculating fine
                    cursor.execute("DELETE FROM Expected_Return_Dates WHERE BookID=? AND MemberID=?", (book_id, member_id))
                    dbmemb.commit()
                if not confirm_fine:
                    # Delete the record from the database even if user wish not to calculate fine on late return
                    cursor.execute("DELETE FROM Expected_Return_Dates WHERE BookID=? AND MemberID=?", (book_id, member_id))
                    dbmemb.commit()
            else:
                messagebox.showinfo("No fine", "Book returned on time")
                # Delete expected return date from the database after successfull return
                cursor.execute("DELETE FROM Expected_Return_Dates WHERE BookID=? AND MemberID=?", (book_id, member_id))
                dbmemb.commit()
        except Exception as e:
            messagebox.showerror("ERROR", f"Error: {e}")
        finally:
            cursor.close()
            dbmemb.close()

    
    def returnfunc(): 
        book_id=book_idEntry.get()
        member_id=member_idEntry.get()
        if not book_id or not member_id:
            messagebox.showwarning("Warning", "Please enter a value!!")
            return
        
        dbmemb=sql.connect(resource_path("MemDB.db"))
        cursor=dbmemb.cursor()
        cursor.execute("SELECT * FROM member WHERE Member_ID=?",(member_id,))
        memb=cursor.fetchone()
        if not memb:
            messagebox.showwarning("Error","Member does not exist!!!")   
            return   
          
        dbbook=sql.connect(resource_path("BookDB.db"))
        cur=dbbook.cursor()
        cur.execute("SELECT * FROM Book WHERE Book_ID=?",(book_id,))
        book_data=cur.fetchone()
        if not book_data:
            messagebox.showwarning("Error","Book does not exist!!!")  
            return
        try:     
            # Check if the book is issued to the member
            cur.execute("SELECT * FROM issue WHERE Book_ID=? AND Member_ID=?", (book_id, member_id))
            issued_book = cur.fetchone()
            if not issued_book:
                messagebox.showwarning("Warning", "Book is not currently issued to the specified member!")      
            else: 
                confirm=messagebox.askyesno("CONFIRM","Do you really want to Return this book!!!")
                if confirm:
                    # Fetch additional details of the book
                    cur.execute("SELECT Title, Author, Price FROM Book WHERE Book_ID=?", (book_id,))
                    book_details = cur.fetchone()
                    title, author, price = book_details
                    cur.execute("SELECT Quantity FROM Book WHERE Book_ID=?",(book_id,))
                    quantity=cur.fetchone()[0]
                    new_quantity=quantity+1
                    cur.execute("UPDATE Book SET Quantity=? WHERE Book_ID=?",(new_quantity,book_id,))
                    cur.execute("DELETE FROM issue WHERE Book_ID=? AND Member_ID=?",(book_id,member_id,))
                    dbbook.commit()

                    # Get the expected return date from the database
                    cursor.execute("SELECT ExpectedReturnDate FROM Expected_Return_Dates WHERE BookID=? AND MemberID=?", (book_id, member_id))
                    expected_return_date = cursor.fetchone()

                    # Calculate and display fine based on expected return date
                    if expected_return_date:
                        fine(book_id, member_id, expected_return_date[0])  

                    messagebox.showinfo("SUCCESS", "Book returned successfully!!!")
                    destry()
                    #update the treeview  
                    book_tree.item(book_id, values=(book_id, title, author, price, new_quantity))   
                else:
                    messagebox.showinfo("INFO", "Return canceled.")
                    destry()
        except Exception as e:
            messagebox.showinfo("Error",f"Sqlite error {e}")
        finally:
            destry()
            cur.close()
            dbbook.close()
            cursor.close()
            dbmemb.close()

#function to issue book to existing member
def issue_book():
    popup = Toplevel(root)
    popup.title("Issue Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    global backbtnImg,book_idImg,member_idImg,issue_dateImg
    def destry():
        popup.destroy()
    
    def is_already_issued(member_id, book_id):
        dbbook = sql.connect(resource_path("BookDB.db"))
        cur = dbbook.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS issue (Member_ID TEXT, Member_Name TEXT, Book_ID TEXT, Issue_Date TEXT)")
        cur.execute("SELECT * FROM issue WHERE Member_ID=? AND Book_ID=?", (member_id, book_id))
        result = cur.fetchone()
        cur.close()
        dbbook.close()
        return result is not None

    #command to issue book
    def handle_issue_book():
        member_id = member_idEntry.get().strip()
        book_id = book_idEntry.get().strip()

        if not book_id or not member_id:
            messagebox.showwarning("Warning", "Please Enter Member ID/Book ID")
            return

        # Check if already issued
        if is_already_issued(member_id, book_id):
            messagebox.showwarning("Warning", "This book is already issued to this member.")
            return

        # Check if member and book exist
        member_exists = check_member_exists(member_id)
        book_exists, book_info = check_book_exists(book_id)

        if not member_exists or not book_exists:
            messagebox.showwarning("Warning", "Invalid Member ID or Book ID")
            return

        try:
            if book_info["Quantity"] > 0:
                new_quantity = book_info["Quantity"] - 1
                update_book_quantity(book_id, new_quantity)
                issue_book_to_member(member_id, book_id)
                messagebox.showinfo("SUCCESS", "Book issued successfully!")

                # update treeview
                dbbook = sql.connect(resource_path("BookDB.db"))
                cur = dbbook.cursor()
                cur.execute("SELECT Title, Author, Price FROM Book WHERE Book_ID=?", (book_id,))
                book_details = cur.fetchone()
                cur.close()
                dbbook.close()

                if book_details:
                    title, author, price = book_details
                    book_tree.item(book_id, values=(book_id, title, author, price, new_quantity))
            else:
                messagebox.showwarning("Warning", "Book is not available.")
        except sql.Error as e:
            messagebox.showerror("ERROR", f"Error: {e}")


    def check_member_exists(member_id):
        dbmemb = sql.connect(resource_path("MemDB.db"))
        cur = dbmemb.cursor()
        cur.execute("SELECT * FROM member WHERE Member_ID=?", (member_id,))
        member_exists = cur.fetchone() is not None
        cur.close()
        dbmemb.close()
        return member_exists

    def check_book_exists(book_id):
        dbbook = sql.connect(resource_path("BookDB.db"))
        cur = dbbook.cursor()
        cur.execute("SELECT * FROM Book WHERE Book_ID=?", (book_id,))
        book_info = cur.fetchone()
        book_exists = book_info is not None
        cur.close()
        dbbook.close()
        return book_exists, {"Quantity": int(book_info[4])} if book_exists else {}

    def update_book_quantity(book_id, new_quantity):
        dbbook = sql.connect(resource_path("BookDB.db"))
        cur = dbbook.cursor()
        cur.execute("UPDATE Book SET Quantity=? WHERE Book_ID=?", (new_quantity, book_id))
        dbbook.commit()
        cur.close()
        dbbook.close()

    def issue_book_to_member(member_id, book_id):
        dbmemb = dbbook = None
        cursor = cur = None
        try:
            dbmemb = sql.connect(resource_path("MemDB.db"))
            cursor = dbmemb.cursor()
            cursor.execute("SELECT Member_Name FROM member WHERE Member_ID=?", (member_id,))
            member = cursor.fetchone()

            if not member:
                messagebox.showwarning("Warning", "Member not found.")
                return

            dbbook = sql.connect(resource_path("BookDB.db"))
            cur = dbbook.cursor()

            # Ensure tables exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS issue (
                    Member_ID TEXT,
                    Member_Name TEXT,
                    Book_ID TEXT,
                    Issue_Date TEXT
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Expected_Return_Dates (
                    Book_ID TEXT,
                    Member_ID TEXT,
                    Expected_Return_Date TEXT
                )
            """)

            issue_date = datetime.now().strftime("%Y-%m-%d")
            expected_return_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

            # Insert into issue table
            cur.execute("INSERT INTO issue VALUES (?, ?, ?, ?)", (member_id, member[0], book_id, issue_date))
            dbbook.commit()

            # Insert into Expected_Return_Dates
            cursor.execute("INSERT INTO Expected_Return_Dates VALUES (?, ?, ?)", (book_id, member_id, expected_return_date))
            dbmemb.commit()

        except Exception as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
        finally:
            if cur: cur.close()
            if dbbook: dbbook.close()
            if cursor: cursor.close()
            if dbmemb: dbmemb.close()


#heading label
    lb1=Label(popup,text="Issue Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file=resource_path("images\\book_id.png"))
    book_idLabel=Label(popup,text="Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=book_idImg)
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")
#member_id label
    member_idImg=PhotoImage(file=resource_path("images\\mem_id.png"))
    mem_idLabel=Label(popup,text="Enter Member ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=member_idImg)
    mem_idLabel.grid(row=2,column=0,padx=20,pady=10,sticky="w")
#member_id entry box
    member_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.insert(0,"Enter Member ID")
    member_idEntry.grid(row=2,column=0,padx=10,pady=10,sticky="s")
#issue date label
    issue_dateImg=PhotoImage(file=resource_path("images\\issue_date.png"))
    issue_dateLabel=Label(popup,text="Issue Date:",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=issue_dateImg)
    issue_dateLabel.grid(row=3,column=0,padx=20,pady=10,sticky="w")
#issue button
    issuebtn=Button(popup,text="ISSUE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=handle_issue_book)
    issuebtn.grid(row=6,column=0,pady=10,padx=30,sticky="s")

#combobox for year,month and date
    issue_year=Combobox(popup,value=y,width=5,font=("Arial 11 bold"),background="white",foreground="black",justify="center",state=DISABLED)
    issue_month=Combobox(popup,value=month,width=6,font=("Arial 11 bold"),background="white",foreground="black",state=DISABLED)
    issue_date=Combobox(popup,value=d,width=5,font=("Arial 11 bold"),background="white",foreground="black",justify="center",state=DISABLED)
   
    issue_year.place(x=200,y=185)
    issue_month.place(x=270,y=185)
    issue_date.place(x=360,y=185)

#set today's/current date,month and year
    now=datetime.now()
    issue_year.set(now.year)
    issue_month.set(month[now.month-1])
    issue_date.set(now.day)

#to update member information 
def update_member_info():
    popup = Toplevel(root)
    popup.title("Update Existing member")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    result_window = None  # Reference to the result window
    global backbtnImg

    def destry():
        popup.destroy()
        if result_window and result_window.winfo_exists():
            result_window.destroy()

#heading label
    lb1=Label(popup,text="Update Member Information",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#Member_id Label
    member_idImg=PhotoImage(file=resource_path("images\\mem_id.png"))
    member_idLabel=Label(popup,text="  Member ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=member_idImg)
    member_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#Member ID entry box
    member_idEntry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.grid(row=1,column=0,padx=10,pady=15,sticky="n")    
#search button
    searchbtn=Button(popup,text="SEARCH",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
            activeforeground="black",cursor="hand2",width=10,command=lambda:search_member())
    searchbtn.grid(row=3,column=0,pady=10,padx=30,sticky="s")

    def update():
        global email_Entry,year_Entry,member_emailImg,member_yearImg
          # Create result window
        result_window = Toplevel(popup)
        result_window.title("Update Member Info")
        result_window.geometry("500x300+600+380")
        result_window.configure(bg="yellow")

    #Update email label
        member_emailImg=PhotoImage(file=resource_path("images\\mem_email.png"))
        email_Label=Label(result_window,text="   Email: ",font=("Arial 12 bold"),bd=4,bg="yellow",compound="left",image=member_emailImg)
        email_Label.grid(row=1,column=0,padx=20,pady=10,sticky="w")
    #Update email entry box
        email_Entry=Entry(result_window,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        email_Entry.grid(row=1,column=1,pady=10,sticky="n")
     #Update year label
        member_yearImg=PhotoImage(file=resource_path("images\\mem_year.png"))
        year_Label=Label(result_window,text="  Year: ",font=("Arial 12 bold"),bd=4,bg="yellow",compound="left",image=member_yearImg)
        year_Label.grid(row=2,column=0,padx=20,pady=10,sticky="w")
    #Update email entry box
        year_Entry=Entry(result_window,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        year_Entry.grid(row=2,column=1,pady=10,sticky="n")
    #button to save changes in database
        savebtn=Button(result_window,text="SAVE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
             activeforeground="black",cursor="hand2",width=10,command=lambda:save())
        savebtn.grid(row=3,column=0,pady=10,padx=30,sticky="n")

        def save():
            memb_id=member_idEntry.get()
            email=email_Entry.get()
            year=year_Entry.get()
            if not email or not year:
                messagebox.showwarning("Warning","Please fill out all the details!!!!")
                return
            else:
                try:
                    year = int(year)
                    if not 1 <= year <= 4:
                        messagebox.showwarning("Warning", "Year should be between 1 and 4!!")
                        return
                except ValueError:
                    messagebox.showwarning("Warning", "Year should be integer values!!")
                    return
                
                try:
                    dbmemb=sql.connect(resource_path("MemDB.db"))
                    cur=dbmemb.cursor()
                    cur.execute("UPDATE member SET Email=?,Year=? WHERE Member_ID=?",(email,year,memb_id))
                    dbmemb.commit()
                    messagebox.showinfo("SUCCESS","Member details updated successfully!!!")
                except sql.Error as e:
                    messagebox.showerror("ERROR", f"SQLite error: {e}")
                finally:
                    cur.close()
                    dbmemb.close()

    def search_member():
        nonlocal result_window
        dbmemb=sql.connect(resource_path("MemDB.db"))
        cur=dbmemb.cursor()
        try:
            memb_id=member_idEntry.get()
            cur.execute("SELECT * FROM member WHERE Member_ID=?",(memb_id,))
            member_data=cur.fetchone()
            if member_data is not None:
                memb_id=member_data[0]
                update()
                email_Entry.insert(0,member_data[2])
                year_Entry.insert(0,member_data[3])
            elif memb_id=="":
                messagebox.showwarning("ERROR","Please provide value!!")
            else:
                messagebox.showwarning("ERROR","Member does not exists in database!!!!")
        except Exception as e:
            messagebox.showerror("Error",f"Sqlite error: {e}")
        finally:
            cur.close()
            dbmemb.close()

#function to display existing members and delete existing member
def display_existing_members():
    popup = Toplevel(root)
    popup.title("Display Existing member")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    # === TreeView ===
    member = ttk.Treeview(popup, height=15, selectmode="extended")
    member['columns'] = ("Member ID", "Member Name", "Email", "Year", "Course")

    member.column("#0", width=0, stretch=NO)  # Hide the default column
    member.column('Member ID', anchor=CENTER, width=100)
    member.column('Member Name', anchor=CENTER, width=140)
    member.column('Email', anchor=CENTER, width=230)
    member.column('Year', anchor=CENTER, width=120)
    member.column('Course', anchor=CENTER, width=140)

    member.heading('Member ID', text="Member ID")
    member.heading('Member Name', text="Member Name")
    member.heading('Email', text="Email")
    member.heading('Year', text="Year")
    member.heading('Course', text="Course")

    member.grid(row=0, column=0, sticky="nsew")

    # === Scrollbars ===
    scrollX = Scrollbar(popup, orient=HORIZONTAL, command=member.xview)
    scrollY = Scrollbar(popup, orient=VERTICAL, command=member.yview)

    scrollX.grid(row=1, column=0, sticky="ew")
    scrollY.grid(row=0, column=1, sticky="ns")

    member.configure(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)

    # === Styling Rows ===
    member.tag_configure('oddrow', background="white")
    member.tag_configure('evenrow', background="lightblue")

    #to delete member permanently from the database
    delete_btn = Button(popup, text="DELETE MEMBER", bg="red", fg="white", font=("Arial 12 bold"),
                    command=lambda: delete_selected_member())
    delete_btn.grid(row=4, column=0, pady=10, padx=10, sticky="n")

    def delete_selected_member():
        selected = member.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to delete.")
            return
        
        member_id = member.item(selected)['values'][0]  # Get Member ID from selected row

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Member ID '{member_id}'?")
        if confirm:
            try:
                db = sql.connect(resource_path("MemDB.db"))
                cur = db.cursor()
                bookdb = sql.connect(resource_path("BookDB.db"))
                cursor = bookdb.cursor()
                cur.execute("DELETE FROM member WHERE Member_ID=?", (member_id,))
                #delete related records from issue table and expected return date table
                cursor.execute("DELETE FROM issue WHERE Member_ID=?", (member_id,))
                cur.execute("DELETE FROM Expected_Return_Dates WHERE MemberID=?", (member_id,))

                db.commit()
                db.close()
                bookdb.commit()
                bookdb.close()
                member.delete(selected)  # Remove from TreeView
                messagebox.showinfo("Success", "Member deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"SQLite error: {e}")


    # === Fetch Data and Insert into TreeView ===
    dbmemb = sql.connect(resource_path("MemDB.db"))
    cur = dbmemb.cursor()

    try:
        cur.execute("SELECT * FROM member")
        records = cur.fetchall()

        member.delete(*member.get_children())  # Clear old data first

        for index, record in enumerate(records):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            member.insert('', 'end', iid=index, values=(record[0], record[1], record[2], record[3], record[4]), tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load members:\n{e}")
    finally:
        cur.close()
        dbmemb.close()

    # Make popup window resizable and TreeView adjust
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)

#to display issued books to members
def display_issued_book():
    popup = Toplevel(root)
    popup.title("Display Issued Book")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

        # === TreeView ===
    issued_book = ttk.Treeview(popup, height=15, selectmode="extended")
    issued_book['columns'] = ("Member ID","Member Name","Book ID","Issue Date")

    issued_book.column("#0", width=0, stretch=NO)  # Hide the default column
    issued_book.column('Member ID', anchor=CENTER, width=100)
    issued_book.column('Member Name', anchor=CENTER, width=140)
    issued_book.column('Book ID', anchor=CENTER, width=230)
    issued_book.column('Issue Date', anchor=CENTER, width=120)

    issued_book.heading('Member ID', text="Member ID")
    issued_book.heading('Member Name', text="Member Name")
    issued_book.heading('Book ID', text="Book ID")
    issued_book.heading('Issue Date', text="Issue Date")

    issued_book.grid(row=0, column=0, sticky="nsew")

    # === Scrollbars ===
    scrollX = Scrollbar(popup, orient=HORIZONTAL, command=issued_book.xview)
    scrollY = Scrollbar(popup, orient=VERTICAL, command=issued_book.yview)

    scrollX.grid(row=1, column=0, sticky="ew")
    scrollY.grid(row=0, column=1, sticky="ns")

    issued_book.configure(xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)

    #Styling Rows
    issued_book.tag_configure('oddrow', background="white")
    issued_book.tag_configure('evenrow', background="lightblue")

    #Fetch Data and Insert into TreeView
    dbbook = sql.connect(resource_path("BookDB.db"))
    cur = dbbook.cursor()

    try:
        cur.execute("SELECT * FROM issue")
        records = cur.fetchall()

        issued_book.delete(*issued_book.get_children())  # Clear old data first

        for index, record in enumerate(records):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            issued_book.insert('', 'end', iid=index, values=(record[0], record[1], record[2], record[3]), tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load issued books:\n{e}")
    finally:
        cur.close()
        dbbook.close()

    # Make popup window resizable and TreeView adjust
    popup.grid_rowconfigure(0, weight=1)
    popup.grid_columnconfigure(0, weight=1)

#visualize book issuance and total book quantity report using matplotlib
def generate_report():
    popup = Toplevel(root)
    popup.title("Generate Report")
    popup.geometry("850x400+400+290")
    popup.configure(bg="#b9f8f8")

    global backbtnImg
    def destry():
        popup.destroy()
#heading label
    lb1=Label(popup,text="Book Issuance Report",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file=resource_path("images\\backbtn.png"))
    backbtn=Button(popup,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#Date Label
    Reportdate_Label=Label(popup,text="Enter date(YYYY-MM-DD):",font=("Arial 12 bold"),bg="#b9f8f8",bd=4)
    Reportdate_Label.grid(row=1,column=0,padx=10,pady=10,sticky="w")
#Date entry box
    Reportdate_Entry=Entry(popup,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    Reportdate_Entry.grid(row=1,column=0,pady=20,sticky="n")
#generate button
    generatebtn=Button(popup,text="Generate",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
            activeforeground="black",cursor="hand2",width=10,command=lambda:generate())
    generatebtn.grid(row=2,column=0,pady=10,padx=30,sticky="s")

    def generate():
        target_date = Reportdate_Entry.get().strip()
        try:
            dbbook = sql.connect(resource_path("BookDB.db"))

            # First check if there are issued books on selected date
            if target_date:
                query2 = "SELECT * FROM issue WHERE Issue_date LIKE ?"
                df_issued = pd.read_sql_query(query2, dbbook, params=(f"{target_date}%",))
            else:
                query2 = "SELECT * FROM issue"
                df_issued = pd.read_sql_query(query2, dbbook)

            if df_issued.empty:
                messagebox.showwarning("No Data", "No books were issued on this date!")
                dbbook.close()
                return

            # Create figure AFTER confirming records exist
            plt.figure(figsize=(14, 6))

            #Bar Chart for Book Quantities
            query1 = "SELECT Book_ID,Quantity FROM Book"
            df_books = pd.read_sql_query(query1, dbbook)

            plt.subplot(1, 2, 1)
            positions = np.arange(len(df_books['Book_ID']))
            plt.barh(positions, df_books['Quantity'], color='hotpink')
            plt.title('Book Quantity Based on Book ID')
            plt.xlabel('Quantity')
            plt.yticks(positions, df_books['Book_ID'])
            plt.grid(axis='x', linestyle='--', alpha=0.7)

           #Line Chart for Book Issuance
            date_counts = df_issued['Issue_date'].value_counts().sort_index()
            plt.subplot(1, 2, 2)
            plt.plot(date_counts.index, date_counts.values, marker='o', color='blue', linestyle='-')
            plt.title('Book Issuance on Selected Date')
            plt.xlabel('Date')
            plt.ylabel('Number of Books Issued')
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='both', linestyle='--', alpha=0.7)

            # Force Y-axis to show only whole numbers
            from matplotlib.ticker import MaxNLocator
            ax = plt.gca()
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout(rect=[0, 0, 1, 0.95])
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            dbbook.close()

# create backup of book and member database in excel and pdf format
def create_backup():
    if getattr(sys, 'frozen', False):
        # Running as EXE
        app_path = os.path.dirname(sys.executable)
    else:
        # Running as script (in VS Code)
        app_path = os.path.dirname(os.path.abspath(__file__))

    backup_folder = os.path.join(app_path, 'backup_folder')

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    def export_to_csv(database, table_name, csv_file):
        connection = sql.connect(database)
        df = pd.read_sql_query(f'SELECT * FROM {table_name}', connection)
        df.to_csv(csv_file, index=False)
        connection.close()

    def convert_csv_to_pdf(csv_file, pdf_file):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(csv_file, 'r') as file:
            for row in csv.reader(file):
                pdf.cell(200, 10, txt=" | ".join(row), ln=True)
        pdf.output(pdf_file)

    try:
        # Resource paths
        def resource_path(relative):
            try:
                base = sys._MEIPASS
            except AttributeError:
                base = os.path.abspath(".")
            return os.path.join(base, relative)

        db1 = resource_path("BookDB.db")
        db2 = resource_path("MemDB.db")

        for table in ['Book', 'issue']:
            csv_path = os.path.join(backup_folder, f'backup_BookDB_{table}.csv')
            pdf_path = os.path.join(backup_folder, f'backup_BookDB_{table}.pdf')
            export_to_csv(db1, table, csv_path)
            convert_csv_to_pdf(csv_path, pdf_path)

        for table in ['member', 'Expected_Return_Dates']:
            csv_path = os.path.join(backup_folder, f'backup_MemDB_{table}.csv')
            pdf_path = os.path.join(backup_folder, f'backup_MemDB_{table}.pdf')
            export_to_csv(db2, table, csv_path)
            convert_csv_to_pdf(csv_path, pdf_path)

        messagebox.showinfo("Success", "Backup files created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"SQLite error: {e}")

#open amazon website to order book
def open_browser():
    webbrowser.open("https://www.amazon.in/b?node=976389031")


# === Left Sidebar with Scrollable Buttons (without Logout) ===
sidebar_frame = tk.Frame(root, bg="yellow", width=250)
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Scrollable part
top_frame = tk.Frame(sidebar_frame, bg="yellow")
top_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(top_frame, bg="yellow", highlightthickness=0)
scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="yellow")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
# Enable touchpad/mouse wheel scroll
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Bind mouse scroll
canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# === Logout Button pinned at the bottom ===
def logout_action(): 
    try:
        ask=messagebox.askyesno("Confirmation","Do you really want to logout?")
        if ask:
            for window in root.winfo_children():
                if isinstance(window, Toplevel):
                    window.destroy()
            root.destroy()
            # to reopen login page again
            subprocess.Popen([sys.executable, "project_login.py"])
        else:
            messagebox.showinfo("Info","Logout cancelled")
    except:
        messagebox.showerror("Error","something went wrong in loging out")


logout_img_path = os.path.join("C:/shruti/Book-Buffet-main/images", "logout.png")
try:
    logout_image = Image.open(logout_img_path).resize((30, 30))
    logout_photo = ImageTk.PhotoImage(logout_image)
    logout_btn = tk.Button(sidebar_frame, text="  LOGOUT", image=logout_photo, compound="left",
                           font=("arial", 12, "bold"), fg="black", bg="pink",
                           relief="raised", bd=5, padx=10, anchor="w", command=logout_action)
    logout_btn.image = logout_photo  # Prevent garbage collection
except:
    logout_btn = tk.Button(sidebar_frame, text="LOGOUT", font=("arial", 12, "bold"),
                           fg="black", bg="pink", relief="raised", bd=5, padx=10, anchor="w", command=logout_action)

logout_btn.pack(side="bottom", fill=tk.X, padx=10, pady=10)


button_data = [
    ("Add Book", "add.png", add_book),
    ("Update Book", "update.png", update_book),
    ("Add New Member", "newmem.png", add_new_member),
    ("Delete Book", "delete.png", delete_book),
    ("Search Book", "search.png", search_book),
    ("Return Book", "return.png", return_book),
    ("Issue Book", "issue.png", issue_book),
    ("Update Member Info", "update_memb.png", update_member_info),
    ("Display Existing Members", "member.png", display_existing_members),
    ("Display Issued Book", "issued_book.png", display_issued_book),
    ("Generate Report", "report.png", generate_report),
    ("Open Browser", "browser.png", open_browser),
    ("Create Backup", "backup.png", create_backup)
]

images = {}
def create_button(text, img_file, command):
    path = os.path.join("C:/shruti/Book-Buffet-main/images", img_file)
    try:
        image = Image.open(path).resize((30, 30))
        images[text] = ImageTk.PhotoImage(image)
        btn = tk.Button(scrollable_frame, text=f"  {text}", image=images[text], compound="left",
                        font=("arial", 12, "bold"), fg="black", bg="pink",
                        relief="raised", bd=5, padx=10, anchor="w", command=command)
    except Exception:
        btn = tk.Button(scrollable_frame, text=text, font=("arial", 12, "bold"),
                        fg="black", bg="pink", relief="raised", bd=5, padx=10, anchor="w", command=command)
    btn.pack(pady=5, fill=tk.X, padx=10)

for text, img_file, command in button_data:
    create_button(text, img_file, command)

# === Right Frame with Book List ===
right_frame = tk.Frame(root, bg="white")
right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

booklist_frame = tk.LabelFrame(right_frame, text="Library Book List", font=("arial", 14, "bold"), fg="black", bg="white")
booklist_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

frame2 = tk.Frame(booklist_frame, bg="white")
frame2.pack(fill=tk.BOTH, expand=True)

# Create Scrollbars
scrollX = tk.Scrollbar(frame2, orient=tk.HORIZONTAL)
scrollY = tk.Scrollbar(frame2, orient=tk.VERTICAL)

# Create Treeview
global book_tree
book_tree = ttk.Treeview(frame2, columns=("Book ID", "Title", "Author", "Price", "Quantity"),xscrollcommand=scrollX.set, yscrollcommand=scrollY.set)

scrollX.config(command=book_tree.xview)
scrollY.config(command=book_tree.yview)

scrollX.pack(side=tk.BOTTOM, fill=tk.X)
scrollY.pack(side=tk.RIGHT, fill=tk.Y)
book_tree.pack(fill=tk.BOTH, expand=True)

#apply styling
style = ttk.Style()
style.theme_use("default")

# Treeview general style
style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=28)

# Selected row color
style.map("Treeview",background=[("selected", "#347083")])

# Treeview heading style
style.configure("Treeview.Heading",background="#347083",foreground="white",font=("Arial", 12, "bold"))

# Column headings and center alignment
book_tree.heading("Book ID", text="Book ID")
book_tree.heading("Title", text="Title")
book_tree.heading("Author", text="Author")
book_tree.heading("Price", text="Price")
book_tree.heading("Quantity", text="Quantity")

for col in ("Book ID", "Title", "Author", "Price", "Quantity"):
    book_tree.column(col, anchor="center", width=120)

# Show only headings (no default column)
book_tree["show"] = "headings"

#striped rows
book_tree.tag_configure("oddrow", background="white")
book_tree.tag_configure("evenrow", background="lightblue")
book_tree.tag_configure("lowstock", background="salmon")

#clear treeview
book_tree.delete(*book_tree.get_children())

#function to display books from database in the treeview
def viewbook():
    global book_tree
    try:
        # Check if the treeview still exists
        if not book_tree.winfo_exists():
            return
        
        for row in book_tree.get_children():
            book_tree.delete(row)

        dbbook = sql.connect(resource_path("BookDB.db"))
        cur = dbbook.cursor()
        cur.execute("SELECT * FROM Book")
        records = cur.fetchall()

        for index, record in enumerate(records):
            tags = ["lowstock"] if int(record[4]) <= 5 else ("evenrow" if index % 2 == 0 else "oddrow")
            book_tree.insert("", "end", iid=record[0], values=record, tags=tags)
        cur.close()
        dbbook.close()

    except Exception as e:
        print("Error in viewbook():", e)

viewbook() 
root.mainloop()
