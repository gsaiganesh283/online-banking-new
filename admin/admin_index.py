import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import hashlib

# Function to handle login
def login(event=None):
    email = email_entry.get()
    password = password_entry.get()
    hashed_password = hashlib.sha1(hashlib.md5(password.encode()).hexdigest().encode()).hexdigest()

    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",      
            user="root",           
            password="Daddy22@",   
            database="internetbanking" 
        )
        cursor = conn.cursor()
        cursor.execute("SELECT email, password, admin_id FROM iB_admin WHERE email=%s AND password=%s", (email, hashed_password))
        result = cursor.fetchone()

        if result:
            admin_id = result[2]
            with open("login_details.txt", "a") as file:
                file.write(f"Email: {email}, Admin ID: {admin_id}\n")
        else:
            messagebox.showerror("Login Failed", "Access Denied. Please Check Your Credentials.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
def toggle_password():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        show_password_button.config(text='Show Password')
    else:
        password_entry.config(show='')
        show_password_button.config(text='Hide Password')
root = tk.Tk()
root.title("Admin Login")
root.geometry("800x600")  # Set the window size

# Apply a theme
style = ttk.Style(root)
style.theme_use('clam')  # You can change to 'alt', 'default', 'classic', etc.

# Create a frame to center the login form
frame = ttk.Frame(root, padding="20")
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the frame

# Create the login form inside the frame with styled widgets
ttk.Label(frame, text="Email:", font=("Helvetica", 12)).grid(row=0, column=0, pady=10, padx=5, sticky=tk.E)
email_entry = ttk.Entry(frame, font=("Helvetica", 12))
email_entry.grid(row=0, column=1, pady=10, padx=5)

ttk.Label(frame, text="Password:", font=("Helvetica", 12)).grid(row=1, column=0, pady=10, padx=5, sticky=tk.E)
password_entry = ttk.Entry(frame, font=("Helvetica", 12), show='*')
password_entry.grid(row=1, column=1, pady=10, padx=5)

# Add "Show Password" button
show_password_button = ttk.Button(frame, text="Show Password", command=toggle_password)
show_password_button.grid(row=2, column=1, pady=10, padx=5, sticky=tk.W)

login_button = ttk.Button(frame, text="Log In as Admin", command=login)
login_button.grid(row=3, columnspan=2, pady=20)

# Add some background color and change title font
root.configure(bg="#f0f0f0")
ttk.Label(frame, text="Admin Login", font=("Helvetica", 16, "bold")).grid(row=4, columnspan=2, pady=20)

# Bind the Enter key to the login function
root.bind('<Return>', login)

root.mainloop()