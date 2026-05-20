two = lambda: 2
mul = lambda x: x * x
pwr = lambda x, y: x**y


def mul_fun(x):
    return x * x


for a in range(-2, 3):
    print(mul(a), end=" ")
    print(pwr(a, two()))


students = [
    {"name": "Ana", "grade": 9.5},
    {"name": "Mihai", "grade": 7.0},
    {"name": "Ioana", "grade": 8.75},
    {"name": "David", "grade": 10},
]

students = sorted(students, key=lambda student: student["grade"], reverse=True)
print(students)
