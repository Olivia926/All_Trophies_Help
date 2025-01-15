import copy
from All_Trophies_App.All_Trophies_RNG.tagrss import TagRss
from globals import TAGS

add_trophies = []

TAGS_DICT = {"AAAA": 0, "1DER": 1, "2BIT": 2, "2L8": 3, "2PAY": 4, "401K": 5, "4BDN": 6, "4BY4": 7, "4EVA": 8,
             "7HVN": 9, "AOK": 10, "ARCH": 11, "ARN": 12, "ASH": 13, "BAST": 14, "BBBB": 15, "BCUZ": 16, "BETA": 17,
             "BOBO": 18, "BOMB": 19, "BONE": 20, "BOO": 21, "BORT": 22, "BOZO": 23, "BUB": 24, "BUD": 25, "BUZZ": 26,
             "BYRN": 27, "CHUM": 28, "COOP": 29, "CUBE": 30, "CUD": 31, "DAYZ": 32, "DIRT": 33, "DIVA": 34, "DNCR": 35,
             "DUCK": 36, "DUD": 37, "DUFF": 38, "DV8": 39, "ED": 40, "ELBO": 41, "FAMI": 42, "FIDO": 43, "FILO": 44,
             "FIRE": 45, "FLAV": 46, "FLEA": 47, "FLYN": 48, "GBA": 49, "GCN": 50, "GLUV": 51, "GR8": 52, "GRIT": 53,
             "GRRL": 54, "GUST": 55, "GUT": 56, "HAMB": 57, "HAND": 58, "HELA": 59, "HEYU": 60, "HI5": 61, "HIKU": 62,
             "HOOD": 63, "HYDE": 64, "IGGY": 65, "IKE": 66, "IMPA": 67, "JAZZ": 68, "JEKL": 69, "JOJO": 70, "JUNK": 71,
             "KEY": 72, "KILA": 73, "KITY": 74, "KLOB": 75, "KNEE": 76, "L33T": 77, "L8ER": 78, "LCD": 79, "LOKI": 80,
             "LULU": 81, "MAC": 82, "MAMA": 83, "ME": 84, "MILO": 85, "MIST": 86, "MOJO": 87, "MOSH": 88, "NADA": 89,
             "ZZZZ": 90, "NAVI": 91, "NELL": 92, "NEWT": 93, "NOOK": 94, "NEWB": 95, "ODIN": 96, "OLAF": 97, "OOPS": 98,
             "OPUS": 99, "PAPA": 100, "PIT": 101, "POP": 102, "PKMN": 103, "QTPI": 104, "RAM": 105, "RNDM": 106,
             "ROBN": 107, "ROT8": 108, "RUTO": 109, "SAMI": 110, "SET": 111, "SETI": 112, "SHIG": 113, "SK8R": 114,
             "SLIM": 115, "SMOK": 116, "SNES": 117, "SNTA": 118, "SPUD": 119, "STAR": 120, "THOR": 121, "THUG": 122,
             "TIRE": 123, "TLOZ": 124, "TNDO": 125, "TOAD": 126, "TOMM": 127, "UNO": 128, "VIVI": 129, "WALK": 130,
             "WART": 131, "WARZ": 132, "WITH": 133, "YETI": 134, "YNOT": 135, "ZAXO": 136, "ZETA": 137, "ZOD": 138,
             "ZOE": 139, "WORM": 140, "GEEK": 141, "DUDE": 142, "WYRN": 143, "BLOB": 144}

