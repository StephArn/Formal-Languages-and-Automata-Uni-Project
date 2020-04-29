def citireLNFA:
    global  n, m, alfabet, q0, stari_fin, l, tranz,k 
    f = open("intrare.txt", "r")

    n = int(f.readline())  # numar stari

    m = int(f.readline())  # numar caractere alfabet

    alfabet = []

    for i in f.readline().strip().split():
        alfabet.append(i)
    alfabet.append('$')

    q0 = int(f.readline())  # stare initiala

    k = int(f.readline())  # numar stari finale

    stari_fin =set()

    for i in f.readline().split():
        stari_fin.add(int(i))

    l = int(f.readline())  # numar tranzitii

    tranz = {}

    for i in range(l):
        si, char, sf= f.readline().strip().split()
        if int(si) not in tranz:
            tranz[int(si)]={char:[int(sf)]} #dictionar cu tranzitii
        else:
            if char not in tranz[int(si)]:
                tranz[int(si)][char]=[int(sf)]
            else:
                tranz[int(si)][char].append(int(sf))
