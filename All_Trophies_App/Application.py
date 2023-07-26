import ApplicationDropdownFunctions as adf
import ApplicationButtonFunctions as abf
import tkinter as tk
import AppGlobals

window = AppGlobals.window


def do_thing():
    """Temporary thing that will be deleted"""
    print(f"HIHIHIHIHIHIHI")


def open_cur():
    """
    Opens the frame tied to the number of cur

    :return: None
    """
    cur = AppGlobals.cur

    if cur == 0:
        abf.open_bonuses()
    elif cur == 1:
        abf.open_trophies()
    else:
        abf.adjust_bonuses()


def create_frames():
    """
    Creates the top buttons for the main application window

    :return: None
    """
    font = {"Impact", 100, "bold"}
    bg = "#010101"
    fg = "#d19a48"
    ab = "#fae400"
    af = "#0a0201"

    frame = tk.Frame(window)
    bonuses_btn = tk.Button(frame, text="Bonuses", font=font, padx=20,
                            command=abf.open_bonuses, bg=bg, fg=fg,
                            activebackground=ab, activeforeground=af)
    bonuses_btn.pack(side='left')

    trophies_btn = tk.Button(frame, text="Trophies", font=font, padx=20,
                             command=abf.open_trophies, bg=bg, fg=fg,
                             activebackground=ab, activeforeground=af)
    trophies_btn.pack(side='left')

    bonuses_sort = tk.Button(frame, text="Organize Bonuses", font=font, padx=20,
                             command=abf.adjust_bonuses, bg=bg, fg=fg,
                             activebackground=ab, activeforeground=af)
    bonuses_sort.pack(side='left')

    frame.pack()

    tk.Frame(window, height=20).pack()


def create_menus():
    """
    Creates the top left menus for saving, opening, and making files as well as other helpful functions

    :return: None
    """
    menu = tk.Menu(window)
    file_menu = tk.Menu(menu, tearoff=0)

    window.config(menu=menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=do_thing)
    file_menu.add_command(label="Open", command=adf.open_file)
    file_menu.add_command(label="Save", command=do_thing)
    file_menu.add_command(label="Save As", command=adf.save_as_file)

    help_menu = tk.Menu(menu)
    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="View Help", command=do_thing)
    help_menu.add_command(label="About", command=do_thing)
    help_menu.add_command(label="Check for Updates", command=do_thing)


def create_window():
    """
    Creates the Application window

    :return: None
    """
    window.title("All Trophies Helper")
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))


def main():
    create_window()
    create_menus()
    create_frames()
    open_cur()
    window.mainloop()


if __name__ == "__main__":
    main()
