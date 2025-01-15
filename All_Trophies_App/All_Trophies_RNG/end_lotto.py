from All_Trophies_App.All_Trophies_RNG.tagrss import TagRss
from All_Trophies_App.ApplicationButtonFunctions import display_lotto


def get_seed() -> (int, [int]):
    from All_Trophies_App.ApplicationButtonFunctions import roll_more_tags

    potential_seed = []
    rolled_tags = []

    while len(potential_seed) != 1:
        rolled_tags, break_flag = roll_more_tags(5)

        if break_flag:
            return None

        potential_seed = TagRss(rolled_tags)

    # I should test the weird case of [l8er, bone, opus, dayz, coop]
    return potential_seed[0][2][len(rolled_tags) - 5]


def main(num_owned_trophies, percent):
    total_available_trophies = 133 + (num_owned_trophies >= 250) * 4
    num_rem_trophies = round(float(percent) / 100 * total_available_trophies) + (num_owned_trophies >= 250) * 4

    seed = get_seed()

    if seed is None:
        return

    # print("\n")
    temp_seed = seed

    succeed = True

    while num_rem_trophies != 0:
        # recalculate the percent chance of getting a new trophy
        if succeed:
            percent = ((total_available_trophies - num_rem_trophies) // total_available_trophies) * 100
        # 2 steps to account for initial rng calls
        temp_seed = (2851891209 * temp_seed + 505908858) & 4294967295
        # find the minimum number of coins needed to get a new trophy from 1 to 20
        for i in range(20):
            # 3 steps to account for a coin being spent
            temp_seed = (-3124220955 * temp_seed + 3539360597) & 4294967295
            # note that the percent will increase by 5 per each coin spent
            if (100 * temp_seed >> 16) >> 16 < (percent + 5 * i):
                # 2 steps to account for ending rng calls
                temp_seed = (2851891209 * temp_seed + 505908858) & 4294967295
                succeed, breaker = display_lotto(i + 1, 0)

                if breaker:
                    break

                if succeed:
                    num_rem_trophies -= 1
                    num_owned_trophies += 1
                    if num_owned_trophies == 250:
                        total_available_trophies = 137
                        num_rem_trophies += 4
                else:
                    seed = get_seed()

                    if seed is None:
                        return

                    temp_seed = seed

                break
        else:
            # none of the 20 coins resulted in a new trophy, so we just spend 1 coin and move on
            temp_seed = (203977589 * seed + 548247209) & 4294967295
            succeed, breaker = display_lotto(1, 1)

            if breaker:
                break

            if not succeed:
                seed = get_seed()

                if seed is None:
                    return

                temp_seed = seed

        if breaker:
            break
