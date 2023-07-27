import globals
from pynput.mouse import Listener
import pytesseract
from pynput import keyboard
import threading
import dxcam  # change
import cv2

thread_local = threading.local()
threadlock = threading.Lock()

stop = False
click_positions = []
all_words = set()
global_index = 0
fps = 8


def clear_bonuses():
    """
    Makes all bonuses uncollected by setting all the second values in the arrays to 0

    :return: None
    """
    for i in range(len(globals.bonuses)):
        globals.bonuses[i][1] = 0


def on_click(x, y, button, pressed):
    """
    Uses mouse clicks and mouse position in order to find a specified user area in which the program
    will continuously take screenshots

    :param x: x position of mouse cursor
    :param y: y position of mouse cursor
    :param button: Necessary to make the code run. Unnecessary in practice
    :param pressed: Checks if mouse cursor is pressed
    :return: Returns False if function has found 2 mouse clicks
    """
    if pressed:
        click_positions.append((x, y))
    if len(click_positions) == 1:
        print(f'Make a second click in the bottom right')
    if len(click_positions) == 2:
        return False


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


def get_two_click_coordinates():
    """
    Ensures that we get exactly two mouse clicks from the user and uses them to create an area in which
    the program will take continuous screenshots

    :return: The positions of the user's mouse clicks
    """
    clicks = 0
    print(f'Make a first click in the top left')
    while clicks < 2:
        with Listener(on_click=on_click) as listener:
            listener.join()
        clicks += 1

    return click_positions


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
    temp1 = ''.join(filter(remove_special_characters, s1)).lower()
    temp2 = ''.join(filter(remove_special_characters, s2)).lower()

    if temp1[0].isdigit()and temp1[1] != '0':
        temp1 = temp1[:1] + "5" + temp1[2:]
    # elif not temp1[0].isupper():
    #     if temp1 != temp2:
    #         return temp1 == temp2[1:]
    #     else:
    #         return True

    poopy = False

    if temp1 in temp2 and temp1 != temp2 and len(temp1) > 1:
        # print(f'found {temp1} in {temp2}')
        if abs(len(temp1) - len(temp2)) <= 2:
            poopy = True
            print(f"guessing that {temp1} is suppposed to be {temp2}")
    
    return temp1 == temp2 or poopy


def start_thread(ind, text):
    """
    This is the beginning of where the program will compare the bonuses. This will check that the
    text is not blank nor the point value of the bonus

    :param ind: index where the program will start looking for bonus
    :param text: screenshotted text
    :return: None
    """
    if len(text) > 1:
        if not text.isnumeric() and text[0] != 'x' and text[0] != '-' and text[0] != '—':
            check_arr_start(ind, text)


def check_arr_start(ind, bonus):
    """
    If this found to be a potential bonus from start_thread, this will search the bonuses array to find the
    bonus that it is. This uses two threads in order to search for the associated bonus. It starts from the
    specified index. One thread goes forwards in the list and the other goes backwards in the list.

    :param ind: Index that is close to the bonuses
    :param bonus: bonus found from screenshot
    :return: None
    """
    if compare_strings(bonus, globals.bonuses[ind][0]):
        globals.bonuses[ind][1] = 1
    else:
        event = threading.Event()
        pos = threading.Thread(target=recursive_arr_check, args=(ind, ind + 1, bonus, 1, event))
        neg = threading.Thread(target=recursive_arr_check, args=(ind, ind - 1, bonus, -1, event))
        pos.start()
        neg.start()
        pos.join()
        neg.join()


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

    if ind >= len(globals.bonuses):
        ind = 0
    elif ind < 0:
        ind = len(globals.bonuses) - 1

    if compare_strings(bonus, globals.bonuses[ind][0]):
        event.set()
        with threadlock:
            if globals.bonuses[ind][1] == 0:
                globals.bonuses[ind][1] = 1
                global_index += 1
        return

    if ind == (start_ind + globals.halfbonus) % len(globals.bonuses):
        return

    recursive_arr_check(start_ind, ind + op, bonus, op, event)


def check_bonuses():
    """
    Grabs text from screenshots made from the video made in order to mark collected bonuses in the array

    :return: None
    """
    global all_words
    global global_index
    # threads = []

    print(all_words)

    print("Please wait while we look at the bonuses")
    for word in all_words:
        if len(word) <= 1:
            continue
        elif word[0] == 'x':
            continue
        
        for b in globals.bonuses:
            if word == b[0]:
                b[1] = 1
                break
        else:
            w = word.lower().replace(' ', '').replace('-', '').replace('—', '').replace('’', '').replace(',', '').replace('.', '')
            for b in globals.bonuses:
                if b[1] == 1:
                    continue
                b_modified = b[0].lower().replace(' ', '').replace('-', '').replace('\'', '').replace(',', '').replace('.', '')
                if w in b_modified and ((len(w) - len(b_modified)) <= 2):
                    print(f'guessing {word} is {b[0]}')
                    b[1] = 1
                    break
        
    #     t = threading.Thread(target=start_thread, args=[global_index, word])
    #     t.start()
    #     threads.append(t)

    # for thread in threads:
    #     thread.join()


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


def make_recording(top_left, bottom_right):
    """
    Creates a video recording of the selected screen region and grabs the text from them

    :param top_left: x,y positions of the top_left click
    :param bottom_right: x,y positions of bottom_right click
    :return: None
    """
    global fps
    global stop
    camera = dxcam.create()
    region = (top_left[0], top_left[1], bottom_right[0], bottom_right[1])

    threads = []
    stop = False

    print(f"Press 'q' to stop recording")
    with keyboard.Listener(on_press=on_press):
        camera.start(region=region, target_fps=fps)
        while not stop:
            t = threading.Thread(target=find_words, args=[camera.get_latest_frame()])
            t.start()
            threads.append(t)

    for thread in threads:
        thread.join()

    camera.stop()


def main():
    # from All_Trophies_App.ApplicationButtonFunctions import get_window_size

    global click_positions

    click_positions.clear()

    coordinates = get_two_click_coordinates()

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # window = get_window_size()

    # coordinates = [[window[0], window[1]],
    #                [window[2], window[3]]]
    # coordinates = find a way to get specific spot in window based on image
    make_recording(coordinates[0], coordinates[1])
    check_bonuses()
