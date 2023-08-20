from All_Trophies_RNG.tagrss import TagRss
import globals

# I really should figure out a better way to implement this
# instead of copy-pasting this for each new file
rng = 0x00000001

TAGS = globals.TAGS


def get_rng() -> int:
    global rng
    return rng


def set_rng(val: int) -> None:
    global rng
    rng = val


def next_rng(custom_rng_val: int = -1) -> int:
    if custom_rng_val == -1:
        global rng
        rng = (214013*rng + 2531011) & 4294967295
        return rng
    else:
        ret = (214013*custom_rng_val + 2531011) & 4294967295
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


def check_buckets(trophy: str, buckets: list[list[str]], delete: bool = True) -> (list[list[str]], list[str]):
    rem = []
    for i, b in enumerate(buckets):
        for j, t in enumerate(b):
            if trophy == t:
                if delete:
                    del b[j]
                    if not len(b):
                        del buckets[i]
                else:
                    rem = buckets[i]
                return buckets, rem


"""
def input_trophies_owned(prompt: str = "Type the names of the trophies that you've collected in the gallery. "
                                       "Substrings are allowed, but be careful. Type 'x' or 'q' to finish.\n",
                         trophies: list[str] = None,
                         buckets: list[list[str]] = None
                         ) -> (list[str], list[list[str]]):
    
    input_trophy = input(prompt)
    if not input_trophy:
        return trophies
    while input_trophy.lower() != 'x' and input_trophy.lower() != 'q':
        confirmed = False
        misinput = False
        multiple_trophies = ''
        substr_matches = False
        
        for i, t in enumerate(trophies):
            exact_match = False
            
            if input_trophy in t:
                exact_match = input_trophy == t
                if not exact_match:
                    multiple_trophies += trophy_str(t)
                    # Check if there are other trophies with the same substring.
                    for t_forward in trophies[i+1:]:
                        if input_trophy in t_forward:
                            exact_match = input_trophy == t_forward
                            multiple_trophies += trophy_str(t_forward)
                            substr_matches = True
                    # If so, then do not proceed; break immediately and reprompt.
                    if not exact_match and substr_matches:
                        multiple_trophies = multiple_trophies[:-1].replace("|", "\n")
                        print(f"These trophies contain the substring '{input_trophy}':\n{multiple_trophies}"
                              f"\nPlease retype the trophy name.")
                        break
                    if exact_match:
                        continue
                trophies, buckets, confirmed = confirm_trophy(roll=i, trophies=trophies, buckets=buckets)
                if confirmed:
                    break
                else:
                    misinput = True
        else:
            if not confirmed:
                print(f'Did not collect {input_trophy}.')
            elif misinput:
                print(f'User misinput detected, please re-input the trophy you received.')
        input_trophy = input("Trophy name (x or q to quit):\n")
    
    return trophies, buckets
"""


def confirm_trophy(roll: int, trophies: list[str], buckets: list[list[str]]) -> (list[str], list[list[str]], bool):
    confirmed = not input(f"Confirm {trophies[roll].upper()} trophy? Hit [ENTER] if yes, otherwise input a character."
                          f"\n")
    if confirmed:
        print(f"Confirmed that you received {trophies[roll]}.")
        buckets, _ = check_buckets(trophies[roll], buckets=buckets)
        del trophies[roll]
    return trophies, buckets, confirmed


def input_tag(rolled_tags: list[str]) -> list[int]:
    global TAGS
    new_tag = input(f"tag #{len(rolled_tags) + 1}: ")
    if new_tag.upper() in TAGS:
        rolled_tags.append(TAGS.index(new_tag.upper()))
    else:
        print('Invalid tag, probably a typo')
    return rolled_tags


def find_ideal_seed(trophies: list[str], temp_seed: int = -1, num_advances: int = 0) -> (int, int, int):
    trophy_stage_roll = -1
    # position_roll = -1
    while True:
        # Advance seed for success/failure roll, and check that it passes (the return value is `< 60`.)
        # 24 advances plus 1 from `get_rand_int(100)`.
        success_roll = (100 * ((-1190463139 * temp_seed + 3357146299) & 4294967295) >> 16) >> 16
        if success_roll < 65:  # sometimes this is 65, not sure what the cause for this is though.
            # Advance seed for trophy roll, and check that it's a 1PO trophy
            # (the second value of the returned index is `True`)
            # 25 advances plus 1 from
            # `get_rand_int(NUM_AVAILABLE_TROPHIES - num_owned_trophies) == get_rand_int(len(trophies))`
            trophy_stage_roll = ((len(trophies)) * ((-1422735383 * temp_seed + 2234209426) & 4294967295) >> 16) >> 16
            return num_advances, trophy_stage_roll, temp_seed
            # We don't have to check for anything else here since we're assuming all other trophies except for the
            # 1PO trophies are owned.
        temp_seed = (214013 * temp_seed + 2531011) & 4294967295
        num_advances += 1


