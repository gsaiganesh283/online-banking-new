import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # For handling images
import subprocess


# Function to fetch system settings from the MySQL database
def fetch_system_settings():
    try:
       
        conn = mysql.connector.connect(
            host="localhost",      
            user="root",           
            password="Daddy22@",   
            database="internetbanking"   
        )
        cursor = conn.cursor()
        
        # Execute SQL query
        cursor.execute("SELECT sys_name, sys_tagline FROM iB_SystemSettings WHERE id = 1")
        settings = cursor.fetchone()  # Fetch the first row
        
        conn.close()  # Close the database connection
        
        if settings:
            return settings
        else:
            return ("Default Name", "Default Tagline")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return None


# Function to refresh the UI
def refresh_ui():
    # Fetch the latest system settings from the database
    settings = fetch_system_settings()
    if settings:
        sys_name, sys_tagline = settings[0], settings[1]  # Adjust index based on your database schema
    else:
        sys_name, sys_tagline = "System Name", "System Tagline"
    
    # Update the labels dynamically
    label_sys_name.config(text=sys_name)
    label_sys_tagline.config(text=sys_tagline)
    
    # Schedule the refresh to occur every 5000 ms (5 seconds)
    root.after(5000, refresh_ui)


# Initialize the main tkinter window
root = Tk()
root.title("System Interface")
root.geometry("800x600")

# Load background image
# bg_image_path = r"C:\Users\gsaig\OneDrive\Documents\online-banking-new\dist\bg.png"  # Replace with your image path
# bg_image = Image.open(bg_image_path)
# bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Updated attribute
# bg_photo = ImageTk.PhotoImage(bg_image)

#     # Display the image on a Canvas
# canvas = Canvas(root, width=800, height=600)
# canvas.pack(fill="both", expand=True)
# canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Fetch system settings for the first time
settings = fetch_system_settings()
if settings:
    sys_name, sys_tagline = settings[0], settings[1]  # Adjust index based on your database schema
else:
    sys_name, sys_tagline = "System Name", "System Tagline"

# Top Navigation
nav_frame = Frame(root, bg="#333")
nav_frame.pack(fill=X)

Label(nav_frame, text=sys_name, fg="white", bg="#333", font=("Helvetica", 16, "bold")).pack(side=LEFT, padx=10)

def open_admin_portal():
    messagebox.showinfo("Info", "Opening Admin Portal...")  # Replace with actual functionality
    subprocess.Popen(['python', 'admin_index.py'])

def open_staff_portal():
    messagebox.showinfo("Info", "Opening Staff Portal...")  # Replace with actual functionality

def open_client_portal():
    messagebox.showinfo("Info", "Opening Client Portal...")  # Replace with actual functionality

Button(nav_frame, text="Join Us", bg="red", fg="white").pack(side=RIGHT, padx=10)
Button(nav_frame, text="Admin Portal", bg="#555", fg="white", command=open_admin_portal).pack(side=RIGHT, padx=25)
Button(nav_frame, text="Staff Portal", bg="#555", fg="white", command=open_staff_portal).pack(side=RIGHT, padx=20)
Button(nav_frame, text="Client Portal", bg="#555", fg="white", command=open_client_portal).pack(side=RIGHT, padx=15)

# Intro Section
intro_frame = Frame(root, bg="#eee", height=400)
intro_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

label_sys_name = Label(intro_frame, text=sys_name, font=("Helvetica", 24, "bold"), bg="#eee")
label_sys_name.pack(pady=20)

label_sys_tagline = Label(intro_frame, text=sys_tagline, font=("Helvetica", 16), bg="#eee")
label_sys_tagline.pack(pady=10)

Button(intro_frame, text="Get Started", bg="green", fg="white").pack(pady=20)

# Start the periodic refresh process
refresh_ui()

# Run the tkinter loop
root.mainloop()
