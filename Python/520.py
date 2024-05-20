import tkinter as tk
from tkinter import ttk

def create_table(rows):
    root = tk.Tk()
    root.title("带滑动条的表")

    tree = ttk.Treeview(root, columns=("col1", "col2", "col3", "col4"), show="headings")
    tree.column("col1", width=100, anchor="center")
    tree.column("col2", width=100, anchor="center")
    tree.column("col3", width=100, anchor="center")
    tree.column("col4", width=100, anchor="center")

    tree.heading("col1", text="列1")
    tree.heading("col2", text="列2")
    tree.heading("col3", text="列3")
    tree.heading("col4", text="列4")

    for i in range(rows):
        tree.insert("", "end", values=(f"行{i + 1}列1", f"行{i + 1}列2", f"行{i + 1}列3", f"行{i + 1}列4"))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(side="left", fill="both", expand=True)

    root.mainloop()

create_table(50)