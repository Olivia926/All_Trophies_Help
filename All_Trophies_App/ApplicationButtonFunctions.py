import globals
from globals import center
import tkinter as tk
import threading
import pynput.mouse
from PIL import Image, ImageTk
from string import digits

window = globals.window
cur = globals.cur

bonuses_frame = tk.Frame(window)
trophies_frame = tk.Frame(window)
bonus_org_frame = tk.Frame(window)

booleans = [0, 0, 0]


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


def make_bonus_checker_windows():
    from All_Trophies_App.All_Trophies_Image_Recognition.MyBonusChecker import on_click, get_output_on_clicks, \
        finish_work
    images = ['Images/First_Click.png', 'Images/Second_Click.png']
    new_window = tk.Toplevel(window)
    new_window.geometry(f"{int(window.winfo_width() * 4 / 5)}x{int(window.winfo_height() * 7 / 9)}")
    center(new_window)
    new_window.grab_set()
    im_1 = ImageTk.PhotoImage(Image.open(images[0]))
    im_2 = ImageTk.PhotoImage(Image.open(images[1]))

    def get_two_click_coordinates():
        """
        Ensures that we get exactly two mouse clicks from the user and uses them to create an area in which
        the program will take continuous screenshots

        :return: The positions of the user's mouse clicks
        """
        nonlocal first_label
        nonlocal second_label
        nonlocal third_label
        nonlocal fourth_label

        button.config(state='disabled')

        clicks = 0
        print(f'Make a first click in the top left')
        while clicks < 2:
            with pynput.mouse.Listener(on_click=on_click) as listener:
                listener.join()
                first_label.configure(fg="black")
                second_label.configure(fg="green")

            clicks += 1

        second_label.configure(fg="black")
        third_label.configure(fg="green")
        fourth_label.configure(fg="green")

        output, top_left, bottom_right = get_output_on_clicks()

        print(f'You clicked on monitor', output)

        print(f'The found coordinates are: (', top_left[0], ',', top_left[1], ')',
              'and (', bottom_right[0], ',', bottom_right[1], ')')

        if output == -1:
            print("Error")
            print(top_left)
            print(bottom_right)
            # TODO: Show error window popup
            return

        t = threading.Thread(target=finish_work(output, top_left, bottom_right))
        t.start()

        def check_if_done():
            if not t.is_alive():
                new_window.destroy()
            else:
                schedule_check()

        def schedule_check():
            new_window.after(1000, check_if_done)

        schedule_check()

    def do_work():
        t = threading.Thread(target=get_two_click_coordinates)
        t.start()

    text_frame = tk.Frame(new_window)
    first_label = tk.Label(text_frame, text="First click on the top left of the bonuses (shown below)",
                           font=['Times New Roman', 15, 'bold'],
                           justify='center',
                           wraplength=new_window.winfo_width()/4)
    first_label.configure(fg="green")
    first_label.grid(row=0, column=0)

    second_label = tk.Label(text_frame, text="Next click on the bottom right of the final bonus on the screen "
                                             "(shown below)",
                            font=['Times New Roman', 15, 'bold'],
                            justify='center',
                            wraplength=new_window.winfo_width()/4)
    second_label.grid(row=0, column=1)

    third_label = tk.Label(text_frame, text="Scroll down on the bonuses until you reach the end! If you want to ensure "
                                            "every bonus is gotten, scroll up after you hit the bottom!",
                           font=['Times New Roman', 15, 'bold'],
                           justify='center',
                           wraplength=new_window.winfo_width()/4)
    third_label.grid(row=0, column=2)

    fourth_label = tk.Label(text_frame, text="Hit q to stop the bonus checker from updating, and the bonuses should "
                                             "automatically update!",
                            font=['Times New Roman', 15, 'bold'],
                            justify='center',
                            wraplength=new_window.winfo_width()/4)
    fourth_label.grid(row=0, column=3)

    image_frame = tk.Frame(new_window)

    btn_frame = tk.Frame(new_window)
    button = tk.Button(btn_frame, text="START", font=['Times New Roman', 15, 'bold'], justify='center',
                       command=do_work)
    button.pack()

    for i in range(0, 4):
        text_frame.grid_columnconfigure(i, weight=1, uniform="Text")
        image_frame.grid_columnconfigure(i, weight=1, uniform="Text")

    text_frame.pack()
    btn_frame.pack()

    new_window.wait_window()


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

    def l_search_update():
        """
        Searches the collected listbox for the current search query
        """
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
        """
        Searches the uncollected listbox for the current search query
        """
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
        nonlocal move_col
        nonlocal move_un
        nonlocal collected
        nonlocal uncollected
        nonlocal r_search_query
        nonlocal l_search_query
        nonlocal r_search
        nonlocal l_search

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

        while move_un.size() > 0:
            index, bonuses_index = get_index(collected, move_un.get(0))
            collected.insert(index, move_un.get(0))
            globals.bonuses[bonuses_index][1] = 1
            move_un.delete(0)

        while move_col.size() > 0:
            index, bonuses_index = get_index(uncollected, move_col.get(0))
            uncollected.insert(index, move_col.get(0))
            globals.bonuses[bonuses_index][1] = 0
            move_col.delete(0)

        globals.updated = True

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
        nonlocal move_un
        nonlocal move_col
        nonlocal collected
        nonlocal uncollected

        move_un.delete(0, tk.END)
        move_col.delete(0, tk.END)
        collected.delete(0, tk.END)
        uncollected.delete(0, tk.END)

    def move_hidden():
        """
        Puts everything that isn't in the search query back into the listboxes in which they were in
        """
        nonlocal r_search
        nonlocal l_search
        nonlocal l_search_query
        nonlocal r_search_query

        l_search_query.set('')
        r_search_query.set('')

        while len(r_search) > 0:
            val = r_search.pop()
            index, _ = get_index(uncollected, val)
            uncollected.insert(index, val)

        while len(l_search) > 0:
            val = l_search.pop()
            index, _ = get_index(collected, val)
            collected.insert(index, val)

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
        move_hidden()
        clear_listboxes()
        run_bonus_checker()

    def run_bonus_checker():
        """
        Runs MyBonusChecker and gives user input to the application once it is done checking

        :return: None
        """
        from All_Trophies_App.All_Trophies_Image_Recognition.MyBonusChecker import main

        t = threading.Thread(target=main)
        t.start()

        def check_if_done():
            if not t.is_alive():
                fill_listboxes()
                open_bonuses()
            else:
                schedule_check()

        def schedule_check():
            bonuses_frame.after(1000, check_if_done)

        schedule_check()

    if globals.finished_updating:
        booleans[0] = 0
        for widget in bonuses_frame.winfo_children():
            widget.destroy()

    if not booleans[0]:
        bg = "#100817"
        fg = "#ffffff"

        l_listbox_frame = tk.Frame(bonuses_frame)
        r_listbox_frame = tk.Frame(bonuses_frame)

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

        collected = tk.Listbox(l_listbox_frame,
                               bg=bg,
                               font=("Franklin_Gothic_Medium", 20, "bold"),
                               fg=fg,
                               justify='right',
                               height=20,
                               selectmode=tk.SINGLE)

        uncollected = tk.Listbox(r_listbox_frame,
                                 bg=bg,
                                 font=("Franklin_Gothic_Medium", 20, "bold"),
                                 fg=fg,
                                 justify='right',
                                 height=20,
                                 selectmode=tk.SINGLE)

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

        tk.Entry(l_listbox_frame, textvariable=l_search_query).grid(row=0)
        tk.Entry(r_listbox_frame, textvariable=r_search_query).grid(row=0)

        l_search_query.trace('w', lambda *args: l_search_update())
        r_search_query.trace('w', lambda *args: r_search_update())

        collected.grid(row=1)
        uncollected.grid(row=1)

        l_listbox_frame.grid(row=1, column=1)
        r_listbox_frame.grid(row=1, column=3)

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
        auto_checker_frame.grid(row=0, column=2)

        left_frame.grid(row=0, column=1)
        right_frame.grid(row=0, column=3)

        booleans[0] = 1

    if not globals.finished_updating:
        hide_cur()
        cur = 0
        bonuses_frame.pack()


