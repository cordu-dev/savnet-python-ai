class ZeroPeopleDivisionError(ZeroDivisionError):
    def __init__(self, *args: object) -> None:
        super().__init__("CUSTOM> Cannot split a budget between 0 people")


def print_args(args):
    lng = len(args)
    if lng == 0:
        print("")
    elif lng == 1:
        print(args[0])
    else:
        print(str(args))


def show_exception(error):
    print(type(error).__name__, error, error.__str__(), sep=" : ", end=" : ")
    print_args(error.args)


def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age < 18:
        raise PermissionError("You must be at least 18 years old")
    return "Access granted"


def divide_budget(total_budget, people_count):
    if people_count == 0:
        raise ZeroPeopleDivisionError()
    return total_budget / people_count


def find_student_email(students, name):
    if name not in students:
        raise KeyError("Student not found", name)
    return students[name]


try:
    validate_age(-3)
except Exception as e:
    show_exception(e)

try:
    validate_age(16)
except Exception as e:
    show_exception(e)

try:
    divide_budget(1200, 0)
except Exception as e:
    show_exception(e)

students = {
    "Ana": "ana@example.com",
    "Vlad": "vlad@example.com",
}

try:
    find_student_email(students, "Maria")
except Exception as e:
    show_exception(e)
