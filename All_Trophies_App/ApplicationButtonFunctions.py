import globals
import AppGlobals
import tkinter as tk
import threading

window = AppGlobals.window
cur = AppGlobals.cur
game_window = AppGlobals.game_window

bonuses_frame = tk.Frame(window)

trophies_frame = tk.Frame(window)
bonus_org_frame = tk.Frame(window)

booleans = [0, 0, 0]


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

        return tk.END, index

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
        move_un.delete(0, tk.END)
        move_col.delete(0, tk.END)
        collected.delete(0, tk.END)
        uncollected.delete(0, tk.END)

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

    if not booleans[0]:
        middle = tk.Frame(bonuses_frame)

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

        left_frame = tk.Frame(bonuses_frame)
        right_frame = tk.Frame(bonuses_frame)

        tk.Label(left_frame,
                 text="Collected Bonuses",
                 font=("Franklin_Gothic_Medium", 20, "bold"),
                 fg="#000000").pack(side='top')
        tk.Label(right_frame,
                 text="Remaining Bonuses",
                 font=("Franklin_Gothic_Medium", 20, "bold"),
                 fg="#000000").pack(side='top')

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

        check_bonuses_btn.pack(side='bottom')

        middle.grid(row=1, column=2)
        auto_checker_frame.grid(row=1, column=0)

        left_frame.grid(row=0, column=1)
        right_frame.grid(row=0, column=3)

        booleans[0] = 1

    hide_cur()
    cur = 0

    bonuses_frame.pack()


