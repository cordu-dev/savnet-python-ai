def fibonacci(number):
    previous1 = previous2 = 1

    for i in range(number):
        if i in [0, 1]:
            yield 1  # Gives control to the caller (by "returning 1")
        else:
            number = previous1 + previous2
            previous2, previous1 = previous1, number
            yield number


# Entry point.
fibs = list(fibonacci(10))  # Give control back to the generator after each item

print(fibs)
