# Original work by Savestate
# Some of this code is adapted from gainge aka Judge9

from typing import Optional

# The following global values and constants are provided by Savestate, and the functions are slightly adapted from Savestate and Judge9
#@804d5f90
rng = 0x00000001
a = 214013
c = 2531011
m = 4294967295

def get_rng() -> int:
    global rng
    return rng

def set_rng(val: int) -> None :
    global rng
    rng = val

# LCG:
# a = 214013
# c = 2531011
# m = 2^32 - 1 -> cuz im using & instead of %, which makes the program more optimized, (thanks to TauKhan for the tip!!)
# Inputs:
# `@custom` is an int passed in to compute the next rng value after the custom value, unsaved. Defaults to -1, which will use the actual rng value and save it.
def next_rng(custom_rng_val: int = -1) -> int:
    if custom_rng_val == -1:
        global rng
        rng = (a*rng + c) & m
        return rng
    else:
        ret = (a*custom_rng_val + c) & m
        return ret

def get_rand_int(i: int, adv = True) -> int:
    temp_rng = next_rng() if adv else get_rng()
    top_bits = temp_rng >> 16
    return (i*top_bits) >> 16

def get_rand_float() -> int:
    temp_rng = next_rng()
    top_bits = temp_rng >> 16
    return top_bits / 65536

# this function is adapted from judge9
def rng_diff(src: int, tgt: int) -> int:
    if src == tgt:
        return 0
    
    step = 0
    temp_src = src
    temp_tgt = tgt
    
    while temp_src != tgt and temp_tgt != src:
        temp_src = next_rng(temp_src)
        temp_tgt = next_rng(temp_tgt)
        step += 1
    
    return step if temp_src == tgt else -1 * step

# The following functions are all made by myself.
# The code in the `old_code.py.example` file is a mix of my own and some from judge9.

def get_hex(tgt: Optional[int] = None) -> int:
    while True:
        # Get initial input
        val = input("Source RNG value: ") if tgt is not None else input("Target RNG value: ")
        val = val.replace(" ", "")
        
        if val.lower() == 'q': # Escape option
            print("Exiting.")
            quit(0)
        elif val.lower() == 'c' and tgt is not None: # Continue by using old tgt as new src
            if tgt == -1:
                print("Cannot continue off of previous value because you just started.")
            else:
                return tgt
        else:
            try:
                return int(val, 16)
            except ValueError:
                print(f'Invalid input: \'{val}\'.')

def use_coin() -> int:
    # This looks funny, but we're returning the rng value generated here at the end.
    next_rng()
    next_rng()
    return next_rng()

# this function helps to compute the coefficient and constant for a variable number of steps in the LCG without having to call `advance_seed()` a bunch
# this way, i can just hard-code numbers instead of doing the super long modular arithmetic that i did in an earlier version
# also this is all thanks to TauKhan again because i couldn't understand how the linear transformations worked hehe :))))
# inputs:
#   `s` = seed
#   `i` = number of times that the seed should be advanced
# returns: an integer
# how to use: 
#   coefficient = advance_star(1, i) - advance_star(0, i)
#   constant = advance_star(0, i)
def advance_star(s: int, i: int) -> int:
    # numbers grabbed from the LCG function at the top of the file
    for _ in range(i):
        s = (214013 * s + 2531011) & 4294967295
    
    return s