def roll_more_tags(n):
    """
    Handles displaying window that allows user to enter tags

    :param: n: Number of tags for user to enter
    """
    tags = globals.TAGS
    tag_bool = []
    svar = []
    close = False

    def on_closing(win):
        """
        Handles user clicking the close button on the window (X in top right)
        """
        nonlocal close

        close = True
        win.destroy()

    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.title("Record_first")
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
        """
        Checks if all tags are available to be submitted and turns on the "submit" button if they are
        """
        for num in tag_bool:
            if num == 0:
                btn.config(state='disabled')
                return
        btn.config(state='normal')

    def text_settings(text, identifier):
        """
        Every time a text field is updated, this method is called and updates text settings

        :param: text: text field that contains the inputted text
        :param: identifier: number used to determine which text field is being used
        """
        if character_limit(text):
            text.set(text.get().upper())

        check_tag(text, identifier)

    def check_tag(text, identifier):
        """
        Checks if the tag is in the "tags" array

        :param: text: text field that contains the inputted text
        :param: identifier: number used to determine which text field is being used
        """
        if len(text.get()) >= 2:
            if text.get() in tags:
                tag_bool[identifier] = 1
                check_finish()
                return

        if tag_bool[identifier]:
            tag_bool[identifier] = 0
            check_finish()

    def character_limit(text):
        """
        Enters characters into field in uppercase and disallows users from entering more than 4 characters

        :param: text: text field that contains the inputted text
        """
        if len(text.get()) > 4:
            text.set(text.get()[:-1].upper())
            return 0

        return 1

    def submit_tags():
        """
        Handles hitting the "submit" button
        """
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
        return tags.index(svar[0].get()), close

    rolled_tags = []
    for tag in svar:
        rolled_tags.append(tags.index(tag.get()))

    return rolled_tags, close


