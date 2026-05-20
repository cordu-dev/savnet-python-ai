print("FILTER EXPERIMENTS")
print("=" * 40)

print("\n1. filter keeps only the items that match a condition.")
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = filter(lambda number: number % 2 == 0, numbers)
print("filter(...) returns:", even_numbers)
print("After converting to a list:", list(even_numbers))

print("\n2. filter is lazy, like map and zip.")
values = [10, 15, 20, 25, 30]
lazy_filter = filter(lambda value: value > 18, values)

print("Before consuming lazy_filter:", lazy_filter)
print("First matching value:", next(lazy_filter))
print("Remaining values:", list(lazy_filter))

print("\n3. If nothing matches, filter returns an empty result.")
small_numbers = [1, 2, 3]
large_only = filter(lambda number: number > 100, small_numbers)
print(list(large_only))

print("\n4. You can use a normal function instead of lambda.")


def is_paid(order):
    return order["status"] == "paid"


orders = [
    {"id": 1, "customer": "Ana", "status": "paid"},
    {"id": 2, "customer": "Mark", "status": "pending"},
    {"id": 3, "customer": "Ioana", "status": "paid"},
]
paid_orders = filter(is_paid, orders)
print(list(paid_orders))

print("\n5. Real-life example: keep only active users.")
users = [
    {"name": "Alice", "active": True},
    {"name": "Bob", "active": False},
    {"name": "Carla", "active": True},
]
active_users = filter(lambda user: user["active"] is True, users)
for user in active_users:
    print(user)

print("\n6. filter can clean messy data.")
raw_names = ["Ana", "", "Bob", "", "Carla"]
non_empty_names = filter(lambda name: name != "", raw_names)
print(list(non_empty_names))

print("\n7. filter(None, iterable) removes falsy values.")
mixed_values = [0, 1, "", "hello", None, True, False, "Python"]
cleaned_values = filter(None, mixed_values)
print(list(cleaned_values))

print("\n8. filter returns an iterator, so once consumed, it is empty.")
example = filter(lambda x: x % 2 == 1, [1, 2, 3, 4, 5])
print("First conversion:", list(example))
print("Second conversion:", list(example))

print("\n9. filter works nicely before map in a data pipeline.")
temperatures = [-5, 12, 18, -2, 25]
positive_temperatures = filter(lambda temp: temp >= 0, temperatures)
fahrenheit = map(lambda temp: temp * 9 / 5 + 32, positive_temperatures)
print(list(fahrenheit))

print("\nCHALLENGE")
print("Create a list of email addresses.")
print("Use filter() to keep only the ones that end with '@gmail.com'.")
