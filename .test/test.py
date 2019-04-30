# import time

# def round_trip(limit):
#     a = time.time()
#     for i in range(limit):
#         for j in range(limit):
#             pass
#     b = time.time()
#     print(limit, b - a)

# for limit in range(0, 10000, 1000):
#     round_trip(limit)
import random

x = [i for i in range(10)]

y = random.shuffle(x)

print(x)