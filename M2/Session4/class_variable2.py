class ExampleClass(object):
    varia = 1

    def __init__(self, val):
        self.something = 1
        ExampleClass.varia = val


print(ExampleClass.__dict__)
example_object = ExampleClass(2)

print(ExampleClass.__dict__)
print()
print(example_object.__dict__)
