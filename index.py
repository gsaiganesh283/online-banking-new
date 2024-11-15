import sqlite3
from tkinter import *
from tkinter import messagebox


# Function to fetch system settings from the database
def fetch_system_settings():
    try:
        conn = sqlite3.connect('config.db')  # Replace with your database path
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM iB_SystemSettings")
        settings = cursor.fetchone()  # Assuming there's only one settings record
        conn.close()
        return settings
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")
        return None


# Function to refresh the UI
def refresh_ui():
    # Fetch the latest system settings from the database
    settings = fetch_system_settings()
    if settings:
        sys_name, sys_tagline = settings[1], settings[2]  # Adjust index based on your database schema
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

# Fetch system settings for the first time
settings = fetch_system_settings()
if settings:
    sys_name, sys_tagline = settings[1], settings[2]  # Adjust index based on your database schema
else:
    sys_name, sys_tagline = "System Name", "System Tagline"

# Top Navigation
nav_frame = Frame(root, bg="#333")
nav_frame.pack(fill=X)

Label(nav_frame, text=sys_name, fg="white", bg="#333", font=("Helvetica", 16, "bold")).pack(side=LEFT, padx=10)

def open_admin_portal():
    messagebox.showinfo("Info", "Opening Admin Portal...")  # Replace with actual functionality

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
