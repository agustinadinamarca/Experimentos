#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arguments as ar
import numpy as np
import agent as ag
import random


def createAgents(numAg, numMaxGoals, numAlt, numMaxAp, limMaxSup, numMaxEp):
    agents = set()
    # creo BGs
    BGs = createGoalsBases(num=numAg, numMaxGoals=numMaxGoals)
    X = createAlternatives(num=numAlt)
    ApBs = createAps(Alternativas=X, numMaxAp=numMaxAp, GBs=BGs, limMaxSup=limMaxSup)
    AeBs = createAes(Alternativas=X, numMaxAe=numMaxEp, GBs=BGs, limMaxSup=limMaxSup)
    
    for i in range(numAg):
        agents.add(ag.Agent("Ag"+str(i+1), set(), BGs[i], X, AeBs[i], ApBs[i]))

    return agents
             


  
def createAlternatives(num):
    if num > 0 and isinstance(num, int):
        alternatives = set()
        for i in range(num):
            alternatives.add("X"+str(i+1)) 
        return alternatives
    else:
        return "Error"
    
def createGoalsBases(num, numMaxGoals):
    if num > 0 and numMaxGoals > 0 and isinstance(num, int) and isinstance(numMaxGoals, int):
        gBases = []
        for i in range(num):
            k = random.randint(1, numMaxGoals)
            g = set()
            for j in range(k):
                w = random.uniform(0.1, 1) # permito importancia cero, cambiar
                g.add(("g"+str(j+1), round(w, 2))) # se podría cambiar
            gBases.append(g)
        return gBases
    else:
        return "Error"
              
def goalFromGoal(G):
    Gp = []
    for gj in G:
        Gp.append(gj[0])
    gi = np.random.choice(Gp, 1)[0]
    k = 0
    for gj in G:
        if gj[0] == gi:
            k = gj[1]  
    return gi


 
def createSupport(limMax, gi):
    Sy = ["a", "b", "c", "d", "e"]
    s = set()
    k = random.randint(1, limMax)
    o = []
    while len(o) <= k:
        fc1 = np.random.choice(Sy, 1)[0]
        fc = np.random.choice([fc1,"-"+fc1], 1)[0]
        if fc == fc1:
            fc2 = "-"+fc1
        else:
            fc2 = fc1
        if fc not in o and fc2 not in o:
            o.append(fc)
    
    if len(o) == 1:
        w = random.uniform(0.1, 1)
        s.add((o[0], round(w, 2))) # fact
        w = random.uniform(0.1, 1)
        s.add((o[0], gi, round(w, 2)))
        return s 
    else:
        w = random.uniform(0.1, 1)
        s.add((o[0], round(w, 2))) # fast
        for e in range(0, len(o)-1):
            w = random.uniform(0.1, 1)
            s.add((o[e], o[e+1], round(w, 2)))
        w = random.uniform(0.1, 1)
        s.add((o[len(o)-1], gi, round(w, 2)))
        return s
        
 
def createAps(Alternativas, numMaxAp, GBs, limMaxSup):
    ApBases = []
    for i in range(len(GBs)):
        Ap = set()
        x = list(Alternativas)
        k = random.randint(len(Alternativas), numMaxAp)
        #k = random.randint(1, numMaxAp)
        if len(x) < k:
            for j in range(k-len(x)):
                x.append(np.random.choice(list(Alternativas), 1)[0])
        #print k, x
        
        for j in range(k):
            typeArg = np.random.choice(["P", "C"], 1)[0]
            gi=goalFromGoal(GBs[i])
            #print "goal", gi
            if typeArg == "P":
                arg = ar.ArgPRO(createSupport(limMax=limMaxSup, gi=gi), gi, x[j], GBs[i])
                Ap.add(arg)
                
            else:
                arg = ar.ArgCON(createSupport(limMax=limMaxSup, gi=gi), gi, x[j], GBs[i])
                Ap.add(arg)
        ApBases.append(Ap) 
    return ApBases

 
 
def createSupportEp(limMax, gi):
    Sy = ["a", "b", "c", "d", "e", gi]
    s = set()
    k = random.randint(1, limMax)
    o = []
    while len(o) <= k+1:
        fc1 = np.random.choice(Sy, 1)[0]
        fc = np.random.choice([fc1,"-"+fc1], 1)[0]
        if fc == fc1:
            fc2 = "-"+fc1
        else:
            fc2 = fc1
        if fc not in o and fc2 not in o:
            o.append(fc)
    
    if len(o) == 2:
        w = random.uniform(0.1, 1)
        s.add((o[0], round(w, 2))) # fact
        w = random.uniform(0.1, 1)
        s.add((o[0], o[1], round(w, 2)))
        return s, o[1] 
    else:
        w = random.uniform(0.1, 1)
        s.add((o[0], round(w, 2))) # fast
        for e in range(0, len(o)-2):
            w = random.uniform(0.1, 1)
            s.add((o[e], o[e+1], round(w, 2)))
        w = random.uniform(0.1, 1)
        s.add((o[len(o)-2], o[len(o)-1], round(w, 2)))
        return s, o[len(o)-1]  


    
def createAes(Alternativas, numMaxAe, GBs, limMaxSup):
    AeBases = []
    for i in range(len(GBs)):
        Ae = set()
        k = random.randint(1, numMaxAe)
        for h in range(k):
            gi=goalFromGoal(GBs[i])
            s, ss = createSupportEp(limMax=limMaxSup, gi=gi)
            Ae.add(ar.ArgEp(s, ss))
        AeBases.append(Ae)
    return AeBases
  
