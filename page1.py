import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import os
from tkcalendar import DateEntry
from datetime import date

# Directories
DB_NAME = "client_info.db"
IMAGE_FOLDER = "uploaded_photos"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

# Database setup
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS client_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    surname TEXT,
    first_name TEXT,
    middle_name TEXT,
    sss_number TEXT,
    sss_employed INTEGER,
    sss_self_employed INTEGER,
    gsis_number TEXT,
    uninformed_personnel TEXT,
    age INTEGER,
    sex TEXT,
    civil_status TEXT,
    dob TEXT,
    landline TEXT,
    mobile TEXT,
    email TEXT,
    current_address TEXT,
    permanent_address TEXT,
    photo_path TEXT
)
""")
conn.commit()

# GUI
root = tk.Tk()
root.title("KAGABAY - Client Registration")
root.geometry("800x700")

# Global variables
uploaded_photo_path = tk.StringVar()

# Main checkbox variables
sss_main_var = tk.IntVar()
gsis_main_var = tk.IntVar()
uniformed_main_var = tk.IntVar()

# SSS membership type variable (radiobutton)
sss_type_var = tk.StringVar(value="")  # "employed" or "self-employed" or ""

def upload_photo():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        dest_path = os.path.join(IMAGE_FOLDER, os.path.basename(file_path))
        with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
            dst.write(src.read())
        uploaded_photo_path.set(dest_path)
        load = Image.open(dest_path)
        load = load.resize((100, 100))
        render = ImageTk.PhotoImage(load)
        img_label.configure(image=render)
        img_label.image = render

def toggle_sss_main():
    if sss_main_var.get():
        gsis_main_var.set(0)
        uniformed_main_var.set(0)
        sss_type_frame.grid(row=4, column=3, columnspan=2)
    else:
        sss_type_frame.grid_remove()
        sss_type_var.set("")

def toggle_gsis_main():
    if gsis_main_var.get():
        sss_main_var.set(0)
        uniformed_main_var.set(0)
        sss_type_frame.grid_remove()
        sss_type_var.set("")

def toggle_uniformed_main():
    if uniformed_main_var.get():
        sss_main_var.set(0)
        gsis_main_var.set(0)
        sss_type_frame.grid_remove()
        sss_type_var.set("")

def submit_and_next():
    # Collect SSS employed/self-employed as integers for DB
    sss_employed = 1 if sss_type_var.get() == "employed" else 0
    sss_self_employed = 1 if sss_type_var.get() == "self-employed" else 0

    # Validation: make sure only one of the three main options selected
    main_selected = sum([sss_main_var.get(), gsis_main_var.get(), uniformed_main_var.get()])
    if main_selected != 1:
        messagebox.showerror("Error", "Please select only one among SSS No., GSIS No., or Uniformed Personnel.")
        return

    # If SSS selected, make sure membership type chosen
    if sss_main_var.get() and sss_type_var.get() == "":
        messagebox.showerror("Error", "Please select either 'Employed' or 'Self-employed' for SSS Membership.")
        return

    # Collect data
    data = (
        surname_entry.get(),
        fname_entry.get(),
        mname_entry.get(),
        sss_entry.get() if sss_main_var.get() else "",  # Only save if selected
        sss_employed,
        sss_self_employed,
        gsis_entry.get() if gsis_main_var.get() else "",
        uniformed_entry.get() if uniformed_main_var.get() else "",
        age_entry.get(),
        sex_var.get(),
        civil_status_var.get(),
        dob_entry.get_date().isoformat(),
        landline_entry.get(),
        mobile_entry.get(),
        email_entry.get(),
        curr_add_entry.get("1.0", tk.END).strip(),
        perm_add_entry.get("1.0", tk.END).strip(),
        uploaded_photo_path.get()
    )

    c.execute("""
        INSERT INTO client_profile (
            surname, first_name, middle_name, sss_number, sss_employed, sss_self_employed, gsis_number,
            uninformed_personnel, age, sex, civil_status, dob, landline, mobile, email,
            current_address, permanent_address, photo_path
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    messagebox.showinfo("Saved", "Client profile saved. Proceeding to next section.")
    root.destroy()

# New function to copy current address to permanent address
def copy_current_to_permanent():
    current_text = curr_add_entry.get("1.0", tk.END).strip()
    perm_add_entry.delete("1.0", tk.END)
    perm_add_entry.insert(tk.END, current_text)

# Frame
frame = tk.LabelFrame(root, text="Client Profile", padx=10, pady=10)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Upload Photo
tk.Label(frame, text="Upload 1x1 Picture:").grid(row=0, column=0, sticky="w")
tk.Button(frame, text="Browse", command=upload_photo).grid(row=0, column=1)
img_label = tk.Label(frame)
img_label.grid(row=0, column=2, rowspan=3, padx=10)

# Name Entries
tk.Label(frame, text="Surname").grid(row=1, column=0, sticky="w")
surname_entry = tk.Entry(frame)
surname_entry.grid(row=1, column=1)

tk.Label(frame, text="First Name").grid(row=2, column=0, sticky="w")
fname_entry = tk.Entry(frame)
fname_entry.grid(row=2, column=1)

tk.Label(frame, text="Middle Name").grid(row=3, column=0, sticky="w")
mname_entry = tk.Entry(frame)
mname_entry.grid(row=3, column=1)

# Main checkboxes for SSS, GSIS, Uniformed Personnel
tk.Checkbutton(frame, variable=sss_main_var, command=toggle_sss_main).grid(row=4, column=0, sticky="e")
tk.Label(frame, text="SSS No.").grid(row=4, column=1, sticky="w")
sss_entry = tk.Entry(frame)
sss_entry.grid(row=4, column=2)

tk.Checkbutton(frame, variable=gsis_main_var, command=toggle_gsis_main).grid(row=5, column=0, sticky="e")
tk.Label(frame, text="GSIS No.").grid(row=5, column=1, sticky="w")
gsis_entry = tk.Entry(frame)
gsis_entry.grid(row=5, column=2)

tk.Checkbutton(frame, variable=uniformed_main_var, command=toggle_uniformed_main).grid(row=6, column=0, sticky="e")
tk.Label(frame, text="Uniformed Personnel").grid(row=6, column=1, sticky="w")
uniformed_entry = tk.Entry(frame)
uniformed_entry.grid(row=6, column=2)

# Frame for SSS Type (Employed/Self-employed) - radiobuttons
sss_type_frame = tk.Frame(frame)
tk.Radiobutton(sss_type_frame, text="Employed", variable=sss_type_var, value="employed").grid(row=0, column=0)
tk.Radiobutton(sss_type_frame, text="Self-employed", variable=sss_type_var, value="self-employed").grid(row=0, column=1)
sss_type_var.set("")  # Explicitly clear selection here
sss_type_frame.grid_remove()  # Hide initially

# Age, Sex
tk.Label(frame, text="Age").grid(row=7, column=0, sticky="w")
age_entry = tk.Entry(frame)
age_entry.grid(row=7, column=1)

tk.Label(frame, text="Sex").grid(row=7, column=2)
sex_var = tk.StringVar()
tk.Radiobutton(frame, text="Male", variable=sex_var, value="Male").grid(row=7, column=3)
tk.Radiobutton(frame, text="Female", variable=sex_var, value="Female").grid(row=7, column=4)
sex_var.set("")  # Clear selection explicitly

# Civil Status
tk.Label(frame, text="Civil Status").grid(row=8, column=0)
civil_status_var = tk.StringVar()
tk.Radiobutton(frame, text="Single", variable=civil_status_var, value="Single").grid(row=8, column=1)
tk.Radiobutton(frame, text="Married", variable=civil_status_var, value="Married").grid(row=8, column=2)
tk.Radiobutton(frame, text="Widow/er", variable=civil_status_var, value="Widow/er").grid(row=8, column=3)
tk.Radiobutton(frame, text="Separated", variable=civil_status_var, value="Separated").grid(row=8, column=4)
civil_status_var.set("")  # Clear selection explicitly

# DOB
tk.Label(frame, text="Date of Birth").grid(row=9, column=0, sticky="w")
dob_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                      year=date.today().year, month=date.today().month, day=date.today().day)
dob_entry.grid(row=9, column=1)

# Contact Info
tk.Label(frame, text="Landline No.").grid(row=10, column=0)
landline_entry = tk.Entry(frame)
landline_entry.grid(row=10, column=1)

tk.Label(frame, text="Mobile No.").grid(row=11, column=0)
mobile_entry = tk.Entry(frame)
mobile_entry.grid(row=11, column=1)

tk.Label(frame, text="Email Address").grid(row=12, column=0)
email_entry = tk.Entry(frame)
email_entry.grid(row=12, column=1)

# Address
tk.Label(frame, text="Current Address").grid(row=13, column=0)
curr_add_entry = tk.Text(frame, height=2, width=40)
curr_add_entry.grid(row=13, column=1, columnspan=3)

# New button to copy current address to permanent address
copy_button = tk.Button(frame, text="Same as Current", command=copy_current_to_permanent)
copy_button.grid(row=14, column=4, padx=5, sticky="w")

tk.Label(frame, text="Permanent Address").grid(row=14, column=0)
perm_add_entry = tk.Text(frame, height=2, width=40)
perm_add_entry.grid(row=14, column=1, columnspan=3)

# Next Button
tk.Button(frame, text="Next", command=submit_and_next).grid(row=15, column=3, pady=10)

root.mainloop()
