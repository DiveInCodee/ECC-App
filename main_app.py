# main_app.py

import tkinter as tk
from tkinter import messagebox
from page1 import Page1
from page2 import Page2

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ECC Application System")
        self.geometry("1000x700")
        self.configure(bg="white")

        # Top Menu Frame
        top_frame = tk.Frame(self, bg="lightgray", height=50)
        top_frame.pack(side="top", fill="x")

        tk.Button(top_frame, text="Search", command=self.search_record).pack(side="left", padx=10, pady=10)
        tk.Button(top_frame, text="Add", command=self.add_record).pack(side="left", padx=10, pady=10)
        tk.Button(top_frame, text="Delete", command=self.delete_record).pack(side="left", padx=10, pady=10)
        tk.Button(top_frame, text="Print", command=self.print_record).pack(side="left", padx=10, pady=10)

        # Navigation Panel on the Left
        nav_frame = tk.Frame(self, bg="#f0f0f0", width=200)
        nav_frame.pack(side="left", fill="y")

        tk.Button(nav_frame, text="Page 1\n(Client Profile)", height=3, command=lambda: self.show_page("Page1")).pack(fill="x", pady=5, padx=5)
        tk.Button(nav_frame, text="Page 2\n(Work Profile)", height=3, command=lambda: self.show_page("Page2")).pack(fill="x", pady=5, padx=5)

        # Page Container
        self.page_container = tk.Frame(self, bg="white")
        self.page_container.pack(side="right", fill="both", expand=True)

        # Ensure container stretches
        self.page_container.grid_rowconfigure(0, weight=1)
        self.page_container.grid_columnconfigure(0, weight=1)

        # Initialize Pages
        self.pages = {}
        for PageClass in (Page1, Page2):
            page_name = PageClass.__name__
            frame = PageClass(self.page_container, self)
            self.pages[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_page("Page1")  # Start with Page1

    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()

    def search_record(self):
        messagebox.showinfo("Search", "Search functionality coming soon.")

    def add_record(self):
        messagebox.showinfo("Add", "Add functionality coming soon.")

    def delete_record(self):
        messagebox.showinfo("Delete", "Delete functionality coming soon.")

    def print_record(self):
        messagebox.showinfo("Print", "Print functionality coming soon.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
