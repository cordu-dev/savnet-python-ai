from os import strerror

srcname = input("Enter the source file name: ")

try:
    source_file = open(srcname, mode="rb")
except IOError as e:
    print("Cannot open the source file: ", strerror(e.errno))
    exit(e.errno)

dstname = input("Enter the destination file name: ")
try:
    dest_file = open(dstname, "wb")
except Exception as e:
    print("Cannot create the destination file: ", strerror(e.errno))
    source_file.close()
    exit(e.errno)

buffer = bytearray(65536)
total = 0
try:
    bytes_read = source_file.readinto(buffer)
    while bytes_read > 0:
        # Write into file at latest position
        bytes_written = dest_file.write(buffer[:bytes_read])
        total += bytes_written
        bytes_read = source_file.readinto(buffer)

except IOError as e:
    print("Cannot create the destination file: ", strerror(e.errno))
    exit(e.errno)

print(total, "byte(s) succesfully written")
source_file.close()
dest_file.close()
