"""
tkinter_test.py
Tkinter basics samjhne ke liye — yeh production code nahi hai.
"""

import tkinter as tk
from tkinter import ttk


def on_button_click():
    """Button click hone par yeh chalega."""
    name = name_entry.get()
    if not name:
        status_label.config(text="⚠️  Naam daal pehle", foreground="red")
        return
    status_label.config(text=f"✅ Hello, {name}!", foreground="green")
    print(f"Button clicked. Naam: {name}")


def on_dropdown_change(event):
    """Dropdown selection change hone par chalega."""
    selected = dropdown.get()
    print(f"Selected: {selected}")
    status_label.config(text=f"Selected: {selected}", foreground="blue")


# === Main window banana ===
root = tk.Tk()
root.title("Tkinter Test")
root.geometry("400x300")  # width x height

# === Label (text dikhane ke liye) ===
title_label = tk.Label(root, text="Tkinter Test Window", font=("Arial", 16, "bold"))
title_label.pack(pady=10)  # pady = vertical padding

# === Entry (text input) ===
tk.Label(root, text="Tera naam:").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# === Dropdown (Combobox) ===
tk.Label(root, text="Favorite color:").pack()
dropdown = ttk.Combobox(root, values=["Red", "Blue", "Green", "Orange"], state="readonly")
dropdown.pack(pady=5)
dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

# === Button ===
submit_btn = tk.Button(root, text="Submit", command=on_button_click, bg="#4CAF50", fg="white")
submit_btn.pack(pady=10)

# === Status label (output dikhane ke liye) ===
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

# === Main event loop start ===
root.mainloop()