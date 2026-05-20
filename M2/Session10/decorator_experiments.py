print("DECORATOR EXPERIMENTS")
print("=" * 40)

import time


print("\n1. A very simple profiling decorator.")
print("It starts a timer, runs the function, then shows how long it took.")


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed_seconds = end - start
        elapsed_milliseconds = elapsed_seconds * 1000
        print(f"{func.__name__} took {elapsed_seconds:.6f} seconds")
        print(f"That is about {elapsed_milliseconds:.3f} milliseconds")
        return result

    return wrapper


@measure_time
def slow_task():
    time.sleep(0.2)
    print("The slow task finished.")


slow_task()

print("\n2. A decorator is a practical use of closures.")
print("The wrapper function remembers the original function.")


def simple_decorator(func):
    def wrapper():
        print("Before the function runs")
        func()
        print("After the function runs")

    return wrapper


def say_hello():
    print("Hello!")


wrapped_hello = simple_decorator(say_hello)
wrapped_hello()

print("\n3. The @ syntax is just shorter syntax.")


@simple_decorator
def say_goodbye():
    print("Goodbye!")


say_goodbye()

print("\n4. Decorators are useful when you want to reuse behavior.")


def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result

    return wrapper


@log_calls
def add(a, b):
    return a + b


answer = add(10, 5)
print("answer:", answer)

print("\n5. Decorators help remove repeated code.")
print("Imagine adding print statements to 20 functions by hand.")
print("A decorator lets you write that logic once.")


def emphasize_output(func):
    def wrapper(*args, **kwargs):
        print("-" * 20)
        result = func(*args, **kwargs)
        print("-" * 20)
        return result

    return wrapper


@emphasize_output
def show_message(message):
    print(message)


show_message("Decorators make repeated behavior reusable.")

print("\n6. A decorator can keep state using a closure.")


def count_calls(func):
    calls = 0

    def wrapper(*args, **kwargs):
        nonlocal calls
        calls += 1
        print(f"{func.__name__} has been called {calls} times")
        return func(*args, **kwargs)

    return wrapper


@count_calls
def greet(name):
    print(f"Hello, {name}!")


greet("Ana")
greet("Mark")
greet("Ioana")

print("\n7. Important mental model")
print("A decorator does not replace your function with magic.")
print("It replaces it with another function that usually calls the original one.")

print("\nCHALLENGE")
print("Create a decorator called repeat_twice.")
print("It should run the decorated function two times.")
print("Then decorate a function that prints 'Python is fun!'.")
