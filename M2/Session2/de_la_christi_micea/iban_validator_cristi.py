import json


def load_country_codes(input_filename: str) -> dict:
    with open(input_filename, "r") as file:
        country_codes = json.load(file)
    return country_codes


def check_valid_iban_len(iban: str, country_codes: dict) -> bool:
    return len(iban) == country_codes.get(iban[:2].upper(), 0)


def check_country_code_exists(iban: str, country_codes: dict) -> bool:
    return iban[:2].upper() in country_codes


# the mod 97 algorithm uses an offset of 10 for letters when converting them to numbers
OFFSET = 10


def check_iban_mod_97_algorithm(iban: str) -> bool:
    # set the country code and check digits to the end of the iban
    iban = (iban[4:] + iban[0:4]).upper()

    ibanAsBigNumber = ""

    for ch in iban:
        if ch.isdigit():
            ibanAsBigNumber += ch
        else:
            ibanAsBigNumber += str(OFFSET + ord(ch) - ord("A"))
    # if not for Python extending the size of int as needed, this would be unsafe
    # in that case, it would have been better to perform the % operation gradually
    iban = int(ibanAsBigNumber)

    return iban % 97 == 1


def validate_IBAN(iban: str, country_codes: dict) -> bool:
    # preliminary sanitization - remove spaces
    iban = iban.replace(" \t\n\r", "")
    # make all characters as uppercase
    iban = iban.upper()

    if not check_country_code_exists(iban, country_codes):
        print("Country code not found.")
        return False

    if not check_valid_iban_len(iban, country_codes):
        print("IBAN entered is too short or too long.")
        return False

    if not iban.isalnum():
        print("You have entered invalid characters.")
        return False

    return check_iban_mod_97_algorithm(iban)


def main():
    country_codes = load_country_codes("country_codes.json")
    iban = input("Enter IBAN, please: ")

    if not validate_IBAN(iban, country_codes):
        print("IBAN entered is invalid.")
    else:
        print("IBAN entered is valid.")


if __name__ == "__main__":
    main()
