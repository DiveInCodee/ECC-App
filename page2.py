import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
import sqlite3

# Connect to database
conn = sqlite3.connect("client_info.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS work_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employment_type TEXT,
    employer_name TEXT,
    nature_of_work TEXT,
    monthly_income REAL,
    with_disability INTEGER,
    solo_parent INTEGER,
    senior_citizen INTEGER,
    indigenous INTEGER,
    other_status TEXT,
    interested_skills_training INTEGER,
    interested_education INTEGER,
    interested_financial INTEGER,
    interested_medical INTEGER,
    other_program TEXT,
    signature_name TEXT,
    signature_date TEXT
)
""")
conn.commit()

# GUI
root = tk.Tk()
root.title("KAGABAY - Page 2: Work Profile")
root.geometry("800x700")

# Employment Type
tk.Label(root, text="Employment Type").grid(row=0, column=0, sticky="w")
employment_var = tk.StringVar()
employment_choices = ["Government", "Private", "Self-employed", "None"]
employment_menu = ttk.Combobox(root, textvariable=employment_var, values=employment_choices, state="readonly")
employment_menu.grid(row=0, column=1)

# Employer or Business Name
tk.Label(root, text="Employer/Business Name").grid(row=1, column=0, sticky="w")
employer_entry = tk.Entry(root, width=50)
employer_entry.grid(row=1, column=1)

# Nature of Work
tk.Label(root, text="Nature of Work").grid(row=2, column=0, sticky="w")
nature_entry = tk.Entry(root, width=50)
nature_entry.grid(row=2, column=1)

# Monthly Income
tk.Label(root, text="Monthly Income").grid(row=3, column=0, sticky="w")
income_entry = tk.Entry(root)
income_entry.grid(row=3, column=1)

# Current Status
tk.Label(root, text="Current Status").grid(row=4, column=0, sticky="w")
with_disability_var = tk.IntVar()
solo_parent_var = tk.IntVar()
senior_citizen_var = tk.IntVar()
indigenous_var = tk.IntVar()
other_status_var = tk.StringVar()

tk.Checkbutton(root, text="With Disability", variable=with_disability_var).grid(row=5, column=0, sticky="w")
tk.Checkbutton(root, text="Solo Parent", variable=solo_parent_var).grid(row=5, column=1, sticky="w")
tk.Checkbutton(root, text="Senior Citizen", variable=senior_citizen_var).grid(row=6, column=0, sticky="w")
tk.Checkbutton(root, text="Indigenous", variable=indigenous_var).grid(row=6, column=1, sticky="w")

tk.Label(root, text="Others (Specify)").grid(row=7, column=0, sticky="w")
other_status_entry = tk.Entry(root, textvariable=other_status_var, width=40)
other_status_entry.grid(row=7, column=1)

# KAGABAY Programs Interested
tk.Label(root, text="KAGABAY Program Interested In").grid(row=8, column=0, sticky="w")
skills_var = tk.IntVar()
education_var = tk.IntVar()
financial_var = tk.IntVar()
medical_var = tk.IntVar()
other_program_var = tk.StringVar()

tk.Checkbutton(root, text="Skills Training", variable=skills_var).grid(row=9, column=0, sticky="w")
tk.Checkbutton(root, text="Educational Assistance", variable=education_var).grid(row=9, column=1, sticky="w")
tk.Checkbutton(root, text="Financial Assistance", variable=financial_var).grid(row=10, column=0, sticky="w")
tk.Checkbutton(root, text="Medical Assistance", variable=medical_var).grid(row=10, column=1, sticky="w")

tk.Label(root, text="Others (Specify)").grid(row=11, column=0, sticky="w")
other_program_entry = tk.Entry(root, textvariable=other_program_var, width=40)
other_program_entry.grid(row=11, column=1)

# Signature and Date
tk.Label(root, text="Signature (Name)").grid(row=12, column=0, sticky="w")
signature_entry = tk.Entry(root, width=40)
signature_entry.grid(row=12, column=1)

tk.Label(root, text="Date").grid(row=13, column=0, sticky="w")
signature_date = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
signature_date.grid(row=13, column=1)

# Submit Button
def submit_page2():
    data = (
        employment_var.get(),
        employer_entry.get(),
        nature_entry.get(),
        income_entry.get(),
        with_disability_var.get(),
        solo_parent_var.get(),
        senior_citizen_var.get(),
        indigenous_var.get(),
        other_status_var.get(),
        skills_var.get(),
        education_var.get(),
        financial_var.get(),
        medical_var.get(),
        other_program_var.get(),
        signature_entry.get(),
        signature_date.get_date().isoformat()
    )

    c.execute("""
        INSERT INTO work_profile (
            employment_type, employer_name, nature_of_work, monthly_income,
            with_disability, solo_parent, senior_citizen, indigenous, other_status,
            interested_skills_training, interested_education, interested_financial,
            interested_medical, other_program, signature_name, signature_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    messagebox.showinfo("Success", "Work profile saved successfully.")
    root.destroy()

tk.Button(root, text="Submit", command=submit_page2, bg="lightblue").grid(row=14, column=1, pady=20)

root.mainloop()
