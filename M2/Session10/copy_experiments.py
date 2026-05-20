import copy

print("COPY EXPERIMENTS")
print("=" * 40)

print("\n1. Assignment does not create a new object.")
original_list = [1, 2, 3]
assigned_list = original_list
assigned_list.append(4)
print("original_list:", original_list)
print("assigned_list:", assigned_list)

print("\n2. Shallow copy creates a new outer object.")
outer_list = [[1, 2], [3, 4]]
shallow_copy = copy.copy(outer_list)
shallow_copy.append([5, 6])
print("outer_list:", outer_list)
print("shallow_copy:", shallow_copy)

print("\n3. But shallow copy still shares nested objects.")
shared_nested = [[10, 20], [30, 40]]
shallow_nested_copy = copy.copy(shared_nested)
shallow_nested_copy[0].append(99)
print("shared_nested:", shared_nested)
print("shallow_nested_copy:", shallow_nested_copy)

print("\n4. Deep copy clones nested objects too.")
deep_source = [[100, 200], [300, 400]]
deep_copied = copy.deepcopy(deep_source)
deep_copied[0].append(999)
print("deep_source:", deep_source)
print("deep_copied:", deep_copied)

print("\n5. Iterators behave differently from normal containers.")
values = [1, 2, 3, 4, 5]
filtered_values = filter(lambda number: number % 2 == 0, values)
iterator_copy = copy.copy(filtered_values)
print("filtered_values:", filtered_values)
print("iterator_copy:", iterator_copy)

print("\n6. Consuming one iterator affects its own internal state.")
print("First item from filtered_values:", next(filtered_values))
print("Remaining items from filtered_values:", list(filtered_values))

print("\n7. It is usually better to convert an iterator to a list if you need to reuse the data.")
filtered_again = filter(lambda number: number % 2 == 0, values)
filtered_list = list(filtered_again)
print("filtered_list:", filtered_list)
print("You can print it again safely:", filtered_list)

print("\nIMPORTANT IDEA")
print("copy() and deepcopy() are most useful with containers like lists, dictionaries, and nested data structures.")
print("With iterators such as filter(), map(), and zip(), the important concept is usually consumption, not copying.")

print("\nCHALLENGE")
print("Create a nested list and test the difference between copy.copy() and copy.deepcopy().")
print("Then try the same thinking with a filter object and observe what changes.")
