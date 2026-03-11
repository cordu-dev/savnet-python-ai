# Luați input de la utilizator un număr și parcurgeți intervalul de la 0 pana la numărul
# introdus de către utilizator, afisand toate numerele pare.

x = int(input("bagă aici:"))

for i in range(0, x + 1, 2):
    print(i, end=' ')
