class Fib:
    # FIB VAL: 1 1 2 3 5 ...
    # FIN IDX: 0 1 2 3 4 ...
    def __init__(self, max_index):
        print("__init__")
        self.__max_index = max_index
        self.__index = 0  # zero-based index?
        self.__previous1 = self.__previous2 = 1

    def __iter__(self):
        print("__iter__")
        return self

    def __next__(self):
        print(f"__next__, {self.__index}")

        if self.__index >= self.__max_index:
            print("__next__: STOP")
            raise StopIteration

        if self.__index in [0, 1]:
            current = 1
        else:
            # Fibonacci business logic.
            current = self.__previous1 + self.__previous2
            self.__previous1, self.__previous2 = self.__previous2, current

        self.__index += 1

        return current


class FibIterator:
    def __init__(self, max_index) -> None:
        self.__iterator = Fib(max_index)

    def __iter__(self):
        return self.__iterator


# for i in Fib(10):
#     print(i)

my_iterator = FibIterator(10)

for i in my_iterator:
    # First thing, calls the __iter__ to obtain an instance of the iterator.
    # After, it uses the iterator instance to call the __next__ from within.
    # It will stop only when __next__ raise StopIteration.
    print(i)
