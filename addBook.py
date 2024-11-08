from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

con = sqlite3.connect('library.db')
cur = con.cursor()


class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x800+450+0")
        self.title("Add Book")
        self.resizable(False, False)

        # frames
        # top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # bottom frame
        self.bottomFrame = Frame(self, height=650, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # heading and image
        self.top_image_original = Image.open('icons/add_book.png')
        self.top_image_resized = self.top_image_original.resize((100, 100), Image.LANCZOS)
        self.top_image = ImageTk.PhotoImage(self.top_image_resized)
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=100, y=30)
        heading = Label(self.topFrame, text='  Add Book', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # entries and labels
        # name
        self.lbl_name = Label(self.bottomFrame, text='Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, 'Please enter a book name')
        self.ent_name.place(x=150, y=45)

        # author
        self.lbl_author = Label(self.bottomFrame, text='Author :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_author.place(x=40, y=80)
        self.ent_author = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_author.insert(0, 'Please enter a author name')
        self.ent_author.place(x=150, y=85)

        # page
        self.lbl_page = Label(self.bottomFrame, text='Page :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_page.place(x=40, y=120)
        self.ent_page = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_page.insert(0, 'Please enter page size')
        self.ent_page.place(x=150, y=125)

        # language
        self.lbl_language = Label(self.bottomFrame, text='Language :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_language.place(x=40, y=160)
        self.ent_language = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_language.insert(0, 'Please enter a language')
        self.ent_language.place(x=150, y=165)

        # button
        button = Button(self.bottomFrame, text='Add Book', command=self.addBook)
        button.place(x=270, y=200)

    def addBook(self):
        name = self.ent_name.get()
        author = self.ent_author.get()
        page = self.ent_page.get()
        language = self.ent_language.get()

        if (name and author and page and language != ""):
            try:
                query = "INSERT INTO 'books' (book_name, book_author, book_page, book_language) VALUES (?, ?, ?, ?)"
                cur.execute(query, (name, author, page, language))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database", icon='info')
            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')
