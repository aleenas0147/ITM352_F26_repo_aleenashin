def flow_pick(student_id, n):
    digits = [int(d) for d in str(student_id)]
    first = sum(digits) % n + 1
    product = 1
    for d in digits:
        if d != 0:
            product = product * d
    second = product % n + 1
    while first == second:
        second = second % n + 1
    return first, second

print(flow_pick(12345678, 7))