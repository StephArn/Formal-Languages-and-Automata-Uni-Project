f = open("intrare.txt", "r")

n=int(f.readline()) #numar stari

m=int(f.readline()) #numar caractere alfabet

alfabet=[]

for i in f.readline().split():
    alfabet.append[i]
    
q0=int(f.readline()) #stare initiala

k=int(f.readline()) #numar stari finale

stari_fin=[]

for i in range(k):
    stari_fin.append(int(f.readline()))
    
l=int(f.readline()) #numar tranzitii

tranz=[[] for i in range(n)]

for i in range(l):
    si,char,sf=f.readline().strip().split() #si=stare initiala a tranz, sf=stare finala a tranz
    tranz[int(si)].append((char, int(sf)))
    
word=f.readline()
   
f.close()
