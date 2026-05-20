def powers_of_2(n):
    """
    A generator is a function that uses yield.
    """
    power = 1
    for i in range(n):
        print(f"About to yield: {power}")
        yield power
        power *= 2


for v in powers_of_2(8):
    # `for`` and `in` is asking from powers_of_2 - generator
    # to CONTINUE from where it left
    # restauring the entire context of the function.
    print(v)

print("-" * 20)

if 64 in powers_of_2(8):
    print("Yes 64 is a power of 2")
