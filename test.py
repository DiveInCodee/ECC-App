import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3
import os
from datetime import date

class ClientRegistrationForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("KAGABAY - Client Registration")
        self.geometry("850x680")
        self.resizable(False, False)

        # Photo
        self.photo_label = tk.Label(self, text="No Image", width=25, height=10, bg="gray")
        self.photo_label.pack(pady=10)
        self.upload_button = tk.Button(self, text="Upload Photo", command=self.upload_photo)
        self.upload_button.pack()

        # Personal Information
        tk.Label(self, text="First Name").pack()
        self.entry_fname = tk.Entry(self)
        self.entry_fname.pack()

        tk.Label(self, text="Last Name").pack()
        self.entry_lname = tk.Entry(self)
        self.entry_lname.pack()

        tk.Label(self, text="Age").pack()
        self.entry_age = tk.Entry(self)
        self.entry_age.pack()

        tk.Label(self, text="Contact Number").pack()
        self.entry_contact = tk.Entry(self)
        self.entry_contact.pack()

        tk.Label(self, text="Email Address").pack()
        self.entry_email = tk.Entry(self)
        self.entry_email.pack()

        # Work Status
        self.sss_var = tk.BooleanVar()
        self.gsis_var = tk.BooleanVar()
        self.uniformed_var = tk.BooleanVar()

        tk.Label(self, text="Work Status").pack()
        tk.Checkbutton(self, text="SSS", variable=self.sss_var).pack()
        tk.Checkbutton(self, text="GSIS", variable=self.gsis_var).pack()
        tk.Checkbutton(self, text="Uniformed Personnel", variable=self.uniformed_var).pack()

        # Sex and Civil Status
        self.sex = tk.StringVar(value="Male")
        self.civil_status = tk.StringVar(value="Single")

        tk.Label(self, text="Sex").pack()
        tk.Radiobutton(self, text="Male", variable=self.sex, value="Male").pack()
        tk.Radiobutton(self, text="Female", variable=self.sex, value="Female").pack()

        tk.Label(self, text="Civil Status").pack()
        tk.Radiobutton(self, text="Single", variable=self.civil_status, value="Single").pack()
        tk.Radiobutton(self, text="Married", variable=self.civil_status, value="Married").pack()
        tk.Radiobutton(self, text="Widowed", variable=self.civil_status, value="Widowed").pack()

        # Address
        tk.Label(self, text="Province").pack()
        self.entry_province = tk.Entry(self)
        self.entry_province.pack()

        tk.Label(self, text="Municipality").pack()
        self.entry_municipality = tk.Entry(self)
        self.entry_municipality.pack()

        tk.Label(self, text="Barangay").pack()
        self.entry_barangay = tk.Entry(self)
        self.entry_barangay.pack()

        tk.Label(self, text="Complete Address").pack()
        self.entry_address = tk.Entry(self, width=60)
        self.entry_address.pack()

        # Buttons
        tk.Button(self, text="Submit", command=self.submit_form, bg="#2ecc71", fg="white").pack(pady=10)
        tk.Button(self, text="Clear Form", command=self.clear_form, bg="#e74c3c", fg="white").pack(pady=5)

    def upload_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.photo_path = file_path
            image = Image.open(file_path)
            image = image.resize((150, 150))
            photo = ImageTk.PhotoImage(image)
            self.photo_label.config(image=photo, text="")
            self.photo_label.image = photo

    def submit_form(self):
        required_fields = [
            (self.entry_fname, "First Name"),
            (self.entry_lname, "Last Name"),
            (self.entry_age, "Age"),
            (self.entry_contact, "Contact Number"),
            (self.entry_email, "Email Address"),
            (self.entry_province, "Province"),
            (self.entry_municipality, "Municipality"),
            (self.entry_barangay, "Barangay"),
            (self.entry_address, "Complete Address"),
        ]

        for field, label in required_fields:
            if not field.get().strip():
                messagebox.showerror("Validation Error", f"{label} is required.")
                return

        # Collect values
        photo_path = getattr(self, 'photo_path', '')
        fname = self.entry_fname.get().strip()
        lname = self.entry_lname.get().strip()
        age = self.entry_age.get().strip()
        contact = self.entry_contact.get().strip()
        email = self.entry_email.get().strip()
        sss_status = self.sss_var.get()
        gsis_status = self.gsis_var.get()
        uniformed_status = self.uniformed_var.get()
        sex = self.sex.get()
        civil_status = self.civil_status.get()
        province = self.entry_province.get().strip()
        municipality = self.entry_municipality.get().strip()
        barangay = self.entry_barangay.get().strip()
        address = self.entry_address.get().strip()
        reg_date = date.today().strftime('%Y-%m-%d')

        try:
            conn = sqlite3.connect("client_info.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clients (
                    photo_path, fname, lname, age, contact, email, sss_status, 
                    gsis_status, uniformed_status, sex, civil_status, province, 
                    municipality, barangay, address, registration_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                photo_path, fname, lname, age, contact, email, sss_status, 
                gsis_status, uniformed_status, sex, civil_status, province, 
                municipality, barangay, address, reg_date
            ))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Client data submitted successfully!")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to insert data: {e}")

    def clear_form(self):
        self.entry_fname.delete(0, tk.END)
        self.entry_lname.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_contact.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)

        self.sss_var.set(False)
        self.gsis_var.set(False)
        self.uniformed_var.set(False)

        self.sex.set("Male")
        self.civil_status.set("Single")

        self.entry_province.delete(0, tk.END)
        self.entry_municipality.delete(0, tk.END)
        self.entry_barangay.delete(0, tk.END)
        self.entry_address.delete(0, tk.END)

        self.photo_label.config(image="", text="No Image", bg="gray")
        self.photo_path = None
