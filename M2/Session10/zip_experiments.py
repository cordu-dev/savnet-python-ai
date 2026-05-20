print("ZIP EXPERIMENTS")
print("=" * 40)

print("\n1. zip pairs items from multiple iterables.")
names = ["Ana", "Bob", "Carla"]
scores = [95, 88, 91]
paired = zip(names, scores)
print("zip(names, scores) returns:", paired)
print("After converting to a list:", list(paired))

print("\n2. zip is lazy, like map.")
letters = ["a", "b", "c"]
numbers = [1, 2, 3]
lazy_zip = zip(letters, numbers)
print("Before consuming lazy_zip:", lazy_zip)
print("First tuple:", next(lazy_zip))
print("Remaining tuples:", list(lazy_zip))

print("\n3. zip stops when the shortest iterable ends.")
products = ["Keyboard", "Mouse", "Monitor", "Laptop"]
prices = [100, 50]
print(list(zip(products, prices)))

print("\n4. zip can combine more than two iterables.")
cities = ["Bucharest", "Cluj", "Iasi"]
temperatures = [26, 22, 24]
conditions = ["sunny", "cloudy", "rainy"]
weather_data = zip(cities, temperatures, conditions)
print(list(weather_data))

print("\n5. Real-life example: building rows for a report.")
student_names = ["Mara", "Tudor", "Elena"]
attendance = [True, False, True]
project_scores = [9.5, 7.0, 10.0]
for name, present, score in zip(student_names, attendance, project_scores):
    print(f"Student: {name}, Present: {present}, Project score: {score}")

print("\n6. zip is great with map because both work item by item.")
coordinates_x = [2, 4, 6]
coordinates_y = [10, 20, 30]
for x, y in zip(coordinates_x, coordinates_y):
    print(f"Point -> x={x}, y={y}, sum={x + y}")

print("\n7. Unzipping: zip can also separate grouped data.")
points = [(1, 10), (2, 20), (3, 30)]
xs, ys = zip(*points)
print("Original points:", points)
print("All x values:", xs)
print("All y values:", ys)

print("\n8. Important reminder.")
print("zip() returns an iterator, so once you fully consume it, it is empty.")
example = zip([1, 2], [3, 4])
print("First conversion:", list(example))
print("Second conversion:", list(example))

print("\nCHALLENGE")
print("Create two lists: product names and stock counts.")
print("Use zip() to print sentences like: 'Keyboard has 12 items in stock.'")