def open_trophies():
    global cur

    hidden_left = []
    hidden_right = []

    r_buc = "All"
    l_buc = "All"

    def set_menus():
        tk.Label(left_frame,
                 text="Collected Trophies",
                 font=("Franklin_Gothic_Medium", 20, "bold"),
                 fg="#000000").pack(side='top')
        tk.Label(right_frame,
                 text="Remaining Trophies",
                 font=("Franklin_Gothic_Medium", 20, "bold"),
                 fg="#000000").pack(side='top')

        left_menu = tk.Menubutton(left_frame, text="Bucket", relief='raised')
        right_menu = tk.Menubutton(right_frame, text="Bucket", relief='raised')

        left_menu.menu = tk.Menu(left_menu, tearoff=0)
        left_menu["menu"] = left_menu.menu

        right_menu.menu = tk.Menu(right_menu, tearoff=0)
        right_menu["menu"] = right_menu.menu

        left_menu.menu.add_command(label='All', command=lambda: left_bucket("All"))
        left_menu.menu.add_command(label='Item', command=lambda: left_bucket("Item"))
        left_menu.menu.add_command(label='Container', command=lambda: left_bucket("Container"))
        left_menu.menu.add_command(label='Shell', command=lambda: left_bucket("Shell"))
        left_menu.menu.add_command(label='Paula BS', command=lambda: left_bucket("Paula BS"))
        left_menu.menu.add_command(label='Starzard', command=lambda: left_bucket("Starzard"))
        left_menu.menu.add_command(label='Cletrodema', command=lambda: left_bucket("Cletrodema"))
        left_menu.menu.add_command(label='Steelix', command=lambda: left_bucket("Steelix"))
        left_menu.menu.add_command(label='Wobbuffet', command=lambda: left_bucket("Wobbuffet"))
        left_menu.menu.add_command(label='Enemies', command=lambda: left_bucket("Enemies"))
        left_menu.menu.add_command(label='Wheels', command=lambda: left_bucket("Wheels"))
        left_menu.menu.add_command(label='Characters', command=lambda: left_bucket("Characters"))
        left_menu.menu.add_command(label='Zelda', command=lambda: left_bucket("Zelda"))
        left_menu.menu.add_command(label='Birdo', command=lambda: left_bucket("Birdo"))
        left_menu.menu.add_command(label='Giants', command=lambda: left_bucket("Giants"))
        left_menu.menu.add_command(label='Octorok', command=lambda: left_bucket("Octorok"))
        left_menu.menu.add_command(label='Sick', command=lambda: left_bucket("Sick"))
        left_menu.menu.add_command(label='Hats', command=lambda: left_bucket("Hats"))
        left_menu.menu.add_command(label='Villains', command=lambda: left_bucket("Villains"))
        left_menu.menu.add_command(label='Lotto', command=lambda: left_bucket("Lotto"))

        right_menu.menu.add_command(label='All', command=lambda: right_bucket("All"))
        right_menu.menu.add_command(label='Item', command=lambda: right_bucket("Item"))
        right_menu.menu.add_command(label='Container', command=lambda: right_bucket("Container"))
        right_menu.menu.add_command(label='Shell', command=lambda: right_bucket("Shell"))
        right_menu.menu.add_command(label='Paula BS', command=lambda: right_bucket("Paula BS"))
        right_menu.menu.add_command(label='Starzard', command=lambda: right_bucket("Starzard"))
        right_menu.menu.add_command(label='Cletrodema', command=lambda: right_bucket("Cletrodema"))
        right_menu.menu.add_command(label='Steelix', command=lambda: right_bucket("Steelix"))
        right_menu.menu.add_command(label='Wobbuffet', command=lambda: right_bucket("Wobbuffet"))
        right_menu.menu.add_command(label='Enemies', command=lambda: right_bucket("Enemies"))
        right_menu.menu.add_command(label='Wheels', command=lambda: right_bucket("Wheels"))
        right_menu.menu.add_command(label='Characters', command=lambda: right_bucket("Characters"))
        right_menu.menu.add_command(label='Zelda', command=lambda: right_bucket("Zelda"))
        right_menu.menu.add_command(label='Birdo', command=lambda: right_bucket("Birdo"))
        right_menu.menu.add_command(label='Giants', command=lambda: right_bucket("Giants"))
        right_menu.menu.add_command(label='Octorok', command=lambda: right_bucket("Octorok"))
        right_menu.menu.add_command(label='Sick', command=lambda: right_bucket("Sick"))
        right_menu.menu.add_command(label='Hats', command=lambda: right_bucket("Hats"))
        right_menu.menu.add_command(label='Villains', command=lambda: right_bucket("Villains"))
        right_menu.menu.add_command(label='Lotto', command=lambda: right_bucket("Lotto"))

        left_menu.pack(side='bottom')
        right_menu.pack(side='bottom')

    def fill_listboxes():
        """
        Use the trophies array to insert the trophies into the collected and uncollected listboxes

        :return: None
        """
        for trophy, state, thing, bucket in globals.trophies:
            if state == 0:
                uncollected.insert(uncollected.size(), trophy)
            else:
                collected.insert(collected.size(), trophy)

    def get_index(listbox, entry):
        """
        Find the index within the listbox for where it should place the current entry. This will also find the index
        in the trophies array to be used for checking off that the trophy has been collected.

        :param listbox:
        :param entry:
        :return: array containing the index in the listbox to put the current value
                 and the index of the trophies array, in that order.
        """
        trophies = globals.trophies
        index = 0

        for i in range(len(trophies)):
            if entry == trophies[i][0]:
                index = i
                break

        for i in range(listbox.size()):
            for j in range(len(trophies)):
                if listbox.get(i) == trophies[j][0]:
                    if j > index:
                        return i, index

        return tk.END, index

    def move_all_trophies():
        """
        Move every trophy from the middle listboxes to the collected and uncollected listboxes

        :return: None
        """
        trophies = globals.trophies
        nonlocal r_buc
        nonlocal l_buc

        while move_col.size() > 0:
            index, trophies_index = get_index(uncollected, move_col.get(0))
            if r_buc != "All":
                if move_col.get(0) == trophies[trophies_index][0]:
                    if r_buc == trophies[trophies_index][3]:
                        uncollected.insert(index, move_col.get(0))
                    else:
                        hidden_right.append(trophies[trophies_index][0])
            else:
                uncollected.insert(index, move_col.get(0))
            trophies[trophies_index][1] = 0
            move_col.delete(0)

        while move_un.size() > 0:
            index, trophies_index = get_index(collected, move_un.get(0))
            if l_buc != "All":
                if move_un.get(0) == trophies[trophies_index][0]:
                    if l_buc == trophies[trophies_index][3]:
                        collected.insert(index, move_un.get(0))
                    else:
                        hidden_left.append(trophies[trophies_index][0])
            else:
                collected.insert(index, move_un.get(0))
            trophies[trophies_index][1] = 1
            move_un.delete(0)

    def move_left_trophies():
        while len(hidden_left) > 0:
            index, _ = get_index(collected, hidden_left[len(hidden_left) - 1])
            collected.insert(index, hidden_left.pop())

    def left_bucket(bucket):
        trophies = globals.trophies
        nonlocal l_buc

        l_buc = bucket
        move_left_trophies()
        if bucket != 'All':
            for trophy, state, _, b in trophies:
                if state == 1 and b != bucket:
                    i = collected.get(0, tk.END).index(trophy)
                    hidden_left.append(collected.get(i))
                    collected.delete(i)

    def move_right_trophies():
        while len(hidden_right) > 0:
            index, _ = get_index(uncollected, hidden_right[len(hidden_right) - 1])
            uncollected.insert(index, hidden_right.pop())

    def right_bucket(bucket):
        trophies = globals.trophies
        nonlocal r_buc

        r_buc = bucket
        move_right_trophies()
        if bucket != 'All':
            for trophy, state, _, b in trophies:
                if state == 0 and b != bucket:
                    i = uncollected.get(0, tk.END).index(trophy)
                    hidden_right.append(uncollected.get(i))
                    uncollected.delete(i)

    def move_trophy_collected_back(event):
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

    def move_trophy_collected(event):
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

    def move_trophy_uncollected_back(event):
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

    def move_trophy_uncollected(event):
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

    def clear_listboxes():
        """
        Delete every entry in the 2 middle, uncollected, and collected listboxes

        :return: None
        """
        move_un.delete(0, tk.END)
        move_col.delete(0, tk.END)
        collected.delete(0, tk.END)
        uncollected.delete(0, tk.END)

    def run_trophy_checker():
        """
        Runs MyTrophyChecker and gives user input to the application once it is done checking

        :return: None
        """
        from All_Trophies_Image_Recognition.MyTrophyChecker import main

        label = tk.Label(auto_checker_frame, text="Checking Trophies...")
        label.pack(side='top')
        check_trophies_btn.config(state='disabled')
        t = threading.Thread(target=main)
        t.start()

        def auto_complete_2():
            enable_children(trophies_frame)
            enable_children(window)
            fill_listboxes()
            open_trophies()

        def check_if_done():
            if not t.is_alive():
                label.pack_forget()
                check_trophies_btn.config(state='normal')
                auto_complete_2()
            else:
                schedule_check()

        def schedule_check():
            trophies_frame.after(1000, check_if_done)

        schedule_check()

    def auto_complete():
        """
        Runs MyTrophyChecker and disables user input to the main window

        :return: None
        """
        if game_window is None:
            no_window_selected()
            return

        clear_listboxes()
        disable_children(trophies_frame)
        disable_children(window)
        run_trophy_checker()

    if not booleans[1]:
        bg = "#7a7a7a"
        fg = "#fdfdfd"

        middle = tk.Frame(trophies_frame)

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

        collected = tk.Listbox(trophies_frame,
                               bg=bg,
                               font=("Franklin_Gothic_Medium", 20, "bold"),
                               fg=fg,
                               justify='left',
                               height=20,
                               selectmode=tk.SINGLE)

        uncollected = tk.Listbox(trophies_frame,
                                 bg=bg,
                                 font=("Franklin_Gothic_Medium", 20, "bold"),
                                 fg=fg,
                                 justify='left',
                                 height=20,
                                 selectmode=tk.SINGLE)

        trophies_frame.grid_columnconfigure(0, weight=1, uniform="trophies")
        trophies_frame.grid_columnconfigure(1, weight=2, uniform="trophies")
        trophies_frame.grid_columnconfigure(2, weight=2, uniform="trophies")
        trophies_frame.grid_columnconfigure(3, weight=2, uniform="trophies")

        left_frame = tk.Frame(trophies_frame)
        right_frame = tk.Frame(trophies_frame)

        set_menus()

        collected.grid(row=1, column=1)
        uncollected.grid(row=1, column=3)

        fill_listboxes()

        collected.bind("<<ListboxSelect>>", move_trophy_collected)
        uncollected.bind("<<ListboxSelect>>", move_trophy_uncollected)
        move_un.bind("<<ListboxSelect>>", move_trophy_uncollected_back)
        move_col.bind("<<ListboxSelect>>", move_trophy_collected_back)

        move_un.pack(side="top")
        tk.Button(middle, text="MOVE", command=move_all_trophies).pack(side="top")
        move_col.pack(side="top")

        auto_checker_frame = tk.Frame(trophies_frame)
        birdobtn = tk.Button(auto_checker_frame, text="Birdo RNG Manip")
        advbtn = tk.Button(auto_checker_frame, text="Adventure 1-1 RNG Manip")
        check_trophies_btn = tk.Button(auto_checker_frame, text="Auto Check Trophies", command=auto_complete)

        birdobtn.pack(side='top')
        advbtn.pack(side='top')
        check_trophies_btn.pack(side='top')

        middle.grid(row=1, column=2)
        auto_checker_frame.grid(row=1, column=0)

        left_frame.grid(row=0, column=1)
        right_frame.grid(row=0, column=3)

        booleans[1] = 1

    hide_cur()
    cur = 1

    trophies_frame.pack()


def adjust_bonuses():
    global cur

    if cur != 2:
        hide_cur()
        cur = 2
