class ExampleClass:
    counter = 0  # class variable

    def __init__(self, pub_var, val=1):
        self.__first = val
        self.pub_var = pub_var  # class attribute / property
        self.some_dict = {}
        ExampleClass.counter += 1
        # self.counter += 1  # this will affect the class variable and will shadow it


example_object_1 = ExampleClass(1)
example_object_2 = ExampleClass(2)
example_object_3 = ExampleClass(4)

print(example_object_1.__dict__, example_object_1.counter)
print(example_object_2.__dict__, example_object_2.counter)
print(example_object_3.__dict__, example_object_3.counter)
