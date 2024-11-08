# Library Management System by MANIS SAHA (22BCE1538)
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import addBook, addMember, giveBook

con = sqlite3.connect('library.db')
cur = con.cursor()


class Main(object):
    def __init__(self, master):  # Fix the typo here
        self.master = master

        def displayStatistics(evt):
            count_books = cur.execute("SELECT count(book_id) FROM books").fetchall()
            count_members = cur.execute("SELECT count(member_id) FROM members").fetchall()
            taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchall()
            print(count_books)
            self.lbl_book_count.config(text='Total :' + str(count_books[0][0]) + ' books in library')
            self.lbl_member_count.config(text='Total member :' + str(count_members[0][0]))
            self.lbl_taken_count.config(text='Total books :' + str(taken_books[0][0]))
            displayBooks(self)

        def displayBooks(self):
            books = cur.execute("SELECT * FROM books").fetchall()
            count = 0
            self.list_books.delete(0, END)
            for book in books:
                print(book)
                self.list_books.insert(count, str(book[0]) + "-" + (book[1]))
                count += 1

            def bookInfo(evt):
                value = str(self.list_books.get(self.list_books.curselection()))
                id = value.split('-')[0]
                book = cur.execute("SELECT * FROM books WHERE book_id=?", (id,))
                book_info = book.fetchall()
                print(book_info)
                self.list_details.delete(0, 'end')
                self.list_details.insert(0, "Book Name : " + book_info[0][1])
                self.list_details.insert(1, "Author : " + book_info[0][2])
                self.list_details.insert(2, "Page : " + book_info[0][3])
                self.list_details.insert(3, "Language : " + book_info[0][4])
                if book_info[0][5] == 0:
                    self.list_details.insert(4, "Status : Available")
                else:
                    self.list_details.insert(4, "Status : Not Available")

            def doubleClick(evt):
                global given_id
                value = str(self.list_books.get(self.list_books.curselection()))
                given_id = value.split('-')[0]
                give_book = GiveBook()

            self.list_books.bind('<<ListboxSelect>>', bookInfo)
            self.tabs.bind('<<NotebookTabChanged>>', displayStatistics)
            # self.tabs.bind('<ButtonRelease-1>', displayBooks)
            self.list_books.bind('<Double-Button-1>', doubleClick)

        # frames
        mainFrame = Frame(self.master)
        mainFrame.pack()
        # top frame
        topFrame = Frame(mainFrame, width=1550, height=80, bg='#f8f8f8', padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)
        # center frame
        centerFrame = Frame(mainFrame, width=1550, relief=RIDGE, bg='#e0f0f0', height=700)
        centerFrame.pack(side=TOP)
        # center left frame
        centerLeftFrame = Frame(centerFrame, width=1200, height=700, bg='#e0f0f0', borderwidth=2, relief=SUNKEN)
        centerLeftFrame.pack(side=LEFT)
        # center right frame
        centerRightFrame = Frame(centerFrame, width=450, height=700, bg='#e0f0f0', borderwidth=2, relief=SUNKEN)
        centerRightFrame.pack()

        # search bar
        search_bar = LabelFrame(centerRightFrame, width=440, height=75, text='Search Box', bg='#9bc9ff')
        search_bar.pack(fill=BOTH)
        self.lbl_search = Label(search_bar, text='Search :', font='arial 12 bold', bg='#9bc9ff', fg='white')
        self.lbl_search.grid(row=0, column=0, padx=20, pady=10)
        self.ent_search = Entry(search_bar, width=30, bd=10)
        self.ent_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        self.btn_search = Button(search_bar, text='Search', font='arial 12', bg='#fcc324', fg='white', command=self.searchBooks)
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)

        # list bar
        list_bar = LabelFrame(centerRightFrame, width=440, height=175, text='List Box', bg='#fcc324')
        list_bar.pack(fill=BOTH)
        lbl_list = Label(list_bar, text='Sort By', font='times 16 bold', fg='#2488ff', bg='#fcc324')
        lbl_list.grid(row=0, column=2)
        self.listChoice = IntVar()
        rb1 = Radiobutton(list_bar, text='All Books', var=self.listChoice, value=1, bg='#fcc324')
        rb2 = Radiobutton(list_bar, text='In Library', var=self.listChoice, value=2, bg='#fcc324')
        rb3 = Radiobutton(list_bar, text='Borrowed Books', var=self.listChoice, value=3, bg='#fcc324')
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)
        btn_list = Button(list_bar, text='List Books', bg='#2488ff', fg='white', font='arial 12', command=self.listBooks)
        btn_list.grid(row=1, column=3, padx=40, pady=10)

        # title and image
        image_bar = Frame(centerRightFrame, width=440, height=350)
        image_bar.pack(fill=BOTH)
        self.title_right = Label(image_bar, text='Welcome to our Library', font='arial 16 bold')
        self.title_right.grid(row=0)
        self.img_library = PhotoImage(file='icons/library.png')
        self.lblImg = Label(image_bar, image=self.img_library)
        self.lblImg.grid(row=1)

        # add book
        self.iconbook_original = Image.open('icons/add_book.png')
        self.iconbook_resized = self.iconbook_original.resize((50, 50), Image.LANCZOS)
        self.iconbook = ImageTk.PhotoImage(self.iconbook_resized)
        self.btnbook = Button(topFrame, text='Add Book', image=self.iconbook, compound=LEFT, font='arial 12 bold', command=self.addBook)
        self.btnbook.pack(side=LEFT, padx=10)

        # add member button
        self.iconmember_original = Image.open('icons/users.png')
        self.iconmember_resized = self.iconmember_original.resize((50, 50), Image.LANCZOS)
        self.iconmember = ImageTk.PhotoImage(self.iconmember_resized)
        self.btnmember = Button(topFrame, text='Add Member', font='arial 12 bold', padx=10, command=self.addMember)
        self.btnmember.configure(image=self.iconmember, compound=LEFT)
        self.btnmember.pack(side=LEFT)

        # give book
        self.icongive_original = Image.open('icons/givebook.png')
        self.icongive_resized = self.icongive_original.resize((50, 50), Image.LANCZOS)
        self.icongive = ImageTk.PhotoImage(self.icongive_resized)
        self.btngive = Button(topFrame, text='Give Book', font='arial 12 bold', padx=10, image=self.icongive, compound=LEFT, command=self.giveBook)
        self.btngive.pack(side=LEFT)

        # tabs
        # tab1
        self.tabs = ttk.Notebook(centerLeftFrame, width=900, height=660)
        self.tabs.pack()
        self.tab1_icon_original = Image.open('icons/books.png')
        self.tab1_icon_resized = self.tab1_icon_original.resize((50, 50), Image.LANCZOS)
        self.tab1_icon = ImageTk.PhotoImage(self.tab1_icon_resized)
        self.tab2_icon_original = Image.open('icons/members.png')
        self.tab2_icon_resized = self.tab2_icon_original.resize((50, 50), Image.LANCZOS)
        self.tab2_icon = ImageTk.PhotoImage(self.tab2_icon_resized)
        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text='Library Management', image=self.tab1_icon, compound=LEFT)
        self.tabs.add(self.tab2, text='Statistics', image=self.tab2_icon, compound=LEFT)

        # list books
        self.list_books = Listbox(self.tab1, width=40, height=30, bd=5, font='times 12 bold')
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.list_books.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb.config(command=self.list_books.yview())
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=0, sticky=N+S+E)

        # list details
        self.list_details = Listbox(self.tab1, width=80, height=30, bd=5, font='times 12 bold')
        self.list_details.grid(row=0, column=1, padx=(10, 0), pady=10, sticky=N)

        # tab2
        # statistics
        self.lbl_book_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.lbl_book_count.grid(row=0)
        self.lbl_member_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.lbl_member_count.grid(row=1, sticky=W)
        self.lbl_taken_count = Label(self.tab2, text="", pady=20, font='verdana 14 bold')
        self.lbl_taken_count.grid(row=2, sticky=W)

        # functions
        displayBooks(self)
        displayStatistics(self)

    def addBook(self):
        add = addBook.AddBook()

    def addMember(self):
        member = addMember.AddMember()

    def searchBooks(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%' + value + '%',)).fetchall()
        print(search)
        self.list_books.delete(0, END)
        count = 0
        for book in search:
            self.list_books.insert(count, str(book[0]) + "-" + book[1])
            count += 1

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks = cur.execute("SELECT * FROM books").fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in allbooks:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status=?", (0,)).fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in books_in_library:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1
        else:
            taken_books = cur.execute("SELECT * FROM books WHERE book_status=?", (1,)).fetchall()
            self.list_books.delete(0, END)
            count = 0
            for book in taken_books:
                self.list_books.insert(count, str(book[0]) + "-" + book[1])
                count += 1

    def giveBook(self):
        give_book = giveBook.GiveBook()


class GiveBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x800+450+0")
        self.title("Lend Book")
        self.resizable(False, False)
        global given_id
        print(type(given_id))
        self.book_id = int(given_id)

        query1 = "SELECT * FROM books"
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
        heading = Label(self.topFrame, text='  Add Person', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # entries and labels
        # book name
        self.book_name = StringVar()
        self.lbl_name = Label(self.bottomFrame, text='Book Name :', font='arial 15 bold', fg='white', bg='#fcc324')
        self.lbl_name.place(x=40, y=40)
        self.combo_name = ttk.Combobox(self.bottomFrame, textvariable=self.book_name)
        self.combo_name['values'] = book_list
        self.combo_name.current(self.book_id - 1)
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


def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1550x800+0+0")
    root.iconbitmap('icons/icon.ico')
    root.mainloop()


if __name__ == '__main__':
    main()
