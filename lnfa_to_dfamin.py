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

def TranzDFA(q0, alfabet, tranzNFA, tranzDFA):

    queue=[[q0]]
    vizitate=[{q0}]

    while(queue):
        vizitate.append({*queue[0]})
        for char in alfabet:
            #noua stari pt caracter:
            new=set()
            for ele in queue[0]:
                #tranzitiile initiale:
                for nod in tranzNFA[ele][char]:
                    #devin o sg mutlime:
                    new.add(nod)
                if new:
                    #verif daca a fost vizitata multimea obtinuta:
                    if new not in vizitate:
                        queue.append([*m])

                #trasformam in string cu _ intre starile combinate pt a diferentia
                stare=''
                for combin in sorted(queue[0],reverse=True):
                    stare=stare+str(combin)
                    stare=stare+'_'
                if stare not in tranzDFA:
                    tranzDFA[stare]={}
                if new:
                    tranzDFA[stare][char]=new
        del queue[0]

def StariFinDFA(stari_finNFA, stari_finDFA, tranzDFA):

    for ele in stari_finNFA:
        for stare in tranzDFA:
            nr=0
            for i in range(0, len(stare), 2):
                nr=nr*10 + int(stare[i])

            while nr>0:
                if nr%10==ele:
                    stari_finDFA.add(stare)
                    break
                nr=nr//10

def Rename(q0, stari_finDFA, tranzDFA, newtranzDFA, notatie):
    for nod in tranzDFA:
        #transf starile multimi in string:
        for char in tranzDFA[nod]:
            stare=''
            for ele in sorted([*tranzDFA[nod][char]], reverse=True):
                stare=stare+str(ele)
                stare=stare+'_'
                tranzDFA[nod][char]=stare

    #stabilim notatii:
    curent=1;
    notatie.append((str(q0)+'_',0))
    for nod in tranzDFA:
        schimbat=str(q0)+'_'
        if nod!=schimbat:
            notatie.append((nod,curent))
            curent+=1

    #dictionar cu noile denumiri pt chei si pt stari:
    for nod in tranzDFA:
        for char in tranzDFA[nod]:
            tranzDFA[nod][char]=str(tranzDFA[nod][char])

    for pair in notatie:
        if pair[0] in tranzDFA:
            newtranzDFA[pair[1]]=tranzDFA[pair[0]]

    for nod in newtranzDFA:
        for char in newtranzDFA[nod]:
            for pair in notatie:
                if newtranzDFA[nod][char]==pair[0]:
                    newtranzDFA[nod][char]=str(pair[1])
                    break

    #noile stari finale:
    for fin in stari_finDFA:
        for pair in notatie:
            if fin==pair[0]:
                stari_finDFA.remove(fin)
                stari_finDFA.add(pair[1])
                break

def NFAtoDFA():
    global  nr_stari, tranzDFA, stari_finDFA
    tranzDFA={}
    TranzDFA(q0,alfabet,tranzNFA,tranzDFA)
    stari_finDFA=set()
    StariFinDFA(stari_finDFA,stari_finDFA,tranzDFA)
    










Citire()
LNFAtoNFA()






