import ApplicationDropdownFunctions as adf
import ApplicationButtonFunctions as abf
import tkinter as tk
from tkinter import END
import AppGlobals
from tkVideoPlayer import TkinterVideo
from pynput.mouse import Listener
from win32gui import WindowFromPoint, GetWindowText, GetWindowRect

window = AppGlobals.window
game_name = AppGlobals.game_name
game_window = AppGlobals.game_window


def do_thing():
    """Temporary thing that will be deleted"""
    print(f"Hi")


def get_window_coords():
    """
    Gives the X and Y coordinates of the top left and bottom right of the window selected.

    :return: Two tuples in an array
    """
    return GetWindowRect(game_window)


def on_click(x, y, button, pressed):
    """
    Allows the user to select a window and takes HWND of the window

    :return: False when the user clicks
    """
    global game_window
    global game_name

    if pressed:
        game_window = WindowFromPoint((x, y))
        game_name = GetWindowText(game_window)

    return False


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

    font = ["Impact", 15, "bold"]
    bg = "#010101"
    fg = "#d19a48"
    ab = "#fae400"
    af = "#0a0201"

    def select_window():
        """
        Allows the user to select the window they want to find bonuses on. Will display the name of the window to the
        application.

        :return: None
        """
        global game_window

        game_window = None

        while game_window is None:
            with Listener(on_click=on_click) as listener:
                listener.join()

        if game_window is not None:
            if len(GetWindowText(game_window)) > 25:
                winbtn.config(text=("%.25s..." % GetWindowText(game_window)))
            else:
                winbtn.config(text=f"{GetWindowText(game_window)}")

    frame = tk.Frame(window)
    tk.Button(frame, text="Help", command=help_1).pack(side='left')
    winbtn = tk.Button(frame, text="Select Window", command=select_window)

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

    winbtn.pack(side='left')

    frame.pack()


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


def help_1():
    file = "../Images/First_Click.png"
    new_window = tk.Toplevel(window, width=200, height=750)
    frame = tk.Frame(new_window, width=200, height=750)
    frame.pack()
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    text = tk.Text(frame, font=['Times New Roman', 15])
    text.pack()
    text.insert(END, f"Click on the top left of the bonuses section to start\n")
    text.insert(END, f"(See reference image below)\n")
    photo = tk.PhotoImage(file=file)
    text.image_create(END, image=photo)
    text.image = photo

    def exit_btn():
        new_window.destroy()
        help_2()

    tk.Button(frame, text="Next", command=exit_btn).pack(side='right')


def help_2():
    file = "../Images/Second_Click.png"
    new_window = tk.Toplevel(window, width=200, height=750)
    frame = tk.Frame(new_window, width=200, height=750)
    frame.pack()
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    text = tk.Text(frame, font=['Times New Roman', 15])
    text.pack()
    text.insert(END, f"Click on the bottom right of the bonuses section\n")
    photo = tk.PhotoImage(file=file)
    text.image_create(END, image=photo)
    text.image = photo

    def exit_btn():
        new_window.destroy()
        help_3()

    tk.Button(frame, text="Next", command=exit_btn).pack(side='right')


def help_3():
    new_window = tk.Toplevel(window, width=200, height=750)
    frame = tk.Frame(new_window)
    frame.pack()
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    label = tk.Label(frame, font=['Times New Roman', 15, 'bold'],
                     text=f"Scroll the screen down quickly using the control stick\n")
    label.pack()
    video = TkinterVideo(frame)
    video.load(r"../Images/Scroll_Help.mp4")
    video.pack(expand=True)
    video.play()

    def load(event):
        video.config(width=193, height=336)

    def loop(event):
        video.play()

    def exit_btn():
        new_window.destroy()
        help_4()

    video.bind("<<Loaded>>", load)
    video.bind('<<Ended>>', loop)

    tk.Button(frame, text="Next", command=exit_btn).pack(side='right')


def help_4():
    new_window = tk.Toplevel(window, width=200, height=750)
    frame = tk.Frame(new_window)
    frame.pack()
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    label = tk.Label(frame, font={'Times New Roman', 20, 'bold'},
                     text=f"When it reaches the bottom, wait for a little bit!\n")
    label.pack()
    video = TkinterVideo(frame)
    video.load(r"../Images/End_Scroll.mp4")
    video.pack(expand=True)
    video.play()

    def load(event):
        video.config(width=193, height=336)

    def loop(event):
        video.play()

    def exit_btn():
        new_window.destroy()
        help_5()

    video.bind("<<Loaded>>", load)
    video.bind('<<Ended>>', loop)

    tk.Button(frame, text="Next", command=exit_btn).pack(side='right')


def help_5():
    new_window = tk.Toplevel(window, width=200, height=750)
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    tk.Label(new_window, font={'Times New Roman', 20, 'bold'},
             text=f"Press 'q' to stop the program from recording!").pack()

    def exit_btn():
        new_window.destroy()
        help_6()

    tk.Button(new_window, text="Next", command=exit_btn).pack(side='right')


def help_6():
    new_window = tk.Toplevel(window, width=200, height=750)
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    tk.Label(new_window, font={'Times New Roman', 20, 'bold'},
             text=f"Something will happen on screen prompting you to wait").pack()

    tk.Label(new_window, font={'Times New Roman', 20, 'bold'},
             text=f"(Placeholder for thing)").pack()

    def exit_btn():
        new_window.destroy()
        help_7()

    tk.Button(new_window, text="Next", command=exit_btn).pack(side='right')


def help_7():
    file = "../Images/Final_Helper.PNG"
    new_window = tk.Toplevel(window, width=200, height=750)
    frame = tk.Frame(new_window, width=200, height=750)
    frame.pack()
    new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
    text = tk.Text(frame, font={'Times New Roman', 20, 'bold'})
    text.pack()
    text.insert(END, f"The bonuses will add based on what you have!\n")
    photo = tk.PhotoImage(file=file)
    photo = photo.subsample(2, 2)
    text.image_create(END, image=photo)
    text.image = photo

    def exit_btn():
        new_window.destroy()

    tk.Button(frame, text="Next", command=exit_btn).pack(side='right')


def main():
    create_window()
    create_menus()
    create_frames()
    open_cur()
    window.mainloop()


if __name__ == "__main__":
    main()
