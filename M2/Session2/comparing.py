string1 = "Something"
string2 = "Somethin"

# string2 = input("Bagă ceva:")

print(id(string1))
print(id(string2))

print(string1 == string2)
print(string1 is string2)

string2 = string2 + "g"

print(string1 == string2)
print(string1 is string2)
