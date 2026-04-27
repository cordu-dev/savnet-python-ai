class Animal(object):
    def __init__(self) -> None:
        # Available from outside the object
        self.public_attr = 11
        # Available for other classes that inherits from the current
        self._protected_attr = 22
        # Available only for the current instance, not accessible from outside
        self.__private_attr = 33


class Mamal(Animal):
    def __init__(self) -> None:
        super().__init__()

    def print_private(self):
        print(self.__private_attr)  # this will crash

    def print(self):
        print(self.public_attr)
        print(self._protected_attr)


bear = Mamal()
penguin = Mamal()

bear.print()

print(bear.public_attr)
print("Checking if python is able to access protected attributes from outside")
print(bear._protected_attr)  # This would not be possible in C / Java

print()
bear.print_private()