def fin_adv():
    """
    Handles the window that shows when every 1P only trophy is collected
    """
    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))
    new_window.geometry(f"{int(window.winfo_width() * 3 / 5)}x{int(window.winfo_height() * 5 / 9)}")
    center(new_window)

    def on_closing(win):
        """
        Handles user clicking the close button on the window (X in top right)
        """
        win.destroy()

    def submit():
        """
        Handles hitting the "submit" button
        """
        new_window.destroy()

    frame = tk.Frame(new_window)

    tk.Label(frame, text="You collected every trophy!\n\n",
             font=['Times New Roman', 15, 'bold'], justify='center').pack(side='top')

    tk.Button(frame, text="Exit", command=submit).pack(side='bottom')

    frame.pack()

    new_window.wait_window()


def display_initial_lotto(coins, trophy, dupe):
    """
    Handles displaying the window that shows user necessary information to obtain the Birdo trophy

    :param: tags: list of tags user inputs
    :param: num_coins: the number of coins the user needs to input into the lottery
    :param: num_steps: the number of times the "random" button needs to be hit on name selection screen
    :return:
    """
    trophies = globals.trophies
    file = "Images/Image_Atlas.png"
    photo = Image.open(file)

    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.geometry(f"{int(window.winfo_width() * 2 / 7)}x{int(window.winfo_height() * 6 / 11)}")
    center(new_window)
    full_frame = tk.Frame(new_window)
    stop = False
    succeed = False

    def on_closing():
        nonlocal new_window
        nonlocal stop

        new_window.destroy()
        stop = True

    def success():
        nonlocal succeed
        nonlocal new_window

        succeed = True
        new_window.destroy()

    def fail():
        nonlocal succeed
        nonlocal new_window

        succeed = False
        new_window.destroy()

    new_window.protocol("WM_DELETE_WINDOW", on_closing)

    if coins == 1:
        coin_label = tk.Label(full_frame, text=f"{coins} coin", font=("Times New Roman", 36))
    else:
        coin_label = tk.Label(full_frame, text=f"{coins} coins", font=("Times New Roman", 36))

    if not dupe:
        trophy_frame = tk.Frame(full_frame, width=250, height=300)
        index = 0
        for i in range(len(trophies)):
            if trophy == trophies[i][0]:
                index = i
                break
        cropped_rect = ((index % 16) * 250, int(index / 16) * 300, (index % 16) * 250 + 250, int(index / 16) * 300 + 300)
        cropped_im = photo.crop(cropped_rect)
        im = ImageTk.PhotoImage(cropped_im)
        img = tk.Text(trophy_frame, font=['Times New Roman', 15, 'bold'])
        img.image_create(tk.END, image=im)
        img.image = im
        img.place(x=0, y=0, width=250, height=300)
        trophy_frame.grid(row=1)
        label = tk.Label(full_frame, text=f"{trophy}", font=("Times New Roman", 24))
    else:
        label = tk.Label(full_frame, text=f"DUPLICATE", font=("Times New Roman", 36))


    btn_frame = tk.Frame(full_frame)
    success_btn = tk.Button(btn_frame, text="Confirm", command=success)
    fail_btn = tk.Button(btn_frame, text="Missed", command=fail)

    coin_label.grid(row=0)
    label.grid(row=2)
    btn_frame.grid(row=3)
    fail_btn.grid(row=0, column=0)
    success_btn.grid(row=0, column=1)
    full_frame.pack(anchor='center')
    new_window.grid_columnconfigure(0, weight=1)

    new_window.wait_window()

    return succeed, stop


