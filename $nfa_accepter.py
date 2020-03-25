def evaluate(word, stare_curenta):

    global stari_fin, tranz

    if word=="":
        if stare_curenta in stari_fin:
            return 1
        else:
            return 0

    urm=[] # retine starea/ starile care pot urma imediat in fct de stare curenta si de litera curenta
    cur=word[0]  # litera curenta din cuvantul de verificat

    for t in tranz[stare_curenta]:
        if t[0]==cur:
            urm.append(t[0])

    if not t:
        return 0

    for stare in urm:
        evaluate(word[1:], stare)



f = open("intrare.txt", "r")

n = int(f.readline())  # numar stari

m = int(f.readline())  # numar caractere alfabet

alfabet = []

for i in f.readline().split():
    alfabet.append(i)

q0 = int(f.readline())  # stare initiala

k = int(f.readline())  # numar stari finale

stari_fin = []

for i in f.readline().split():
    stari_fin.append(int(i))

l = int(f.readline())  # numar tranzitii

tranz = [[] for i in range(n)]

for i in range(l):
    si, char, sf = f.readline().strip().split()  # si=stare initiala a tranz, sf=stare finala a tranz
    tranz[int(si)].append((char, int(sf)))

word = input("testing the word: ")

ok=evaluate(word, q0)

if ok:
    print("DA")
else:
    print("NU")

f.close()