# Lottery simulator
def lotto_sim(num_owned_trophies: int, num_remaining_1p_lotto: int, src: int, trophies: list[list[str, int, bool]]) -> None:
    NUM_AVAILABLE_TROPHIES = 84
    set_rng(src)
    
    # Overall stats
    total_coins = 0
    resets = 0
    
    # Now we can start the lottery simulation.
    print(f'Beginning lottery simulation with seed {hex(src)}')
    while num_remaining_1p_lotto > 0:
        # The purpose of the first call is just to randomize the position of the coin animation as it decreases to 00.
        get_rand_int(15)
        
        # Setting up variables to be used in the coin loop
        temp_rng = src = get_rng()
        coins = 0
        first_outcome_index = -1
        
        # The coin loop; determines how many coins to use to 1) get a trophy and 2) ensure that the trophy is in the 1p/lotto category
        while True:
            coins += 1
            
            # If we have to use more than 20 coins, just spend one to update the rng value and move on.
            if coins > 20:
                # Updating counters
                resets += 1
                total_coins += 1
                
                # Because we're just going to spend one coin, we can use the pre-computed first outcome.
                if first_outcome_index == -1:
                    print(f'Reset #{resets}. No ideal outcome. Just spend 1 coin to get a dupe trophy.')
                else:
                    print(f'Reset #{resets}. No ideal outcome. Just spend 1 coin to get '
                          f'{trophies[first_outcome_index][0]}')
                    trophies[first_outcome_index][1] = 0
                    num_owned_trophies += 1
                # Now we want to spend the one coin.
                # Before we can do that, remember that we already advanced the rng by a total of 20 coins.
                # So we need to reset our rng to the correct position.
                set_rng(src)
                use_coin()
                next_rng()
                next_rng()
                break

            # set rng to be src each time at the beginning
            set_rng(temp_rng)
            
            # 3 steps are called per coin. 
            temp_rng = use_coin()
            
            # Now the game determines whether this roll is sucessful or not. This changes depending on the following formula
            success_roll = get_rand_int(100)
            rem_trophies = NUM_AVAILABLE_TROPHIES - num_owned_trophies
            chance = int((rem_trophies / NUM_AVAILABLE_TROPHIES) * 100)
            if success_roll < chance:
                # In this case, we get a new trophy.
                trophy_roll_rand_int = get_rand_int(rem_trophies)
                # The actual trophy that we roll is found by only counting through trophies that we dont have owned.
                # For example, if we roll `15` (0-indexed), then the actual trophy that we get is not just the `15`th trophy (0-indexed), but it's the `15`th (0-indexed) *unowned* trophy.
                # We'll use `trophy_roll_actual_index` to store the actual index of the trophy that we roll in the big Trophies list above.
                # And we'll reuse `trophy_roll_rand_int` as a counter to let us know when we've gone through that number of unowned trophies.
                trophy_roll_actual_index = -1
                for t in trophies:
                    trophy_roll_actual_index += 1
                    if t[1] == 1:
                        trophy_roll_rand_int -= 1
                        if trophy_roll_rand_int == -1:
                            break
                # At the end of this loop, `trophy_roll_actual_index` should give us the index of the trophy in the big
                # Trophies list that we actually rolled, and not just `get_rand_int(x)`.
                # If the boolean field in the trophies tuple is True and it is not owned, then we want to use this
                # number of coins.
                if trophies[trophy_roll_actual_index][2] and trophies[trophy_roll_actual_index][1] == 1:
                    print(f'{coins} -> {trophies[trophy_roll_actual_index][0]}')
                    # Mark that we now own the trophy and update counters.
                    trophies[trophy_roll_actual_index][1] = 0
                    num_owned_trophies += 1
                    num_remaining_1p_lotto -= 1
                    total_coins += coins
                    break
                elif coins == 1:
                    first_outcome_index = trophy_roll_actual_index
                # Note that we don't use an else case here, because we did not get a trophy in the 1p/lotto category,
                # so we loop again.
            # Similarly, we don't use an else case here because we did not get a new trophy, so we loop again.
        # Now, the game advances the RNG one more time to determine the pose of the received trophy.
        next_rng()
    
    print('-------------------------------')
    print('Results')
    print('-------------------------------')
    print(f'Total trophies collected: {num_owned_trophies}')
    print(f'Total number of resets: {resets}')
    print(f'Total coins spent {total_coins}')

# Simple function to append to a string depending on some trophy flags
def trophy_str(t: list[str, int, bool]) -> str:
    ret = f'- {t[0]} '
    if t[1] == 0:
        ret += f' (owned)|'
    else:
        ret += f' (new)|'
    return ret

