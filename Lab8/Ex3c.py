import random

def make_pairs(n):
    pairs = []
    for a in range(1, n + 1):
        for b in range(a + 1, n + 1):
            pairs.append((a, b))
    random.shuffle(pairs)
    return pairs

def shuffle_pick(student_id, pairs):
    return pairs[(student_id - 10000000) % len(pairs)]

pairs = make_pairs(7)
print(shuffle_pick(12345678, pairs))