def display_lotto(coins, dupe):
    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.geometry("250x150")
    center(new_window)
    stop = False
    succeed = False

    def on_closing():
        nonlocal new_window
        nonlocal stop

        new_window.destroy()
        stop = True
        
    def success():
        nonlocal succeed
        nonlocal new_window
        
        succeed = True
        new_window.destroy()
        
    def fail():
        nonlocal succeed
        nonlocal new_window

        succeed = False
        new_window.destroy()

    new_window.protocol("WM_DELETE_WINDOW", on_closing)

    if dupe:
        label = tk.Label(new_window, text="Unable to find a new trophy in the next roll.\n"
                                          "Please spend 1 coin and continue!")
    else:
        if coins == 1:
            label = tk.Label(new_window, text=f"Go to the lottery and spend {coins} coin\n"
                                              f"in the lottery to get a new trophy!")
        else:
            label = tk.Label(new_window, text=f"Go to the lottery and spend {coins} coins\n"
                                              f"in the lottery to get a new trophy!")

    if coins == 1:
        coin_label = tk.Label(new_window, text=f"{coins} coin", font=("Times New Roman", 36))
    else:
        coin_label = tk.Label(new_window, text=f"{coins} coins", font=("Times New Roman", 36))

    btn_frame = tk.Frame(new_window)
    success_btn = tk.Button(btn_frame, text="Confirm", command=success)
    fail_btn = tk.Button(btn_frame, text="Missed", command=fail)

    label.grid(row=0, column=0)
    coin_label.grid(row=1, column=0)
    btn_frame.grid(row=2, column=0)
    fail_btn.pack(side="left")
    success_btn.pack(side="left")
    new_window.grid_columnconfigure(0, weight=1)

    new_window.wait_window()

    return succeed, stop


def display_adv(tags, trophy, goomba_trophies):
    """
    Handles displaying the window that shows user the trophies that can be acquired in an adventure run

    :param: tags: list of tags user inputs
    :param: trophy: the trophy that will spawn on the stage
    :param: goomba_trophies: the trophy(ies) that can be acquired by jumping on goombas
    """

    trophies = globals.trophies
    file = "Images/Image_Atlas.png"
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
        """
        Handles hitting the "submit" button
        """

        new_window.destroy()

    def on_closing(win):
        """
        Handles user clicking the close button on the window (X in top right)
        """
        nonlocal close

        close = True
        win.destroy()

    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.title('Record')
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


def display_birdo(tags, num_coins, num_steps):
    """
    Handles displaying the window that shows user necessary information to obtain the Birdo trophy

    :param: tags: list of tags user inputs
    :param: num_coins: the number of coins the user needs to input into the lottery
    :param: num_steps: the number of times the "random" button needs to be hit on name selection screen
    :return:
    """
    index = 94
    file = "Images/Image_Atlas.png"
    photo = Image.open(file)
    close = False
    confirmed = 0

    def submit():
        """
        Handles user clicking "not found" button
        """

        new_window.destroy()

    def submit_confirm():
        """
        Handles user clicking "found" button
        """
        nonlocal confirmed

        confirmed = 1
        globals.updated = True
        new_window.destroy()

    def on_closing(win):
        """
        Handles user clicking the close button on the window (X in top right)
        """
        nonlocal close

        close = True
        win.destroy()

    def change_text():
        """
        Unimplemented method that will dynamically update the text on screen
        """
        nonlocal num_steps
        if num_steps > 0:
            num_steps -= 1
        add_text()

    def add_text():
        """
        Helper method that changes text on screen
        """
        nonlocal label

        if len(tags) == 0:
            text = 'Do not roll more tags!\n'
        elif len(tags) <= 5:
            text = f'Roll {num_steps} more tags!\nThe order of tags will be:\n'
            for i in range(len(tags)):
                if i != len(tags) - 1:
                    text = f'{text}{tags[i]}, '
                else:
                    text = f'{text}{tags[i]}'
        else:
            text = f'Roll {num_steps} more tags!\nThe final 5 tags will be:\n'
            for i in range(len(tags) - 5, len(tags), 1):
                if i != len(tags) - 1:
                    text = f'{text}{tags[i]}, '
                else:
                    text = f'{text}{tags[i]}'

        label.config(text=f'{text}\n'
                          f'When you have made it to the end,\n'
                          f'go to the lottery and spend {num_coins} coins!\n')

    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.title("Record")
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))
    new_window.geometry(f"{int(window.winfo_width() * 3 / 5)}x{int(window.winfo_height() * 7 / 11)}")
    center(new_window)

    text_frame = tk.Frame(new_window)
    trophy_frame = tk.Frame(new_window, width=250, height=300)
    button_frame = tk.Frame(new_window)

    label = tk.Label(text_frame, text="",
                     font=['Times New Roman', 15, 'bold'],
                     justify='center')

    add_text()
    label.pack()

    cropped_rect = ((index % 16) * 250, int(index / 16) * 300, (index % 16) * 250 + 250, int(index / 16) * 300 + 300)
    cropped_im = photo.crop(cropped_rect)
    im = ImageTk.PhotoImage(cropped_im)
    birdo_img = tk.Text(trophy_frame, font=['Times New Roman', 15, 'bold'])
    birdo_img.image_create(tk.END, image=im)
    birdo_img.image = im

    tk.Button(button_frame, text="Found", command=submit_confirm).pack(side='left')
    tk.Button(button_frame, text="Not Found", command=submit).pack(side='left')

    birdo_img.place(x=0, y=0, width=250, height=300)
    text_frame.grid(row=0)
    trophy_frame.grid(row=1)
    button_frame.grid(row=2)
    new_window.grid_columnconfigure(0, weight=1)

    new_window.wait_window()

    return confirmed, close


