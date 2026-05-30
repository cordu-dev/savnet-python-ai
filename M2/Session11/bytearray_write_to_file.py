from os import strerror

data = bytearray(50)

for i in range(len(data)):
    data[i] = 10 + i

for b in data:
    print(hex(b))

try:
    stream = open("M2/Session11/files/file.bin", "wb")

    stream.write(data)

    stream.close()
except IOError as e:
    print("I/O error occurred:", strerror(e.errno))

# Your code that reads bytes from the stream should go here.
