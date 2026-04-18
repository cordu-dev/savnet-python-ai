# Demonstrating min() - Example 1:
some_string = " aAbByYzZ"

for character in some_string:
    print(f'{character} = {ord(character)}')

print(min(some_string))


# Demonstrating min() - Examples 2 & 3:
t = 'The Knights Who Say "Ni!"'
print("[" + min(t) + "]")

t = [0, 1, 2]
print(min(t))
