coordinates_x = (11, 22, 33)
coordinates_y = (8, 6, 5)


def do_something_complicated(x, y):
    return 2 ** (x + y)


gen = map(lambda x, y: 2 ** (x + y), coordinates_x, coordinates_y)
# gen = map(do_something_complicated, coordinates_x, coordinates_y)

print(list(gen))
