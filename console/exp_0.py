#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sintetic as sin
import nego as n
from scipy import stats
import time
import agentPaf as ap
import numpy as np
import arguments as ar
import cProfile

def exp():
    # Ingreso el número de agentes en la negociación
    numAg = 5

    # Creo los agentes
    # numMaxGoals: número máximo de goals por agente
    # numAlt: número de alternativas a negociar
    # numMaxAp: cantidad máxima de argumentos prácticos por agente
    # numMaxEp: cantidad máxima de argumentos epistémicos por agente

    sol = -1

    while sol != 1:
        agents = sin.createAgents(numAg=numAg, numMaxGoals=2, numAlt=3, numMaxAp=5, limMaxSup=1, numMaxEp=5)

        # Genero archivo con el ejemplo de sistema de agentes negociadores
        fileI = open("exp-example.txt", "w")

        #fileI.write("Number of agents: "+str(numAg)+"\n")
        fileI.write(str(numAg)+"\n")
        fileI.write("Name\n")
        for ag in agents:
            fileI.write(str(ag.name)+"\n")
            fileI.write("Goals\n ")
            for g in ag._Agent__G: 
                fileI.write(str(g[0])+" "+str(g[1])+"\n")
                
            fileI.write("Alternatives\n")
            for x in ag._Agent__X:
                fileI.write(str(x)+" ")

            fileI.write("\nCandidates decisions preferred order\n")
            fileI.write(str(ag.candidatesDecisionPrefOrder())+"\n")
            
            X = ag._Agent__X
            fileI.write("Practical Arguments")

            for e in ag._Agent__Ap:
                if isinstance(e, ar.ArgPRO):
                    fileI.write("\nPRO "+e.x+" "+e.C+" ")
                    for s in e.S:
                        if len(s) == 2:
                            fileI.write(str(2)+" "+str(s[0])+" "+str(s[1])+" ")
                        else:
                            fileI.write(str(3)+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+" ")
                    
                elif isinstance(e, ar.ArgCON):
                    fileI.write("\nCON "+e.x+" "+e.C+" ")
                    for s in e.S:
                        if len(s) == 2:
                            fileI.write(str(2)+" "+str(s[0])+" "+str(s[1])+" ")
                        else:
                            fileI.write(str(3)+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+" ")
                    
            fileI.write("\nEpistemic Arguments")
      
            for a in ag._Agent__Ae:
                fileI.write("\n"+str(a.h)+" ")
                for s in a.H:
                    if len(s) == 2:
                        fileI.write(str(2)+" "+str(s[0])+" "+str(s[1])+" ")
                    else:
                        fileI.write(str(3)+" "+str(s[0])+" "+str(s[1])+" "+str(s[2])+" ")

            fileI.write("\nName\n")
     
        fileI.close()
        
        fileF = open("attacks-example.txt", "w")
        for am in agents:
            fileF.write("\n"+am.name+"\n")
            fileF.write("\nA\n")
            fileF.write(str(am._Agent__attacks))
            fileF.write("\nU\n")
            fileF.write(str(am._Agent__undercuts))
            fileF.write("\nSA\n")
            fileF.write(str(am._Agent__stronglyAttacks))
            fileF.write("\nSU\n")
            fileF.write(str(am._Agent__stronglyUndercuts))
        fileF.close()

        # Ejecuto la negociación N veces

        lst = []
        times = []
        turns = []

        # Cantidad de ejecuciones de la negociación
        N = 1000

        for i in range(N):
            t0 = time.time() # tiempo inicial
            r = n.negociation(agents, X)
            tf = time.time() # tiempo final
            turns.append([r[2], r[3], r[4]])
            if r[1] == True:
                lst.append(r[2])
            times.append(tf - t0) # duración de la negociación
                
        
        agreements = len(lst) # cantidad de agreements
        optimalAgreement = set(lst) # set de soluciones óptimas
        sol = len(set(lst))
        optima = -1
        if agreements > 0:
            optima = lst[0] ### guardo la solución optima (si esta es 1)
        else:
            optima = None

        lst = []
        order = stats.itemfreq(turns)
        for i in range(len(order)-1):
            lst.append(list(order[i]))
            
        tur = []
        for e in lst:
            tur.append(e[0])
            
        l=[]
        for e in tur:
            s = []
            for k in turns:
                if e == k[1]:
                    s.append(k[0])
            l.append(s)

        d = []
        for x in l:
            d.append([len(x), set(x)])

        # Genero archivo con la información de la negociación
        file1 = open("results-optimo.txt", "w")

        file1.write("Results without Ignorance Relation\n")
        file1.write("Number of executions: "+str(N)+"\n")
        file1.write("Number of agreements: "+str(agreements)+"\n")
        file1.write("Optimal agreement: "+str(optima)+"\n")
        file1.write("Average Time (1 execution):"+str(np.mean(times))+"\n")
        file1.write("Turns vs # Agreements:\n")
        for k in lst:
            file1.write(str(k)+"\n")
        file1.write("Turns vs Agreements:\n")
        for k in range(len(tur)):
            file1.write(tur[k]+" "+str(d[k])+"\n")

        file1.close()

        # Ejecuto la negociación N veces

        lst = []
        times = []
        turns = []

        # Cantidad de ejecuciones de la negociación
        N = 1000

        for i in range(N):
            t0 = time.time() # tiempo inicial
            r = n.negociation(agents, X)
            #cProfile.run("n.negociation(agents, X)", "test.profile")
            tf = time.time() # tiempo final
            turns.append([r[2], r[3], r[4]])
            if r[1] == True:
                lst.append(r[2])
            times.append(tf - t0) # duración de la negociación
                
        
        agreements = len(lst) # cantidad de agreements
        optimalAgreement = set(lst) # set de soluciones óptimas
        sol = len(set(lst))
        optima = -1
        if agreements > 0:
            optima = lst[0] ### guardo la solución optima (si esta es 1)
        else:
            optima = None

        lst = []
        order = stats.itemfreq(turns)
        for i in range(len(order)-1):
            lst.append(list(order[i]))
            
        tur = []
        for e in lst:
            tur.append(e[0])
            
        l=[]
        for e in tur:
            s = []
            for k in turns:
                if e == k[1]:
                    s.append(k[0])
            l.append(s)

        d = []
        for x in l:
            d.append([len(x), set(x)])

        # Genero archivo con la información de la negociación
        file1 = open("results-optimo.txt", "w")

        file1.write("Results without Ignorance Relation\n")
        file1.write("Number of executions: "+str(N)+"\n")
        file1.write("Number of agreements: "+str(agreements)+"\n")
        file1.write("Optimal agreement: "+str(optima)+"\n")
        file1.write("Average Time (1 execution):"+str(np.mean(times))+"\n")
        file1.write("Turns vs # Agreements:\n")
        for k in lst:
            file1.write(str(k)+"\n")
        file1.write("Turns vs Agreements:\n")
        for k in range(len(tur)):
            file1.write(tur[k]+" "+str(d[k])+"\n")

        file1.close()
        
#cProfile.run("exp()", "test.profile")
exp()
