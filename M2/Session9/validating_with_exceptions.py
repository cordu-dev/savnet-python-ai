def validate_with_exceptions(data_input: str) -> str:
    if not data_input == "the_right_value":
        raise ValueError("Data input is not the right value")

    return data_input


try:
    validate_with_exceptions("xxxx")
    print("Everything OK!")
except ValueError as e:
    print(f"It is not OK, {e}")
