class ExampleClass:
    something_class_variable = 1

    def __init__(self):
        self.__something_private = 0
        self._something_protected = 0
        self.something_public = 0


# Checkibng if the CLASS (the blueprint) has some attributes aka class variables
print(hasattr(ExampleClass, "something_class_variable"))
print(hasattr(ExampleClass, "__something_private"))
print(hasattr(ExampleClass, "_something_protected"))
print(hasattr(ExampleClass, "something_public"))

obj = ExampleClass()

print()
# Check if the OBJECT (theinstance) has some attributes / properties and class variables.
print(hasattr(obj, "something_class_variable"))
print(hasattr(obj, "__something_private"))
print(hasattr(obj, "_something_protected"))
print(hasattr(obj, "something_public"))
