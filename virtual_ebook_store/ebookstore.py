# Import packages to use
import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext

# Create or open the database
db = sqlite3.connect('ebookstore.db')

# Get a cursor object
cursor = db.cursor()

# Try load or create the database
try:
    # Create books table if it does not already exist
    cursor.execute("CREATE TABLE IF NOT EXISTS books (id integer PRIMARY KEY, title text, author text, QTY text)")
    # Commit
    db.commit()
except Exception as e:
    db.rollback()
    raise e


# Function to be performed on search click
def search_click():
    # Command for each permutation of entries - there may be an easier (less code-intensive way to do this)
    if(id_input.get()=="" and title_input.get()=="" and author_input.get()==""):
        cursor.execute("SELECT * FROM books")
        all_rows_search = cursor.fetchall()
        #messagebox.showinfo('Error Message', 'Need at least one non-empty field to perform a search')
        #return
    elif(id_input.get()!="" and title_input.get()=="" and author_input.get()==""):
        cursor.execute("SELECT * FROM books WHERE id=?",(int(id_input.get()),))
        all_rows_search = cursor.fetchall()
    elif(id_input.get()=="" and title_input.get()!="" and author_input.get()==""):
        cursor.execute("SELECT * FROM books WHERE title LIKE ?",('%'+title_input.get()+'%',))
        all_rows_search = cursor.fetchall()
    elif(id_input.get()=="" and title_input.get()=="" and author_input.get()!=""):
        cursor.execute("SELECT * FROM books WHERE author LIKE ?",('%'+author_input.get()+'%',))
        all_rows_search = cursor.fetchall()    
    elif(id_input.get()!="" and title_input.get()!="" and author_input.get()==""):
        cursor.execute("SELECT * FROM books WHERE id=? AND title LIKE ?",(int(id_input.get()), '%'+title_input.get()+'%'))
        all_rows_search = cursor.fetchall()
    elif(id_input.get()!="" and title_input.get()=="" and author_input.get()!=""):
        cursor.execute("SELECT * FROM books WHERE id=? AND author LIKE ?",(int(id_input.get()), '%'+author_input.get()+'%'))
        all_rows_search = cursor.fetchall()
    elif(id_input.get()=="" and title_input.get()!="" and author_input.get()!=""):
        cursor.execute("SELECT * FROM books WHERE title LIKE ? AND author LIKE ?",('%'+title_input.get()+'%', '%'+author_input.get()+'%'))
        all_rows_search = cursor.fetchall()
    elif(id_input.get()!="" and title_input.get()!="" and author_input.get()!=""):
        cursor.execute("SELECT * FROM books WHERE id=? AND title LIKE ? AND author LIKE ?",(int(id_input.get()), '%'+title_input.get()+'%', '%'+author_input.get()+'%'))
        all_rows_search = cursor.fetchall()

    # create a new window with a table of books which match the search fields above
    window_search = tkinter.Tk()
    window_search.title("Search results")
    window_search.geometry('700x200')
    id_search_label = Label(window_search, text="id", font=("Calibri", 9, "bold italic")).grid(row=0, column=0)
    title_search_label = Label(window_search, text="title", font=("Calibri", 9, "bold italic")).grid(row=0, column=1)
    author_search_label = Label(window_search, text="author", font=("Calibri", 9, "bold italic")).grid(row=0, column=2)
    qty_search_label = Label(window_search, text="qty", font=("Calibri", 9, "bold italic")).grid(row=0, column=3)
    # Printing the results as a label
    for j in range(0,len(all_rows_search)):
        record = all_rows_search[j]
        record = list(record)
        for i in range(0,4):
            rec = str(record[i])
            Label(window_search, text=rec, font=("Calibri", 8)).grid(row=j+1, column=i, padx=(10,10))

# Check if ID exists in database
def id_check(number):
    cursor.execute("SELECT * FROM books WHERE id=?", (number,))
    check_ids = cursor.fetchall()
    return(check_ids != [])