TROPHIES_1PL_LOT = [['Ray Gun', True], ['Super Scope', True], ['Fire Flower', True], ['Star Rod', True],
                    ['Home-Run Bat', True], ['Fan', True], ['Red Shell', False], ['Flipper', True],
                    ['Mr. Saturn', True], ['Bob-omb', True], ['Super Mushroom', True], ['Starman 64', True],
                    ['Barrel Cannon', True], ['Party Ball', True], ['Crate', True], ['Barrel', True], ['Capsule', True],
                    ['Egg', True], ['Squirtle', True], ['Blastoise', True], ['Clefairy', True], ['Weezing', True],
                    ['Chansey', False], ['Goldeen', True], ['Snorlax', True], ['Chikorita', True], ['Cyndaquil', True],
                    ['Bellossom', True], ['Wobbuffet', True], ['Scizor', True], ['Porygon2', True], ['Toad', True],
                    ['Coin', True], ['Kirby Hat 1', True], ['Kirby Hat 2', True], ['Kirby Hat 3', True],
                    ['Lakitu', True], ['Birdo', True], ['Klap Trap', True], ['Slippy Toad', True],
                    ['Koopa Troopa', True], ['Topi', True], ['Metal Mario', True], ['Daisy', True], ['Thwomp', True],
                    ['Bucket', True], ['Racing Kart', True], ['Baby Bowser', True], ['Raphael Raven', True],
                    ['Dixie Kong', False], ['Dr. Stewart', True], ['Jody Summer', True], ['Andross 64', True],
                    ['Metroid', True], ['Ridley', True], ['Fighter Kirby', False], ['Ball Kirby', True],
                    ['Waddle Dee', True], ['Rick', True], ['Jeff', False], ['Starman EB', True], ['Bulbasaur', True],
                    ['Poliwhirl', True], ['Eevee', False], ['Totodile', True], ['Crobat', True], ['Igglybuff', True],
                    ['Steelix', True], ['Heracross', True], ['Professor Oak', False], ['Misty', False],
                    ['ZERO-ONE', True], ['Maruo Maruhige', False], ['Ryota Hayami', True], ['Ray Mk II', False],
                    ['Heririn', True], ['Excitebike', True], ['Ducks', True], ['Bubbles', False],
                    ['Eggplant Man', False], ['Balloon Fighter', True], ['Dr. Wright', True], ['Donbe & Hikari', True],
                    ['Monster', True]]

DSTAR = {1: [675975949, 2727824503],
         2: [-191841887, 2115878600],
         3: [-2157176827, 2531105853],
         4: [1084380025, 2165923046],
         5: [-389939651, 586225427],
         6: [-605770863, 3109564500],
         7: [-3310955595, 3566711417],
         8: [-1422735383, 2234209426],
         9: [-1492584851, 2784856047],
         10: [-762265983, 2186156320],
         11: [-3133008795, 3255514357],
         12: [896611673, 2974409086],
         13: [-2201834595, 4082973451],
         14: [2963202673, 1172243756],
         15: [191990293, 2947833777],
         16: [-668333111, 3265965994],
         17: [-811643443, 2952203367],
         18: [2226784097, 763478136],
         19: [3798852805, 152809133],
         20: [-727532743, 3073944342]}


def get_trophies(base_trophy_set, user_trophies):
    trophies = base_trophy_set

    for trophy in user_trophies:
        for i in range(len(trophies)):
            if trophies[i][0] == trophy:
                trophies.remove(trophies[i])
                break
    """
    skip = input_trophy is not None
    if input_trophy is None:
        input_trophy = input(
            "Type the names of the trophies that you've collected in the gallery. "
            "Substrings are allowed, but be careful. Type 'x' or 'q' to finish.\n")
    while input_trophy.lower() != 'x' and input_trophy.lower() != 'q':
        found = False
        misinput = False
        multiple_trophies = ''
        substr_matches = False

        for i, t in enumerate(trophies):
            tt = t[0] if len(t) == 2 else t
            if input_trophy in tt:
                exact_match = input_trophy == tt
                if not exact_match:
                    multiple_trophies += trophy_str(tt)
                    for t_forward in trophies[i + 1:]:
                        ttt = t_forward[0] if len(t_forward) == 2 else t_forward
                        if input_trophy in ttt:
                            exact_match = input_trophy == ttt
                            multiple_trophies += trophy_str(t_forward)
                            substr_matches = True
                    if not exact_match and substr_matches:
                        multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                        print(
                            f"These trophies contain the substring '{input_trophy}':\n{multiple_trophies}\n"
                            f"Please retype the trophy name.")
                        break
                    if exact_match:
                        continue
                print(f'{tt} found!')
                confirmed = not input(f"Confirm {tt} trophy? Hit [ENTER] if yes, otherwise input a character.\n")
                if confirmed:
                    del trophies[i]
                    found = True
                    break
                else:
                    misinput = True
        else:
            if not found:
                print(
                    f'Could not find {input_trophy}. '
                    f'If this is a trophy that isn\'t in 1PO or 1PL, ignore this message.')
            elif misinput:
                print(f'User misinput detected, please re-input the trophy you received.')
        if skip and found:
            break
        else:
            input_trophy = input("Trophy name (x or q to quit):\n")
            """
    return trophies


