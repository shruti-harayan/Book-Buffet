from tkinter import *
from tkinter import messagebox,ttk
import sqlite3 as sql,time
from datetime import datetime,timedelta
from tkinter.ttk import Combobox
import numpy as np,matplotlib.pyplot as plt
import pandas as pd,webbrowser,csv,os
from fpdf import FPDF

month=['January','February','March','April','May','June','July','August','September','October','November','December']
y = list(range(2023, 2040))
d = list(range(1,32))

root=Tk()
root.title("BOOK BUFFET")
root.iconbitmap('images\\library.ico')
root.geometry('1530x800+0+0')
root.resizable(False, False)

#funtion for displaying date and time
def clock():
    date=time.strftime('%d/%m/%Y')
    currenttime=time.strftime('%H:%M:%S')
    datelabel.config(text=f'     Date: {date} \n Time: {currenttime}')
    datelabel.after(1000,clock)

#function to display heading
count=0
text=''
def slider():
    global text,count
    if count==len(head):
        count=0
        text=''
    text=text+head[count]
    heading.config(text=text)
    count+=1
    heading.after(200,slider)

datelabel=Label(root,font=('arial 15 bold'),bg="blue",fg="white")
datelabel.place(x=1300,y=0)
clock()

#heading of the page
head="!!! WELCOME ADMIN !!!"
heading=Label(root,font=('arial 25 italic bold'))
heading.pack()
# heading.place(x=670,y=10)
slider()

#left side to display buttons yellow color
frame1=Frame(root,width=600,height=900,bg="yellow",highlightbackground="black",highlightthickness=2)    
frame1.place(x=0,y=0)
frame1.pack_propagate(False)
#right side to display treeview
frame2=Frame(root,width=900,height=300,bg="pink",highlightbackground="black",highlightthickness=2)     
frame2.place(x=600,y=70)
frame2.pack_propagate(False)

