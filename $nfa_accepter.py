def evaluate(stare_curenta,word,poz,mat):
    global cases,stari_fin,n
    lungime=len(word)
    if poz==lungime:
        if stare_curenta in stari_fin:
            cases.append(1)
        else:
            lambd=0
            for stare2 in range(n):
                if type(mat[stare_curenta][stare2]) is list:
                    if '$' in mat[stare_curenta][stare2]:
                        lambd=1
                else:
                    if mat[stare_curenta][stare2]=='$':
                        lambd=1

            if lambd==0:
                cases.append(0)
            else:
                for stare2 in range(n):
                    if type(mat[stare_curenta][stare2]) is list:
                        for char in range(len(mat[stare_curenta][stare2])):
                            if mat[stare_curenta][stare2][char] == '$':
                                evaluate(stare2, word, poz,mat)
                    else:
                        if mat[stare_curenta][stare2] == '$':
                            evaluate(stare2, word, poz,mat)

    else:
        good=0
        for stare2 in range(n):
            if type(mat[stare_curenta][stare2]) is list:
                if '$' in mat[stare_curenta][stare2] or  word[poz] in mat[stare_curenta][stare2]:
                    good=1
            else:
                if word[poz] == mat[stare_curenta][stare2] or '$' == mat[stare_curenta][stare2]:
                    good=1
        if good==0:
            cases.append(0)
        else:
            for stare2 in range(n):
                if type(mat[stare_curenta][stare2]) is list:
                    lenmat=len(mat[stare_curenta][stare2])
                    for char in range(lenmat):
                        if mat[stare_curenta][stare2][char] == '$':
                            evaluate(stare2, word, poz,mat)
                        elif mat[stare_curenta][stare2][char] == word[poz]:
                            evaluate(stare2, word, poz+1,mat)
                else:
                    if mat[stare_curenta][stare2] == '$':
                        evaluate(stare2, word, poz,mat)
                    elif mat[stare_curenta][stare2] == word[poz]:
                        evaluate(stare2, word, poz+1,mat)




f = open("intrare.txt", "r")

n = int(f.readline())  # numar stari

m = int(f.readline())  # numar caractere alfabet

alfabet = []

for i in f.readline().strip().split():
    alfabet.append(i)
alfabet.append('$')

q0 = int(f.readline())  # stare initiala

k = int(f.readline())  # numar stari finale

stari_fin = []

for i in f.readline().split():
    stari_fin.append(int(i))

l = int(f.readline())  # numar tranzitii

tranz = []

for i in range(l):
    si, char, sf= f.readline().strip().split()
    tranz.append([int(si),char,int(sf)]) #lista cu liste cu tranzitii

f.close()

word = input("testing the word: ")

#cases=[]
cases=[]

mat=[[0]*n for i in range(n)]
for t in tranz:
    if mat[t[0]][t[2]] == 0:
        mat[t[0]][t[2]] = t[1] #practic punem prima legatura gasita
    else:
        #punem toate legaturile existente intre acele doua stari
        mat[t[0]][t[2]] = [mat[t[0]][t[2]]]
        mat[t[0]][t[2]].append(t[1])


evaluate(q0,word,0,mat)

if 1 in cases:
    print("DA")
else:
    print("NU")