def get_seed() -> tuple[int, list[int]]:
    from All_Trophies_App.ApplicationButtonFunctions import roll_more_tags

    """ Returns the seed and the list of rolled tags as a tuple."""
    potential_seed = []
    rolled_tags = []
    while len(potential_seed) != 1:
        rolled_tags, break_flag = roll_more_tags(5)

        if break_flag:
            return [], break_flag

        # let the user input each of the rolled tags
        potential_seed = TagRss(rolled_tags)

    return potential_seed[0][2][len(rolled_tags) - 5], rolled_tags


"""
def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t} '
    added_str = f' (new)|' if t[1] else f' (owned)|'
    return ''.join([ret, added_str])
"""


def print_tags(tags_to_roll: list[str]):
    from All_Trophies_App.ApplicationButtonFunctions import display_tag_rolls

    close = display_tag_rolls(tags_to_roll, len(tags_to_roll))

    return close

# this is meant to get 83/84 of the initial trophies because of reasons that were not explained to me.
# the way this is accomplished is by keeping track of the LOT trophies that are collected,
# and ensuring that we only ever get 11/12 of them.
# thus the last uncollected trophy is from LOT.

# this also features a new algorithm where fewer coins are spent due to this being run at the beginning of a run.
# note that the greedy algorithm is also toggleable here.


"""
def update_spending_log(coin_count):
    log_file = "coin_spending_log_3_coins.txt"
    spending_data = {}

    try:
        with open(log_file) as file:
            lines = file.readlines()
            for line in lines:
                coin, count = line.strip().rstrip(",").split(": ")
                spending_data[int(coin)] = int(count)
    except FileNotFoundError:
        spending_data = {i: 0 for i in range(1, 21)}

    # Update the spending data
    spending_data[coin_count] += 1

    # Write updated data back to the file
    with open(log_file, "w") as file:
        for coin, count in spending_data.items():
            file.write(f"{coin}: {count},\n")


def log_total_coins_spent(coins):
    try:
        with open("total_coins_spent_3_8_dfs.txt", "a") as file:
            file.write(f"{coins}\n")
    except Exception as e:
        print(f"An error occurred: {e}")


def read_total_coins_spent(fname):
    total_coin_costs = []
    try:
        # change filename to match necessary stuff
        with open(fname) as file:
            # Read each line, convert to integer, and append to the list
            total_coin_costs = [int(line.strip()) for line in file]
    except Exception as e:
        print(f"An error occurred: {e}")
    return total_coin_costs
"""


"""
def plot_data():
    import matplotlib.pyplot as plt
    import re
    filenames = ["./old_scripts_and_other/coin_spending_logs/total_coins_spent_greedy.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_3_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_2_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_6_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_5_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_7_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_6_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_9_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_8_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_7_dfs.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_3_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_20_2_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_6_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_5_5_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_7_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_4_6_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_9_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_8_dfs+et.txt",
                 "./old_scripts_and_other/coin_spending_logs/total_coins_spent_3_7_dfs+et.txt",
                 ]

    file_data = []
    for filename in filenames:
        file_data.append(read_total_coins_spent(filename))

    num_files = len(file_data)
    columns = 4  # Number of columns for subplots
    rows = (num_files // columns) + (num_files % columns > 0)

    plt.figure(figsize=(20, 12))

    for i, data in enumerate(file_data):
        plt.subplot(rows, columns, i + 1)
        plt.hist(data, bins=20, edgecolor='black', alpha=0.7)
        plt.title(re.search(r'[^/]+$', filenames[i]).group()[18:-4].replace("_", "^", 1).replace("_", " ", 1),
                  fontsize=10)
        plt.xlabel("Coin Values", fontsize=8)
        plt.ylabel("Frequency", fontsize=8)
        plt.tight_layout()

    plt.show()
"""


