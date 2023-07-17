import globals
import AppGlobals
import tkinter as tk
from tkinter import END
from tkVideoPlayer import TkinterVideo
import threading
from pyautogui import getAllWindows
from pynput.mouse import Listener
from win32gui import WindowFromPoint, GetWindowText

window = AppGlobals.window
cur = AppGlobals.cur
game_window = globals.game_window

bonuses_frame = tk.Frame(window)
middle = tk.Frame(bonuses_frame)

trophies_frame = tk.Frame(window)
bonus_org_frame = tk.Frame(window)

booleans = [0, 0, 0]


def disable_children(widget):
    for child in widget.winfo_children():
        if isinstance(child, tk.Button) or isinstance(child, tk.Listbox):
            child.configure(state='disabled')
        if isinstance(child, tk.Frame):
            disable_children(child)


def enable_children(widget):
    for child in widget.winfo_children():
        if isinstance(child, tk.Button) or isinstance(child, tk.Listbox):
            child.configure(state='normal')
        if isinstance(child, tk.Frame):
            enable_children(child)


def hide_cur():
    if cur == 0:
        bonuses_frame.pack_forget()
    elif cur == 1:
        trophies_frame.pack_forget()
    else:
        bonus_org_frame.pack_forget()


def open_bonuses():
    global cur
    global sel_window

    def get_index(listbox, entry):
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
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            move_col.delete(index)
            collected.insert(get_index(collected, data)[0], data)

    def move_bonus_collected(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            collected.delete(index)
            move_col.insert(get_index(move_col, data)[0], data)

    def move_bonus_uncollected_back(event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            move_un.delete(index)
            uncollected.insert(get_index(uncollected, data)[0], data)

    def move_bonus_uncollected(event):
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
        for bonus, state in globals.bonuses:
            if state == 0:
                uncollected.insert(uncollected.size(), bonus)
            else:
                collected.insert(collected.size(), bonus)

    def clear_listboxes():
        move_un.delete(0, END)
        move_col.delete(0, END)
        collected.delete(0, END)
        uncollected.delete(0, END)

    def auto_complete():
        clear_listboxes()
        disable_children(bonuses_frame)
        disable_children(window)
        run_bonus_checker()

    def run_bonus_checker():
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
        global game_window

        if pressed:
            game_window = WindowFromPoint((x, y))

        return False

    def select_window():
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

        winbtn = tk.Button(auto_checker_frame, text="Window not selected yet!", command=select_window)

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
