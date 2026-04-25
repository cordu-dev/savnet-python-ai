class Stack(object):
    def __init__(self):
        self.__stack_list = []

    def __str__(self):
        return str(self.__stack_list)

    def push(self, val):
        if not isinstance(val, int):
            # raise ValueError("Băă e non int! Nasol!")
            return

        self.__stack_list.append(val)

    def pop(self):
        val = self.__stack_list[-1]
        del self.__stack_list[-1]
        return val


class AddingStack(Stack):  # this is a simple inheritance.
    def __init__(self):
        super().__init__()
        # Stack.__init__()
        self.__sum = 0  # I want to keep a dynamic sum of all items in the stack.

    def push(self, val):
        super().push(val)  # do what you did before
        self.__sum += val

    def pop(self):
        val = super().pop()
        self.__sum -= val
        return val

    def get_sum(self):
        return self.__sum


little_stack = Stack()
another_stack = Stack()
funny_stack = Stack()

little_stack.push("ceva")
little_stack.push(22)
little_stack.push(funny_stack)


print(little_stack)

print("Adding Stack example")

adding_stack = AddingStack()

adding_stack.push(33)
adding_stack.push(22)
adding_stack.push(11)
adding_stack.pop()

print(adding_stack.get_sum())
