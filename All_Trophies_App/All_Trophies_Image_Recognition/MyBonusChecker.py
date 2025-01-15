import time

import mss
import globals
from globals import bonuses
import pynput.keyboard
import pytesseract
import threading
import os
from PIL import Image

thread_local = threading.local()
threadlock = threading.Lock()

stop = False
click_positions = []
all_words = set()
global_index = 0


def recursive_arr_check(start_ind, ind, bonus, op, event):
    """
    Recursive function that searches through the sorted array in order to match the screenshotted bonus with
    a bonus in the list. If the bonus is found, we update the bonus array to be found and exit. If nothing is found,
    the threads will exit when the starting index is found

    :param start_ind: The starting index of where we searched
    :param ind: The current index that we are comparing the bonus to
    :param bonus: The screenshotted bonus we are trying to find
    :param op: (+) or (-) that helps the program move forward or backward in the array
    :param event: boolean value that stops other child thread if set
    :return: None
    """
    global global_index
    if event.is_set():
        return

    if ind >= len(bonuses):
        ind = 0
    elif ind < 0:
        ind = len(bonuses) - 1

    if compare_strings(bonus, bonuses[ind][0]):
        event.set()
        with threadlock:
            if bonuses[ind][1] == 0:
                globals.updated = True
                bonuses[ind][1] = 1
                global_index += 1
        return

    if ind == (start_ind + int(len(bonuses) / 2) + 1) % len(bonuses):
        return

    recursive_arr_check(start_ind, ind + op, bonus, op, event)


def remove_special_characters(character):
    """
    Removes special characters and confusing characters from text of bonuses

    :param character: character from bonus text
    :return: True if the value is a number or letter and is not a confusing character
    """
    if character.isalnum():
        if character == 'g' or character == 'O' or character == 'Q':
            return False
        return True
    else:
        return False


def compare_strings(s1, s2):
    """
    Compares screenshotted bonuses from the list of bonuses

    :param s1: bonus that program finds from screenshot
    :param s2: bonus that we need to find
    :return: True if they match and False if they don't
    """
    temp1 = ''.join(filter(remove_special_characters, s1))
    temp2 = ''.join(filter(remove_special_characters, s2))

    if len(temp1) <= 1:
        return False

    if temp1[0].isdigit():
        if len(temp1) > 1 and temp1[1] != '0':
            s = list(temp1)
            s[1] = '5'
            temp1 = "".join(s)
    elif not temp1[0].isupper():
        if temp1 != temp2:
            return temp1 == temp2[1:]
        else:
            return True

    return temp1 == temp2


def check_arr_start(ind, bonus):
    """
    If this found to be a potential bonus from start_thread, this will search the bonuses array to find the
    bonus that it is. This uses two threads in order to search for the associated bonus. It starts from the
    specified index. One thread goes forwards in the list and the other goes backwards in the list.

    :param ind: Index that is close to the bonuses
    :param bonus: bonus found from screenshot
    :return: None
    """
    if compare_strings(bonus, bonuses[ind][0]):
        bonuses[ind][1] = 1
        globals.updated = True
    else:
        event = threading.Event()
        threading.Thread(target=recursive_arr_check, args=(ind, ind + 1, bonus, 1, event)).start()
        threading.Thread(target=recursive_arr_check, args=(ind, ind - 1, bonus, -1, event)).start()

        # pos.start()
        # neg.start()
        # pos.join()
        # neg.join()


def start_thread(ind, text):
    """
    This is the beginning of where the program will compare the bonuses. This will check that the
    text is not blank nor the point value of the bonus

    :param ind: index where the program will start looking for bonus
    :param text: screenshotted text
    :return: None
    """
    if (
        not text.isnumeric()
        and len(text) >= 3
        and text[0] != 'x'
        and text[0] != '-'
        and text[0] != '—'
    ):
        check_arr_start(ind, text)


