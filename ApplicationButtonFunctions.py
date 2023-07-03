import tkinter

import globals
import AppGlobals
import tkinter as tk
from tkinter import END

window = AppGlobals.window
cur = AppGlobals.cur

bonuses_frame = tk.Frame(window)
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


trophies_frame = tk.Frame(window)
bonus_org_frame = tk.Frame(window)


def first_click():
    text = tk.Text(window)
    text.pack(padx=20, pady=20)
    text.insert(END, f"Please click on the top left part of the bonuses\n")
    text.insert(END, f"(See reference image below for area to be selected)\n")
    image = tk.PhotoImage(file="../Images/First_Click.png")
    text.window_create(END, window=tk.Label(text, image=image))


def clear_listboxes():
    move_un.delete(0, END)
    move_col.delete(0, END)
    collected.delete(0, END)
    uncollected.delete(0, END)


def auto_complete():
    from All_Trophies_Image_Recognition.MyBonusChecker import main

    main()
    clear_listboxes()
    open_bonuses()


def consistent_order():
    print()


def hide_cur():
    if cur == 0:
        bonuses_frame.pack_forget()
    elif cur == 1:
        trophies_frame.pack_forget()
    else:
        bonus_org_frame.pack_forget()


def open_bonuses():
    global cur
    bonuses_frame.grid_columnconfigure(1, weight=1, uniform="bonuses")
    bonuses_frame.grid_columnconfigure(2, weight=1, uniform="bonuses")
    bonuses_frame.grid_columnconfigure(3, weight=1, uniform="bonuses")

    if cur != 0:
        hide_cur()
        cur = 0

    tk.Label(bonuses_frame,
             text="Collected Bonuses",
             font=("Franklin_Gothic_Medium", 20, "bold"),
             fg="#000000").grid(row=0, column=1)
    tk.Label(bonuses_frame,
             text="Remaining Bonuses",
             font=("Franklin_Gothic_Medium", 20, "bold"),
             fg="#000000").grid(row=0, column=3)

    for bonus, state in globals.bonuses:
        if state == 0:
            uncollected.insert(uncollected.size(), bonus)
        else:
            collected.insert(collected.size(), bonus)

    collected.grid(row=1, column=1)
    uncollected.grid(row=1, column=3)

    collected.bind("<<ListboxSelect>>", move_bonus_collected)
    uncollected.bind("<<ListboxSelect>>", move_bonus_uncollected)

    move_un.pack(side="top")
    tk.Button(middle, text="MOVE", command=move_all_bonuses).pack(side="top")
    move_col.pack(side="top")

    middle.grid(row=1, column=2)
    tk.Button(bonuses_frame, text="Use Auto Checker", command=auto_complete).grid(row=1, column=0)

    bonuses_frame.pack()


def move_all_bonuses():
    while move_col.size() > 0:
        uncollected.insert(uncollected.size(), move_col.get(0))
        move_col.delete(0)

    while move_un.size() > 0:
        collected.insert(collected.size(), move_un.get(0))
        move_un.delete(0)


def move_bonus_collected(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        collected.delete(index)
        move_col.insert(move_col.size(), data)


def move_bonus_uncollected(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        data = event.widget.get(index)
        uncollected.delete(index)
        move_un.insert(move_un.size(), data)


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
