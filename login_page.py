from tkinter import *
from PIL import ImageTk,Image
import ast
from file_system import run
from tkinter import messagebox
import sqlite3
import hashlib

def user_loginf():
    w=Toplevel()
    wi, he = w.winfo_screenwidth(), w.winfo_screenheight()
    w.geometry("%dx%d+0+0" % (wi, he))
    w.title('Home')
    w.resizable(0, 0)
    """ bg_frame = Image.open('./images/usersignin.png')
    photo = ImageTk.PhotoImage(bg_frame)
    bg_panel = Label(w, image=photo)
    bg_panel.image = photo
    bg_panel.place(width=1366,height=768)     """
    
#------------------------------------------------------------------------------------------------------------

    def signin():        
        def on_enter(e):
            e1.delete(0,'end')    
        def on_leave(e):
            if e1.get()=='':   
                e1.insert(0,'User Name')

        e1 =Entry(w,width=30,fg='black',border=0,bg='white')
        e1.config(font=('Microsoft YaHei UI Light',16))
        e1.bind("<FocusIn>", on_enter)
        e1.bind("<FocusOut>", on_leave)
        e1.insert(0,'User name')
        e1.place(relx=0.510,rely=0.344)

        def on_enter(e):
            e2.delete(0,'end')    
        def on_leave(e):
            if e2.get()=='':   
                e2.insert(0,'Password')

        e2 =Entry(w,width=30,fg='black',border=0,bg='white')
        e2.config(font=('Microsoft YaHei UI Light',16))
        e2.bind("<FocusIn>", on_enter)
        e2.bind("<FocusOut>", on_leave)
        e2.insert(0,'Password')
        e2.place(relx=0.510,rely=0.505)


        def back():
            w.destroy()
        
        Button(w,width=6,text='<Back',border=0,bg='white',fg='black', cursor='hand2',command=back).place(relx=0.755,rely=0.780)

        db_file = 'users.db'

        def validate_login():
            name = e1.get()
            password=e2.get()
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Users WHERE name = ? AND password = ?', (name, hashlib.sha256(password.encode()).hexdigest()))
            user = cursor.fetchone()
            conn.close()
            if user:
                messagebox.showinfo("Logged in",f"Logged in as {user[1]}")
                w.destroy()
                run()
            else:
                messagebox.showwarning('try again', 'invalid username or password')
                w.destroy()
                signin()
                
        
        Button(w, text='Login', font=("gotham",12,"bold"), width=10, bd=0,
        bg='white', cursor='hand2', fg='black',command=validate_login).place(relx=0.600,rely=0.773)

    signin()
    w.mainloop()