# Function to add new book to the database
def new_click():
    # Creating a new window for the add function
    window_add = tkinter.Tk()
    window_add.title("Enter a new book")
    window_add.geometry('1000x50')

    f1_add = Frame(window_add, width=300)
    f1_add.pack()
    
    idlabel_add = tkinter.Label(f1_add, text="ID:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
    id_input_add = Entry(f1_add, width=10)
    id_input_add.pack(side=LEFT)

    titlelabel_add = tkinter.Label(f1_add, text="Title:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
    title_input_add = Entry(f1_add, width=50)
    title_input_add.pack(side=LEFT)

    authorlabel_add = tkinter.Label(f1_add, text="Author:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
    author_input_add = Entry(f1_add, width=50)
    author_input_add.pack(side=LEFT)

    qty_add = tkinter.Label(f1_add, text="QTY:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
    qty_input_add = Entry(f1_add, width=10)
    qty_input_add.pack(side=LEFT)

    # Function to commit the program to save the book in the database
    def commit_add():
        if(id_input_add.get() == "" or title_input_add.get() == "" or author_input_add.get() == "" or qty_input_add.get() == ""):
            messagebox.showinfo("Book add error", "All record fields must be filled.")
            
        elif(id_check(int(id_input_add.get()))):
            messagebox.showinfo("Book add error", "This ID has already been taken. Please use a different one.")
            
        else:
            try:
                cursor.execute("INSERT INTO books(id, title, author, QTY) VALUES(?,?,?,?)", (int(id_input_add.get()), title_input_add.get(), author_input_add.get(), int(qty_input_add.get())))
                db.commit()
                messagebox.showinfo("Success", "Book has been added to the database.")
                window_add.destroy()
            except Exception as e:
                db.rollback()
                raise e    

    cancel_add_bt = Button(f1_add, text="Cancel", command=window_add.destroy).pack(side=LEFT, padx=5)
    add_bt = Button(f1_add, text="Add", command=commit_add).pack(side=LEFT, padx=5)
    
    window_add.mainloop()

# Function to close the program and the database from the ebookstore
def close_program():
    db.close()
    window.destroy()

# Function to update/edit book details in the database
def update_click():
    # Create a new window for this
    window_update = tkinter.Tk()
    window_update.title("Update book record")
    window_update.geometry('500x300')

    f1_update = Frame(window_update, width=500)
    f1_update.pack()

    id_to_update_label = Label(f1_update, text = "Enter book ID to update details:", font=("Calibri", 9)).pack(side=LEFT, padx=(0,20), pady=(20,10))
    id_to_update = Entry(f1_update, width=10)
    id_to_update.pack(side=LEFT, pady=(20,10))
    
    f2_update = Frame(window_update, width=500)
    f2_update.pack()
    book_columns_label = Label(f2_update, text="Type ID above")
    book_columns_label.pack(side=TOP)
    book_label =  Label(f2_update, text = "The result will appear here")
    book_label.pack(side=BOTTOM)

    # Additional frames to appear once an id is entered and the update button is clicked
    def make_update():
        if(id_to_update.get()==""):
            return
        else:
            cursor.execute("SELECT * FROM books WHERE id=?",(int(id_to_update.get()),))
            book_to_update = list(cursor.fetchall())
            if(book_to_update==[]):
                messagebox.showinfo("Book ID error", "The ID you have entered does not exist in the database")
            else:
                book_columns_label.config(text="id, title, author, qty", font=("Calibri", 10, "bold italic"))
                book_label.config(text = str(book_to_update[0][0])+", "+book_to_update[0][1]+", "+book_to_update[0][2]+", "+str(book_to_update[0][3]))
                f3_update = Frame(window_update, width=500)
                f3_update.pack()
                l3 = Label(f3_update, text="Enter fields you would like to change for the above book:").pack(side=LEFT, pady = (20, 10))
                f4_update = Frame(window_update, width=500)
                f4_update.pack()
                l4 = Label(f4_update, text="title:", font=("Calibri", 10, "italic")).pack(side=LEFT, padx=(0,35))
                title_change = Entry(f4_update, width=50)
                title_change.pack(side=LEFT)
                f5_update = Frame(window_update, width=500)
                f5_update.pack()
                l5 = Label(f5_update, text="author:", font=("Calibri", 10, "italic")).pack(side=LEFT, padx=(0,20))
                author_change = Entry(f5_update, width=50)
                author_change.pack(side=LEFT)
                f6_update = Frame(window_update, width=500)
                f6_update.pack()
                l6 = Label(f6_update, text="qty:", font=("Calibri", 10, "italic")).pack(side=LEFT, padx=(0,25))
                qty_change = Entry(f6_update, width=10)
                qty_change.pack(side=LEFT)
                f7_update = Frame(window_update, width=500)
                f7_update.pack()

                # Function to apply the changes on apply changes button click
                def apply_changes():
                    if(title_change.get()=="" and author_change.get()=="" and qty_change.get()==""):
                        messagebox.showinfo("Error applying changes", "No fields have been set to change")
                        return
                    elif(title_change.get()!="" and author_change.get()=="" and qty_change.get()==""):
                        cursor.execute("UPDATE books SET title = ? WHERE id = ?", (title_change.get(), int(id_to_update.get())))
                    elif(title_change.get()=="" and author_change.get()!="" and qty_change.get()==""):
                        cursor.execute("UPDATE books SET author = ? WHERE id = ?", (author_change.get(), int(id_to_update.get())))
                    elif(title_change.get()=="" and author_change.get()=="" and qty_change.get()!=""):
                        cursor.execute("UPDATE books SET qty = ? WHERE id = ?", (int(qty_change.get()), int(id_to_update.get())))
                    elif(title_change.get()!="" and author_change.get()!="" and qty_change.get()==""):
                        cursor.execute("UPDATE books SET title = ?, author = ? WHERE id = ?", (title_change.get(), author_change.get(), int(id_to_update.get())))
                    elif(title_change.get()=="" and author_change.get()!="" and qty_change.get()!=""):
                        cursor.execute("UPDATE books SET author = ?, qty = ? WHERE id = ?", (author_change.get(), int(qty_change.get()), int(id_to_update.get())))
                    elif(title_change.get()!="" and author_change.get()=="" and qty_change.get()!=""):
                        cursor.execute("UPDATE books SET title = ?, qty = ? WHERE id = ?", (title_change.get(), int(qty_change.get()), int(id_to_update.get())))
                    elif(title_change.get()!="" and author_change.get()!="" and qty_change.get()!=""):
                        cursor.execute("UPDATE books SET title = ?, author = ?, qty = ? WHERE id = ?", (title_change.get(), author_change.get(), int(qty_change.get()), int(id_to_update.get())))
                    db.commit()
                    messagebox.showinfo("Success", "Your changes have been made")
                    window_update.destroy()
                    window_update.mainloop()

                # apply changes button    
                apply_changes_btn = Button(f7_update, text="Apply changes", command=apply_changes).pack(pady=(20,10))
    
    # update button
    update_btn = Button(f1_update, text="Update", command=make_update).pack(side=LEFT, padx=(20,0), pady=(20,10))  
    
# Function to delete a book from the database
def delete_click():
    # Create new window for this
    window_delete = tkinter.Tk()
    window_delete.title("Delete book record")
    window_delete.geometry('450x180')

    f1_delete = Frame(window_delete, width=500)
    f1_delete.pack()
    
    id_to_delete_label = Label(f1_delete, text = "Enter ID of book you want to delete:", font=("Calibri", 9)).pack(side=LEFT, padx=(0,20), pady=(20,10))
    id_to_delete = Entry(f1_delete, width=10)
    id_to_delete.pack(side=LEFT, padx=(0,20), pady=(20,10))

    f2_delete = Frame(window_delete, width=500)
    f2_delete.pack()
    are_you_sure_label = Label(f2_delete, text="")
    are_you_sure_label.pack(side=TOP)
    book_delete_label =  Label(f2_delete, text = "")
    book_delete_label.pack(side=BOTTOM)

    # Function once delete button is clicked to bring up the book and an are you sure message.
    def set_delete():
        if(id_to_delete.get()==""):
            return
        else:
            cursor.execute("SELECT * FROM books WHERE id=?",(int(id_to_delete.get()),))
            book_to_delete = list(cursor.fetchall())
            if(book_to_delete==[]):
                messagebox.showinfo("Book ID error", "The ID you have entered does not exist in the database")
            else:
                are_you_sure_label.config(text="Are you sure you want to delete this book from the database?", font=("Calibri", 10, "bold"))
                book_delete_label.config(text = str(book_to_delete[0][0])+", "+book_to_delete[0][1]+", "+book_to_delete[0][2])
                f3_delete = Frame(window_delete, width=500)
                f3_delete.pack(pady=(20,0))

                # Function to confirm delete of book
                def confirm_delete():
                    cursor.execute("DELETE FROM books WHERE id=?",(int(id_to_delete.get()),))
                    db.commit()
                    messagebox.showinfo("Deletion successful", "Book has been removed from database.")
                    window_delete.destroy()

                # Function to cancel delete request
                def cancel_delete():
                    window_delete.destroy()


                cancel_del_btn = Button(f3_delete, text="No, cancel.", command=cancel_delete).pack(side=LEFT, padx=(0,5))
                confirm_del_button = Button(f3_delete, text="Yes, delete!", command=confirm_delete).pack(side=LEFT)
    
    del_button = Button(f1_delete, text="Delete", command=set_delete).pack(side=LEFT, pady=(20,10))


# Main ebookstore window
window = tkinter.Tk()
window.title("ebookstore")
window.geometry('900x320')
window.resizable(0,0) # prevents window resizing

# Splitting up window into frames
f1 = Frame(window, width=400, pady=20)
f1.pack()
f2 = Frame(window, width=400)
f2.pack()
f3 = Frame(window, width=400, pady=10)
f3.pack()
f4 = Frame(window, width=400, pady=100)
f4.pack()
f5 = Frame(window, width=400, pady=10)
f5.pack()
f6 = Frame(window, width=400)
f6.pack()
f7 = Frame(window, width=400, pady=30)
f7.pack()

# Adding the labels and buttons to the frames within the window
label_main = tkinter.Label(f1, text="Welcome to the ebookstore.", font=("Bookman Old Style", 21)).pack(fill=X)

search_label = tkinter.Label(f2, text="Search for a book:", font=("Calibri", 14)).pack(side=LEFT)

idlabel = tkinter.Label(f3, text="ID:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
id_input = Entry(f3, width=10)
id_input.pack(side=LEFT)

titlelabel = tkinter.Label(f3, text="Title:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
title_input = Entry(f3, width=50)
title_input.pack(side=LEFT)

authorlabel = tkinter.Label(f3, text="Author:", font=("Calibri", 10)).pack(side=LEFT, padx=5)
author_input = Entry(f3, width=50)
author_input.pack(side=LEFT)

bt_search = Button(f3, text="Search", command=search_click).pack(side=RIGHT, padx=10)

database_label = tkinter.Label(f5, text="Database functions:", font=("Calibri", 14)).pack(side=BOTTOM)

bt_add = Button(f6, text="Enter new book", command=new_click).pack(side=LEFT, padx=40)
bt_update = Button(f6, text="Update book record", command=update_click).pack(side=LEFT, padx=40)
bt_delete = Button(f6, text="Delete book record", command = delete_click).pack(side=LEFT, padx=40)

bt_close = Button(f7, text="Exit", command=close_program).pack(side=BOTTOM)


window.mainloop()




