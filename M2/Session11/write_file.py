from os import strerror
from os.path import exists

file_path = "M2/Session11/files/newtext.txt"

try:
    # TODO: Try to rename the file if this already exists.
    if exists(file_path):
        print("The newtext.txt file already exists.")
        raise SystemExit

    file = open(file_path, "wt")  # A new file (newtext.txt) is created.

    for i in range(10):
        s = "line #" + str(i + 1) + "\n"
        for char in s:
            file.write(char)

    file.close()
except IOError as e:
    print("I/O error occurred: ", strerror(e.errno))
