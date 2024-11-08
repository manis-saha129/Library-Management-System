from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

con = sqlite3.connect('library.db')
cur = con.cursor()


class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x800+450+0")
        self.title("Lend Book")
        self.resizable(False, False)

        query1 = "SELECT * FROM books WHERE book_status=0"
        books = cur.execute(query1).fetchall()
        book_list = []
        for book in books:
            book_list.append(str(book[0]) + "-" + book[1])

        query2 = "SELECT * FROM members"
        members = cur.execute(query2).fetchall()
        member_list = []
        for member in members:
            member_list.append(str(member[0]) + "-" + member[1])

        # frames
        # top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # bottom frame
        self.bottomFrame = Frame(self, height=650, bg='#fcc324')
        self.bottomFrame.pack(fill=X)

        # heading and image
        self.top_image_original = Image.open('icons/addperson.png')
        self.top_image_resized = self.top_image_original.resize((100, 100), Image.LANCZOS)
        self.top_image = ImageTk.PhotoImage(self.top_image_resized)
        top_image_lbl = Label(self.topFrame, image=self.top_image, bg='white')
        top_image_lbl.place(x=100, y=30)
        heading = Label(self.topFrame, text='  Lend a Book', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # entries and labels
        # book name
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='Book Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name['values'] = book_list
        self.combo_name.place(x=200, y=45)

        # member name
        self.member_name = StringVar()
        self.lbl_phone = Label(self.bottomFrame, text='Member Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_phone.place(x=40, y=80)
        self.combo_member = ttk.Combobox(self.bottomFrame, textvariable=self.member_name)
        self.combo_member['values'] = member_list
        self.combo_member.place(x=200, y=85)

        # button
        button = Button(self.bottomFrame, text='Lend Book', command=self.lendBook)
        button.place(x=275, y=120)

    def lendBook(self):
        book_name = self.book_name.get()
        self.book_id = book_name.split('-')[0]
        member_name = self.member_name.get()

        if (book_name and member_name !=""):
            try:
                query = "INSERT INTO 'borrows' (bbook_id, bmember_id) VALUES(?, ?)"
                cur.execute(query, (book_name, member_name))
                con.commit()
                messagebox.showinfo("Success", "Successfully added to database!", icon='info')
                cur.execute("UPDATE books SET  book_status=? WHERE book_id=?", (1, self.book_id))
                con.commit()
            except:
                messagebox.showerror("Error", "Cant add to database", icon='warning')
        else:
            messagebox.showerror("Error", "Fields cant be empty", icon='warning')
