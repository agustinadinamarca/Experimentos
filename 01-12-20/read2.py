#!/usr/bin/env python
# -*- coding: utf-8 -*-

from agent import Agent

def readFile():
    F = open("exp-example.txt", "r")

    N = int(F.readline())

    f = []
    for line in F:
        f.append(line.replace("\n", ""))

    F.close()

    l = []
    a = []
    for k in f:
        if k != "Name":
            l.append(k)
        else:
            a.append(l)
            l = []
    a.pop(0)

    PafAgents = set()

    for j in a:
        name = j[0]
        temp = j[1] # Goals
        G = set()
        cnt1 = 2
        while temp!="Altenatives":
            #print(temp=="Alternatives")
            if temp != "Alternatives":
                k = j[cnt1].split()
                #print(cnt1, k)
                G.add((k[0], float(k[1])))
            else:
                break
            cnt1+=1
            temp = j[cnt1]
        
        if j[cnt1] == "Alternatives":
            alt = set(j[cnt1+1].split())
        
        Ae=[]
        if j[cnt1+4] == "Practical Arguments":
            Ap = []
            temp = j[cnt1+5]
            cnt2=0
            while temp != "Epistemic Arguments":
                t = temp.split()
            #    #print(t)
                Ap.append([t[0], t[1], t[2], t[4:], float(t[3]), []])
                cnt2+=1
                temp = j[cnt1+5+cnt2]
        
        c=0
        for i in range(len(j)):
            if j[i] == "Epistemic Arguments":
                c=i
        #print(j[len(j)-1])
        if j[c] == "Epistemic Arguments":
            Ae = []
            temp = j[c+1]
            cnt=0
            while c+1+cnt < len(j):
                t = temp.split()
                Ae.append([t[0], t[1:], []])
                cnt+=1
                if c+1+cnt < len(j):
                    temp = j[c+1+cnt]
                else:
                    break

        PafAgents.add(Agent(name=name, K=set(), G=G, X=alt, Ae=Ae, Ap=Ap, np=0.5))

    return PafAgents

"""    
ags = readFile()
for a in ags:
    print(a.name)
    print(a._Agent__X)
    print(a._Agent__G)
    print(a._Agent__Ap)
    print(a._Agent__Ae)
"""    
