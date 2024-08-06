from tkinter import filedialog
from All_Trophies_App.FileHandling import write_file, open_file_work, reset_everything
import webbrowser
import globals

file_types = [("CSV File", '*.csv')]
working_file = None


def new_file():
    """
    Makes a completely new file and ditches the old file that was in use

    :return: None
    """
    global working_file
    # Check if working_file is not None and ask to save (or give user the option to turn it off)

    working_file = None

    bonuses = globals.bonuses
    trophies = globals.trophies

    for i in range(len(bonuses)):
        bonuses[i][1] = 0

    for i in range(len(trophies)):
        trophies[i][1] = 0

    reset_everything()


def open_file():
    """
    Handles opening files and updating the window with corresponding values

    :return: None
    """
    global working_file
    # Check if working file is not None and update happens

    file = filedialog.askopenfile(mode='r', filetypes=file_types)
    if file is None:
        return
    open_file_work(file)
    working_file = file
    working_file.close()


def save_file():
    """
    Handles saving a file. If the user is currently using a saved file, saving will overwrite the current save.
    If there is no current working file, it will call save_as_file

    :return: None
    """
    global working_file

    if working_file is None:
        save_as_file()
        return

    file = open(working_file.name, 'w')
    write_file(file)
    file.close()


def save_as_file():
    """
    Handles saving files and gives user the option to name the file

    :return: None
    """
    global working_file

    file = filedialog.asksaveasfile(filetypes=file_types, defaultextension=".csv", mode='w')
    if file is None:
        return
    file.truncate(0)
    write_file(file)
    working_file = file
    working_file.close()


def open_website(index):
    """
    Handles opening specific websites that contain help for the app

    :param: index: The index of the website to open
    :return: None
    """
    # Change index 2, 4, and 5
    sites = ['https://livesplit.org/', 'https://livesplit.org/', 'https://github.com/Toufool/AutoSplit',
             'https://github.com/Toufool/AutoSplit',
             'https://docs.google.com/document/d/1xoKp8pZ_PPzWJ52XBebdwQpNrNeyxVCF2tGYkv-46fA'
             '/edit?tab=t.0#heading=h.r0e6akhofv4z',
             'https://docs.google.com/spreadsheets/d/1MvoGhQ1brCmx77mHmrCyAZDHLvB1tL_gdrTXmNY8yv0/edit?usp=sharing',
             'https://docs.google.com/spreadsheets/d/1sbLJvkdcp-YIpyb6EfQaXQDEs3G2tmgBVz6w-iT_pjA/edit?usp=sharing',
             'https://www.speedrun.com/ssbm?h=All_Trophies-Console&x=02q3w7jk-ylp69ojn.9qjk9e31']

    webbrowser.open(sites[index])
