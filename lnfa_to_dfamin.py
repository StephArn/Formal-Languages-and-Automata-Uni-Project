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
                        queue.append([*new])

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
    global tranzDFA, stari_finDFA, nDFA
    tranzDFA={}
    stari_finDFA = set()
    notatie=[]
    newtranzDFA={}

    TranzDFA(q0,alfabet,tranzNFA,tranzDFA)

    StariFinDFA(stari_finNFA,stari_finDFA,tranzDFA)

    Rename(q0,stari_finDFA,tranzDFA,newtranzDFA,notatie)

    tranzDFA=newtranzDFA

    for nod in tranzDFA:
        for char in tranzDFA[nod]:
            tranzDFA[nod][char]=int(tranzDFA[nod][char].replace("_",""))

    print("DFA-ul obtinut:")
    for nod in tranzDFA:
        print(f"{nod}: {tranzDFA[nod]}")
    print(f"Stari finale:{stari_finDFA}")
    print()

    nDFA=len(tranzDFA)

def Echivalente(alfabet, stari_finDFA, tranzDFA, groups):

    #matrice cu stari:
    mat=[[1 for i in range(len(tranzDFA))] for j in range(len(tranzDFA))]
    #fin cu nefin ->0:
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if i in stari_finDFA and j not in stari_finDFA:
                mat[i][j]=0
                mat[j][i]=0

    ok=1
    while ok:
        ok=0
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if mat[i][j]==1:
                    for char in alfabet:
                        #inchiderea:
                        x=tranzDFA[i][char]
                        y=tranzDFA[j][char]
                        if mat[x][y]==0:
                            mat[i][j]=0
                            mat[j][i]=0
                            ok=1

    for i in range(len(mat)):
        multime=set()
        for j in range(len(mat[i])):
            if mat[i][j]==1:
                multime.add(j)
        if multime not in groups:
            groups.append(multime)

def TranzDFAMin(tranzDFA, groups, stari, tranzDFAMin):

    #dictionar cu starile urmatoare dintr-o anumita stare:
    for nod in groups:
        stare=''
        for ele in sorted([*nod], reverse=True):
            stare=stare+str(ele)
            stare=stare+'_'

        tranzDFAMin[stare]={}

        for ele in nod:
            stari[ele]=stare

    for nod in tranzDFA:
        for char in tranzDFA[nod]:
            #aflam noile stari:
            #start1 si stop1 pt dfa, start2 si stop2 pt dfa min
            start1=nod
            stop1=tranzDFA[nod][char]
            start2=stari[start1]
            stop2=stari[stop1]
            tranzDFAMin[start2][char]=stop2

def StariFinDFAMin(stari, stari_finDFA, stari_finDFAMin):

    for fin in stari_finDFA:
        stari_finDFAMin.add(stari[fin])

def ParcurgereDFAMin(nod, viz, tranzDFAMin):

    if viz[nod]==0:
        viz[nod]=1
        for char in tranzDFAMin[nod]:
            if viz[tranzDFAMin[nod][char]]==0:
                ParcurgereDFAMin(tranzDFAMin[nod][char], viz, tranzDFAMin)

def Deadend(tranzDFAMin, stari_finDFAMin, newtranzDFAMin):

    eliminate=[]
    for nod in tranzDFAMin:
        viz={}
        ok=0

        for ele in tranzDFAMin:
            viz[ele]=0

        ParcurgereDFAMin(nod,viz,tranzDFAMin)

        for fin in stari_finDFAMin:
            if viz[fin]==1:
                ok=1

        if ok==0:
            eliminate.append(nod)

    for nod in tranzDFAMin:
        if nod not in eliminate:
            newtranzDFAMin={}
            for char in tranzDFAMin[nod]:
                if tranzDFAMin[nod][char] not in eliminate:
                    newtranzDFAMin[nod][char]=tranzDFAMin[nod][char]

def Neaccesibile(stare_init_min, tranzDFAMin, newtranzDFAMin):

    eliminate=[]
    viz={}

    for nod in tranzDFAMin:
        viz[nod]=0

    ParcurgereDFAMin(stare_init_min,viz,tranzDFAMin)

    for nod in viz:
        if viz[nod]==0:
            eliminate.append(nod)

    for nod in tranzDFAMin:
        if nod not in eliminate:
            newtranzDFAMin[nod]={}
            for char in tranzDFAMin[nod]:
                if tranzDFAMin[nod][char] not in eliminate:
                    newtranzDFAMin[nod][char]=tranzDFAMin[nod][char]

def Eroare(nDFA, tranzDFA, alfabet):

    global eroare
    eroare=nDFA

    for nod in range(nDFA):
        if nod not in tranzDFA:
            tranzDFA[nod]={}
            for char in alfabet:
                tranzDFA[nod][char]=nDFA

        for char in alfabet:
            if char not in tranzDFA[nod]:
                tranzDFA[nod][char]=nDFA

    tranzDFA[eroare]={}

    for char in alfabet:
        tranzDFA[eroare][char]=nDFA

def DFAtoDFAMin():

    global nDFA, tranzDFAMin, stari_finDFAMin, stare_init_min

    Eroare(nDFA,tranzDFA,alfabet)

    tranzDFAMin={}
    groups=[]
    stari={}
    stari_finDFAMin=set()
    newtranzDFAMin={}

    Echivalente(alfabet,stari_finDFA,tranzDFA,groups)

    TranzDFAMin(tranzDFA,groups,stari,tranzDFAMin)

    if q0 in stari:
        stare_init_min=stari[q0]

    StariFinDFAMin(stari,stari_finDFA,stari_finDFAMin)

    Deadend(tranzDFAMin,stari_finDFAMin,newtranzDFAMin)

    tranzDFAMin=newtranzDFAMin

    newtranzDFAMin={}

    Neaccesibile(stare_init_min,tranzDFAMin,newtranzDFAMin)

    tranzDFAMin=newtranzDFAMin

    print("DFA-ul Minimal obtinut:")
    for nod in tranzDFAMin:
        print(f"{nod}: {tranzDFAMin[nod]}")
    print(f"Stari finale: {stari_finDFAMin}")


Citire()
LNFAtoNFA()
NFAtoDFA()
DFAtoDFAMin()






