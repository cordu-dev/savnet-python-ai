# functions


def message():
    print("Enter a value: ")


print("We start here.")
message()
print("We end here.")


counter = 1


def sum_numbers(number_a, number_b):
    global counter
    # var1 = var1 + 1
    counter += 1
    result = number_a + number_b + counter
    return result


result1 = sum_numbers(10, 20)
result2 = sum_numbers(10, 20)
result3 = sum_numbers(10, 20)

print(result1)
print(result2)
print(result3)

print(counter)
