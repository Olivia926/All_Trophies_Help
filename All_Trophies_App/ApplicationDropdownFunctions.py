from tkinter import filedialog
from All_Trophies_App.FileHandling import write_file, open_file_work

file_types = [("CSV File", '*.csv')]
working_file = None


def open_file():
    global working_file
    file = filedialog.askopenfile(mode='r', filetypes=file_types)
    if file is None:
        return
    open_file_work(file)
    working_file = file
    working_file.close()


def save_as_file():
    global working_file

    file = filedialog.asksaveasfile(filetypes=file_types, defaultextension=".csv", mode='w')
    if file is None:
        return
    file.truncate(0)
    write_file(file)
    working_file = file
    working_file.close()


def save_file():
    if working_file is None:
        save_as_file()
        return

    file = open(working_file.name, 'w')
    write_file(file)
    file.close()