def check_bonuses():
    """
    Grabs text from screenshots made from the video made in order to mark collected bonuses in the array

    :return: None
    """
    global all_words
    global global_index
    # threads = []

    for word in all_words:
        threading.Thread(target=start_thread, args=[global_index, word]).start()
        # t.start()
        # threads.append(t)

    # for thread in threads:
      #  thread.join()


def find_words(frame):
    """
    Finds the words from a screenshot and adds it to a set

    :param: frame: The next frame of the video
    :return: None
    """
    global all_words

    temp = pytesseract.image_to_string(frame)
    text = temp.split('\n')
    for word in text:
        all_words.add(word)


def on_press(key):
    """
    Uses keyboard input in order to stop the program from taking screenshots

    :param key: Keyboard input key (will eventually be user specified)
    :return: None
    """
    global stop

    try:
        if key.char == 'q':
            stop = True
    except AttributeError:
        pass


def make_recording(output, top_left, bottom_right):
    """
    Creates a video recording of the selected screen region and grabs the text from them

    :param output: monitor that we are targeting
    :param top_left: x,y positions of the top_left click
    :param bottom_right: x,y positions of bottom_right click
    :return: None
    """
    global stop

    coords = {
        "top": top_left[1],
        "left": top_left[0],
        "width": bottom_right[0] - top_left[0],
        "height": bottom_right[1] - top_left[1],
        "mon": output,
    }

    threads = []
    stop = False

    print(f"Press 'q' to stop recording")
    with pynput.keyboard.Listener(on_press=on_press):
        sleep_time = .01
        while not stop:
            im = mss.mss().grab(coords)
            region = Image.frombytes("RGB", im.size, im.rgb)

            t = threading.Thread(target=find_words, args=[region])
            t.start()
            threads.append(t)
            time.sleep(sleep_time)

    for thread in threads:
        thread.join()

    check_bonuses()


def get_output_on_clicks():
    global click_positions

    x1 = click_positions[0][0]
    y1 = click_positions[0][1]
    x2 = click_positions[1][0]
    y2 = click_positions[1][1]

    with mss.mss() as sct:
        for i in range(1, len(sct.monitors)):
            print(sct.monitors[i])
            left = sct.monitors[i].get('left')
            right = sct.monitors[i].get('width') + left
            top = sct.monitors[i].get('top')
            bottom = sct.monitors[i].get('height') + top

            if left <= x1 <= right and left <= x2 <= right:
                if top <= y1 <= bottom and top <= y2 <= bottom:
                    new_coord_1 = [x1 - left, y1 - top]
                    new_coord_2 = [x2 - left, y2 - top]
                    return i, new_coord_1, new_coord_2

    return -1, click_positions[0], click_positions[1]


def on_click(x, y, button, pressed):
    """
    Uses mouse clicks and mouse position in order to find a specified user area in which the program
    will continuously take screenshots

    :param x: x position of mouse cursor
    :param y: y position of mouse cursor
    :param button: Checking if we right-click or right click
    :param pressed: Checks if mouse cursor is pressed
    :return: Returns False if function has found 2 mouse clicks
    """
    global click_positions
    if button.name == 'right':
        return True

    if pressed:
        click_positions.append((x, y))
        if len(click_positions) == 1:
            print(f'Click the bottom right')
        return False


def get_two_click_coordinates():
    """
    Ensures that we get exactly two mouse clicks from the user and uses them to create an area in which
    the program will take continuous screenshots

    :return: The positions of the user's mouse clicks
    """
    clicks = 0
    print(f'Make a first click in the top left')
    while clicks < 2:
        with pynput.mouse.Listener(on_click=on_click) as listener:
            listener.join()

        clicks += 1


def finish_work(output, top_left, bottom_right):
    file = r'Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = os.path.abspath(file)
    make_recording(output, top_left, bottom_right)


def main():
    from All_Trophies_App.ApplicationButtonFunctions import make_bonus_checker_windows
    global all_words
    global click_positions

    all_words = set()
    click_positions.clear()

    make_bonus_checker_windows()
