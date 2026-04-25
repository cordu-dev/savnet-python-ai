# There are two ways of populating / changing the state of the attributes:
# 1. Constructors
# 2. Setters


class Animal(object):
    def __init__(self, number_of_legs=0) -> None:
        self.number_of_legs = number_of_legs

    def __str__(self) -> str:
        return f"This animal has {self.number_of_legs}"

    def set_number_of_legs(self, n):
        self.number_of_legs = n

    def display_internal_state(self):
        print(self.number_of_legs)

    @staticmethod
    def breath():
        print("... huh huh ...")


print("Bear")
bear = Animal()
bear.set_number_of_legs(2)  # use setter to change internal state
bear.display_internal_state()
print(bear.__str__())

print("Dog")
dog = Animal(4)  # use constructor to change internal state
dog.display_internal_state()

print('Omida')
omida = Animal()
omida.number_of_legs = 200
omida.display_internal_state()
omida.breath()
