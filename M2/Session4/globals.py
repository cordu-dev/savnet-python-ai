global_var = 55


def do_something():
    # Example of shadowing a global variable
    global_var = 44
    global_var += 1
    print(global_var)


do_something()

print(global_var)
