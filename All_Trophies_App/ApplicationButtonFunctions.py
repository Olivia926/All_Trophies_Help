import sys
sys.path.append(sys.path[0]+"\\..")
import globals
import AppGlobals
import tkinter as tk
from tkinter import END
from tkVideoPlayer import TkinterVideo
import threading
from pynput.mouse import Listener
from win32gui import WindowFromPoint, GetWindowText, GetWindowRect

window = AppGlobals.window
cur = AppGlobals.cur
game_name = AppGlobals.game_name
game_window = None

bonuses_frame = tk.Frame(window)
middle = tk.Frame(bonuses_frame)

trophies_frame = tk.Frame(window)
bonus_org_frame = tk.Frame(window)

booleans = [0, 0, 0]


def get_window_coords():
    """
    Gives the X and Y coordinates of the top left and bottom right of the window selected.

    :return: Two tuples in an array
    """
    return GetWindowRect(game_window)


def disable_children(widget):
    """
    Recursive function that disables every child widget within a widget.

    :param widget: App widget, such as a listbox, button, window, etc.
    :return: None
    """
    for child in widget.winfo_children():
        if isinstance(child, tk.Button) or isinstance(child, tk.Listbox):
            child.configure(state='disabled')
        if isinstance(child, tk.Frame):
            disable_children(child)


def enable_children(widget):
    """
    Recursive function that enables every child widget within a widget.

    :param widget: App widget, such as a listbox, button, window, etc.
    :return: None
    """
    for child in widget.winfo_children():
        if isinstance(child, tk.Button) or isinstance(child, tk.Listbox):
            child.configure(state='normal')
        if isinstance(child, tk.Frame):
            enable_children(child)


def hide_cur():
    """
    Uses the global variable 'cur' to close off the current frame.

    :return: None
    """
    global cur

    if cur == 0:
        bonuses_frame.pack_forget()
    elif cur == 1:
        trophies_frame.pack_forget()
    else:
        bonus_org_frame.pack_forget()


