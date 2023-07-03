from timeit import default_timer as timer
from tagrss import TagRss, generate_tags, rand_int, MAXINT, next

def performance_test():
    misses = []
    stats_start = timer()
    seeds = 0
    maxtime = 0.0
    lb = 1
    ub = MAXINT

    for i in range(lb, ub, 5000001):
        samples, curr = generate_tags(i)
        print("reversing seed:", i, "   taglist:", samples)
        start = timer()
        res = TagRss(samples)
        if len(res) == 0:
            misses.append(i)

        print("reversing result:",res)

        end = timer()
        interv = end - start
        if interv > maxtime:
            maxtime = interv

        print("\nSearch_time:", interv, "\n\n\n")
        seeds += 1

    end = timer()
    total = end - stats_start
    print("\n\n\nSeeds reversed:", seeds)
    print("\n\n\nTotal_time:", total)
    print("average time:", total / seeds)
    print("worst time:", maxtime)
    print("list of failed seed reverses:", misses)
def main():
   performance_test()

if __name__ == '__main__':
    main()