def coin_step(trophies, clot: int, coins_spent: list[int], seed: int, coins_to_spend):
    chance = int((len(trophies) / 84) * 100)
    temp_seed = (DSTAR[coins_to_spend][0] * seed + DSTAR[coins_to_spend][1]) & 4294967295
    trophy_idx = -1
    invalid = False
    if (100 * temp_seed >> 16) >> 16 < chance + (5 * (coins_to_spend - 1)):
        # 1 step for trophy roll
        trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
        # if the trophy is LOT, add it to the count. if this is the LAST LOT trophy, do not accept it.
        # if clot != 11 -> accept the trophy and add clot count if necessary
        # else -> if not LOT, then accept the trophy
        #      -> else do not accept the trophy -> FLAG BRANCH AS INVALID ??
        if clot != 11:
            clot += not trophies[trophy_idx]
        else:
            if not trophies[trophy_idx]:
                invalid = True
    if not invalid:
        # 2 steps to realign rng
        seed = (2851891209 * temp_seed + 505908858) & 4294967295
        coins_spent.append(coins_to_spend)

    if trophy_idx == -1:
        # print get dupe trophy
        return trophies, clot, coins_spent, seed, invalid
    if not invalid:
        del trophies[trophy_idx]
    return trophies, clot, coins_spent, seed, invalid


def coin_sim(trophies, seed, debug, max_depth, max_breadth, count_lot):
    from All_Trophies_App.ApplicationButtonFunctions import display_initial_lotto
    global add_trophies
    total_coins = 0
    while len(trophies) != 1:
        """
        if not debug:
            print(f"\ntrophies remaining: {len(trophies)}")
        """
        # if you want to add a toggle, do that here.
        # note that you'll have to add break statements to exit the loop when you switch between the modes.
        # I've commented them below.
        # just note that there's practically 0 reason to do this. im providing the option because I was asked to.
        # remember to comment out the `mode = False` line below.
        # if not debug:
        #     mode = input("press [ENTER] for coin saver, anything else for greedy: \n").lower() != ""

        # default to coin saver
        mode = False

        if mode:
            # greedy mode
            chance = int((len(trophies) / 84) * 100)
            trophy_idx = -1
            coins = 0
            # advance twice
            temp_seed = (2851891209 * seed + 505908858) & 4294967295
            for i in range(20):
                # 3 steps for success/failure roll
                temp_seed = (-3124220955 * temp_seed + 3539360597) & 4294967295
                if (100 * temp_seed >> 16) >> 16 < chance + (5 * i):
                    # 1 step for trophy roll
                    trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
                    # if the trophy is LOT, add it to the count. if this is the LAST LOT trophy, do not accept it.
                    if count_lot != 11:
                        count_lot += not trophies[trophy_idx][1]
                    else:
                        if not trophies[trophy_idx][1]:
                            continue
                    coins = i + 1
                    total_coins += i + 1
                    # 2 steps to realign rng
                    seed = (2851891209 * temp_seed + 505908858) & 4294967295
                    if debug:
                        # update_spending_log(coins)
                        pass
                    break
            if trophy_idx == -1:
                coins += 1
                total_coins += 1
                # print("No new trophy, spend 1 coin to advance rng.")
                # advance by 7 to account for lack of trophy -> inputting 1 coin to advance rng
                seed = (203977589 * seed + 548247209) & 4294967295
                if debug:
                    # update_spending_log(1)
                    pass
            else:
                # confirm trophy has been received
                if debug:
                    del trophies[trophy_idx]
                else:
                    trophies = get_trophies(trophies, trophies[trophy_idx][0])
                    # mode = input("Press [ENTER] to continue in greedy,
                    # else any other button to switch to greedy.") == ""
                    # if not mode:
                    #     total_coins += c
                    #     break
        else:
            initial_trophy_count = len(trophies)
            partial_trophies = [t[1] for t in trophies]
            max_new_trophies = 0
            min_coins_spent = 999
            best_path = []
            # DFS
            stack = []
            for i in range(max_breadth):
                stack.append((copy.deepcopy(partial_trophies), copy.deepcopy(count_lot), copy.deepcopy([]),
                              copy.deepcopy(seed), i + 1))
            while len(stack) > 0:
                q = stack.pop()
                c = coin_step(*q)
                # invalid check
                if not c[4]:
                    if len(c[2]) == max_depth or len(c[2]) == initial_trophy_count - 1:
                        if max_new_trophies < initial_trophy_count - len(c[0]):
                            min_coins_spent = sum(c[2])
                            best_path = c[2]
                            max_new_trophies = initial_trophy_count - len(c[0])
                            count_lot = c[1]
                        elif max_new_trophies == initial_trophy_count - len(c[0]) and sum(c[2]) < min_coins_spent:
                            min_coins_spent = sum(c[2])
                            best_path = c[2]
                            count_lot = c[1]
                        # early term
                        if max_new_trophies == max_depth or max_new_trophies == initial_trophy_count - 1:
                            break
                    else:
                        for i in range(max_breadth, 0, -1):
                            stack.append(
                                (copy.deepcopy(c[0]), copy.deepcopy(c[1]), copy.deepcopy(c[2]), copy.deepcopy(c[3]), i))
                else:
                    # branch is dead due to invalid (this means it ends up completing the LOT set,
                    # which it shouldn't do)
                    pass

            # stack is now empty; we've traversed the tree.
            # the best path is defined by the number of coins to spend.
            for c in best_path:
                temp_seed = (DSTAR[c][0] * seed + DSTAR[c][1]) & 4294967295
                chance = int((len(trophies) / 84) * 100)
                trophy_idx = -1
                if (100 * temp_seed >> 16) >> 16 < chance + (5 * (c - 1)):
                    # 1 step for trophy roll
                    trophy_idx = (len(trophies) * ((214013 * temp_seed + 2531011) & 4294967295) >> 16) >> 16
                # 2 steps to realign rng
                seed = (2851891209 * temp_seed + 505908858) & 4294967295

                if trophy_idx == -1:
                    if not debug:
                        success, stop = display_initial_lotto(c, "", 1)

                        if not success or stop:
                            return
                else:
                    if not debug:
                        add_trophies.append(trophies[trophy_idx][0])
                        success, stop = display_initial_lotto(c, trophies[trophy_idx][0], 0)

                        if not success or stop:
                            return

                        trophies.remove(trophies[trophy_idx])
                        # mode = input("Press [ENTER] to continue in coin saver,
                        # else any other button to switch to greedy.") != ""
                        # if mode:
                        #     total_coins += c
                        #     break
                    else:
                        del trophies[trophy_idx]
                        # update_spending_log(c)
                total_coins += c
                # early terminate when simulating
                if debug and total_coins > 170:
                    return -1
    return total_coins


