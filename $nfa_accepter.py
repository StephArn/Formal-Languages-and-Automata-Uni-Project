def evaluate(word, stare_curenta):
    print(word)
    global stari_fin, tranz, ok
    if word=="":
        if stare_curenta in stari_fin:
            ok=1
            return 1
        else:
            ok=-1
            return 0

    urm=[]# retine starea/ starile care pot urma imediat in fct de stare curenta si de litera curenta
    cur=word[0]  # litera curenta din cuvantul de verificat
    lambd=0

    for t in tranz[stare_curenta]:
        if t[0]==cur:
            urm.append(t[1])
        elif t[0]=='$':
            lambd =1
            stare_curenta = t[1]
            urm.append(t[1])


    if not urm:
        ok=-1
        return 0
    for stare in urm:
        print(stare)
        print("aici")
        if lambd==0:
            evaluate(word[1:], stare)
        if lambd==1:
            evaluate(word, stare)




f = open("intrare.txt", "r")

n = int(f.readline())  # numar stari

m = int(f.readline())  # numar caractere alfabet

alfabet = []

for i in f.readline().strip().split():
    alfabet.append(i)

stari_fin = []

q0 = int(f.readline())  # stare initiala

k = int(f.readline())  # numar stari finale

for i in f.readline().split():
    stari_fin.append(int(i))

l = int(f.readline())  # numar tranzitii

tranz = [[] for i in range(n)]

for i in range(l):
    si, char, sf = f.readline().strip().split()  # si=stare initiala a tranz, sf=stare finala a tranz
    tranz[int(si)].append((char, int(sf)))

word = input("testing the word: ")

ok=0

okret= evaluate(word, q0)

if ok==1:
    print("DA")
if ok==-1:
    print("NU")


f.close()