def display_tag_rolls(tags, num_steps):
    """
    Handles displaying the window that shows user how many times to roll tags

    :param: tags: list of tags user inputs
    :param: num_steps: the number of times the "random" button needs to be hit on name selection screen
    :return:
    """
    close = False

    def submit():
        """
        Handles user clicking "not found" button
        """

        new_window.destroy()

    def on_closing(win):
        """
        Handles user clicking the close button on the window (X in top right)
        """
        nonlocal close

        close = True
        win.destroy()

    def add_text():
        """
        Helper method that changes text on screen
        """
        nonlocal label

        if len(tags) == 0:
            text = 'Do not any roll more tags!\n'
        elif len(tags) <= 5:
            text = f'Roll {num_steps} more tags!\nThe order of tags will be:\n'
            for i in range(len(tags)):
                if i != len(tags) - 1:
                    text = f'{text}{tags[i]}, '
                else:
                    text = f'{text}{tags[i]}'
        else:
            text = f'Roll {num_steps} more tags!\nThe final 5 tags will be:\n'
            for i in range(len(tags) - 5, len(tags), 1):
                if i != len(tags) - 1:
                    text = f'{text}{tags[i]}, '
                else:
                    text = f'{text}{tags[i]}'

        label.config(text=f"{text}")

    new_window = tk.Toplevel(window)
    new_window.grab_set()
    new_window.title("Record")
    new_window.protocol("WM_DELETE_WINDOW", lambda: on_closing(new_window))
    new_window.geometry("400x150")
    center(new_window)

    text_frame = tk.Frame(new_window)
    button_frame = tk.Frame(new_window)

    label = tk.Label(text_frame, text="",
                     font=['Times New Roman', 15, 'bold'],
                     justify='center')

    add_text()
    label.pack()

    tk.Button(button_frame, text="DONE", command=submit).pack()

    text_frame.grid(row=0)
    button_frame.grid(row=1)
    new_window.grid_columnconfigure(0, weight=1)

    new_window.wait_window()

    return close


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
        from All_Trophies_App.All_Trophies_RNG.initial_birdo import main
        nonlocal collected
        nonlocal uncollected

        index = 94
        trophies = globals.trophies
        birdo = trophies[index]

        if not birdo[1]:
            owned_trophies = []

            for i in range(collected.size()):
                owned_trophies.append(collected.get(i))

            confirmed, break_flag = main(owned_trophies)

            while not confirmed and not break_flag:
                confirmed, break_flag = main(owned_trophies)

            if confirmed:
                i = uncollected.get(0, tk.END).index(birdo[0])
                new_index, _, _ = get_index(collected, birdo[0])
                collected.insert(new_index, birdo[0])
                uncollected.delete(i)
                trophies[index][1] = 1

    def start_adv():
        from All_Trophies_App.All_Trophies_RNG.end_adv1_1 import main
        from globals import trophies
        nonlocal collected

        owned_trophies = []
        for i in range(collected.size()):
            owned_trophies.append(collected.get(i))

        confirmed = main(owned_trophies)

        for trophy in confirmed:
            i = uncollected.get(0, tk.END).index(trophy)
            index, trophies_index, _ = get_index(collected, trophy)
            collected.insert(index, trophy)
            collected.itemconfig(index, {'bg': 'green'})
            uncollected.delete(i)
            trophies[trophies_index][1] = 1

    def start_initial_lotto():
        from All_Trophies_App.All_Trophies_RNG.initial_lotto import main
        from globals import trophies
        nonlocal collected

        owned_trophies = []
        for i in range(collected.size()):
            owned_trophies.append(collected.get(i))

        confirmed = main(owned_trophies)

        for trophy in confirmed:
            print(trophy)
            i = uncollected.get(0, tk.END).index(trophy)
            index, trophies_index, _ = get_index(collected, trophy)
            collected.insert(index, trophy)
            uncollected.delete(i)
            trophies[trophies_index][1] = 1

    def start_lotto():
        from All_Trophies_App.All_Trophies_RNG.end_lotto import main

        new_window = tk.Toplevel(window)
        new_window.grab_set()
        new_window.geometry("300x100")
        center(new_window)
        stop = False

        def close_window():
            nonlocal stop
            nonlocal new_window

            new_window.destroy()
            stop = True

        new_window.protocol("WM_DELETE_WINDOW", close_window)

        num_trophies = tk.StringVar()
        perc = tk.StringVar()

        num_frame = tk.Frame(new_window)
        perc_frame = tk.Frame(new_window)
        num_trophies_entry = tk.Entry(num_frame, textvariable=num_trophies)
        num_trophies_entry.bind('<Control-v>', lambda e: 'break')
        num_trophies_entry.bind('<Button-3>', lambda e: 'break')
        perc_entry = tk.Entry(perc_frame, textvariable=perc)
        perc_entry.bind('<Control-v>', lambda e: 'break')
        perc_entry.bind('<Button-3>', lambda e: 'break')

        num_trophies_lbl = tk.Label(num_frame, text="Trophies collected: ")
        perc_lbl = tk.Label(perc_frame, text="Lottery percentage: ")

        def submit():
            new_window.destroy()

        submitbtn = tk.Button(new_window, text="SUBMIT", state="disabled", command=submit)

        def check_both():
            if (num_trophies.get() and perc.get()
                    and num_trophies.get()[-1] != "." and perc.get()[-1] != ".")\
                    and int(num_trophies.get()) != 0 and float(perc.get()) != 0:
                submitbtn.config(state="normal")
            else:
                submitbtn.config(state="disabled")

        def check_trophies():
            if num_trophies.get():
                for i in range(len(num_trophies.get())):
                    if not num_trophies.get()[i].isdigit():
                        if i == 0:
                            num_trophies.set(num_trophies.get()[1:])
                        elif i == len(num_trophies.get()) - 1:
                            num_trophies.set(num_trophies.get()[:-1])
                        else:
                            num_trophies.set(num_trophies.get()[0:i] + num_trophies.get()[i+1:len(num_trophies.get())])
                if int(num_trophies.get()) >= 290:
                    num_trophies.set(289)

            check_both()

        def check_percentage():
            if perc.get():
                for i in range(len(perc.get())):
                    if not perc.get()[i].isdigit() and not perc.get()[i] == ".":
                        if i == 0:
                            perc.set(perc.get()[1:])
                        elif i == len(perc.get()) - 1:
                            perc.set(perc.get()[:-1])
                        else:
                            perc.set(perc.get()[0:i] + perc.get()[i+1:len(perc.get())])
                        break

                count = 0
                inds = []
                for i in range(len(perc.get())):
                    if perc.get()[i] == ".":
                        count += 1
                        inds.append(i)

                        if count >= 2:
                            max_first = max(inds[0], len(perc.get()) - inds[0])
                            max_second = max(inds[1], len(perc.get()) - inds[1])
                            if max_first > max_second:
                                if inds[0] == 0:
                                    perc.set(perc.get()[1:])
                                elif inds[0] == len(perc.get()) - 1:
                                    perc.set(perc.get()[:-1])
                                else:
                                    perc.set(perc.get()[0:inds[0]] + perc.get()[inds[0] + 1:len(perc.get())])
                            else:
                                if inds[1] == 0:
                                    perc.set(perc.get()[1:])
                                elif inds[1] == len(perc.get()) - 1:
                                    perc.set(perc.get()[:-1])
                                else:
                                    perc.set(perc.get()[0:inds[1]] + perc.get()[inds[1] + 1:len(perc.get())])
                            break

                if perc.get()[0] == '0':
                    perc.set(perc.get()[1:])
                elif float(perc.get()) > 100:
                    perc.set(str(int(float(perc.get())/10)) + perc.get().lstrip(digits))
                elif len(perc.get().lstrip(digits)) > 2:
                    perc.set(perc.get()[:-1])

            check_both()

        perc.trace('w', lambda * args: check_percentage())
        num_trophies.trace('w', lambda * args: check_trophies())

        num_trophies_lbl.pack(side='left')
        num_trophies_entry.pack(side='left')
        perc_lbl.pack(side='left')
        perc_entry.pack(side='left')

        num_frame.grid(row=0, column=0)
        perc_frame.grid(row=1, column=0)
        submitbtn.grid(row=2, column=0)

        new_window.grid_columnconfigure(0, weight=1)

        new_window.wait_window()

        if stop:
            return

        main(float(perc.get()), int(num_trophies.get()))

    def fill_listboxes():
        """
        Use the trophies array to insert the trophies into the collected and uncollected listboxes

        :return: None
        """
        for trophy, state, lotto, bucket in globals.trophies:
            if state == 0:
                uncollected.insert(uncollected.size(), trophy)
                if not lotto:
                    uncollected.itemconfig(uncollected.size() - 1, {'bg': 'green'})
            else:
                collected.insert(collected.size(), trophy)
                if not lotto:
                    collected.itemconfig(collected.size() - 1, {'bg': 'green'})

    def get_index(listbox, entry):
        """
        Find the index within the listbox for where it should place the current entry. This will also find the index
        in the trophies array to be used for checking off that the trophy has been collected.

        :param listbox:
        :param entry:
        :return: array containing
                 the index in the listbox to put the current value,
                 the index of the trophies array,
                 and if it is a one player trophy
                 in that order.
        """
        trophies = globals.trophies
        index = 0
        lotto = 1

        for i in range(len(trophies)):
            if entry == trophies[i][0]:
                index = i
                break

        if not trophies[index][2]:
            lotto = 0

        for i in range(listbox.size()):
            for j in range(len(trophies)):
                if listbox.get(i) == trophies[j][0]:
                    if j > index:
                        return i, index, lotto

        return tk.END, index, lotto

    def move_all_trophies():
        """
        Move every trophy from the middle and search listboxes to the collected and uncollected listboxes

        :return: None
        """
        trophies = globals.trophies
        nonlocal r_buc
        nonlocal l_buc
        nonlocal r_search
        nonlocal r_search_query
        nonlocal l_search
        nonlocal r_search_query
        nonlocal collected
        nonlocal uncollected
        nonlocal move_un
        nonlocal move_col

        r_search_query.set('')
        l_search_query.set('')

        while len(r_search) > 0:
            val = r_search.pop()
            index, _, lotto = get_index(uncollected, val)
            uncollected.insert(index, val)
            if not lotto:
                uncollected.itemconfig(index, {'bg': 'green'})

        while len(l_search) > 0:
            val = l_search.pop()
            index, _, lotto = get_index(collected, val)
            collected.insert(index, val)
            if not lotto:
                collected.itemconfig(index, {'bg': 'green'})

        while move_col.size() > 0:
            index, trophies_index, lotto = get_index(uncollected, move_col.get(0))
            if r_buc != "All":
                if move_col.get(0) == trophies[trophies_index][0]:
                    if r_buc == trophies[trophies_index][3]:
                        uncollected.insert(index, move_col.get(0))
                        if not lotto:
                            uncollected.itemconfig(uncollected.size() - 1, {'bg': 'green'})
                    else:
                        hidden_right.append(trophies[trophies_index][0])
            else:
                uncollected.insert(index, move_col.get(0))
                if not lotto:
                    uncollected.itemconfig(index, {'bg': 'green'})
            trophies[trophies_index][1] = 0
            move_col.delete(0)

        while move_un.size() > 0:
            index, trophies_index, lotto = get_index(collected, move_un.get(0))
            if l_buc != "All":
                if move_un.get(0) == trophies[trophies_index][0]:
                    if l_buc == trophies[trophies_index][3]:
                        collected.insert(index, move_un.get(0))
                        if not lotto:
                            collected.itemconfig(index, {'bg': 'green'})
                    else:
                        hidden_left.append(trophies[trophies_index][0])
            else:
                collected.insert(index, move_un.get(0))
                if not lotto:
                    collected.itemconfig(index, {'bg': 'green'})
            trophies[trophies_index][1] = 1
            move_un.delete(0)

            globals.updated = True

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
                index, _, lotto = get_index(collected, val)
                collected.insert(index, val)
                if not lotto:
                    collected.itemconfig(index, {'bg': 'green'})
            return

        while search_index < int(search_len):
            if l_search[search_index][0:n].lower() == s:
                index, _, lotto = get_index(collected, l_search[search_index])
                collected.insert(index, l_search[search_index])
                if not lotto:
                    collected.itemconfig(index, {'bg': 'green'})
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
                index, _, lotto = get_index(uncollected, val)
                uncollected.insert(index, val)
                if not lotto:
                    uncollected.itemconfig(index, {'bg': 'green'})
            return

        while search_index < search_len:
            if r_search[search_index][0:n].lower() == s:
                index, _, lotto = get_index(uncollected, r_search[search_index])
                uncollected.insert(index, r_search[search_index])
                if not lotto:
                    uncollected.itemconfig(index, {'bg': 'green'})
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
            index, _, lotto = get_index(collected, hidden_left[len(hidden_left) - 1])
            collected.insert(index, hidden_left.pop())
            if not lotto:
                collected.itemconfig(index, {'bg': 'green'})

    def left_bucket(bucket):
        trophies = globals.trophies
        nonlocal l_buc
        nonlocal l_search_query
        nonlocal l_search
        nonlocal collected

        l_search_query.set('')

        while len(l_search) > 0:
            val = l_search.pop()
            index, _, lotto = get_index(collected, val)
            collected.insert(index, val)
            if not lotto:
                collected.itemconfig(index, {'bg': 'green'})

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
            index, _, lotto = get_index(uncollected, hidden_right[len(hidden_right) - 1])
            uncollected.insert(index, hidden_right.pop())
            if not lotto:
                uncollected.itemconfig(index, {'bg': 'green'})

    def right_bucket(bucket):
        trophies = globals.trophies
        nonlocal r_buc
        nonlocal r_search
        nonlocal r_search_query
        nonlocal uncollected

        r_search_query.set('')

        while len(r_search) > 0:
            val = r_search.pop()
            index, _, lotto = get_index(uncollected, val)
            uncollected.insert(index, val)
            if not lotto:
                uncollected.itemconfig(index, {'bg': 'green'})

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
            ind, _, lotto = get_index(collected, data)
            collected.insert(ind, data)
            if not lotto:
                collected.itemconfig(ind, {'bg': 'green'})

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
            ind, _, lotto = get_index(move_col, data)
            move_col.insert(ind, data)
            if not lotto:
                move_col.itemconfig(ind, {'bg': 'green'})

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
            ind, _, lotto = get_index(uncollected, data)
            uncollected.insert(ind, data)
            if not lotto:
                uncollected.itemconfig(ind, {'bg': 'green'})

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
            ind, _, lotto = get_index(move_un, data)
            move_un.insert(ind, data)
            if not lotto:
                move_un.itemconfig(ind, {'bg': 'green'})

    if globals.finished_updating:
        booleans[1] = 0
        for widget in trophies_frame.winfo_children():
            widget.destroy()

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
        initiallottobtn = tk.Button(auto_checker_frame, text="Initial Lotto RNG Manip", command=start_initial_lotto)
        lottobtn = tk.Button(auto_checker_frame, text="Lotto RNG Manip", command=start_lotto)
        # check_trophies_btn = tk.Button(auto_checker_frame, text="Auto Check Trophies", command=auto_complete)

        birdobtn.grid(row=0, column=0)
        advbtn.grid(row=1, column=0)
        initiallottobtn.grid(row=0, column=1)
        lottobtn.grid(row=1, column=1)
        # check_trophies_btn.pack(side='top')

        middle.grid(row=1, column=2)
        auto_checker_frame.grid(row=0, column=2)

        left_frame.grid(row=0, column=1)
        right_frame.grid(row=0, column=3)

        booleans[1] = 1

    if not globals.finished_updating:
        hide_cur()
        cur = 1
        trophies_frame.pack()