def main(user_trophies):
    global add_trophies

    add_trophies = []

    max_depth = 9
    max_breadth = 3

    trophies = get_trophies(TROPHIES_1PL_LOT, user_trophies)
    count_lot = 12 - sum([1 for x in trophies if not x[1]])
    seed, rolled_tags = get_seed()

    if not seed:
        return add_trophies

    tags_to_roll = []

    total_coins = 999

    while total_coins > 170 or total_coins == -1:
        total_coins = coin_sim(copy.deepcopy(trophies), copy.deepcopy(seed), True, max_depth, max_breadth,
                               copy.deepcopy(count_lot))
        if total_coins < 170 and total_coins != -1:
            break
        seed = (214013 * seed + 2531011) & 4294967295
        tag_roll = (145 * (seed >> 16)) >> 16
        while tag_roll in rolled_tags:
            seed = (214013 * seed + 2531011) & 4294967295
            tag_roll = (145 * (seed >> 16)) >> 16
        tags_to_roll.append(TAGS[tag_roll])
        del rolled_tags[0]
        rolled_tags.append(tag_roll)

    close = print_tags(tags_to_roll)

    if close:
        return add_trophies

    coin_sim(copy.deepcopy(trophies), copy.deepcopy(seed), False, max_depth, max_breadth, copy.deepcopy(count_lot))

    return add_trophies

    # if debug:
    #     total_coins = coin_sim(copy.deepcopy(trophies), copy.deepcopy(seed),
    #     True, max_depth, max_breadth, copy.deepcopy(count_lot))
    #     print(f"Iteration {iteration} done! Coins spent: ", total_coins)
    #     log_total_coins_spent(total_coins)
