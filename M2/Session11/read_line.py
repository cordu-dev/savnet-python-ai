from os import strerror

try:
    line_character_counter = character_counter = line_counter = 0

    stream = open("M2/Session11/files/something.txt", "rt")
    line = stream.readline()

    while line != "":
        line_counter += 1
        line_character_counter = 0

        for char in line:
            print(char, end="")
            character_counter += 1
            line_character_counter += 1

        print(f"Line Character Count: {line_character_counter}")
        line = stream.readline()

    stream.close()

    print("\n\nCharacters in file:", character_counter)
    print("Lines in file:     ", line_counter)
except IOError as e:
    print("I/O error occurred:", strerror(e.errno))
