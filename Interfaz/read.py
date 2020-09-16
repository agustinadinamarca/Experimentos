#!/usr/bin/env python
# -*- coding: utf-8 -*-

import agentPaf as ag
import arguments as ar

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

        if j[cnt1+4] == "Practical Arguments":
            Ap = set()
            temp = j[cnt1+5]
            cnt2=0
            while temp != "Epistemic Arguments":
                t = temp.split()
                #print(t)
                if t[0] == "PRO":
                    S=set()
                    count=3
                    while count < len(t):
                        if t[count] == "2":
                            S.add((t[count+1], float(t[count+2])))
                            count+= 3
                        elif t[count] == "3":
                            S.add((t[count+1], t[count+2], float(t[count+3])))
                            count+= 4
                    Ap.add(ar.ArgPRO(S, t[2], t[1], G))
                else:
                    S=set()
                    count=3
                    while count<len(t):
                        if t[count] == "2":
                            S.add((t[count+1], float(t[count+2])))
                            count+= 3
                        elif t[count] == "3":
                            S.add((t[count+1], t[count+2], float(t[count+3])))
                            count+= 4
                    Ap.add(ar.ArgCON(S, t[2], t[1], G))

                cnt2+=1
                temp = j[cnt1+5+cnt2]
        
        c=0
        for i in range(len(j)):
            if j[i] == "Epistemic Arguments":
                c=i
        #print(j[len(j)-1])
        if j[c] == "Epistemic Arguments":
            Ae = set()
            temp = j[c+1]
            cnt=0
            while c+1+cnt < len(j):
                t = temp.split()
                #print(temp)
                H = set()
                count=1
                while count < len(t):
                    if t[count] == "2":
                        H.add((t[count+1], float(t[count+2])))
                        count+= 3
                    elif t[count] == "3":
                        H.add((t[count+1], t[count+2], float(t[count+3])))
                        count+= 4

                Ae.add(ar.ArgEp(H, t[0]))
                cnt+=1
                if c+1+cnt < len(j):
                    temp = j[c+1+cnt]
                else:
                    break
        #print(Ae)
        PafAgents.add(ag.Agent(name=name, K=set(), G=G, X=alt, Ae=Ae, Ap=Ap, semanticRoRI="RI", numAttacksToProcessInit=0, numAttacksToProcessByTurn=0))

    #print(PafAgents)

    #for a in PafAgents:
    #    print(a.name)
    #    print(a._Agent__X)
    #    print(a._Agent__G)
    #    for k in a._Agent__Ap:
    #        print(k.S, k.C, k.x, type(k))
    #    for k in a._Agent__Ae:
    #        print(k.H, k.h, type(k))
    return PafAgents