# this time we're going to have to figure out the order of the trophies for the 1PO+1PL list
def main(owned_trophies):
    # here, we're going to store the trophies list a little differently than in previous implementations
    # instead of keeping track whether a trophy is owned and if a trophy is in the desired category,
    # we can just keep track of if the trophy is 1PO or not.
    from All_Trophies_App.ApplicationButtonFunctions import roll_more_tags, display_adv, fin_adv

    trophies = ['Warp Star', 'Beam Sword', 'Green Shell', 'Freezie', 'Parasol', 'Screw Attack', 'Charizard',
                'Electrode', 'Staryu', 'Marill', 'Vegetable', 'Banzai Bill', 'Four Giants', 'Master Sword',
                'Koopa Paratroopa', 'ReDead', 'Octorok', 'Like Like', 'Plum', 'Viruses', 'Goron', 'Fire Kirby',
                'Paula', 'Cleffa', 'Love Giant', 'Pit', 'Ayumi Tachibana']

    buckets = [['Beam Sword', 'Paula'], ['Freezie', 'Parasol', 'Screw Attack'], ['Ayumi Tachibana', 'Love Giant'],
               ['Staryu', 'Charizard'], ['Like Like', 'ReDead'], ['Four Giants'], ['Plum'],
               ['Cleffa', 'Electrode', 'Marill'], ['Fire Kirby'], ['Banzai Bill', 'Koopa Paratroopa'],
               ['Green Shell'], ['Pit'], ['Vegetable', 'Warp Star'], ['Viruses'], ['Octorok'],
               ['Goron', 'Master Sword']]

    confirmed_trophies = []
    # Get the trophies owned from the gallery
    # trophies, buckets = input_trophies_owned(trophies=trophies, buckets=buckets)

    for trophy in owned_trophies:
        if trophy in trophies:
            trophies.pop(trophy)

    # stage_trophy_spawn_locations = ['first wall', 'low wall', 'on top of the bricks', 'pipe before cliff']
    while len(trophies) > 0:
        rolled_tags, break_flag = roll_more_tags(5)

        if break_flag:
            break

        # tagRSS
        potential_seed = TagRss(rolled_tags)
        
        # if more than one seed, then instruct user to roll more tags (in the future, OCR should be able to grab
        # all the tags for us)
        while len(potential_seed) > 1:
            # print(f"There are {len(potential_seed)} potential seeds, please keep rolling tags as prompted.")
            # rolled_tags = input_tag(rolled_tags=rolled_tags)

            tag, break_flag = roll_more_tags(1)

            if break_flag:
                break

            rolled_tags.append(tag)

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
        
        # At this point, we've figured out what the seed is.
        # Now we want to find an ideal seed.
        # print('Found the current seed, calculating ideal seed...')
        seed = potential_seed[0][2][len(rolled_tags) - 5]
        num_advances, trophy_stage_roll, temp_seed = find_ideal_seed(trophies=trophies, temp_seed=seed)
        
        # here we determine the rng manip path via rolling tags
        # in the future, possibly implement CSS manip path since it should probably take less time
        tags_to_roll = []
        while num_advances != 0:
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
            
            if num_advances != 0:
                num_advances, trophy_stage_roll, temp_seed = find_ideal_seed(trophies=trophies, temp_seed=temp_seed,
                                                                             num_advances=temp_num_advances)
        
        # At this point, we are certain that 1) we know what our current seed is, and 2) we can manipulate the seed
        # to get a desired outcome.
        trophy_name = trophies[trophy_stage_roll]

        # need to check if goomba trophy is desirable or dupe
        _, rem = check_buckets(trophy=trophy_name, buckets=buckets, delete=False)

        goomba_trophies = []
        if len(rem) > 1:
            for t in rem:
                if t != trophy_name:
                    goomba_trophies.append(t)

        to_del, break_flag = display_adv(tags_to_roll, trophy_name, goomba_trophies)

        if break_flag:
            break

        while len(to_del) > 0:
            var = to_del.pop()
            trophies.remove(var)
            confirmed_trophies.append(var)

        if break_flag:
            break

    if len(trophies) == 0:
        fin_adv()

    return confirmed_trophies
