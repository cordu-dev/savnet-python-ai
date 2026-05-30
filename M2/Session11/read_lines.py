from os import strerror

try:
    ccnt = lcnt = 0
    my_stream = open("M2/Session11/files/something.txt", "rt")
    lines = my_stream.readlines(50)  # hint = Max Buffer size

    while len(lines) != 0:
        for line in lines:
            lcnt += 1
            for ch in line:
                print(ch, end="")
                ccnt += 1
        lines = my_stream.readlines(50)

    my_stream.close()

    print("\n\nCharacters in file:", ccnt)
    print("Lines in file:     ", lcnt)
except IOError as e:
    print("I/O error occurred:", strerror(e.errno))
