def outer(par):
    loc = par

    def inner():
        return loc

    return inner


var = 1
fun = outer(var)
print(fun())


some_constant = 55


def do_something():
    print(some_constant)


do_something()
