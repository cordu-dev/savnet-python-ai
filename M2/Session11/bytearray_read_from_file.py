from os import strerror

data = bytearray(10)

try:
    binary_file = open(file="M2/Session11/files/file.bin", mode="rb")

    # If the file is bigger than 10 bytes, it will read the first 10 bytes.
    bytes_count = binary_file.readinto(data)

    binary_file.close()

    print(f"Bytes Count: {bytes_count}")
    for b in data:
        print(hex(b), end=" ")
except IOError as e:
    print("I/O error occurred:", strerror(e.errno))
