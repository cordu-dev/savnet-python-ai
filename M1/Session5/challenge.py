from string import ascii_lowercase


# ARE BUBE!

def caesar_decode(text: str, shift_position: int = 1) -> str:
    """Decode Caesar"""
    decoded_text = ""
    for character in text:
        i = ascii_lowercase.index(character)
        new_pos = len(ascii_lowercase) % (i + shift_position)
        decoded_text += ascii_lowercase[i + new_pos]
        
    return decoded_text


print(caesar_decode("aaabbbz", 1))
