from tkinter import *
from PIL import ImageTk,Image
import ast
from tkinter import messagebox
from login_page import user_loginf
import hashlib
import sqlite3

def user_registerf():
    
    global w
    w=Toplevel()
    w.geometry('1920x768')
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
                e1.insert(0,'Name')

        e1 =Entry(w,width=30,fg='black',border=0,bg='white')
        e1.config(font=('Microsoft YaHei UI Light',16))
        e1.bind("<FocusIn>", on_enter)
        e1.bind("<FocusOut>", on_leave)
        e1.insert(0,'Name')
        e1.place(relx=0.510,rely=0.344)

        def on_enter(e):
            e2.delete(0,'end')    
        def on_leave(e):
            if e2.get()=='':   
                e2.insert(0,'Username')

        e2 =Entry(w,width=30,fg='black',border=0,bg='white')
        e2.config(font=('Microsoft YaHei UI Light',16))
        e2.bind("<FocusIn>", on_enter)
        e2.bind("<FocusOut>", on_leave)
        e2.insert(0,'Mail')
        e2.place(relx=0.510,rely=0.505)

        def on_enter(e):  
            e3.delete(0,'end')   
            e3.configure(fg='black',show='*')

        e3 =Entry(w,width=30,fg='black',border=0,bg='white')
        e3.config(font=('Microsoft YaHei UI Light',16))
        e3.bind("<FocusIn>", on_enter)
        e3.insert(0,'Password')
        e3.place(relx=0.510,rely=0.666)

        def back():
            w.destroy()
            user_loginf()
        Button(w,width=6,text='<Back',border=0,bg='white',fg='black', cursor='hand2',command=back).place(relx=0.755,rely=0.780)

        db_file = 'users.db'
        
        def register():
            name =e1.get()
            email = e2.get()
            password=e3.get()
            
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO Users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
                conn.commit()
                conn.close()
                messagebox.showinfo("","   successfully registered   ")
                w.destroy()

            except sqlite3.IntegrityError:
                messagebox.showwarning('try again', 'invalid username or password')
                w.destroy()
                conn.close()
                signin()

        Button(w, text='Register', font=("gotham",12,"bold"), width=10, bd=0,
        bg='white', cursor='hand2', fg='black',command=register).place(relx=0.600,rely=0.773)

    signin()
    w.mainloop()
