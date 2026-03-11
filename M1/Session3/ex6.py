# Luați ca input de la utilizator un cuvant si afisati numarul ocurentei primei litere din
# cuvant. Exemplu:
# Introduceti un cuvant (fara majuscule): rabdare
# r apare de 2 ori.

word = input("Bagă mare: ")

word = word.lower()

print(word.count(word[0]))
