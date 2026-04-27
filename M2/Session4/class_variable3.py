class Classy:
    varia = 2  # class variable

    def __init__(self) -> None:
        self.var = None

    def method(self):
        # Read only access of the class variable
        # print(self.varia, self.var)
        print(Classy.varia, self.var)

    @classmethod
    def show_varia(cls):
        print(cls.varia)

    @classmethod
    def set_varia(cls, val):
        cls.varia = val


obj1 = Classy()
obj2 = Classy()

obj1.var = 3
obj1.method()
obj2.method()

Classy.varia += 1

obj1.method()
obj2.method()

# Calls a class method
obj1.set_varia(66)
obj1.show_varia()
obj2.show_varia()
