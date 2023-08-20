import globals
import AppGlobals
import tkinter as tk
import threading
from PIL import Image, ImageTk

window = AppGlobals.window
cur = AppGlobals.cur
game_window = AppGlobals.game_window

bonuses_frame = tk.Frame(window)

trophies_frame = tk.Frame(window)
bonus_org_frame = tk.Frame(window)

booleans = [0, 0, 0]


def fin_adv():
    new_window = tk.Toplevel(window)
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))
    new_window.geometry(f"{int(window.winfo_width() * 3 / 5)}x{int(window.winfo_height() * 5 / 9)}")
    center(new_window)

    def on_closing(win):
        new_window.destroy()

    def submit():
        new_window.destroy()

    frame = tk.Frame(new_window)

    tk.Label(frame, text="You collected every trophy!\n\n",
             font=['Times New Roman', 15, 'bold'], justify='center').pack(side='top')


    tk.Button(frame, text="Exit", command=submit).pack(side='bottom')

    frame.pack()

    new_window.wait_window()


def display_adv(tags, trophy, goomba_trophies):
    trophies = globals.trophies
    file = "../Images/Image_Atlas.png"
    photo = Image.open(file)
    confirmed = [0]
    close = False

    def change_state(ind, txt):
        nonlocal confirmed

        if confirmed[ind]:
            confirmed[ind] = 0
            txt.config(background='white')
        else:
            confirmed[ind] = 1
            txt.config(background='green')

    def submit():
        new_window.destroy()

    def on_closing(win):
        nonlocal close

        close = True
        win.destroy()

    new_window = tk.Toplevel(window)
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))
    new_window.geometry(f"{int(window.winfo_width() * 3 / 5)}x{int(window.winfo_height() * 5 / 9)}")
    center(new_window)

    text_frame = tk.Frame(new_window)
    trophy_frame = tk.Frame(new_window)

    tk.Label(text_frame, text="Click on trophies you collected! If the background is green, that means it is marked as"
                              " collected!\n", font=['Times New Roman', 15, 'bold'],
             justify='center').pack(side='top')

    if len(tags) == 0:
        text = 'Do not roll any tags!'
    elif len(tags) <= 5:
        text = f'Roll {len(tags)} tags!\nThe order of tags will be:\n'
        for i in range(len(tags)):
            if i != len(tags)-1:
                text = f'{text}{tags[i]}, '
            else:
                text = f'{text}{tags[i]}'
    else:
        text = f'Roll {len(tags)} tags!\nThe final 5 tags will be:\n'
        for i in range(len(tags)-5, len(tags), 1):
            if i != len(tags) - 1:
                text = f'{text}{tags[i]}, '
            else:
                text = f'{text}{tags[i]}'

    tk.Label(text_frame, text=text, font=['Times New Roman', 15, 'bold'], justify='center').pack(side='top')

    text_frame.pack(side='top')

    frame_1 = tk.Frame(trophy_frame, width=250, height=300)
    frame_1.grid(row=0, column=0)
    text_stage = tk.Text(frame_1, font=['Times New Roman', 15, 'bold'])
    text_stage.place(x=0, y=0, width=250, height=300)
    text_stage.insert(tk.END, f"Stage trophy:\n{trophy}\n")

    for i in range(len(trophies)):
        if trophy == trophies[i][0]:
            cropped_rect = ((i % 16) * 250, int(i / 16) * 300, (i % 16) * 250 + 250, int(i / 16) * 300 + 300)
            cropped_im = photo.crop(cropped_rect)
            im = ImageTk.PhotoImage(cropped_im)
            text_stage.image_create(tk.END, image=im)
            text_stage.image = im
            break

    if len(goomba_trophies) == 1:
        frame_2 = tk.Frame(trophy_frame, width=250, height=300)
        frame_2.grid_propagate(False)
        frame_2.grid(row=0, column=1)
        text_goomba = tk.Text(frame_2, font=['Times New Roman', 15, 'bold'])
        text_goomba.place(x=0, y=0, width=250, height=300)
        text_goomba.insert(tk.END, f"Possible Goomba Trophy:\n{goomba_trophies[0]}\n")

        for i in range(len(trophies)):
            if goomba_trophies[0] == trophies[i][0]:
                cropped_rect = ((i % 16) * 250, int(i / 16) * 300, (i % 16) * 250 + 250, int(i / 16) * 300 + 300)
                cropped_im = photo.crop(cropped_rect)
                im_2 = ImageTk.PhotoImage(cropped_im)
                text_goomba.image_create(tk.END, image=im_2)
                text_goomba.image = im_2
                confirmed.append(0)
                break

        text_goomba.bind("<Button-1>", lambda *args: change_state(1, text_goomba))
    elif len(goomba_trophies) == 2:
        frame_2 = tk.Frame(trophy_frame, width=250, height=300)
        frame_2.grid(row=0, column=1)
        text_goomba_1 = tk.Text(frame_2, font=['Times New Roman', 15, 'bold'])
        text_goomba_1.place(x=0, y=0, width=250, height=300)
        text_goomba_1.insert(tk.END, f"Possible Goomba Trophy:\n{goomba_trophies[0]}\n")

        frame_3 = tk.Frame(trophy_frame, width=250, height=300)
        frame_3.grid(row=0, column=2)
        text_goomba_2 = tk.Text(frame_3, font=['Times New Roman', 15, 'bold'])
        text_goomba_2.place(x=0, y=0, width=250, height=300)
        text_goomba_2.insert(tk.END, f"Possible Goomba Trophy:\n{goomba_trophies[1]}\n")

        num = 0

        for i in range(len(trophies)):
            if goomba_trophies[0] == trophies[i][0]:
                cropped_rect = ((i % 16) * 250, int(i / 16) * 300, (i % 16) * 250 + 250, int(i / 16) * 300 + 300)
                cropped_im = photo.crop(cropped_rect)
                im_2 = ImageTk.PhotoImage(cropped_im)
                text_goomba_1.image_create(tk.END, image=im_2)
                text_goomba_1.image = im_2
                num += 1
                confirmed.append(0)
                if num == 2:
                    break

            if goomba_trophies[1] == trophies[i][0]:
                cropped_rect = ((i % 16) * 250, int(i / 16) * 300, (i % 16) * 250 + 250, int(i / 16) * 300 + 300)
                cropped_im = photo.crop(cropped_rect)
                im_3 = ImageTk.PhotoImage(cropped_im)
                text_goomba_2.image_create(tk.END, image=im_3)
                text_goomba_2.image = im_3
                num += 1
                confirmed.append(0)
                if num == 2:
                    break

        text_goomba_1.bind("<Button-1>", lambda *args: change_state(1, text_goomba_1))
        text_goomba_2.bind("<Button-1>", lambda *args: change_state(2, text_goomba_2))

    tk.Button(new_window, text="Submit", font=['Times New Roman', 15, 'bold'],
              justify='center', command=submit).pack(side='bottom')

    text_stage.bind("<Button-1>", lambda *args: change_state(0, text_stage))

    trophy_frame.pack(side='bottom')

    new_window.wait_window()

    if close:
        return [], close

    results = []
    for i in range(len(confirmed)):
        if i == 0:
            if confirmed[0]:
                results.append(trophy)
        if i == 1:
            if confirmed[1]:
                results.append(goomba_trophies[0])
        if i == 2:
            if confirmed[2]:
                results.append(goomba_trophies[1])

    return results, close


