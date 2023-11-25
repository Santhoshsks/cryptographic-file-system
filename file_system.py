from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os
from tkinter import *
from tkinter import filedialog, messagebox
from cryptography.hazmat.primitives import hashes

class SecureFileSystemApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure File System")
        self.master.geometry("400x300")

        self.user_password_map = {
            'u1': 'p1',
            'user2': 'password2',
            # Add more users as needed
        }

        self.current_user = None  # To track the currently logged-in user
        self.user_directory_path = None

        # Labels and Entry Widgets
        self.label_username = Label(self.master, text="Enter Username:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=W)

        self.entry_username = Entry(self.master, width=20)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = Label(self.master, text="Enter Password:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=W)

        self.entry_password = Entry(self.master, show='*', width=20)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        # Buttons
        self.button_login = Button(self.master, text="Login", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)

        # File Operations Section
        self.label_file_operations = Label(self.master, text="File Operations", font=("Helvetica", 14, "bold"))
        self.label_file_operations.grid(row=3, column=0, columnspan=2, pady=10)

        self.button_new_file = Button(self.master, text="Create New File", command=self.create_new_file)
        self.button_new_file.grid(row=4, column=0, columnspan=2, pady=5)

        self.button_open_file = Button(self.master, text="Open File", command=self.open_file)
        self.button_open_file.grid(row=5, column=0, columnspan=2, pady=5)

        self.button_delete_file = Button(self.master, text="Delete File", command=self.delete_file)
        self.button_delete_file.grid(row=6, column=0, columnspan=2, pady=5)

    def derive_key(self, password, salt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return urlsafe_b64encode(kdf.derive(password.encode()))[:32]



    def encrypt_file(self, file_path, password):
        salt = os.urandom(16)
        key = self.derive_key(password, salt)

        # Ensure the key is the correct size for AES (128, 192, or 256 bits)
        key = key[:32]  # Use the first 32 bytes (256 bits) if the key is longer

        # Generate a random IV for CFB mode
        iv = os.urandom(16)

        with open(file_path, 'rb') as file:
            plaintext = file.read()

        cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()

        with open(file_path + '.enc', 'wb') as file:
            file.write(salt + iv + ciphertext)

    def decrypt_file(self, file_path, password):
        with open(file_path, 'rb') as file:
            data = file.read()

        salt = data[:16]
        iv = data[16:32]
        ciphertext = data[32:]

        key = self.derive_key(password, salt)

        cipher = Cipher(algorithms.AES(key), modes.CFB8(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        decrypted_file_path = file_path.rstrip('.enc')
        with open(decrypted_file_path, 'wb') as file:
            file.write(plaintext)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username in self.user_password_map and password == self.user_password_map[username]:
            # Successful login
            self.current_user = username
            self.user_directory_path = f"user_directories/{username}"  # Assuming directories are stored in a folder named 'user_directories'

            # Create the user directory if it doesn't exist
            if not os.path.exists(self.user_directory_path):
                os.makedirs(self.user_directory_path)

            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def create_new_file(self):
        if not self.current_user:
            messagebox.showwarning("Not Logged In", "Please log in before creating a new file.")
            return

        file_name = filedialog.asksaveasfilename(initialdir=self.user_directory_path, title="Select file",
                                                  defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_name:
            # You may add file content input here if needed
            with open(file_name, 'w') as file:
                file.write("This is a new file.")

            self.encrypt_file(file_name, self.user_password_map[self.current_user])
            messagebox.showinfo("File Created", "New file created successfully.")

    def open_file(self):
        if not self.current_user:
            messagebox.showwarning("Not Logged In", "Please log in before opening a file.")
            return

        file_name = filedialog.askopenfilename(initialdir=self.user_directory_path, title="Select file",
                                               filetypes=[("Text files", "*.txt.enc")])

        if file_name:
            try:
                self.decrypt_file(file_name, self.user_password_map[self.current_user])
                with open(file_name.rstrip('.enc'), 'r') as file:
                    file_content = file.read()
                messagebox.showinfo("File Content", f"File Content:\n{file_content}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def delete_file(self):
        if not self.current_user:
            messagebox.showwarning("Not Logged In", "Please log in before deleting a file.")
            return

        file_name = filedialog.askopenfilename(initialdir=self.user_directory_path, title="Select file",
                                               filetypes=[("Text files", "*.txt.enc")])

        if file_name:
            try:
                os.remove(file_name)
                messagebox.showinfo("File Deleted", "File deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = SecureFileSystemApp(root)
    root.mainloop()
