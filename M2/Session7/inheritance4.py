from typing import override


class Base(object):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self):
        return "My name is " + self.name + "."

    def do_something(self):
        print(f"Doing something {self.name}")


class Child(Base):
    def __init__(self, name):
        # Two ways of calling base class methods.
        # Base.__init__(self, name)
        super().__init__(name)

    @override
    def do_something(self):
        print(f"Do Something from CHILD {self.name}")


obj = Child("Andy")

obj.do_something()

print(obj)
