SOME_CONSTANT = """

This is a simple English template
It contains some placeholder text
    Indented line here
    Another indented line
    Final indented line
Back to normal indentation

{number_one}
{number_two}

"""


def some_function():
    """
    This is doing great.
    """

    some_string_multiline = SOME_CONSTANT.format(number_one=11, number_two=22)

    return some_string_multiline


print(some_function())
