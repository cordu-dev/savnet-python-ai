from os import strerror
import locale

try:
    counter = 0
    stream = open(
        "M2/Session11/files/something.txt",  # relative path, depends from where you execute the python script.
        mode="rt",
    )

    print("Default Encoding: ", locale.getencoding())

    char = stream.read(1)
    while char != "":
        print(char, end="")
        counter += 1
        char = stream.read(1)

    stream.close()
    print("\n\nCharacters in file:", counter)
except IOError as e:
    print("I/O error occurred: ", strerror(e.errno))
