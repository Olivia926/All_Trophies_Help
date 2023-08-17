from All_Trophies_RNG.tagrss import *

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
        print(f"{type(SEEDMULT)}\n{type(rng)}\n{type(MAXINT)}")
        rng = (SEEDMULT*rng + SEEDCONST) & MAXINT
        return rng
    else:
        ret = (SEEDMULT*custom_rng_val + SEEDCONST) & MAXINT
        return ret


def get_rand_int(i: int, adv=True) -> int:
    temp_rng = next_rng() if adv else get_rng()
    top_bits = temp_rng >> 16
    return (i*top_bits) >> 16


def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t[0]} '
    if t[1] == 0:
        ret += f' (owned)|'
    else:
        ret += f' (new)|'
    return ret


def main(rolled_tags, owned_trophies):
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

    potential_seed = TagRss(rolled_tags)
    
    # if there's only one seed, then we can move on ahead
    if len(potential_seed) == 1:
        print('found a seed, now calculating rng manip path...')
        # run a lotto sim to figure out if we can get birdo in the first 5 coins
        # if it's not possible, then advance seed by 1 until we find a possible seed, and manip via generating tags
        # (and maybe css in the future?)
        seed = potential_seed[0][2]
        set_rng(seed)
        next_rng()
        # this is the seed that we want to get to, if we can find it in a reasonable amount of time
        found_seed = False
        num_advances = 0
        coins_to_spend = 0
        tags_to_roll = []
        temp_rng = get_rng()
        
        while not found_seed:
            for i in range(1, 6):
                set_rng(temp_rng)
                # 3 per coin
                next_rng(), next_rng(), next_rng()
                temp_rng = get_rng()
                # int((83 / 84) * 100) = 98; this is the success roll
                if get_rand_int(100) < 98:
                    # this is the actual trophy roll
                    trophy_roll_rand_int = get_rand_int(83)
                    
                    if trophy_roll_rand_int == birdo_index:
                        coins_to_spend = i
                        found_seed = True
                        break
            else:
                # if we get through the for-loop and don't find birdo then add to the number of advances
                num_advances += 1
                if num_advances > 100:
                    print('this seed requires over 100 steps; just reset and try again :(')
                    quit()
                # advance rng by 1 step and see if it works
                set_rng(seed)
                for _ in range(num_advances):
                    next_rng()
                temp_rng = get_rng()
                # ideal_seed = previous(get_rng())
        
        # bring back the rng value back to the seed, so we can figure out if we can get to the desired seed
        # (via the `num_advances`)
        set_rng(seed)
        
        # at this point we now know how many times to advance and how many coins to spend in the lotto.
        # we just have to tell the user how to advance the seed to the desired seed, using `num_advances`.
        # this means that we need to simulate tagRSS to get to the desired seed, if possible.
        temp_num_advances = 1
        while temp_num_advances < num_advances:
            tag_roll = get_rand_int(145)
            temp_num_advances += 1
            while tag_roll in rolled_tags:
                tag_roll = get_rand_int(145)
                temp_num_advances += 1
            tags_to_roll.append(TAGS[tag_roll])
            rolled_tags.pop(0)
            rolled_tags.append(tag_roll)
        
        if temp_num_advances == num_advances:
            if len(tags_to_roll) == 0:
                print('NO ROLLS NECESSARY!!!')
            else:
                print(f'ok now u gotta roll {len(tags_to_roll)} tags, good luck o7\n')
                for t in tags_to_roll:
                    print(t)
                print('\n##### OK STOP NOW #####')
                # print(f'seed after manip: {get_rng()}')
            print(f'COINS TO SPEND IN LOTTO: {coins_to_spend}')
        else:
            print('unlucky rng means that things don\'t align nicely here :/ reset run and restart the script')
    else:
        print('well tagRSS couldn\'t find your seed so... just reset and restart the script')
