class PizzaError(Exception):
    def __init__(self, pizza, message):
        Exception.__init__(self, message)
        self.pizza = pizza


class TooMuchCheeseError(PizzaError):
    def __init__(self, pizza, cheese, message):
        PizzaError.__init__(self, pizza, message)
        self.cheese = cheese


def make_pizza(pizza, cheese):
    if pizza not in ["margherita", "capricciosa", "calzone"]:
        raise PizzaError(pizza, "no such pizza on the menu")
    if cheese > 100:
        raise TooMuchCheeseError(pizza, cheese, "too much cheese")
    print("Pizza ready!")


# Point of entry!

for pizza, cheese_qty in [("calzone", 0), ("margherita", 110), ("mafia", 20)]:
    try:
        make_pizza(pizza, cheese_qty)
    except BaseException:
        print("Am prins orice poate crăpa!")
    except TooMuchCheeseError as tmce:
        print(tmce, ":", tmce.cheese)
    except PizzaError as pe:
        print(pe, ":", pe.pizza)
