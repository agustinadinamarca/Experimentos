#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import module.agent as ag
import random


def createAgents(numAg, numMaxGoals, numAlt, numMaxAp, numMaxEp, attacksDensity):
    agents = set()

    BGs = createGoalsBases(num=numAg, numMaxGoals=numMaxGoals)
    X = createAlternatives(num=numAlt)
    
    A = createArguments(numAg, numMaxAp, numMaxEp, attacksDensity, X)

    for i in range(numAg):
        agents.add(ag.Agent("Ag"+str(i+1), set(), BGs[i], X, A[i][1], A[i][0], attacksDensity))

    return agents
             


def createArguments(numAg, nMPrac, nMEpis, attacksDensity, Alt):
    ArgsBases = []
    for i in range(numAg):
        ap = random.randint(len(Alt), nMPrac)
        ae = random.randint(1, nMEpis)
        
        numAtMax = ap * ae + ae * (ae - 1) / 2
        numAt = round(numAtMax * attacksDensity, 0)
        
        Ap=set()
        Ae=set()
        
        for j in range(ap):
            Ap.add("ap"+str(j+1)+"Ag"+str(i+1))
        for j in range(ae):
            Ae.add("ae"+str(j+1)+"Ag"+str(i+1))

        At = set()
        for e in Ap:
            At.add(e)
        for e in Ae:
            At.add(e)

        attacks = set()

        while len(attacks) < numAt:
            arg1 = np.random.choice(list(Ae), 1)[0]
            arg2 = np.random.choice(list(At), 1)[0]
            if arg1 != arg2:
            	if (arg1, arg2) not in attacks and (arg2, arg1) not in attacks:
            		attacks.add((arg1, arg2))
        
        x = list(Alt)

        if len(x) < ap:
            for j in range(ap - len(x)):
                x.append(np.random.choice(list(Alt), 1)[0])
                
        App = []
        c=0
        for e in Ap:
            t = np.random.choice(["P", "C"], 1)[0]
            f = random.random()
            arg = (e, t, x[c], [], f, [])
            for k in attacks:
                if e == k[1]:
                    arg[3].append(k[0])
            App.append(arg)
            c+=1
            
        Aee = []
        for e in Ae:
            arg = (e, [], [])
            for k in attacks:
                if e == k[1]:
                    arg[1].append(k[0])
            Aee.append(arg)
            
        ArgsBases.append([App, Aee])
    return ArgsBases
            
            
  
def createAlternatives(num):
    if num > 0:
        alternatives = set()
        for i in range(num):
            alternatives.add("X"+str(i+1)) 
        return alternatives
    else:
        return "Error"
    
def createGoalsBases(num, numMaxGoals):
    if num > 0 and numMaxGoals > 0:
        gBases = []
        for i in range(num):
            k = random.randint(1, numMaxGoals)
            g = set()
            E = list(np.random.choice(numMaxGoals, k, replace=False))
            for j in range(k):
                w = random.uniform(0.01, 1) # (0, 1]
                g.add(("g"+str(E[j]+1), round(w, 2)))
            gBases.append(g)
        return gBases
    else:
        return "Error"