def roll_more_tags(n):
    tags = globals.TAGS
    tag_bool = []
    svar = []
    close = False

    def on_closing(win):
        nonlocal close

        close = True
        win.destroy()

    new_window = tk.Toplevel(window)
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))
    new_window.geometry(f"{int(window.winfo_width() * 3 / 5)}x{int(window.winfo_height() * 5 / 9)}")
    center(new_window)

    text_frame = tk.Frame(new_window)

    for i in range(n):
        tag_bool.append(0)
        var = tk.StringVar()
        tk.Label(text_frame, text=f"Entry {i + 1}", font=['Times New Roman', 15, 'bold'],
                 justify='center').grid(row=0, column=i)
        text_frame.grid_columnconfigure(i, weight=1, uniform="text")
        tk.Entry(text_frame, textvariable=var).grid(row=1, column=i)
        svar.append(var)

    if n == 1:
        svar[0].trace('w', lambda *args: text_settings(svar[0], 0))
    else:
        svar[0].trace('w', lambda *args: text_settings(svar[0], 0))
        svar[1].trace('w', lambda *args: text_settings(svar[1], 1))
        svar[2].trace('w', lambda *args: text_settings(svar[2], 2))
        svar[3].trace('w', lambda *args: text_settings(svar[3], 3))
        svar[4].trace('w', lambda *args: text_settings(svar[4], 4))

    def check_finish():
        for num in tag_bool:
            if num == 0:
                btn.config(state='disabled')
                return
        btn.config(state='normal')

    def text_settings(text, identifier):
        if character_limit(text):
            text.set(text.get().upper())

        check_tag(text, identifier)

    def check_tag(text, identifier):
        if len(text.get()) >= 2:
            if text.get() in tags:
                tag_bool[identifier] = 1
                check_finish()
                return

        if tag_bool[identifier]:
            tag_bool[identifier] = 0
            check_finish()

    def character_limit(text):
        if len(text.get()) > 4:
            text.set(text.get()[:-1].upper())
            return 0

        return 1

    def submit_tags():
        new_window.destroy()

    if n == 1:
        tk.Label(new_window, text='We couldn\'t find the seed based on the tags provided!\n'
                                  '\nPlease enter another tag!\n',
                 justify='center', wraplength=new_window.winfo_width(),
                 font=['Times New Roman', 20, 'bold']).pack(side='top')
    else:
        tk.Label(new_window, text='Press "Random" in the Character Selection Screen tag selection window 5 '
                                  'times and type them into the following boxes!\n\nORDER MATTERS!\n',
                 justify='center', wraplength=new_window.winfo_width(),
                 font=['Times New Roman', 20, 'bold']).pack(side='top')

    btn = tk.Button(text_frame, text="Submit", font=['Times New Roman', 15, 'bold'],
                    justify='center', command=submit_tags)
    btn.config(state='disabled')

    btn.grid(row=2, column=int(n/2))

    text_frame.pack()

    new_window.wait_window()

    if close:
        return [], close

    if n == 1:
        return tags.index(svar[0].get())

    rolled_tags = []
    for tag in svar:
        rolled_tags.append(tags.index(tag.get()))

    return rolled_tags, close


