f = open("intrare.txt", "r")

n = int(f.readline())  # numar stari

m = int(f.readline())  # numar caractere alfabet

alfabet = []

for i in f.readline().strip().split():
    alfabet.append(i)


q0 = f.readline()  # stare initiala
q0 = q0[:-1]

k = int(f.readline())  # numar stari finale

stari_fin = []

for i in f.readline().split():
    stari_fin.append(int(i))

l = int(f.readline())  # numar tranzitii

tranz = []

for i in range(l):
    t= f.readline()
    t = t.strip().split(" ")
    tranz.append(t) #lista cu liste cu tranzitii

word = input("testing the word: ")

lungime_cuv = len(word)

print(lungime_cuv)
cur=[q0]
i=0

litera_curenta=0

print(word)

while litera_curenta < lungime_cuv:
    urm=[]
    for stare in cur:
        #print(stare)
        for t in range(l):
            if tranz[t][1]=='$' and stare==tranz[t][0]:
                cur.append(tranz[t][2])
                urm.append(tranz[t][2])
            if litera_curenta < lungime_cuv and stare==tranz[t][0] and word[litera_curenta]==tranz[t][1] :
                print(tranz[t])
                urm.append(tranz[t][2])
           # print(cur)
            #print(urm)
    if not urm:
        print("NU")
        break
    else:
        cur=list(urm)
    litera_curenta += 1
else:
    ok=0
    for finala in stari_fin:
        for stare in cur:
            if int(stare) == finala:
                ok=1
                print("DA")
                break
        if ok==1:
            break
    else:
        print("NU")

print(tranz)

f.close()
