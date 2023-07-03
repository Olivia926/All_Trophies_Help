# import numpy as np
import copy

# order should be [[rng_steps_added, coins_needed]]
coin_vals = []
order_arr = []


def find_rng_coin_val(rng):
    global coin_vals
    global order_arr
    size = len(coin_vals)

    for j in range(size):
        if rng == coin_vals[j][0]:
            return -1
        elif rng < coin_vals[j][0]:
            return j

    return len(coin_vals)


def find_rng_own(rng, arr):
    size = len(arr)

    for j in range(size):
        if rng == arr[j][0]:
            return -1
        elif rng < arr[j][0]:
            return j

    return len(arr)


def next_rng_steps(val, num):
    global coin_vals
    global order_arr

    temp_coins = []
    temp_order = []

    rng = start_rng_steps(val)[0]
    size = len(coin_vals)

    ind_new_arr = 0

    for i in range(size):
        if len(order_arr[i]) > num:
            pass
        else:
            total_coins = val + coin_vals[i][1]
            total_rng = rng + coin_vals[i][0]
            ind = find_rng_coin_val(total_rng)

            if ind != -1:
                ind2 = find_rng_own(total_rng, temp_coins)
                if ind2 != -1:
                    order = copy.copy(order_arr[i])
                    order.append(val)
                    temp_coins.insert(ind2, [total_rng, total_coins, ind_new_arr+ind])
                    temp_order.insert(ind2, order)

                    ind_new_arr += 1

    for i in range(len(temp_coins)):
        coin_vals.insert(temp_coins[i][2], [temp_coins[i][0], temp_coins[i][1]])
        order_arr.insert(temp_coins[i][2], temp_order[i])


def find_next_steps(max_order):
    for i in range(max_order):
        for j in range(1, 21):
            next_rng_steps(j, i+1)


def start_rng_steps(val):
    rng = 0

    for i in range(val):
        if i == 0:
            rng += 7
        else:
            rng += 3

    return [rng, val]


def main():
    global coin_vals
    global order_arr

    for i in range(1, 21):
        rng, val = start_rng_steps(i)
        coin_vals.append([rng, val])
        order_arr.append([val])

    find_next_steps(3)

    order = copy.copy(order_arr[0])
    order.append(1)

    size = len(order_arr[len(order_arr) - 1])
    size *= 4

    with open('rng_steps.txt', 'w') as f:
        f.write(f'{f"Order":<{size+2}s}{f"RNG Steps":<{12}s}{f"Coins":<{5}s}\n')
        for i in range(len(coin_vals)):
            f.write(f'{f"{order_arr[i]}":<{size + 2}s}{f"{coin_vals[i][0]}":<{12}s}{f"{coin_vals[i][1]}":<{5}s}\n')


if __name__ == "__main__":
    main()
