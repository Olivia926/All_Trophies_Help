import tkinter as tk
from tkinter import filedialog

file_types = [("Text Document", '*.txt'),
              ('JSON Files', '*.JSON')]


def open_file():
    tk.Tk().withdraw()
    folder_path = filedialog.askopenfile(mode='r', filetypes=file_types)


def save_as_file():
    tk.Tk().withdraw()
    file = filedialog.asksaveasfilename(filetypes=file_types, defaultextension=".txt")

"""
def new_file():
    
    
    
def save_file():
"""