def center(win):
    """
    Centers a tkinter window

    :param win: the window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


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
        if isinstance(child, tk.Button) or isinstance(child, tk.Listbox) or isinstance(child, tk.Menubutton):
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
        if isinstance(child, tk.Button) or isinstance(child, tk.Listbox) or isinstance(child, tk.Menubutton):
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

    l_search = []
    r_search = []

    l_search_query = tk.StringVar()
    r_search_query = tk.StringVar()

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
        """
        if game_window is None:
            no_window_selected()
            return
        """
        clear_listboxes()
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

    l_search = []
    r_search = []

    l_search_query = tk.StringVar()
    r_search_query = tk.StringVar()

    r_buc = "All"
    l_buc = "All"

    def enable_all():
        enable_children(window)
        fill_listboxes()
        open_trophies()

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
        left_menu.menu.add_command(label='D Bucket', command=lambda: left_bucket("D Bucket"))
        left_menu.menu.add_command(label='Characters', command=lambda: left_bucket("Characters"))
        left_menu.menu.add_command(label='Zelda', command=lambda: left_bucket("Zelda"))
        left_menu.menu.add_command(label='Birdo', command=lambda: left_bucket("Birdo"))
        left_menu.menu.add_command(label='Giants', command=lambda: left_bucket("Giants"))
        left_menu.menu.add_command(label='Octorok', command=lambda: left_bucket("Octorok"))
        left_menu.menu.add_command(label='Sick', command=lambda: left_bucket("Sick"))
        left_menu.menu.add_command(label='Hats', command=lambda: left_bucket("Hats"))
        left_menu.menu.add_command(label='Villains', command=lambda: left_bucket("Villains"))
        left_menu.menu.add_command(label='Vacuum Luigi', command=lambda: left_bucket("Vacuum Luigi"))
        left_menu.menu.add_command(label='Dog', command=lambda: left_bucket("Dog"))
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
        right_menu.menu.add_command(label='D Bucket', command=lambda: right_bucket("D Bucket"))
        right_menu.menu.add_command(label='Characters', command=lambda: right_bucket("Characters"))
        right_menu.menu.add_command(label='Zelda', command=lambda: right_bucket("Zelda"))
        right_menu.menu.add_command(label='Birdo', command=lambda: right_bucket("Birdo"))
        right_menu.menu.add_command(label='Giants', command=lambda: right_bucket("Giants"))
        right_menu.menu.add_command(label='Octorok', command=lambda: right_bucket("Octorok"))
        right_menu.menu.add_command(label='Sick', command=lambda: right_bucket("Sick"))
        right_menu.menu.add_command(label='Hats', command=lambda: right_bucket("Hats"))
        right_menu.menu.add_command(label='Villains', command=lambda: right_bucket("Villains"))
        right_menu.menu.add_command(label='Vacuum Luigi', command=lambda: right_bucket("Vacuum Luigi"))
        right_menu.menu.add_command(label='Dog', command=lambda: right_bucket("Dog"))
        right_menu.menu.add_command(label='Lotto', command=lambda: right_bucket("Lotto"))

        left_menu.pack(side='bottom')
        right_menu.pack(side='bottom')

    def start_birdo():
        from All_Trophies_RNG.initial_birdo import main
        nonlocal collected

        rolled_tags = roll_more_tags(5)

        owned_trophies = []

        for i in range(collected.size()):
            owned_trophies.append(collected.get(i))

        main(rolled_tags, owned_trophies)

    def start_adv():
        from All_Trophies_RNG.end_adv1_1 import main
        from globals import trophies
        nonlocal collected

        disable_children(window)

        owned_trophies = []
        for i in range(collected.size()):
            owned_trophies.append(collected.get(i))

        confirmed = main(owned_trophies)

        enable_children(window)

        for trophy in confirmed:
            index, trophies_index = get_index(collected, trophy)
            uncollected.insert(index, trophy)
            trophies[trophies_index][1] = 1

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
        nonlocal r_search
        nonlocal r_search_query
        nonlocal l_search
        nonlocal r_search_query

        r_search_query.set('')
        l_search_query.set('')

        while len(r_search) > 0:
            val = r_search.pop()
            index, _ = get_index(uncollected, val)
            uncollected.insert(index, val)

        while len(l_search) > 0:
            val = l_search.pop()
            index, _ = get_index(collected, val)
            collected.insert(index, val)

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

    def l_search_update():
        nonlocal l_search_query
        nonlocal collected
        nonlocal l_search

        s = l_search_query.get().lower()
        n = len(s)

        search_index = 0
        search_len = len(l_search)

        ind = 0
        listbox_len = int(collected.size())

        if s == '':
            while len(l_search) > 0:
                val = l_search.pop()
                index, _ = get_index(collected, val)
                collected.insert(index, val)
            return

        while search_index < int(search_len):
            if l_search[search_index][0:n].lower() == s:
                index, _ = get_index(collected, l_search[search_index])
                collected.insert(index, l_search[search_index])
                l_search.pop(search_index)
                search_len -= 1
            else:
                search_index += 1

        while ind < int(listbox_len):
            if collected.get(ind)[0:n].lower() != s:
                l_search.append(collected.get(ind))
                collected.delete(ind)
                listbox_len -= 1
            else:
                ind += 1

    def r_search_update():
        nonlocal r_search_query
        nonlocal uncollected
        nonlocal r_search

        s = r_search_query.get().lower()
        n = len(s)

        search_index = 0
        search_len = len(r_search)

        ind = 0
        listbox_len = uncollected.size()

        if s == '':
            while len(r_search) > 0:
                val = r_search.pop()
                index, _ = get_index(uncollected, val)
                uncollected.insert(index, val)
            return

        while search_index < search_len:
            if r_search[search_index][0:n].lower() == s:
                index, _ = get_index(uncollected, r_search[search_index])
                uncollected.insert(index, r_search[search_index])
                r_search.pop(search_index)
                search_len -= 1
            else:
                search_index += 1

        while ind < listbox_len:
            if uncollected.get(ind)[0:n].lower() != s:
                r_search.append(uncollected.get(ind))
                uncollected.delete(ind)
                listbox_len -= 1
            else:
                ind += 1

    def move_left_trophies():
        nonlocal collected
        nonlocal hidden_left

        while len(hidden_left) > 0:
            index, _ = get_index(collected, hidden_left[len(hidden_left) - 1])
            collected.insert(index, hidden_left.pop())

    def left_bucket(bucket):
        trophies = globals.trophies
        nonlocal l_buc
        nonlocal l_search_query
        nonlocal l_search
        nonlocal collected

        l_search_query.set('')

        while len(l_search) > 0:
            val = l_search.pop()
            index, _ = get_index(collected, val)
            collected.insert(index, val)

        l_buc = bucket
        move_left_trophies()
        if bucket != 'All':
            for trophy, state, _, b in trophies:
                if state == 1 and b != bucket:
                    i = collected.get(0, tk.END).index(trophy)
                    hidden_left.append(collected.get(i))
                    collected.delete(i)

    def move_right_trophies():
        nonlocal hidden_right
        nonlocal uncollected

        while len(hidden_right) > 0:
            index, _ = get_index(uncollected, hidden_right[len(hidden_right) - 1])
            uncollected.insert(index, hidden_right.pop())

    def right_bucket(bucket):
        trophies = globals.trophies
        nonlocal r_buc
        nonlocal r_search
        nonlocal r_search_query
        nonlocal uncollected

        r_search_query.set('')

        while len(r_search) > 0:
            val = r_search.pop()
            index, _ = get_index(uncollected, val)
            uncollected.insert(index, val)

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

    if not booleans[1]:
        bg = "#7a7a7a"
        fg = "#fdfdfd"

        middle = tk.Frame(trophies_frame)
        l_listbox_frame = tk.Frame(trophies_frame)
        r_listbox_frame = tk.Frame(trophies_frame)

        l_listbox_frame.grid(row=1, column=1)
        r_listbox_frame.grid(row=1, column=3)

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

        collected = tk.Listbox(l_listbox_frame,
                               bg=bg,
                               font=("Franklin_Gothic_Medium", 20, "bold"),
                               fg=fg,
                               justify='left',
                               height=20,
                               selectmode=tk.SINGLE)

        uncollected = tk.Listbox(r_listbox_frame,
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

        tk.Entry(l_listbox_frame, textvariable=l_search_query).grid(row=0)
        tk.Entry(r_listbox_frame, textvariable=r_search_query).grid(row=0)

        l_search_query.trace('w', lambda *args: l_search_update())
        r_search_query.trace('w', lambda *args: r_search_update())

        collected.grid(row=1)
        uncollected.grid(row=1)

        fill_listboxes()

        collected.bind("<<ListboxSelect>>", move_trophy_collected)
        uncollected.bind("<<ListboxSelect>>", move_trophy_uncollected)
        move_un.bind("<<ListboxSelect>>", move_trophy_uncollected_back)
        move_col.bind("<<ListboxSelect>>", move_trophy_collected_back)

        move_un.pack(side="top")
        tk.Button(middle, text="MOVE", command=move_all_trophies).pack(side="top")
        move_col.pack(side="top")

        auto_checker_frame = tk.Frame(trophies_frame)
        birdobtn = tk.Button(auto_checker_frame, text="Birdo RNG Manip", command=start_birdo)
        advbtn = tk.Button(auto_checker_frame, text="Adventure 1-1 RNG Manip", command=start_adv)
        # check_trophies_btn = tk.Button(auto_checker_frame, text="Auto Check Trophies", command=auto_complete)

        birdobtn.pack(side='top')
        advbtn.pack(side='top')
        # check_trophies_btn.pack(side='top')

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
