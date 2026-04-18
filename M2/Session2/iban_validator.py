# IBAN Validator.

# IBAN example: GB 82 WEST12345698765432
# Structure: GB - country code (2 letters)
#           82 - check digits (2 numbers)
#           WEST - bank code (4 letters)
#           123456 - sort code (6 numbers)
#           98765432 - account number (8 numbers)

iban = input("Enter IBAN, please: ")
iban = iban.replace(" ", "")  # Data cleaning.

if not iban.isalnum():
    print("You have entered invalid characters.")
elif len(iban) < 15:
    print("IBAN entered is too short.")
elif len(iban) > 31:
    print("IBAN entered is too long.")
else:
    iban = (iban[4:] + iban[0:4]).upper()
    iban2 = ""
    for ch in iban:
        if ch.isdigit():
            iban2 += ch
        else:
            iban2 += str(10 + ord(ch) - ord("A"))
    iban = int(iban2)
    if iban % 97 == 1:
        print("IBAN entered is valid.")
    else:
        print("IBAN entered is invalid.")

