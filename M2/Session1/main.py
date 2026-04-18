from pprint import pprint

import math as m
from package1 import utils as u

# pagage > package ... > module > functions / classes / consts
from package1.package_nested import goldmine
# from package1.package_nested.goldmine import miner

just_for_fun = goldmine.miner()

the_sum = u.add_two_nbumbers(5, 6)

some_sin = m.sin(55)
some_cos = m.cos(11)

some_special_sin = u.sin(999)

print(some_sin)
print(some_cos)
print(the_sum)
print(m.pi)


# pprint(dir(m))
