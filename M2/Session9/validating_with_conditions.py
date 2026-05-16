def validate_with_condition_by_excluding_right_values(data_input: str) -> bool:
    if data_input not in ["the_right_value", "the_other_right_value"]:
        return False

    return True


def validate_with_condition_by_excluding_wrong_values(data_input: str) -> bool:
    if data_input in ["the_bad_value", "xxx"]:
        return False

    return True


is_valid_right_values = validate_with_condition_by_excluding_right_values(
    "something ok"
)
is_valid_wrong_values = validate_with_condition_by_excluding_wrong_values(
    "something ok"
)

if is_valid_right_values:
    print("Right Values: Everything OK!")
else:
    print("Right Values: NOT OK!")

if is_valid_wrong_values:
    print("Right Values: Everything OK!")
else:
    print("Right Values: NOT OK!")
