"""
functions_experiments.py
=========================
A mini-lab of Python function patterns. Run this file to see the printed
examples in order, and skim the comments/docstrings to understand each idea.
"""


def show_section(title: str) -> None:
    """Utility helper so each example stands out in the console output."""
    print("\n" + "=" * 80)
    print(title.upper())
    print("=" * 80)


show_section("functions keep code reusable")


def greet(name: str) -> str:
    """Return a friendly greeting for the provided name."""
    return f"Hello, {name}!"


print(greet("Ada"))
print("Docstring:", greet.__doc__)


show_section("positional vs keyword arguments")


def describe_pet(animal_type: str, pet_name: str, *args, mood="curious", friendly=True):
    """Demonstrate positional, default, and keyword-only parameters."""
    friendliness = "friendly" if friendly else "independent"
    return f"{pet_name.title()} is a {mood} {animal_type} who is {friendliness}."


print(describe_pet("cat", "milo"))  # pure positional arguments
print(describe_pet("cat", "milo", "something else"))
print(describe_pet("parrot", "rio", mood="chatty", friendly=False))  # mix


show_section("return values")


def rectangle_stats(width: float, height: float) -> tuple:
    """Return both area and perimeter to show multi-value returns."""
    area = width * height
    perimeter = 2 * (width + height)
    return area, perimeter  # tuples allow returning multiple values


area, perimeter = rectangle_stats(4.0, 2.5)
print(f"Area: {area}")
print(f"Perimeter: {perimeter}")


show_section("arbitrary argument lists")


def sum_all(*numbers):
    """Accept any amount of positional numbers; *numbers packs them into a tuple."""
    total = sum(numbers)
    print(f"Received {len(numbers)} numbers: {numbers}")
    return total


print("Total:", sum_all(1, 2, 3, 4, 5, 6, 7, 8, 9))


def build_profile(**attributes):
    """Accept any keyword arguments; **attributes packs them into a dict."""
    summary = ", ".join(f"{key}={value}" for key, value in attributes.items())
    return f"Profile -> {summary}"


print(build_profile(name="Jordan", role="coach", likes_python=True))

show_section("rectangle stats with kwargs")


def rectangle_stats_with_kwargs(**kwargs) -> tuple:
    """Return both area and perimeter to show multi-value returns."""
    width = kwargs.get("width")
    height = kwargs.get("height")

    area = width * height
    perimeter = 2 * (width + height)
    return area, perimeter  # tuples allow returning multiple values


a, p = rectangle_stats_with_kwargs(height=77.9, width=88.9)
print(f"Area: {a:.2f}, perimeter: {p:.2f}")

show_section("combining *args and **kwargs")


def demo_args_kwargs(*args, **kwargs):
    """Just print how Python bundles the dynamic inputs."""
    print("Positional args tuple:", args)
    print("Keyword args dict:", kwargs)


demo_args_kwargs(10, 20, debug=True, verbose=False)


show_section("functions as data")


def apply_operation(numbers: list, operation: any) -> list:
    """Functions are first-class: pass them around like any other object."""
    return [operation(n) for n in numbers]  # list comprehensions


def double(number):
    return number * 2


numbers = [1, 2, 3]
print("Original:", numbers)
print("Doubled:", apply_operation(numbers, double))
print("Squared via lambda:", apply_operation(numbers, lambda n: n * n))


show_section("nested functions and closures")


def make_multiplier(factor):
    """Closure retains the factor value even after make_multiplier finishes."""

    def multiplier(number):
        return number * factor

    return multiplier


times_three = make_multiplier(3)
print("3 * 7 =", times_three(7))
print("3 * 11 =", times_three(11))


show_section("recursion")


def countdown(start: int) -> None:
    """A simple recursion example with a base case to stop the calls."""
    if start <= 0:
        print("Lift-off!")
        return

    print(start)
    countdown(start - 1)


countdown(3)


show_section("factorial recursion with return values")


def factorial(n: int) -> int:
    """Return n! (n factorial). Raises ValueError for negative inputs."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)


print("5! =", factorial(5))


show_section("type hints and annotations")


def format_name(first: str, last: str, /, *, uppercase: bool = False) -> str:
    """Demonstrates positional-only (/), keyword-only (*), and annotations."""
    full = f"{first} {last}".strip()
    return full.upper() if uppercase else full.title()


print(format_name("grace", "hopper"))
print(format_name("grace", "hopper", uppercase=True))
print("Annotations:", format_name.__annotations__)


show_section("docstrings + help")

print("Use help(format_name) in the REPL to see rich documentation.")
print("For scripts, you can also inspect:", format_name.__doc__)


show_section("wrapping up")
print("Functions let us package behavior, reuse logic, and reason about code.")
print(
    "Experiment by editing parameters, adding new sections, or calling these"
    " helpers with different inputs."
)