def pmain():
    # Initial trophy list: [trophy_name, not_owned=1/owned=0]
    trophies = [['Ray Gun', 1], ['Super Scope', 1], ['Fire Flower', 1], ['Star Rod', 1], ['Home-Run Bat', 1],
                ['Fan', 1], ['Hammer', 1], ['Red Shell', 1], ['Flipper', 1], ['Mr. Saturn', 1], ['Bob-omb', 1],
                ['Super Mushroom', 1], ['Poison Mushroom', 1], ['Starman 64', 1], ['Cloaking Device', 1],
                ['Barrel Cannon', 1], ['Party Ball', 1], ['Crate', 1], ['Barrel', 1], ['Capsule', 1], ['Egg', 1],
                ['Poké Ball', 1], ['Venusaur', 1], ['Squirtle', 1], ['Blastoise', 1], ['Clefairy', 1], ['Weezing', 1],
                ['Chansey', 1], ['Goldeen', 1], ['Snorlax', 1], ['Articuno', 1], ['Zapdos', 1], ['Moltres', 1],
                ['Chikorita', 1], ['Cyndaquil', 1], ['Togepi', 1], ['Bellossom', 1], ['Wobbuffet', 1], ['Scizor', 1],
                ['Porygon2', 1], ['Raikou', 1], ['Suicune', 1], ['Lugia', 1], ['Ho-oh', 1], ['Toad', 1], ['Coin', 1],
                ['Megavitamins', 1], ['Kirby Hat 1', 1], ['Kirby Hat 2', 1], ['Kirby Hat 3', 1],
                ['Princess Peach\'s Castle', 1], ['Lakitu', 1], ['Pidgit', 1], ['Birdo', 1], ['Klap Trap', 1],
                ['Shy Guys', 1], ['Pak E. Derm', 1], ['Tingle', 1], ['Moon', 1], ['Turtle', 1], ['Arwing', 1],
                ['Great Fox', 1], ['Peppy Hare', 1], ['Slippy Toad', 1], ['Chozo Statue', 1], ['Whispy Woods', 1],
                ['Fountain of Dreams', 1], ['Pokémon Stadium', 1], ['Koopa Troopa', 1], ['Topi', 1], ['Polar Bear', 1],
                ['Metal Mario', 1], ['Daisy', 1], ['Thwomp', 1], ['Boo', 1], ['Bucket', 1], ['Racing Kart', 1],
                ['Baby Mario', 1], ['Baby Bowser', 1], ['Raphael Raven', 1], ['Dixie Kong', 1], ['King K. Rool', 1],
                ['Ocarina of Time', 1], ['Samurai Goroh', 1], ['Dr. Stewart', 1], ['Jody Summer', 1], ['Andross', 1],
                ['Andross 64', 1], ['Metroid', 1], ['Ridley', 1], ['Fighter Kirby', 1], ['Ball Kirby', 1],
                ['Waddle Dee', 1], ['King Dedede', 1], ['Rick', 1], ['Gooey', 1], ['Meta-Knight', 1], ['Jeff', 1],
                ['Poo', 1], ['Starman EB', 1], ['Bulbasaur', 1], ['Poliwhirl', 1], ['Ditto', 1], ['Eevee', 1],
                ['Totodile', 1], ['Crobat', 1], ['Igglybuff', 1], ['Steelix', 1], ['Heracross', 1],
                ['Professor Oak', 1], ['Misty', 1], ['ZERO-ONE', 1], ['Maruo Maruhige', 1], ['Ryota Hayami', 1],
                ['Kensuke Kimachi', 1], ['Hate Giant', 1], ['Ray Mk II', 1], ['Bayonette', 1], ['Annie', 1],
                ['Totakeke', 1], ['Heririn', 1], ['Alpha', 1], ['Vacuum Luigi', 1], ['Pikmin', 1],
                ['Excitebike', 1], ['Ducks', 1], ['Bubbles', 1], ['Eggplant Man', 1], ['Balloon Fighter', 1],
                ['Stanley', 1], ['Dr. Wright', 1], ['Donbe & Hikari', 1], ['Monster', 1]]

    Extras = [[71, ['Raccoon Mario', 1]], [72, ['Waluigi', 1]],
              [74, ['Koopa Clown Car', 1]], [len(trophies), ['GCN', 1]]]

    #TODO:
    # Ask user for total trophies they own. (Inform user information must be correct)
    # Mark trophies obtained by checking the user's inputted trophies.
    # Get rid of unnecessary code.
    # When they get to 250 trophies, tell the user to back out of lotto to get new trophies.
    #   Figure out if rng changes when final four trophies get added.
    # Update existing rng to find the lowest amount of rng steps to find next trophy.
    #   Dynamically update based on user input
    #   If 1-20 coins doesn't work, check the next successful trophy roll and see if it is possible to get that with a
    #       a combination of coin amounts (i.e. [1, 1])
    #   Update rng as user is allowed input (Might not be implemented)
    # Make application windows to display lotto stuff.
    #   Initial lotto rng stuff
    #       Ask user what trophy was collected and add it if new trophy automatically
    #   Trophy to be gotten
    #       Asking user if done correctly (and asking what the trophy was if not)
    #       Total coins needed to spend and order of coin spends
    #       Image of trophy as well as the trophy name
    #   All trophies gotten window
    #   Break flags if user wants to stop for any reason

    # the game starts off with 1 trophy already owned.
    num_owned_trophies = 0
    #num_remaining_trohies
    NUM_AVAILABLE_TROPHIES = len(trophies) + 4

    # Now begins the RSS for lotto section.
    # Here, the idea is that the user will spend x coins on the lottery to receive some trophies.
    # There are 2 visual aspects of each roll that we can use:
    #   The roll's success (aka new trophy is rolled, or an old trophy is rolled)
    #   The actual trophy received
    # Both of these outcomes can help us to find whatever seed we're currently at.
    # The ideal outcome would be that the first roll is rejected, as that would significantly cut down on the portion of seeds to calculate.
    # The initial basic algorithm was to just test every seed, but this will be improved upon as described below
    # Before we do that though, we need to collect the user's input.
    possible_seeds = []
    get_rand_int_100_range = [42991616, 85917696, 128909312, 171835392, 214761472, 257753088, 300679168, 343605248, 386596864, 429522944, 472449024, 515440640, 558366720, 
                              601358336, 644284416, 687210496, 730202112, 773128192, 816054272, 859045888, 901971968, 944898048, 987889664, 1030815744, 1073741824, 1116733440, 
                              1159659520, 1202651136, 1245577216, 1288503296, 1331494912, 1374420992, 1417347072, 1460338688, 1503264768, 1546190848, 1589182464, 1632108544, 
                              1675100160, 1718026240, 1760952320, 1803943936, 1846870016, 1889796096, 1932787712, 1975713792, 2018639872, 2061631488, 2104557568, 2147483648, 
                              2190475264, 2233401344, 2276392960, 2319319040, 2362245120, 2405236736, 2448162816, 2491088896, 2534080512, 2577006592, 2619932672, 2662924288, 
                              2705850368, 2748841984, 2791768064, 2834694144, 2877685760, 2920611840, 2963537920, 3006529536, 3049455616, 3092381696, 3135373312, 3178299392, 
                              3221225472, 3264217088, 3307143168, 3350134784, 3393060864, 3435986944, 3478978560, 3521904640, 3564830720, 3607822336, 3650748416, 3693674496, 
                              3736666112, 3779592192, 3822583808, 3865509888, 3908435968, 3951427584, 3994353664, 4037279744, 4080271360, 4123197440, 4166123520, 4209115136, 
                              4252041216, 4294967295]
    
    print("Input the results of using the lottery.")
    while len(possible_seeds) != 1:
        trophy_roll_name = input("Trophy received from lotto:\n")
        successful = False
        
        found = False
        trophy_roll_int = -1
        orig_owned_trophies = num_owned_trophies
        
        # Validating trophy received from lotto and updating counters/flags
        while not found:
            multiple_trophies = ''
            substr_matches = 0
            for i, t in enumerate(trophies):
                # `trophy_roll_int` is a counter to help figure out what the result of the get_rand_int() function as
                # we only get the actual trophy name.
                # Because the field at t[1] is 1 if we own it, and is 0 otherwise, then we know that if the roll is a
                # new trophy, then the sum of the t[1] values will tell us what index we're at since it "skips"
                # counting the trophies that are already owned.
                trophy_roll_int += t[1]
                exact_match = False
                
                if trophy_roll_name in t[0]:
                    exact_match = trophy_roll_name == t[0]
                    if not exact_match:
                        multiple_trophies += trophy_str(t)
                        substr_matches += 1
                        # Check if there are other trophies with the same substring.
                        for t_ in trophies[i+1:]:
                            if trophy_roll_name in t_[0]:
                                if trophy_roll_name == t_[0]:
                                    exact_match = True
                                multiple_trophies += trophy_str(t_)
                        # If so, then do not proceed; break immediately and reprompt.
                        if not exact_match and substr_matches > 1:
                            multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                            trophy_roll_name = input(f"These trophies contain the substring '{trophy_roll_name}':\n{multiple_trophies}\nPlease retype the trophy name:")
                            break
                        if exact_match:
                            continue
                    # If the trophy is not owned yet, then the roll is 'succesful' as it's a new trophy.
                    successful = t[1] == 1
                    if successful:
                        t[1] = 0
                        num_owned_trophies += 1
                        if t[2]:
                            num_remaining_1p_lotto -= 1
                    else:
                        # On the other hand, if the trophy is owned, then we know that it must be the `i - trophy_roll_int - 1`th unowned trophy.
                        trophy_roll_int = i - trophy_roll_int - 1
                    print(f'{t[0]} collected!')
                    found = True
                    break
            # If the trophy was not found at all, then the user must be reprompted.
            if not found:
                print(f'Could not find {trophy_roll_name}')
                trophy_roll_name = input("Trophy received from lotto:\n")
        
        trophy_roll_cond_amt = NUM_AVAILABLE_TROPHIES - orig_owned_trophies if successful else orig_owned_trophies
        chance = int((trophy_roll_cond_amt / NUM_AVAILABLE_TROPHIES) * 100)
        
        # As a preliminary filter for ruling out a large number of seeds, we can simply precalculate which seeds
        # when advanced 4 times, would return an integer less than `chance` when `get_rand_int(100)` is called.
        # We can then further filter this by checking the very next value and seeing if that returns the integer
        # that corresponds with `trophy_roll_int`, which is given by running `get_rand_int(trophy_roll_cond_amt)`.
        
        # If this is the first run, then we need to filter out the possible RNG values from the impossible ones.
        # Instead of computing the output of each possibility, we can instead used a pre-computed range that corresponds
        # to the possible integers that are output by `get_rand_int(100)`. Then, we can simply iterate over all those values
        # and see which ones would give the correct `trophy_roll_int`.
        
        # On the first run, we need to populate `possible_seeds` with only the seeds that could belong in it.
        # Note that we use 3 lists here, the original `possible_seeds` list will be used throughout loops, the `temp_possible_seeds` 
        # will be used after filtering for success/failure, and the `new_possible_seeds` will be used to store the new list of seeds 
        # after each seed has also been filtered for the `trophy_roll_int` and also prepped for the next loop.
        new_possible_seeds = []
        temp_possible_seeds = []
        if not len(possible_seeds):
            if successful:
                temp_possible_seeds = range(get_rand_int_100_range[chance])
            else:
                temp_possible_seeds = range(get_rand_int_100_range[chance], get_rand_int_100_range[-1])
        else:
            # In this case, we need to iterate over each seed in the list of possible seeds, advance them 5 times, then determine if that seed
            # would return a value that's less than `get_rand_int_100_range[chance]` if successful, and greater than or equal to 
            # `get_rand_int_100_range[chance]` otherwise.
            # Then, we can do the next filter by advancing the seed once more and checking if the `returned_trophy_int` is equal to the actual
            # `trophy_roll_int` just like the logic above, and then advancing the logic one more time.
            # Because we're advancing the seed 5 times and the function is an LCG, we can just compound the functions.
            # Instead of doing the modular arithmetic that I did previously, we can use a simple linear compounding 
            # function that TauKhan suggested, called `advance_star()`
            if successful:
                for s in possible_seeds:
                    temp_rng = (675975949 * s + 2727824503) & 4294967295
                    if temp_rng < get_rand_int_100_range[chance]:
                        temp_possible_seeds.append(temp_rng)
            else:
                for s in possible_seeds:
                    temp_rng = (675975949 * s + 2727824503) & 4294967295
                    if temp_rng >= get_rand_int_100_range[chance]:
                        temp_possible_seeds.append(temp_rng)
            # I'm aware that a faster and more elegant solution would be to throw in:
            # `if (successful and temp_rng < get_rand_int_100_range[chance]) or (not successful and temp_rng >= get_rand_int_100_range[chance]):
            #    temp_possible_seeds.append(temp_rng)`
            # in just a single loop, under `temp_rng`, but I think that not having to access the variable `successful` a few hundred million times
            # should save some time. It sucks that the code style has to suffer as a result, though.
        # This is the end of the if / else statement above. We can now work on the `temp_possible_seeds` list, as both have
        # seeds which are in line with the success/failure roll.
        # Because these values skip calculating any RNG advancements from the beginning, we know that there are only 
        # 2 more RNG advancements: the trophy roll, and the trophy pose.
        # So, we can just filter on each of these seeds with the conditional: `get_rand_int(trophy_roll_cond_amt) == trophy_roll_int`.
        # And lastly, we need to update each of the seeds in order to keep the seed usable for the next loop.
        # Also confusingly, all the function calls will be re-written here to save on runtime and to decrease overhead at the cost of
        # code legibility, because tbh who even reads this lol
        for s in temp_possible_seeds:
            # Advance the seed once
            temp_rng = (214013 * s + 2531011) & 4294967295
            # Calculate the returned_trophy_int, which is `get_rand_int(trophy_roll_cond_amt)`
            returned_trophy_int = (trophy_roll_cond_amt * (temp_rng >> 16)) >> 16
            # Check the conditional as mentioned before
            if returned_trophy_int == trophy_roll_int:
                # Append the seed advanced a second time so that the value will be usable for the next while loop
                new_possible_seeds.append((214013 * temp_rng + 2531011) & 4294967295)
        # Now we replace the old list with the new one.
        possible_seeds = new_possible_seeds
        
        # The last thing to note is that the stuff above *is* the RSS algorithm and it is being done within this loop, as opposed to
        # passing it to another function. Part of the reason why it looks so confusing is because it's extremely computation heavy, so I decided
        # to try to optimize it pretty hard.
        
        print(f'num of possible seeds: {len(possible_seeds)}')
        
        if len(possible_seeds) == 0:
            print('No seeds found, either there\'s a bug or you misinput something. Try rerunning the program and be careful with your inputs.')
            quit()
    
    print(f'The current seed is: {possible_seeds[0]}')
    # Now that we have exactly 1 seed, we can now run the lottery simulator.
    lotto_sim(num_owned_trophies, num_remaining_1p_lotto, possible_seeds[0], trophies)
    print('\nProgram finished. At the moment, there is no course correction, so please try to input the correct trophies!')

def main():
    # gets the number of steps between seeds
    while True:
        src = get_hex()
        tgt = get_hex()
        print(rng_diff(src, tgt))

# def main():
#     temp = advance_star(0, 26)
#     print(f'coefficient for 26 = {advance_star(1, 26) - temp}')
#     print(f'constant for 26 = {temp}')


if __name__ == "__main__":
    main()