"""
Bytes Experiments - UTF-8 Encoding and Hexadecimal Display
"""

# Experiment 1: String to bytes conversion with UTF-8
text = "Hello, World!"
utf8_bytes = text.encode('utf-8')

print("Original string:", text)
print("UTF-8 bytes:", utf8_bytes)
print("Type:", type(utf8_bytes))
print("Length:", len(utf8_bytes), "bytes")
print()

# Experiment 2: Display bytes in hexadecimal
print("Bytes in hexadecimal format:")
print("Using hex() method:", utf8_bytes.hex())
print()

# Experiment 3: Individual byte values in hex
print("Individual bytes in hexadecimal:")
for i, byte in enumerate(utf8_bytes):
    print(f"Byte {i}: {byte} (decimal) = {hex(byte)} (hexadecimal) = {chr(byte)} (character)")
print()

# Experiment 4: Working with special characters (UTF-8)
special_text = "Hello, 世界! 👋"
special_utf8_bytes = special_text.encode('utf-8')

print("Special characters example:")
print("Original:", special_text)
print("UTF-8 bytes:", special_utf8_bytes)
print("Hexadecimal:", special_utf8_bytes.hex())
print("Length:", len(special_utf8_bytes), "bytes")
print()

# Experiment 5: Manual byte creation and hex display
manual_bytes = bytes([72, 101, 108, 108, 111])  # "Hello" in ASCII
print("Manual byte creation:")
print("Bytes:", manual_bytes)
print("Hexadecimal:", manual_bytes.hex())
print("Decoded:", manual_bytes.decode('utf-8'))
print()

# Experiment 6: Hexadecimal analysis
print("Hexadecimal analysis of 'Hello, World!':")
hex_string = utf8_bytes.hex()
# Group into pairs for readability
hex_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
print("Hex pairs:", hex_pairs)

# Dynamic ASCII mapping from the utf8_bytes variable
ascii_map = {hex(byte)[2:].zfill(2): chr(byte) for byte in utf8_bytes}

print("Character mapping:")
for pair in hex_pairs:
    char = ascii_map.get(pair, '?')
    print(f"0x{pair} -> '{char}'")
print()

# Experiment 7: Converting hex back to bytes
hex_input = "48656c6c6f2c20576f726c6421"
recovered_bytes = bytes.fromhex(hex_input)
recovered_text = recovered_bytes.decode('utf-8')

print("Hex to bytes conversion:")
print("Hex input:", hex_input)
print("Recovered bytes:", recovered_bytes)
print("Recovered text:", recovered_text)
