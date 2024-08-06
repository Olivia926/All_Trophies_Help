import globals
from globals import bonuses, trophies
from All_Trophies_App.ApplicationButtonFunctions import open_bonuses, open_trophies


def write_file(file):
    for i in range(len(bonuses)):
        if bonuses[i][1]:
            file.write("1")
        else:
            file.write("0")

    file.write("\n")

    for i in range(len(trophies)):
        if trophies[i][1]:
            file.write("1")
        else:
            file.write("0")

    globals.updated = False


def open_file_work(file):
    bon_ind = 0
    while 1:
        c = file.read(1)
        if c == '\n':
            break
        bonuses[bon_ind][1] = int(c)
        bon_ind += 1

    tro_ind = 0
    while 1:
        c = file.read(1)
        if c == '':
            break
        trophies[tro_ind][1] = int(c)
        tro_ind += 1

    reset_everything()


def reset_everything():
    globals.finished_updating = True

    open_bonuses()
    open_trophies()

    globals.finished_updating = False
    globals.updated = False
