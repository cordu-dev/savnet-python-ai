class ExampleClass:
    def __init__(self, val):
        if val % 2 != 0:
            self.a = 11
        else:
            self.b = 22


example_object = ExampleClass(2)

# print(example_object.a)
# print(example_object.b)

# A way to make sure program is not crashing when attribute is not defined.
print(getattr(example_object, "a", 111))
print(getattr(example_object, "b", 666))
