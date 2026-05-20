list_1 = [x for x in range(5)]


def raise_two_to_the_power_of(x):
    return 2**x


the_map = map(lambda x: 2**x, list_1)

print(the_map)
list_2 = list(the_map)
print(list_2)

for x in map(lambda x: x * x, list_2):
    print(x, end=" ")
print()
