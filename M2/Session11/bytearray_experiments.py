data = bytearray(10)

for i in range(len(data)):
    data[i] = 10 - i

for b in data:
    print(hex(b))


# 01011101 = 8 bits = 1 byte.
# bytearray of 10 bytes.
