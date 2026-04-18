from random import random
from platform import machine

for i in range(5):
    print(random())


def something_huge():
    from math import sin

    return 77 * sin(55)


print(machine())
