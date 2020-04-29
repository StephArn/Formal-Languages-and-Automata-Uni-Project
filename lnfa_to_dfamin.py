def Citire():

    global  n, m, alfabet, q0, stari_fin, l, tranz,k

    f = open("intrare.txt", "r")

    n = int(f.readline())  # numar stari

    m = int(f.readline())  # numar caractere alfabet

    alfabet = []

    for i in f.readline().strip().split():
        alfabet.append(i)

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

    for nod in range(n):
        if nod not in tranz:
            tranz[nod]={}
        for litera in alfabet:
            if litera not in tranz[nod]:
                tranz[nod][litera]=[]

def ParcurgereLambda(current, principal, viz, tranz, lambda_inchidere):

    if viz[current]==0:

        viz[current]=1
        lambda_inchidere[principal].append(current)

        if '$' in tranz[current]:
            for rel in tranz[current]['$']:
                if viz[rel]==0:
                    ParcurgereLambda(rel,principal,viz,tranz,lambda_inchidere)

def LambdaInchidere(n, tranz, lambda_inchidere):

    for nod in range(n):
        lambda_inchidere[nod] = []
        viz=[0]*n
        if nod in tranz:
            ParcurgereLambda(nod,nod,viz,tranz,lambda_inchidere)
        #tranz[nod].sort()

def FctTranzToNFA(n,tranz,tranzNFA,lambda_inchidere,alfabet):

    for nod in range(n):
        tranzNFA[nod]={}

        for char in alfabet:
            tranzNFA[nod][char]=[]
            lambda_before=lambda_inchidere[nod]
            l_char=[]
            lambda_after=[]

            for i in lambda_before:
                if char in tranz[i]:
                    for leg in tranz[i][char]:
                        l_char.append(leg)
            l_char=set(l_char)

            for j in l_char:
                if j in lambda_inchidere:
                    for leg in lambda_inchidere[j]:
                        lambda_after.append(leg)

            lambda_after=[*set(lambda_after)]
            tranzNFA[nod][char]=lambda_after

def StariFinNFA(stari_fin, stari_finNFA, tranzNFA, lambda_inchidere):

    for fin in stari_fin:
        stari_finNFA.add(fin)
        for nod in tranzNFA:
            if nod in lambda_inchidere:
                if fin in lambda_inchidere[nod]:
                    stari_finNFA.add(nod)

def Redundant(n, stari_finNFA, tranzNFA):

    same=[]
    for nod1 in range(n-1): #luam perechi
        for nod2 in range(nod1+1,n):
            if tranzNFA[nod1]==tranzNFA[nod2] and (nod1 in stari_finNFA)==(nod2 in stari_finNFA):
                same.append((nod1,nod2))

    for pair in same:
        for nod in tranzNFA:
            for char in tranzNFA[nod]:
                lungime=len(tranzNFA[nod][char])
                for leg in range(lungime):
                    nodleg=tranzNFA[nod][char][leg]
                    if nodleg==pair[1]:
                        tranzNFA[nod][char][leg]=pair[0]

                tranzNFA[nod][char]=[*set(tranzNFA[nod][char])]

        if pair[1] in tranzNFA:
            del tranzNFA[pair[1]]
        if pair[1] in stari_finNFA:
            stari_finNFA.remove(pair[1])

def LNFAtoNFA():
    global stari_finNFA, lambda_inchidere, tranzNFA

    lambda_inchidere={}
    tranzNFA={}
    stari_finNFA=set()

    LambdaInchidere(n,tranz,lambda_inchidere)

    FctTranzToNFA(n,tranz,tranzNFA,lambda_inchidere,alfabet)

    StariFinNFA(stari_fin,stari_finNFA,tranzNFA,lambda_inchidere)

    Redundant(n,stari_finNFA,tranzNFA)

    #refacem starile finale dupa eliminarea celor redundante:
    StariFinNFA(stari_fin,stari_finNFA,tranzNFA,lambda_inchidere)

    print("NFA-ul obtinut:")
    for nod in tranzNFA:
        print(f"{nod}: {tranzNFA[nod]}")
    print(f"Stari finale: {stari_finNFA}")
    print()




Citire()
LNFAtoNFA()






