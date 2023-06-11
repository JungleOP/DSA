import tkinter as tk
import ctypes
from tkinter import filedialog
import verification
import os
import sign
import key


key.keyGeneration()


def check_admin():
    try:
        # Check if running with admin privileges
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if is_admin:
            result_label.config(text="You are running as admin!", foreground="green")
            open_secret_key()
        else:
            result_label.config(text="You are not running as admin.", foreground="red")
    except Exception as e:
        result_label.config(text="Error: " + str(e), foreground="red")


def open_secret_key():
    try:
        with open('secretkey.txt', 'r') as file:
            secret_key = file.read().strip()
            secret_key_label.config(text="Secret Key: " + secret_key)
    except FileNotFoundError:
        secret_key_label.config(text="File not found.", foreground="red")


def get_twenty_digits():
    try:
        with open('key.txt', 'r') as file:
            content = file.read().strip()
            digits = ''.join(c for c in content if c.isdigit())[:20]
            return "Key: "+digits
    except FileNotFoundError:
        return ""


def show_full_secret_key():
    try:
        with open('key.txt', 'r') as file:
            full_key = file.read().strip()
            secret_key_label.config(text="Key: " + full_key)
    except FileNotFoundError:
        secret_key_label.config(text="File not found.", foreground="red")


def hide_the_key():
    twenty_digits = get_twenty_digits()
    secret_key_label.config(text="" + twenty_digits)


def open_file_dialog():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select a .txt File", filetypes=(("Text files", "*.txt"),))
    if filepath:
        file_label.config(text="Selected File: " + filepath)
    else:
        file_label.config(text="No file selected.")


def run_sign_script():
    filepath = file_label.cget("text").split(": ")[1]
    if filepath.endswith('.txt'):
        sign.sign(filepath)
        result_label.config(text="Sign script executed for file: " + filepath)
    else:
        result_label.config(text="Invalid file format. Only .txt files are supported.", foreground="red")


def run_verification_script():
    filepath = filedialog.askopenfilename(initialdir="/", title="Select a .txt File", filetypes=(("Text files", "*.txt"),))
    if filepath.endswith('.txt'):
        if verification.verification(filepath):
            result_label.config(text="Valid", foreground="green")
        else:
            result_label.config(text="Invalid", foreground="red")
    else:
        result_label.config(text="Invalid file format. Only .txt files are supported.", foreground="red")
        cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in %r: %s" % (cwd, files))

def toggle_key():
    global show_key
    if show_key:
        toggle_btn.config(text="Hide Key")
        show_full_secret_key()
    else:
        toggle_btn.config(text="Show Key")
        hide_the_key()
    show_key = not show_key

# Create the main window
window = tk.Tk()
window.title("Mahmoud,Bader,Saeed DSA")

frame = tk.Frame(window)
frame.pack(pady=50)

# Set the background color and font for the window
window.configure(bg="#F5F5F5")
window.option_add("*Font", "Arial 10")

group_names = tk.Label(frame, text="Done by: Mahmoud, Bader, Saeed")
group_names.pack()

# Create a button to check if running as admin
check_button = tk.Button(frame, text="admin", command=check_admin, bg="#838B8B", fg="red")
check_button.pack(pady=10)

# Create a label for the result
result_label = tk.Label(frame, text="", bg="#F5F5F5")
result_label.pack()

# Create a button to open file dialog
sign_button = tk.Button(frame, text="Sign", command=open_file_dialog, bg="#838B8B", fg="black")
sign_button.pack(pady=10)

# Create a label to display the selected file
file_label = tk.Label(frame, text="No file selected.", bg="#F5F5F5")
file_label.pack()

# Create a button to run sign script
run_button = tk.Button(frame, text="Run Sign Script", command=run_sign_script, bg="#838B8B", fg="black")
run_button.pack(pady=10)

# Create a button to run verification script
verify_button = tk.Button(frame, text="Verify", command=run_verification_script, bg="#838B8B", fg="black")
verify_button.pack(pady=10)

# Toggle botton to show/hide the key
show_key = False
toggle_btn = tk.Button(frame, text="Show Key", command=toggle_key)
toggle_btn.pack()

# Create a frame for the "Secret Key" label
secret_key_frame = tk.Frame(frame, bg="#F5F5F5")
secret_key_frame.pack(anchor="se", padx=10, pady=10)

# Create a label to display the 20 digits
digits_label = tk.Label(secret_key_frame, text="", bg="#F5F5F5")
digits_label.pack(side="left")

# Create a label to display the actual key
twenty_digits = get_twenty_digits()
secret_key_label = tk.Label(secret_key_frame, text=twenty_digits, bg="#F5F5F5", fg="#2196f3", font=("Arial", 12, "bold"))
secret_key_label.pack(side="right")

frame.pack_configure(anchor='center')

window.mainloop()