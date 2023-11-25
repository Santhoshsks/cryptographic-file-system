from tkinter import *
from login_page import user_loginf
from register_page import user_registerf
import os
import sqlite3
import hashlib

def home():
    w=Toplevel()
    wi, he = w.winfo_screenwidth(), w.winfo_screenheight()
    w.geometry("%dx%d+0+0" % (wi, he))
    w.title('Home')
    w.resizable(0, 0)

    def register():
        w.destroy()
        user_registerf() 

    def login():
        w.destroy()
        user_loginf()
    
    admin = Button(w, text='Register', font=("gotham",15,"bold"), width=15, bd=0,
                            bg='white', cursor='hand2', fg='black',command=register)
    admin.place(relx=0.30,rely=0.553)

    user = Button(w, text='Login', font=("gotham",15,"bold"), width=15, bd=0,
                            bg='white', cursor='hand2', fg='black',command=login)
    user.place(relx=0.550,rely=0.554)
    w.mainloop()

if __name__ == '__main__':
    root = Tk()
    root.overrideredirect(1)
    root.withdraw()
    db_file = 'users.db'
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    home()