def open_bonuses():
    """
    Function that opens the bonuses frame and displays it to the user.

    :return: None
    """
    global cur
    global booleans

    def get_index(listbox, entry):
        """
        Find the index within the listbox for where it should place the current entry. This will also find the index
        in the bonuses array to be used for checking off that the bonus has been collected.

        :param listbox:
        :param entry:
        :return: array containing the index in the listbox to put the current value
                 and the index of the bonuses array, in that order.
        """
        bonuses = globals.bonuses
        index = 0

        for i in range(len(bonuses)):
            if entry == bonuses[i][0]:
                index = i
                break

        for i in range(listbox.size()):
            for j in range(len(bonuses)):
                if listbox.get(i) == bonuses[j][0]:
                    if j > index:
                        return i, index

        return END, index

    def move_all_bonuses():
        """
        Move every bonus from the middle listboxes to the collected and uncollected listboxes

        :return: None
        """
        while move_col.size() > 0:
            index, bonuses_index = get_index(uncollected, move_col.get(0))
            uncollected.insert(index, move_col.get(0))
            globals.bonuses[bonuses_index][1] = 0
            move_col.delete(0)

        while move_un.size() > 0:
            index, bonuses_index = get_index(collected, move_un.get(0))
            collected.insert(index, move_un.get(0))
            globals.bonuses[bonuses_index][1] = 1
            move_un.delete(0)

    def move_bonus_collected_back(event):
        """
        Move from the middle listbox to the collected listbox

        :return: None
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            move_col.delete(index)
            collected.insert(get_index(collected, data)[0], data)

    def move_bonus_collected(event):
        """
        Move from the collected listbox to the middle listbox

        :return: None
        """
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            collected.delete(index)
            move_col.insert(get_index(move_col, data)[0], data)

    def move_bonus_uncollected_back(event):
        """
        Move from the middle listbox to the uncollected listbox

        :return: None
        """

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            move_un.delete(index)
            uncollected.insert(get_index(uncollected, data)[0], data)

    def move_bonus_uncollected(event):
        """
        Move from the uncollected listbox to the middle listbox

        :return: None
        """

        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            uncollected.delete(index)
            move_un.insert(get_index(move_un, data)[0], data)

    def help_1():
        file = "../Images/First_Click.png"
        new_window = tk.Toplevel(window, width=200, height=750)
        frame = tk.Frame(new_window, width=200, height=750)
        frame.pack()
        new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
        text = tk.Text(frame, font={'Times New Roman', 20, 'bold'})
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
        text = tk.Text(frame, font={'Times New Roman', 20, 'bold'})
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
        label = tk.Label(frame, font={'Times New Roman', 20, 'bold'},
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

    def fill_listboxes():
        """
        Use the bonuses array to insert the bonuses into the collected and uncollected listboxes

        :return: None
        """
        for bonus, state in globals.bonuses:
            if state == 0:
                uncollected.insert(uncollected.size(), bonus)
            else:
                collected.insert(collected.size(), bonus)

    def clear_listboxes():
        """
        Delete every entry in the 2 middle, uncollected, and collected listboxes

        :return: None
        """
        move_un.delete(0, END)
        move_col.delete(0, END)
        collected.delete(0, END)
        uncollected.delete(0, END)

    def no_window_selected():
        """
        Give user dialogue that tells them that they need to select a window to use the program

        :return: None
        """
        new_window = tk.Toplevel(window, width=200, height=750)
        new_window.geometry(f"+{window.winfo_x() + 100}+{window.winfo_y() + 100}")
        tk.Label(new_window, font={'Times New Roman', 20, 'bold'},
                 text=f'You have not selected a window yet!\n'
                      f'Please select a window using the "Select Window" button').pack()

    def auto_complete():
        """
        Runs MyBonusChecker and disables user input to the main window

        :return: None
        """
        if game_window is None:
            no_window_selected()
            return

        clear_listboxes()
        disable_children(bonuses_frame)
        disable_children(window)
        run_bonus_checker()

    def run_bonus_checker():
        """
        Runs MyBonusChecker and gives user input to the application once it is done checking

        :return: None
        """
        from All_Trophies_Image_Recognition.MyBonusChecker import main

        label = tk.Label(auto_checker_frame, text="Checking Bonuses...")
        label.pack(side='top')
        check_bonuses_btn.config(state='disabled')
        t = threading.Thread(target=main)
        t.start()

        def auto_complete_2():
            enable_children(bonuses_frame)
            enable_children(window)
            fill_listboxes()
            open_bonuses()

        def check_if_done():
            if not t.is_alive():
                label.pack_forget()
                check_bonuses_btn.config(state='normal')
                auto_complete_2()
            else:
                schedule_check()

        def schedule_check():
            bonuses_frame.after(1000, check_if_done)

        schedule_check()

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

    if not booleans[0]:
        move_un = tk.Listbox(middle,
                             font=("Franklin_Gothic_Medium", 10, "bold"),
                             fg="#000000",
                             height=18,
                             selectmode=tk.SINGLE)

        move_col = tk.Listbox(middle,
                              font=("Franklin_Gothic_Medium", 10, "bold"),
                              fg="#000000",
                              height=18,
                              selectmode=tk.SINGLE)

        collected = tk.Listbox(bonuses_frame,
                               bg="#100817",
                               font=("Franklin_Gothic_Medium", 20, "bold"),
                               fg="#ffffff",
                               justify='right',
                               height=20,
                               selectmode=tk.SINGLE)

        uncollected = tk.Listbox(bonuses_frame,
                                 bg="#100817",
                                 font=("Franklin_Gothic_Medium", 20, "bold"),
                                 fg="#ffffff",
                                 justify='right',
                                 height=20,
                                 selectmode=tk.SINGLE)

        bonuses_frame.grid_columnconfigure(0, weight=1, uniform="bonuses")
        bonuses_frame.grid_columnconfigure(1, weight=2, uniform="bonuses")
        bonuses_frame.grid_columnconfigure(2, weight=2, uniform="bonuses")
        bonuses_frame.grid_columnconfigure(3, weight=2, uniform="bonuses")

        tk.Label(bonuses_frame,
                 text="Collected Bonuses",
                 font=("Franklin_Gothic_Medium", 20, "bold"),
                 fg="#000000").grid(row=0, column=1)
        tk.Label(bonuses_frame,
                 text="Remaining Bonuses",
                 font=("Franklin_Gothic_Medium", 20, "bold"),
                 fg="#000000").grid(row=0, column=3)

        collected.grid(row=1, column=1)
        uncollected.grid(row=1, column=3)

        fill_listboxes()

        collected.bind("<<ListboxSelect>>", move_bonus_collected)
        uncollected.bind("<<ListboxSelect>>", move_bonus_uncollected)
        move_un.bind("<<ListboxSelect>>", move_bonus_uncollected_back)
        move_col.bind("<<ListboxSelect>>", move_bonus_collected_back)

        move_un.pack(side="top")
        tk.Button(middle, text="MOVE", command=move_all_bonuses).pack(side="top")
        move_col.pack(side="top")

        auto_checker_frame = tk.Frame(bonuses_frame)
        check_bonuses_btn = tk.Button(auto_checker_frame, text="Use Auto Checker", command=auto_complete)

        winbtn = tk.Button(auto_checker_frame, text="Select Window", command=select_window)

        check_bonuses_btn.pack(side='bottom')
        winbtn.pack(side='bottom')

        middle.grid(row=1, column=2)
        auto_checker_frame.grid(row=1, column=0)
        tk.Button(bonuses_frame, text="Help", command=help_1).grid(row=0, column=0)

        booleans[0] = 1

    hide_cur()
    cur = 0

    bonuses_frame.pack()


def open_trophies():
    global cur

    if cur != 1:
        hide_cur()
        cur = 1


def adjust_bonuses():
    global cur

    if cur != 2:
        hide_cur()
        cur = 2