#function to add new book
def addbook():
    addbookframe=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2) 
    addbookframe.place(x=620,y=400)
    global backbtnImg,book_idImg,book_idLabel,book_titleLabel,book_titleImg,book_authorImg,book_authorLabel,book_priceImg
    global book_priceLabel,book_quantityImg,book_quantityLabel,addbookLabel,clear
    def clear():
        book_idEntry.delete(0,END)
        book_titleEntry.delete(0,END)
        book_authorEntry.delete(0,END)
        book_priceEntry.delete(0,END)
        book_quantityEntry.delete(0,END)

    def destry():
       addbookframe.destroy()

    def addnewbook():        
        global book_id,title,author,price,quantity,dbbook,cur
        book_id=book_idEntry.get()
        title=book_titleEntry.get()
        author=book_authorEntry.get()
        price=book_priceEntry.get()
        quantity=book_quantityEntry.get()

        dbbook=sql.connect('BookDB.db')
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
                table.insert("","end",values=(value[0], value[1], value[2], value[3], value[4]) ) #update the treeview after adding new values
                refresh()           #update the treeview after adding new values
                clear()
        except Exception as e:
            messagebox.showerror("ERROR","Price and Quantity should be an integer value")
        cur.close()
        dbbook.close()
    
    def add():
        if book_idEntry.get() == "" or book_titleEntry.get()=="" or book_quantityEntry.get()==" " or book_authorEntry.get()=="" or book_priceEntry.get()=="":
            messagebox.showwarning("Warning","Please fill out all the details!!")
        else:
            addnewbook()
    
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(addbookframe,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#heading
    addbookLabel=Label(addbookframe,text="ADD BOOK",anchor="center",bg="blue",width=60,fg="white",font=("Arial 14 bold"))
    addbookLabel.grid(row=0,column=1,sticky="nsew")
#book_id label
    book_idImg=PhotoImage(file="images\\book_id.png")
    book_idLabel=Label(addbookframe,text="    BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_idImg,compound="left",bd=4)
    book_idLabel.grid(row=1,column=1,rowspan=1,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(addbookframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=1,padx=10,pady=10,sticky="s")

#book title label
    book_titleImg=PhotoImage(file="images\\book_title.png")
    book_titleLabel=Label(addbookframe,text="    TITLE: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_titleImg,compound="left",bd=4)
    book_titleLabel.grid(row=2,column=1,sticky="w")
#book title entry box
    book_titleEntry=Entry(addbookframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_titleEntry.insert(0,"Enter Book Name")
    book_titleEntry.grid(row=2,column=1,padx=10,pady=10,sticky="s")

#book Author label
    book_authorImg=PhotoImage(file="images\\book_author.png")
    book_authorLabel=Label(addbookframe,text="    AUTHOR: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_authorImg,compound="left",bd=4)
    book_authorLabel.grid(row=3,column=1,sticky="w")
#book title entry box
    book_authorEntry=Entry(addbookframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_authorEntry.insert(0,"Enter Author Name")
    book_authorEntry.grid(row=3,column=1,padx=10,pady=10,sticky="s")

#book Price label
    book_priceImg=PhotoImage(file="images\\book_price.png")
    book_priceLabel=Label(addbookframe,text="    PRICE: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_priceImg,compound="left",bd=4)
    book_priceLabel.grid(row=4,column=1,sticky="w")
#book Price entry box
    book_priceEntry=Entry(addbookframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_priceEntry.insert(0,"Enter Book Price")
    book_priceEntry.grid(row=4,column=1,padx=10,pady=10,sticky="s")

#book Quantity label
    book_quantityImg=PhotoImage(file="images\\book_quantity.png")
    book_quantityLabel=Label(addbookframe,text="    QUANTITY: ",font=("Arial 12 bold"),bg="#b9f8f8",image=book_quantityImg,compound="left",bd=4)
    book_quantityLabel.grid(row=5,column=1,sticky="w")
#book Quantity entry box
    book_quantityEntry=Entry(addbookframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_quantityEntry.insert(0,"Enter Book Quantity")
    book_quantityEntry.grid(row=5,column=1,padx=10,pady=10,sticky="s")
  
#add button
    addbtn=Button(addbookframe,text="ADD",background="green",font=("Arial 14 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:add())
    addbtn.grid(row=1,column=1,pady=20,sticky="e")
#reset button
    reset=Button(addbookframe,text="CLEAR",background="red",font=("Arial 14 bold"),bd=5,activebackground="red",activeforeground="black"
                 ,cursor="hand2",command=clear,width=10)
    reset.grid(row=2,column=1,pady=20,sticky="e")


#function for updating book details
def update():
    updateframe=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2) 
    updateframe.place(x=620,y=400)
    global updatebookLabel,backbtnImg,book_id,book_idEntry,book_idImg
    def destry():
        updateframe.destroy()
        backbtnImg.config()

    def updt():
        up=Tk()
        up.title('Edit Book')
        up.geometry("800x400+630+400")
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

            try:
                cur.execute("UPDATE Book SET Book_ID=?,Title=?,Author=?,Price=?,Quantity=? WHERE Book_ID=?",(new_book_id,title,author,price,quantity,book_id))
                dbbook.commit()
                messagebox.showinfo("SUCCESS","Details updated successfully!")
                #update the treeview
                updated_values = (new_book_id, title, author, price, quantity)
                tree_item_id = book_id                     
                table.item(tree_item_id, values=updated_values)
                up.destroy()
                cur.close()
                dbbook.close()
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
            dbbook=sql.connect('BookDB.db')
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
            dbbook=sql.connect('BookDB.db')
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
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(updateframe,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#heading
    updatebookLabel=Label(updateframe,text="UPDATE BOOK",anchor="center",bg="blue",width=60,fg="white",font=("Arial 14 bold"))
    updatebookLabel.grid(row=0,column=1,sticky="nsew")
    #book_id label
    book_idImg=PhotoImage(file="images\\book_id.png")
    book_idLabel=Label(updateframe,text="  BOOK ID:",font=("Arial 12 bold"),bg="#b9f8f8",image=book_idImg,compound="left",bd=4)
    book_idLabel.grid(row=1,column=1,rowspan=2,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(updateframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=1,padx=5,pady=20,sticky="s")
#submit button
    submitbtn=Button(updateframe,text="SUBMIT",background="green",font=("Arial 14 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:check())
    submitbtn.grid(row=1,column=1,pady=20,sticky="e")


#to delete existing book
def delete():
    deleteframe=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    deleteframe.place(x=620,y=400)
    global book_idEntry,book_idImg,backbtnImg
    def destry():
        deleteframe.destroy()
        
    #delete book from database
    def delfunc():
        global book_id
        book_id=book_idEntry.get()
        dbbook=sql.connect('BookDB.db')
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
                    table.delete(book_id)
                else:
                    messagebox.showinfo("INFO", "Deletion canceled.")
            except sql.Error as e:
                messagebox.showerror("ERROR", f"SQLite error: {e}")
        cur.close()
        dbbook.close()

#heading label
    lb1=Label(deleteframe,text="Delete Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(deleteframe,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=destry)
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file="images\\book_id.png")
    book_idLabel=Label(deleteframe,text="   Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=book_idImg,compound="left")
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(deleteframe,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")
#submit button
    submit=Button(deleteframe,text="DELETE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=delfunc)
    submit.grid(row=2,column=0,pady=10,padx=30,sticky="s")



#to add new member
def newmem():
    new_mem_frame=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    new_mem_frame.place(x=620,y=400)
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
        new_mem_frame.destroy()

#heading label
    lb1=Label(new_mem_frame,text="Add New Member",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(new_mem_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#member_id label
    member_idImg=PhotoImage(file="images\\mem_id.png")
    member_idLabel=Label(new_mem_frame,text=" Enter Member ID:",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_idImg,compound="left")
    member_idLabel.grid(row=1,column=0,padx=20,pady=5,sticky="w")
#member_id entry box
    member_idEntry=Entry(new_mem_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.insert(0,"Enter Member ID")
    member_idEntry.grid(row=1,column=0,padx=10,pady=5,sticky="s")

#member_name label
    member_nameImg=PhotoImage(file="images\\mem_name.png")
    member_nameLabel=Label(new_mem_frame,text=" Enter Member Name:",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_nameImg,compound="left")
    member_nameLabel.grid(row=2,column=0,padx=10,pady=5,sticky="w")
#member_name entry box
    member_nameEntry=Entry(new_mem_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_nameEntry.insert(0,"Enter Member Name")
    member_nameEntry.grid(row=2,column=0,padx=10,pady=5,sticky="s")

#member email label
    member_emailImg=PhotoImage(file="images\\mem_email.png")
    member_emailLabel=Label(new_mem_frame,text="  Enter Email ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_emailImg,compound="left")
    member_emailLabel.grid(row=3,column=0,padx=20,pady=5,sticky="w")
#member_email entry box
    member_emailEntry=Entry(new_mem_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_emailEntry.insert(0,"Enter Email ID")
    member_emailEntry.grid(row=3,column=0,padx=10,pady=5,sticky="s")

#member year of studying label
    member_yearImg=PhotoImage(file="images\\mem_year.png")
    member_yearLabel=Label(new_mem_frame,text="Enter year of studying: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_yearImg,compound="left")
    member_yearLabel.grid(row=4,column=0,padx=20,pady=5,sticky="w")
#member year of studying entry box
    member_yearEntry=Entry(new_mem_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_yearEntry.insert(0,"Enter Year of studying")
    member_yearEntry.grid(row=4,column=0,padx=10,pady=5,sticky="s")

#member select course label
    member_courseImg=PhotoImage(file="images\\mem_course.png")
    member_courseLabel=Label(new_mem_frame,text="  Enter Course Name: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=member_courseImg,compound="left")
    member_courseLabel.grid(row=5,column=0,padx=20,pady=5,sticky="w")
#member select course entry box
    member_courseEntry=Entry(new_mem_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_courseEntry.insert(0,"Enter Course Name")
    member_courseEntry.grid(row=5,column=0,padx=10,pady=5,sticky="s")

#save button
    save=Button(new_mem_frame,text="SAVE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:addnewmember())
    save.grid(row=1,column=1,pady=20,sticky="w")
#reset button
    reset=Button(new_mem_frame,text="CLEAR",background="red",font=("Arial 14 bold"),bd=5,activebackground="red",activeforeground="black"
                 ,cursor="hand2",command=lambda:clear(),width=10)
    reset.grid(row=2,column=1,pady=20,sticky="w")


#add new member in database
def addnewmember():
    global mem_id,mem_name,year,email,course,dbmemb,cur
    mem_id=member_idEntry.get()
    mem_name=member_nameEntry.get()
    email=member_emailEntry.get()
    year=member_yearEntry.get()
    course=member_courseEntry.get()

    if not mem_id or not mem_name or not email or not year or not course:
        messagebox.showwarning("Warning","Please fill out require details!!")  

    def clear():
        member_idEntry.delete(0,END)
        member_nameEntry.delete(0,END)
        member_emailEntry.delete(0,END)
        member_yearEntry.delete(0,END)
        member_courseEntry.delete(0,END)

    dbmemb=sql.connect('MemDB.db')
    cur=dbmemb.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS member(
            Member_ID INT,Member_Name TEXT,Email TEXT,
            Year INT,Course TEXT)
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
        else:
            cur.execute("INSERT INTO member(Member_ID,Member_Name,Email,Year,Course) VALUES(?,?,?,?,?)",(mem_id,mem_name,email,year,course))
            dbmemb.commit()
            messagebox.showinfo("SUCCESS", "Member Added Successfully!!!!!")
            clear()
    except sql.Error as e:
        messagebox.showerror("ERROR", f"SQLite error: {e}")
    cur.close()
    dbmemb.close()

   
#to search existing book
def search():
    search_frame=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    search_frame.place(x=620,y=400)
    search_result_frame=Frame(root,bg="#b9f8f8",width=600,height=200,highlightbackground="black",highlightthickness=2)   
    search_result_frame.place(x=620,y=590)
    global search,backbtnImg,book_idImg
    def destry():
        search_frame.destroy()
        search_result_frame.destroy()
#heading label
    lb1=Label(search_frame,text="Search Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(search_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file="images\\book_id.png")
    book_idLabel=Label(search_frame,text=" Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,image=book_idImg,compound="left")
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(search_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")

    def perform_search():
        dbbook=sql.connect('BookDB.db')
        cur=dbbook.cursor()
        try:
            book_id=book_idEntry.get()
            if not book_id:
                messagebox.showwarning("Warning", "Please enter Book ID!!")
                return
            cur.execute("SELECT * FROM Book WHERE Book_ID=?",(book_id,))
            book_data=cur.fetchone()
            if not book_data:
                messagebox.showwarning("Error","Book does not exist!!!")
            else:
                # Clear previous results
                for widget in search_result_frame.winfo_children():
                    widget.destroy()
                details_labels = ["Book_ID", "Title", "Author", "Price", "Quantity"]
                for i, attribute in enumerate(details_labels):
                    label = Label(search_result_frame, text=f"{attribute}: {book_data[i]}", font=("Arial 12 bold"), bg="#b9f8f8")
                    label.grid(row=i + 3, column=0)
        except Exception as e:
            messagebox.showinfo("Error",f"Sqlite error {e}")
        finally:
            cur.close()
            dbbook.close()
#search button
    searchbtn=Button(search_frame,text="SEARCH",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
            activeforeground="black",cursor="hand2",width=10,command=lambda:perform_search())
    searchbtn.grid(row=2,column=0,pady=10,padx=30,sticky="s")


#return book
def retrn():
    return_frame=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    return_frame.place(x=620,y=400)
    global retrn,backbtnImg,book_idImg,member_idImg,return_dateImg
    def destry():
        return_frame.destroy()
#heading label
    lb1=Label(return_frame,text="Return Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(return_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file="images\\book_id.png")
    book_idLabel=Label(return_frame,text="Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=book_idImg)
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(return_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")
#member_id label
    member_idImg=PhotoImage(file="images\\mem_id.png")
    member_idLabel=Label(return_frame,text="Enter Member ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=member_idImg)
    member_idLabel.grid(row=2,column=0,padx=20,pady=10,sticky="w")
#member_id entry box
    member_idEntry=Entry(return_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.insert(0,"Enter Member ID")
    member_idEntry.grid(row=2,column=0,padx=10,pady=10,sticky="s")
#return date label
    return_dateImg=PhotoImage(file="images\\return_date.png")
    return_dateLabel=Label(return_frame,text="Return Date: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=return_dateImg)
    return_dateLabel.grid(row=3,column=0,padx=20,pady=10,sticky="w")
#return date combobox
    return_year=Combobox(return_frame,value=y,width=5,font=("Arial 11 bold"),background="white",foreground="black",justify="center")
    return_month=Combobox(return_frame,value=month,width=6,font=("Arial 11 bold"),background="white",foreground="black",justify="center")
    return_date=Combobox(return_frame,value=d,width=5,font=("Arial 11 bold"),background="white",foreground="black",justify="center")
    return_year.place(x=200,y=185)
    return_month.place(x=270,y=185)
    return_date.place(x=360,y=185)
    #set today's/current date,month and year
    now=datetime.now()
    return_year.set(now.year)
    return_month.set(month[now.month-1])
    return_date.set(now.day)

#return button
    returnbtn=Button(return_frame,text="RETURN",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:returnfunc())
    returnbtn.grid(row=4,column=0,pady=10,padx=30,sticky="n")
    

#to calculate fine on late return
    def fine(book_id, member_id, expected_return_date_str):
        dbmemb=sql.connect("MemDB.db")
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

    
    def returnfunc(): 
        book_id=book_idEntry.get()
        member_id=member_idEntry.get()
        if not book_id or not member_id:
            messagebox.showwarning("Warning", "Please enter a value!!")
            return
        
        dbmemb=sql.connect('MemDB.db')
        cursor=dbmemb.cursor()
        cursor.execute("SELECT * FROM member WHERE Member_ID=?",(member_id,))
        memb=cursor.fetchone()
        if not memb:
            messagebox.showwarning("Error","Member does not exist!!!")   
            return   
          
        dbbook=sql.connect('BookDB.db')
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
                    #update the treeview  
                    table.item(book_id, values=(book_id, title, author, price, new_quantity))   
                else:
                    messagebox.showinfo("INFO", "Return canceled.")
        except Exception as e:
            messagebox.showinfo("Error",f"Sqlite error {e}")
        finally:
            cur.close()
            dbbook.close()
            cursor.close()
            dbmemb.close()


#function to issue book 
def issue():
    issue_frame=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    issue_frame.place(x=620,y=400)
    global backbtnImg,book_idImg,member_idImg,issue_dateImg
    def destry():
        issue_frame.destroy()
#heading label
    lb1=Label(issue_frame,text="Issue Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(issue_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#book_id label
    book_idImg=PhotoImage(file="images\\book_id.png")
    book_idLabel=Label(issue_frame,text="Enter BOOK ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=book_idImg)
    book_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#book_id entry box
    book_idEntry=Entry(issue_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    book_idEntry.insert(0,"Enter Book ID")
    book_idEntry.grid(row=1,column=0,padx=10,pady=10,sticky="s")
#member_id label
    member_idImg=PhotoImage(file="images\\mem_id.png")
    mem_idLabel=Label(issue_frame,text="Enter Member ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=member_idImg)
    mem_idLabel.grid(row=2,column=0,padx=20,pady=10,sticky="w")
#member_id entry box
    member_idEntry=Entry(issue_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.insert(0,"Enter Member ID")
    member_idEntry.grid(row=2,column=0,padx=10,pady=10,sticky="s")
#issue date label
    issue_dateImg=PhotoImage(file="images\\issue_date.png")
    issue_dateLabel=Label(issue_frame,text="Issue Date:",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=issue_dateImg)
    issue_dateLabel.grid(row=3,column=0,padx=20,pady=10,sticky="w")
#issue button
    issuebtn=Button(issue_frame,text="ISSUE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",activeforeground="black"
               ,cursor="hand2",width=10,command=lambda:issue_book())
    issuebtn.grid(row=6,column=0,pady=10,padx=30,sticky="s")

#combobox for year,month and date
    issue_year=Combobox(issue_frame,value=y,width=5,font=("Arial 11 bold"),background="white",foreground="black",justify="center",state=DISABLED)
    issue_month=Combobox(issue_frame,value=month,width=6,font=("Arial 11 bold"),background="white",foreground="black",state=DISABLED)
    issue_date=Combobox(issue_frame,value=d,width=5,font=("Arial 11 bold"),background="white",foreground="black",justify="center",state=DISABLED)
   
    issue_year.place(x=200,y=185)
    issue_month.place(x=270,y=185)
    issue_date.place(x=360,y=185)

#set today's/current date,month and year
    now=datetime.now()
    issue_year.set(now.year)
    issue_month.set(month[now.month-1])
    issue_date.set(now.day)

#command to issue book
    def issue_book():
        member_id = member_idEntry.get()
        book_id = book_idEntry.get()
    #if fields are empty
        if not book_id or not member_id:
            messagebox.showwarning("Warning", "Please Enter Member ID/Book ID")
            return
        
    # Check if member and book exist
        member_exists = check_member_exists(member_id)
        book_exists, book_info = check_book_exists(book_id)
        if not member_exists or not book_exists:
            messagebox.showwarning("Warning", "Invalid Member ID or Book ID")
            return

        try:
            # Check if the book is available
            if book_info["Quantity"] > 0:
                # Update book quantity
                new_quantity = book_info["Quantity"] - 1
                update_book_quantity(book_id, new_quantity)
                # Update issuer's record
                issue_book_to_member(member_id, book_id)
                messagebox.showinfo("SUCCESS", "Book issued successfully!")
                dbbook = sql.connect('BookDB.db')
                cur = dbbook.cursor()
                cur.execute("SELECT Title, Author, Price FROM Book WHERE Book_ID=?", (book_id,))
                book_details = cur.fetchone()
                title, author, price = book_details
                #update the treeview                    
                table.item(book_id, values=(book_id, title, author, price, new_quantity))
            else:
                messagebox.showwarning("Warning", "Book is not available.")
        except sql.Error as e:
            messagebox.showerror("ERROR", f"Error: {e}")

    def check_member_exists(member_id):
        dbmemb = sql.connect('MemDB.db')
        cur = dbmemb.cursor()
        cur.execute("SELECT * FROM member WHERE Member_ID=?", (member_id,))
        member_exists = cur.fetchone() is not None
        cur.close()
        dbmemb.close()
        return member_exists

    def check_book_exists(book_id):
        dbbook = sql.connect('BookDB.db')
        cur = dbbook.cursor()
        cur.execute("SELECT * FROM Book WHERE Book_ID=?", (book_id,))
        book_info = cur.fetchone()
        book_exists = book_info is not None
        cur.close()
        dbbook.close()
        return book_exists, {"Quantity": book_info[4] if book_info else 0}

    def update_book_quantity(book_id, new_quantity):
        dbbook = sql.connect('BookDB.db')
        cur = dbbook.cursor()
        cur.execute("UPDATE Book SET Quantity=? WHERE Book_ID=?", (new_quantity, book_id))
        dbbook.commit()
        cur.close()
        dbbook.close()

    def issue_book_to_member(member_id, book_id):
        try:
            dbmemb=sql.connect('MemDB.db')
            cursor=dbmemb.cursor()
            cursor.execute("SELECT Member_Name FROM member WHERE Member_ID=?",(member_id,))
            member=cursor.fetchone()

            due_period = 7
            # Convert dates to string format
            issue_date = datetime.now().strftime("%Y-%m-%d")
            expected_return_date = (datetime.now() + timedelta(days=due_period)).strftime("%Y-%m-%d")
            
            dbbook = sql.connect('BookDB.db')
            cur = dbbook.cursor()
            q = 'INSERT INTO issue VALUES(?, ?, ?, ?)'
            cur.execute(q,(member_id, member[0],book_id, issue_date))
            dbbook.commit()

            # Store the expected return date in the database
            cursor.execute("INSERT INTO Expected_Return_Dates VALUES (?, ?, ?)",(book_id, member_id, expected_return_date))
            dbmemb.commit()
        except Exception as e:
            messagebox.showerror("Error",f"sqlite error: {e}")
        finally:
            cursor.close()
            dbmemb.close()
            cur.close()
            dbbook.close()
        

#function to display existing members of library in a treeview
def existing_member():
    existing_mem_frame=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    existing_mem_frame.place(x=620,y=400)
    global backbtnImg
    def destry():
        existing_mem_frame.destroy()
#heading label
    lb1=Label(existing_mem_frame,text="Existing Members",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(existing_mem_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#treeview
    member=ttk.Treeview(existing_mem_frame,height=8,selectmode="extended")
    member['columns']=("Member ID","Member Name","Email","Year","Course")

    member.column("#0",width=0,stretch=NO)                           #to hide the default first column
    member.column('Member ID',anchor=CENTER,width=100,minwidth=100)
    member.column('Member Name',anchor=CENTER,width=120,minwidth=140)
    member.column('Email',anchor=CENTER,width=180,minwidth=230)
    member.column('Year',anchor=CENTER,width=120,minwidth=120)
    member.column('Course',anchor=CENTER,width=140,minwidth=140)

    member.heading('Member ID',text="Member ID")
    member.heading('Member Name',text="Member Name")
    member.heading('Email',text="Email")
    member.heading('Year',text="Year")
    member.heading('Course',text="Course")
    member.grid(row=2, column=0, sticky="nsew")

    #create scrollbar
    scrollX=Scrollbar(existing_mem_frame,orient=HORIZONTAL,command=member.xview)
    scrollY=Scrollbar(existing_mem_frame,orient=VERTICAL,command=member.yview)
    scrollX.grid(row=3, column=0, sticky="ew")
    scrollY.grid(row=2, column=1, sticky="ns")

    #configure scrollbar
    member.config(yscrollcommand=scrollY.set,xscrollcommand=scrollX.set)

    #striped row tags
    member.tag_configure('oddrow',background="white")
    member.tag_configure('evenrow',background="lightblue")
    #clear the treeview
    member.delete(*member.get_children())

    dbmemb=sql.connect("MemDB.db")
    cur = dbmemb.cursor()
    cur.execute("SELECT * FROM member")
    records=cur.fetchall()
    global test
    test=0
    for record in records:
        if test % 2==0:
            member.insert(parent='',index='end',iid=test,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('evenrow',)  )
        else:
            member.insert(parent='',index='end',iid=test,text='',values=(record[0],record[1],record[2],record[3],record[4]),tags=('oddrow',)  )
        test+=1
    dbmemb.commit()
    cur.close()
    dbmemb.close()


#to display issued books to members
def issued_book():
    issued_book_frame=Frame(root,bg="#b9f8f8",width=600,height=320,highlightbackground="black",highlightthickness=2)   
    issued_book_frame.place(x=620,y=400)
    global backbtnImg
    def destry():
        issued_book_frame.destroy()
#heading label
    lb1=Label(issued_book_frame,text="Issued Book",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(issued_book_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#treeview
    issued_book=ttk.Treeview(issued_book_frame,height=8,selectmode="extended")
    issued_book['columns']=("Member ID","Member Name","Book ID","Issue Date")

    issued_book.column("#0",width=0,stretch=NO)                           #to hide the default first column
    issued_book.column('Member ID',anchor=CENTER,width=100,minwidth=100)
    issued_book.column('Member Name',anchor=CENTER,width=120,minwidth=140)
    issued_book.column('Book ID',anchor=CENTER,width=100,minwidth=100)
    issued_book.column('Issue Date',anchor=CENTER,width=140,minwidth=140)

    issued_book.heading('Member ID',text="Member ID")
    issued_book.heading('Member Name',text="Member Name")
    issued_book.heading('Book ID',text="Book ID")
    issued_book.heading('Issue Date',text="Issue Date")
    issued_book.grid(row=2, column=0, sticky="nsew")

    #create scrollbar
    scrollX=Scrollbar(issued_book_frame,orient=HORIZONTAL,command=issued_book.xview)
    scrollY=Scrollbar(issued_book_frame,orient=VERTICAL,command=issued_book.yview)
    scrollX.grid(row=3, column=0, sticky="ew")
    scrollY.grid(row=2, column=1, sticky="ns")

    #configure scrollbar
    issued_book.config(yscrollcommand=scrollY.set,xscrollcommand=scrollX.set)

    #striped row tags
    issued_book.tag_configure('oddrow',background="white")
    issued_book.tag_configure('evenrow',background="lightblue")
    #clear the treeview
    issued_book.delete(*issued_book.get_children())

    dbbook=sql.connect("BookDB.db")
    cur = dbbook.cursor()
    cur.execute("SELECT * FROM issue")
    result=cur.fetchall()
    global test1
    test1=0
    for record in result:
        if test1 % 2==0:
            issued_book.insert(parent='',index='end',iid=test1,text='',values=(record[0],record[1],record[2],record[3]),tags=('evenrow',)  )
        else:
            issued_book.insert(parent='',index='end',iid=test1,text='',values=(record[0],record[1],record[2],record[3]),tags=('oddrow',)  )
        test1 += 1
    dbbook.commit()
    cur.close()
    dbbook.close()


#to update member information
def update_memb():
    updt_mem_frame=Frame(root,bg="#b9f8f8",width=700,height=320,highlightbackground="black",highlightthickness=2)   
    updt_mem_frame.place(x=620,y=400)
    search_result_frame=Frame(root,bg="#b9f8f8",width=800,height=200,highlightbackground="black",highlightthickness=2)   
    search_result_frame.place(x=620,y=590)
    search_result_frame.pack_propagate(False)
    global search,backbtnImg,member_idImg
    def destry():
        updt_mem_frame.destroy()
        search_result_frame.destroy()
#heading label
    lb1=Label(updt_mem_frame,text="Update Member Information",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(updt_mem_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#Member_id Label
    member_idImg=PhotoImage(file="images\\mem_id.png")
    member_idLabel=Label(updt_mem_frame,text="  Member ID: ",font=("Arial 12 bold"),bg="#b9f8f8",bd=4,compound="left",image=member_idImg)
    member_idLabel.grid(row=1,column=0,padx=20,pady=10,sticky="w")
#Member ID entry box
    member_idEntry=Entry(updt_mem_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    member_idEntry.grid(row=1,column=0,padx=10,pady=15,sticky="n")

    def update():
        global email_Entry,year_Entry,member_emailImg,member_yearImg
    #Update email label
        member_emailImg=PhotoImage(file="images\\mem_email.png")
        email_Label=Label(search_result_frame,text="   Email: ",font=("Arial 12 bold"),bd=4,bg="#b9f8f8",compound="left",image=member_emailImg)
        email_Label.grid(row=1,column=0,padx=20,pady=10,sticky="w")
    #Update email entry box
        email_Entry=Entry(search_result_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        email_Entry.grid(row=1,column=1,pady=10,sticky="n")
     #Update year label
        member_yearImg=PhotoImage(file="images\\mem_year.png")
        year_Label=Label(search_result_frame,text="  Year: ",font=("Arial 12 bold"),bd=4,bg="#b9f8f8",compound="left",image=member_yearImg)
        year_Label.grid(row=2,column=0,padx=20,pady=10,sticky="w")
    #Update email entry box
        year_Entry=Entry(search_result_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
        year_Entry.grid(row=2,column=1,pady=10,sticky="n")
    #button to save changes in database
        savebtn=Button(search_result_frame,text="SAVE",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
             activeforeground="black",cursor="hand2",width=10,command=lambda:save())
        savebtn.grid(row=3,column=0,pady=10,padx=30,sticky="n")

        def save():
            memb_id=member_idEntry.get()
            email=email_Entry.get()
            year=year_Entry.get()
            if not email or not year:
                messagebox.showwarning("Warning","Please fill out all the details!!!!")
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
                    dbmemb=sql.connect('MemDB.db')
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
        dbmemb=sql.connect('MemDB.db')
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
#search button
    searchbtn=Button(updt_mem_frame,text="SEARCH",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
            activeforeground="black",cursor="hand2",width=10,command=lambda:search_member())
    searchbtn.grid(row=3,column=0,pady=10,padx=30,sticky="s")



#library image on left side frame1
libraryImg=PhotoImage(file="images\\lib.png")
libraryLabel=Label(frame1,image=libraryImg)
libraryLabel.grid(row=0,columnspan=2,padx=50,pady=20)

#button to add new book
addImg=PhotoImage(file="images\\add.png")
addbtn=Button(frame1,text="Add Book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",image=addImg,compound="left",command=lambda: addbook())
addbtn.config(image=addImg)   
addbtn.grid(row=1,column=0,padx=10,pady=20)

#button to update book details
updateImg=PhotoImage(file="images\\update.png")
updatebtn=Button(frame1,text="Update Book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
                 activeforeground="black",cursor="hand2",image=updateImg,compound="left",command=lambda:update())
updatebtn.config(image=updateImg)
updatebtn.grid(row=1,column=1,padx=10,pady=20)

#button to add new member
memImg=PhotoImage(file="images\\newmem.png")
membtn=Button(frame1,text="Add New Member",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",image=memImg,compound="left",command=lambda:newmem())
membtn.config(image=memImg)
membtn.grid(row=2,column=0,padx=10,pady=20)

#button to delete existing book
delImg=PhotoImage(file="images\\delete.png")
delbtn=Button(frame1,text="Delete Book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda: delete(),image=delImg,compound="left")
delbtn.config(image=delImg)
delbtn.grid(row=2,column=1,padx=10,pady=20)

#button to search book
searchImg=PhotoImage(file="images\\search.png")
searchbtn=Button(frame1,text="Search Book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda: search(),image=searchImg,compound="left")
searchbtn.config(image=searchImg)
searchbtn.grid(row=3,column=0,padx=10,pady=20)

#button to return book
returnImg=PhotoImage(file="images\\return.png")
returnbtn=Button(frame1,text="Return Book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda: retrn(),image=returnImg,compound="left")
returnbtn.config(image=returnImg)
returnbtn.grid(row=3,column=1,padx=10,pady=20)

#button to issue a book
issueImg=PhotoImage(file="images\\issue.png")
issuebtn=Button(frame1,text="Issue Book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:issue(),image=issueImg,compound="left")
issuebtn.config(image=issueImg)
issuebtn.grid(row=4,column=0,padx=10,pady=20)

#button update member information
update_membImg=PhotoImage(file="images\\update_memb.png")
update_membbtn=Button(frame1,text="Update Member Info",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:update_memb(),image=update_membImg,compound="left")
update_membbtn.config(image=update_membImg)
update_membbtn.grid(row=4,column=1,padx=10,pady=20)

#button to display existing members
existing_memImg=PhotoImage(file="images\\member.png")
existing_membtn=Button(frame1,text="Display Existing Members",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:existing_member(),image=existing_memImg,compound="left")
existing_membtn.config(image=existing_memImg)
existing_membtn.grid(row=5,column=0,padx=20,pady=20)

#button to display issued books to members
issued_bookImg=PhotoImage(file="images\\issued_book.png")
issued_bookbtn=Button(frame1,text="Display Issued book",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:issued_book(),image=issued_bookImg,compound="left")
issued_bookbtn.config(image=issued_bookImg)
issued_bookbtn.grid(row=5,column=1,padx=10,pady=20)

#button to generate report of library
reportImg=PhotoImage(file="images\\report.png")
reportbtn=Button(frame1,text="Generate Report",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:report(),image=reportImg,compound="left")
reportbtn.config(image=reportImg)
reportbtn.grid(row=6,column=0,padx=10,pady=20)

#button to launch web browser to purchase books for library
browserImg=PhotoImage(file="images\\browser.png")
browserbtn=Button(frame1,text="Open Browser",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:browser(),image=browserImg,compound="left")
browserbtn.config(image=browserImg)
browserbtn.grid(row=6,column=1,padx=10,pady=20)

#button to create backup of databases in pdf and csv format
backupImg=PhotoImage(file="images\\backup.png")
backupbtn=Button(frame1,text="Create Backup",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:backup(),image=backupImg,compound="left")
backupbtn.config(image=backupImg)
backupbtn.grid(row=7,column=0,padx=10,pady=20)

#button to logout from dashboard page
logoutImg=PhotoImage(file="images\\logout.png")
logoutbtn=Button(frame1,text="LOGOUT",background="pink",font=("Arial 12 bold"),bd=5,activebackground="pink",
              activeforeground="black",cursor="hand2",command=lambda:logout(),image=logoutImg,compound="left")
logoutbtn.config(image=logoutImg)
logoutbtn.grid(row=7,column=1,padx=10,pady=20)


# ------------------Treeview to display list of existing books--------------------------------
#Add style to treeview
style=ttk.Style(frame2)    
style.theme_use('default')  
style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=28)
#change selected row color
style.map('Treeview',background=[('selected',"#347083")])
#change color of heading
style.configure("Treeview.Heading",background="#347083",foreground="white")

#to display available books in library
table=ttk.Treeview(frame2,height=8,selectmode="extended")
table['columns']=("Book ID","Title","Author","Price","Quantity")

table.column("#0",width=0,stretch=NO)                        #to hide the default first column
table.column('Book ID',anchor=CENTER,width=120,minwidth=120)
table.column('Title',anchor=CENTER,width=180,minwidth=230)
table.column('Author',anchor=CENTER,width=170,minwidth=170)
table.column('Price',anchor=CENTER,width=120,minwidth=120)
table.column('Quantity',anchor=CENTER,width=180,minwidth=180)

table.heading('Book ID',text="Book ID")
table.heading('Title',text="Title")
table.heading('Author',text="Author")
table.heading('Price',text="Price")
table.heading('Quantity',text="Quantity")
table.pack(side=LEFT)
table.place(x=10,y=20)

#create scrollbar
scrollX=Scrollbar(frame2,orient=HORIZONTAL,command=table.xview)
scrollY=Scrollbar(frame2,orient=VERTICAL,command=table.yview)
scrollX.pack(side=BOTTOM,fill=X)
scrollY.pack(side=RIGHT,fill=Y)

#configure scrollbar
scrollX.config(command=table.xview)
scrollY.config(command=table.yview)
table.config(yscrollcommand=scrollY.set,xscrollcommand=scrollX.set)

#striped row tags
table.tag_configure('oddrow',background="white")
table.tag_configure('evenrow',background="lightblue")

#clear the treeview
table.delete(*table.get_children())


#function to display books from database in the treeview
def viewbook():
        dbbook=sql.connect("BookDB.db")
        cur = dbbook.cursor()
        cur.execute("""
                CREATE TABLE IF NOT EXISTS Book(book_id TEXT,title TEXT,
                    author TEXT,price INTEGER,quantity INTEGER)
                    """)

        cur.execute("SELECT * FROM Book")
        records=cur.fetchall()
        for test, record in enumerate(records):
            table.insert(parent='', index='end',iid=record[0], text='', values=(record[0], record[1], record[2], record[3], record[4]), 
                         tags=('evenrow' if test % 2 == 0 else 'oddrow',))
        dbbook.commit()
        cur.close()
        dbbook.close()
viewbook()        


#function to generate library report
def report():
    report_frame=Frame(root,bg="#b9f8f8",width=700,height=320,highlightbackground="black",highlightthickness=2)   
    report_frame.place(x=620,y=400)
    global backbtnImg
    def destry():
        report_frame.destroy()
#heading label
    lb1=Label(report_frame,text="Book Issuance Report",font=("Arial 14 bold"),bd=5,bg="blue",fg="white",width=60,anchor="center")
    lb1.grid(row=0,column=0,sticky="nsew")
#back button
    backbtnImg=PhotoImage(file="images\\backbtn.png")
    backbtn=Button(report_frame,text=" BACK",image=backbtnImg,font=("Arial 12 bold"),compound="left",bd=5,command=lambda:destry())
    backbtn.grid(row=0,column=0,sticky="w")
#Date Label
    Reportdate_Label=Label(report_frame,text="Enter date(YYYY-MM-DD):",font=("Arial 12 bold"),bg="#b9f8f8",bd=4)
    Reportdate_Label.grid(row=1,column=0,padx=10,pady=10,sticky="w")
#Date entry box
    Reportdate_Entry=Entry(report_frame,bd=5,font=("Arial 12 bold"),fg="blue",width=30)
    Reportdate_Entry.grid(row=1,column=0,pady=20,sticky="n")
#generate button
    generatebtn=Button(report_frame,text="Generate",background="green",font=("Arial 12 bold"),bd=5,activebackground="green",
            activeforeground="black",cursor="hand2",width=10,command=lambda:generate())
    generatebtn.grid(row=2,column=0,pady=10,padx=30,sticky="s")

    def generate():
        target_date=Reportdate_Entry.get()
        # Check if the target date is entered
        if not target_date:
            messagebox.showwarning("Warning", "Please enter the target date.")
            return
        try:
            # Call the functions to generate charts
            generate_book_quantity()
            generate_issued_books(target_date)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    # Function to generate a bar chart for book quantities
    def generate_book_quantity():
        try:
            dbbook = sql.connect('BookDB.db')
            # Query the database to get Book ID and Quantity
            query = "SELECT Book_ID, Quantity FROM Book"
            df = pd.read_sql_query(query, dbbook)
            # Generate positions for bars with some space between them
            positions = np.arange(len(df['Book_ID']))

            # Plot the bar chart
            plt.subplot(1,2,1)
            plt.barh(positions, df['Quantity'], color='hotpink', height=0.6)
            plt.title('Book Quantity Based on Book ID (Bar Chart)')
            plt.xlabel('Quantity')
            plt.ylabel('Book ID')
            plt.yticks(positions, df['Book_ID'])  # Set Book IDs as y-axis labels
            
            # Set x-axis ticks to whole numbers with a gap of 4
            x_ticks = np.arange(0, max(df['Quantity']) + 4, 4)
            plt.xticks(x_ticks)
            plt.grid(axis='x', linestyle='--', alpha=0.7)  # Add grid lines for better readability         
        except Exception as e:
            messagebox.showerror("Error", f"SQLite error: {e}")
        finally:
            dbbook.close()
        
    # Function to generate a line chart for the number of issued books on the specified date
    def generate_issued_books(target_date):
        try:
            dbbook = sql.connect('BookDB.db') 
            # Query the database for issued books on the specified date
            query = f"SELECT * FROM issue WHERE Issue_date LIKE '{target_date}%'"
            df = pd.read_sql_query(query, dbbook)
            # Count the occurrences of each date
            date_counts = df['Issue_date'].value_counts().sort_index()

            # Plot the line chart
            plt.subplot(1,2,2)
            plt.plot(date_counts.index, date_counts.values, marker='o', color='blue', linestyle='-')
            plt.title('Book Issuance on Each Date (Line Chart)')
            plt.xlabel('Date')
            plt.ylabel('Number of Books Issued')
            plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
            plt.yticks(np.arange(0, date_counts.max() + 2, 2)) 
            plt.grid(axis='both', linestyle='--', alpha=0.7)  # Add grid lines for better readability                
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error","No book is issued on this date!!!!")
        finally:
            dbbook.close()


#function to refresh the treeview
def refresh():
    #to change the bg color of row based on even or odd number of row
    table.tag_configure('oddrow',background="white")
    table.tag_configure('evenrow',background="lightblue")
    #clear the treeview
    table.delete(*table.get_children())

    #refresh the table
    dbbook=sql.connect("BookDB.db")
    cur = dbbook.cursor()
    cur.execute("SELECT * FROM Book")
    records=cur.fetchall()
    for test, record in enumerate(records):
        table.insert(parent='', index='end',iid=record[0], text='', values=(record[0], record[1], record[2], record[3], record[4]), 
                         tags=('evenrow' if test % 2 == 0 else 'oddrow',))
    dbbook.commit()
    cur.close()
    dbbook.close()

#open browser to purchase books for library
def browser():
    webbrowser.open("https://www.amazon.in/b?node=976389031")

#function to logout of dashboard page
def logout():
    global project_login  
    try:
        ask=messagebox.askyesno("Confirmation","Do you really want to logout?")
        if ask:
            root.destroy()
            import project_login
        else:
            messagebox.showinfo("Info","Logout cancelled")
    except:
        messagebox.showerror("Error","something went wrong in loging out")


#create backup using csv and pdf format
def backup():
    backup_folder = 'backup_folder'
    # Create the backup folder if it doesn't exist
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    def export_to_csv(database, table_name, csv_file):
        connection = sql.connect(database)
        query = f'SELECT * FROM {table_name}'
        df = pd.read_sql_query(query, connection)
        df.to_csv(csv_file, index=False)
        connection.close()

    def convert_csv_to_pdf(csv_file, pdf_file):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with open(csv_file, 'r') as file:
            for row in csv.reader(file):
                pdf.cell(200, 10, txt=" ".join(row), ln=True)
        pdf.output(pdf_file)

    try:
        # Backup for Database 1 BookDB
        database1 = 'BookDB.db'
        tables_database1 = ['Book', 'issue']
        for table in tables_database1:
            csv_file = os.path.join(backup_folder, f'backup_{database1}_{table}.csv')
            pdf_file = os.path.join(backup_folder, f'backup_{database1}_{table}.pdf')
            export_to_csv(database1, table, csv_file)
            convert_csv_to_pdf(csv_file, pdf_file)

        # Backup for Database 2 MemDB
        database2 = 'MemDB.db'
        tables_database2 = ['member', 'Expected_Return_Dates']
        for table in tables_database2:
            csv_file = os.path.join(backup_folder, f'backup_{database2}_{table}.csv')
            pdf_file = os.path.join(backup_folder, f'backup_{database2}_{table}.pdf')
            export_to_csv(database2, table, csv_file)
            convert_csv_to_pdf(csv_file, pdf_file)

            #display success message afer successful backup
        messagebox.showinfo("Success","Backup files created successfully !!!!")
    except Exception as e:
        messagebox.showerror("Error",f'Sqlite error {e}')

root.mainloop()
