from All_Trophies_App.All_Trophies_RNG.tagrss import *

# no readme for this atm, so ill explain everything in this file
# this assumes that you start on a fresh save of the game; no trophies owned besides the one you start with
# and only the 5 coins that you start on

# TO USE: run the file
# 1: go to gallery and enter the name (or substring) of the trophy that you own
# 2: go to vs mode -> name entry -> NEW -> left, down, down (these inputs will get you to the RANDOM button)
# 3: hit the random button and enter the tag that you get into the program 5 times (so you roll 5 tags total)
# 4a: if you get lucky, then the program will tell you if you can roll certain tags. 
#     roll the number of times it says (it will print the tags to help you along the way)
# 4b: if you don't get lucky, the program will explain why and tell you to reset the run and also reset the script.
# if you have any other questions, please let me know!
# I am also thinking about putting all of this in a big fat loop so that this script doesn't have to be restarted,
# but will hold off for now unless if someone really wants it!

rng = 0x00000001


def get_rng() -> int:
    global rng
    return rng


def set_rng(val: int) -> None:
    global rng
    rng = val


def next_rng(custom_rng_val: int = -1) -> int:
    if custom_rng_val == -1:
        global rng
        rng = (214013 * rng + 2531011) & 4294967295
        return rng
    else:
        ret = (214013 * custom_rng_val + 2531011) & 4294967295
        return ret


def get_rand_int(i: int, adv=True) -> int:
    temp_rng = next_rng() if adv else get_rng()
    top_bits = temp_rng >> 16
    return (i * top_bits) >> 16


def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t[0]} '
    if t[1] == 0:
        ret += f' (owned)|'
    else:
        ret += f' (new)|'
    return ret


# returns num_advances, coins_to_spend, and seed
def find_ideal_seed(seed: int, birdo_index: int, num_advances: int = 0) -> (int, int, int):
    temp_rng = (214013 * seed + 2531011) & 4294967295

    while True:
        for i in range(1, 6):
            # 3 steps per coin
            temp_rng = (-3124220955 * temp_rng + 3539360597) & 4294967295
            # int((83 / 84) * 100) = 98; this is the success roll
            temp_roll_rng = (214013 * temp_rng + 2531011) & 4294967295
            if ((100 * (temp_roll_rng >> 16)) >> 16) < 98:
                # this is the actual trophy roll
                temp_roll_rng = (214013 * temp_roll_rng + 2531011) & 4294967295

                # the math stuff is the trophy roll index
                if ((83 * (temp_roll_rng >> 16)) >> 16) == birdo_index:
                    return num_advances, i, seed
        else:
            # if we get through the for-loop and don't find birdo then add to the number of advances
            num_advances += 1
            if num_advances > 1000:
                print('this seed requires over 1000 steps; just reset and try again :(')
                quit()
            # advance rng by 1 step and see if it works
            const = 0
            coeff = 1
            for _ in range(num_advances):
                const = (214013 * const + 2531011) & 4294967295
                coeff = (214013 * coeff + 2531011) & 4294967295
            coeff = coeff - const
            temp_rng = (coeff * seed + const) & 4294967295


def main(owned_trophies):
    from All_Trophies_App.ApplicationButtonFunctions import roll_more_tags, display_birdo

    # Initial trophy list: [trophy_name]
    trophies = {'Ray Gun', 'Super Scope', 'Fire Flower', 'Star Rod', 'Home-Run Bat', 'Fan', 'Red Shell', 'Flipper',
                'Mr. Saturn', 'Bob-omb', 'Super Mushroom', 'Starman 64', 'Barrel Cannon', 'Party Ball', 'Crate',
                'Barrel', 'Capsule', 'Egg', 'Squirtle', 'Blastoise', 'Clefairy', 'Weezing', 'Chansey', 'Goldeen',
                'Snorlax', 'Chikorita', 'Cyndaquil', 'Bellossom', 'Wobbuffet', 'Scizor', 'Porygon 2', 'Toad', 'Coin',
                'Kirby Hat 1', 'Kirby Hat 2', 'Kirby Hat 3', 'Lakitu'}

    birdo_index = 37

    for trophy in owned_trophies:
        if trophy in trophies:
            birdo_index = 36
            break

    rolled_tags, break_flag = roll_more_tags(5)

    if break_flag:
        return [], break_flag

    # let the user input each of the rolled tags
    potential_seed = TagRss(rolled_tags)

    # if more than one seed, then instruct user to roll more tags (in the future,
    # OCR should be able to grab all the tags for us)
    while len(potential_seed) != 1:
        rolled_tags, break_flag = roll_more_tags(5)

        if break_flag:
            return [], break_flag

        # let the user input each of the rolled tags
        potential_seed = TagRss(rolled_tags)
        """
        if len(potential_seed) == 0:
            rolled_tags = roll_more_tags(5)
        else:
            rolled_tags.append(roll_more_tags(1))

            bad_seeds = []
            # since we're iterating through the list, I don't think we can remove the bad seed from the list,
            # so we keep a list of the bad seeds and remove them later.
            for i, seed in enumerate(potential_seed):
                if seed[1][len(rolled_tags) - 1] != rolled_tags[-1]:
                    # insert at the beginning of the list, so we don't have to reverse the list when deleting
                    # (deleting from the end will prevent deleting wrong indexes.)
                    bad_seeds.insert(0, i)

            for b in bad_seeds:
                del potential_seed[b]
        """
    # if there's only one seed, then we can move on ahead
    # run a lotto sim to figure out if we can get birdo in the first 5 coins
    # if it's not possible, then advance seed by 1 until we find a possible seed,
    # and manip via generating tags (and maybe css in the future?)
    seed = potential_seed[0][2][len(rolled_tags) - 5]
    num_advances, coins_to_spend, seed = find_ideal_seed(seed=seed, birdo_index=birdo_index)

    # bring back the rng value back to the seed, so we can figure out if we can get to the desired seed
    # (via the `num_advances`)
    set_rng(seed)

    # at this point we now know how many times to advance and how many coins to spend in the lotto.
    # we just have to tell the user how to advance the seed to the desired seed, using `num_advances`.
    # this means that we need to simulate tagRSS to get to the desired seed, if possible.
    num_advances -= 1
    tags_to_roll = []

    while num_advances != 0:
        tags_to_roll = []
        temp_num_advances = num_advances
        set_rng(seed)
        while num_advances > 0:
            tag_roll = get_rand_int(145)
            num_advances -= 1
            while tag_roll in rolled_tags:
                tag_roll = get_rand_int(145)
                num_advances -= 1
            tags_to_roll.append(TAGS[tag_roll])
            del rolled_tags[0]
            rolled_tags.append(tag_roll)

        # automatically begin looking for an ideal seed if we can't manipulate the RNG to be the correct value
        if num_advances != 0:
            num_advances, coins_to_spend, seed = find_ideal_seed(seed=seed, birdo_index=birdo_index,
                                                                 num_advances=temp_num_advances)

    return display_birdo(tags_to_roll, coins_to_spend, len(tags_to_roll))
