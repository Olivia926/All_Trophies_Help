import All_Trophies_App.ApplicationDropdownFunctions as adf
import All_Trophies_App.ApplicationButtonFunctions as abf
import tkinter as tk
import globals

window = globals.window


def do_thing():
    """Temporary thing that will be deleted"""
    print(f"Hi")


def open_cur():
    """
    Opens the frame tied to the number of cur

    :return: None
    """
    cur = globals.cur

    if cur == 0:
        abf.open_bonuses()
    elif cur == 1:
        abf.open_trophies()


def create_frames():
    """
    Creates the top buttons for the main application window

    :return: None
    """

    font = ["Impact", 15, "bold"]
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

    frame.pack()


def create_menus():
    """
    Creates the top left menus for saving, opening, and making files as well as other helpful functions

    :return: None
    """
    menu = tk.Menu(window)
    file_menu = tk.Menu(menu, tearoff=0)
    resources_menu = tk.Menu(window, tearoff=0)
    help_menu = tk.Menu(menu, tearoff=0)

    window.config(menu=menu)
    menu.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=adf.new_file)
    file_menu.add_command(label="Open", command=adf.open_file)
    file_menu.add_command(label="Save", command=adf.save_file)
    file_menu.add_command(label="Save As", command=adf.save_as_file)

    menu.add_cascade(label="Resources", menu=resources_menu)
    resources_menu.add_command(label="Livesplit", command=lambda *args: adf.open_website(0))
    resources_menu.add_command(label="Livesplit Accessories and Tips", command=lambda *args: adf.open_website(1))
    resources_menu.add_command(label="Autosplit", command=lambda *args: adf.open_website(2))
    resources_menu.add_command(label="Autosplit Accessories and Tips", command=lambda *args: adf.open_website(3))
    resources_menu.add_command(label="Run Document", command=lambda *args: adf.open_website(4))
    resources_menu.add_command(label="Speedster Excel Sheet", command=lambda *args: adf.open_website(5))
    resources_menu.add_command(label="Bonuses Excel Sheet", command=lambda *args: adf.open_website(6))
    resources_menu.add_command(label="Leaderboard", command=lambda *args: adf.open_website(7))

    menu.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=do_thing)
    help_menu.add_command(label="View Updates", command=do_thing)
    help_menu.add_command(label="Contact Information", command=do_thing)


def create_window():
    """
    Creates the Application window

    :return: None
    """
    window.title("All Trophies Helper")
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    window.geometry("%dx%d" % (width, height))
    window.protocol("WM_DELETE_WINDOW", lambda: close_window())

    def close_window():
        """
        Handles closing the main window

        :return: None
        """
        destroy = True

        def save(win):
            """
            Handles the save button

            :param: win: toplevel window
            :return: None
            """
            adf.save_file()
            win.destroy()

        def exit_window(win):
            """
            Handles hitting the exit without saving button

            :param: win: toplevel window
            :return: None
            """
            win.destroy()

        def cancel(win):
            """
            Handles the cancel button and user closing the window

            :param: win: toplevel window
            :return: None
            """
            nonlocal destroy

            destroy = False
            win.destroy()

        if globals.updated:
            new_window = tk.Toplevel(window)
            new_window.grab_set()
            new_window.title("Record")
            new_window.geometry('400x100')

            new_window.protocol("WM_DELETE_WINDOW", lambda *args: cancel(new_window))

            globals.center(new_window)

            tk.Label(new_window, font={'Times New Roman', 20, 'bold'},
                     text=f"Do you want to save before you exit?").pack(side='top')
            btn_frame = tk.Frame(new_window)
            btn_frame.pack(side='top')
            tk.Button(btn_frame, text="save", command=lambda *args: save(new_window)).grid(row=0, column=0, padx=10)
            tk.Button(btn_frame, text="exit without saving",
                      command=lambda *args: exit_window(new_window)).grid(row=0, column=1, padx=10)
            tk.Button(btn_frame, text="cancel", command=lambda *args: cancel(new_window)).grid(row=0, column=2, padx=10)

            new_window.wait_window()

        if destroy:
            window.destroy()


def main():
    create_window()
    create_menus()
    create_frames()
    open_cur()
    window.mainloop()


if __name__ == "__main__":
    main()
