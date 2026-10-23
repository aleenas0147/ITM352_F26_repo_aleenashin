import random

def simple_pick(n):
    reqs = list(range(1, n + 1))
    r1 = random.choice(reqs)
    reqs.remove(r1)
    r2 = random.choice(reqs)
    return r1, r2

print(simple_pick(7))
