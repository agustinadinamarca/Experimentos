#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sintetic as s
import nego as n
from scipy import stats
import time
import agentPaf as ap
import numpy as np
import arguments as ar
import read2 as red

def lenInt(setA, setB):
    count = 0
    for a in setA:
        for b in setB:
            if a[0].t == "E" and a[1].t == "P" and b[0].t == "E" and b[1].t == "P":
                if a[0].H == b[0].H and a[0].h == b[0].h  and a[1].S == b[1].S and a[1].C == b[1].C and a[1].x == b[1].x:
                    count += 1
            elif a[0].t == "E" and a[1].t == "C" and b[0].t == "E" and b[1].t == "C":
                if a[0].H == b[0].H and a[0].h == b[0].h  and a[1].S == b[1].S and a[1].C == b[1].C and a[1].x == b[1].x:
                    count += 1
            elif a[0].t == "E" and a[1].t == "E" and b[0].t == "E" and b[1].t == "E":
                if a[0].H == b[0].H and a[0].h == b[0].h  and a[1].H == b[1].H and a[1].h == b[1].h:
                    count += 1
    return count

def get_optima():
    F = open("results-optimo.txt", "r")
    count = 0
    optima = -111
    for line in F:
        if count==3:
            l = line.split()
            F.close()
            return l[2]
        count+=1
    
def getNumR(S):
    count = 0
    for s in S:
        if s == "R":
            count += 1
    return count
###########################################
# CASO CON IGNORANCE RELATION
# En cada agente se puede especificar:
# + semántica (R o RI)
# + número de ataques a procesar antes de que el agente comience a negociar
# + número de ataques a procesar al recibir un argumento durante la negociación

def experiment(it, kinit, kturn):

    fname = "metric-d.txt"
    
    agents = red.readFile()

    optima = get_optima()

    Ag = list(agents)
    
    del agents
    
    #print(Ag)
    
    L = len(Ag)
    X = Ag[0]._Agent__X
    
    # Semánticas: R o RI
    SSet = []
    for i in range(0, L+1):
        S = []
        if i == 0:
            for j in range(L):
                S.append("RI")
            SSet.append(S)
        else:
            for w in range(i):
                S.append("R")
            for k in range(i, L):
                S.append("RI")
            SSet.append(S)

    # Número de ataques a procesar al inicio
    AT1 = []
    #18
    val1 = [int(x) for x in kinit]
    

    for k in val1:
        at1 = []
        for i in range(L):
            at1.append(k) # especifico valor de número de ataques a procesar
        AT1.append(at1)
    # Número de ataques a procesar durante la negociación
    AT2 = []
    #3
    val2 = [int(x) for x in kturn]
    for k in val2:
        at2 = []
        for i in range(L):
            at2.append(k) # especifico valor de número de ataques a procesar
        AT2.append(at2)

    countQ = 0

    countat2 = 0

    #print(len(SSet), len(AT1), len(AT2))
    
    fileA = open(fname, "w")
    fileA.write("k_Init k_Turn N_R N_I Davg Dstd TimeAvg TimeStd AvFNR StdFNR AvFPR StdFPR\n")
    fileA.close()
    
    while countat2 < len(val2):
      countat1 = 0
      while countat1 < len(val1):
          c = 0
          for S in SSet:
              c+=1
              pafAgents = set()
              #gc.collect()
              print(countat1, countat2, c)
              D = [] # arreglo para guardar métrica d
              # introduzco aleatoriedad en el/los agentes con semántica/s R y RI
              #np.random.shuffle(S)
              print(S)
              for i in range(L):
                  k = Ag[i]
                  nn = ap.Agent(name=k.name, K=k._Agent__K, G=k._Agent__G, X=k._Agent__X, Ae=k._Agent__Ae, Ap=k._Agent__Ap, semanticRoRI=S[i], numAttacksToProcessInit=AT1[countat1][i], numAttacksToProcessByTurn=AT2[countat2][i])
                  #print(k._Agent__Ap)
                  #k.semanticRoRI= S[i]
                  #k.numAttacksToProcessInit=AT1[countat1][i]
                  #k.numAttacksToProcessByTurn=AT2[countat2][i]
                  #print(k._Agent__accArgs)
                  pafAgents.add(nn)
                  #print(k.semanticRoRI,k.numAttacksToProcessInit, k.numAttacksToProcessByTurn)
                  del k
                  del nn
              print("Ok")
              #print(pafAgents, len(pafAgents))
              
              fileA = open(fname, "a+")
              #file1 = open("results_"+str("cRI-")+str(countQ)+".txt", "w")
              countQ += 1
              
              #file1.write("Results with Ignorance Relation\n")
              card = [] # para almacenar |R|, |R*|, etc
              lst = []
              turns = []
              tim = [] # lista de tiempos de ejecución
              di = [] # métrica d por ejecución
              
              N = it # número de ejecuciones
              for i in range(N):
                  np.random.shuffle(S)
                  i=0
                  for w1 in pafAgents:
                    w1.sem = S[i]
                    #print(w1.numAttacksToProcessByTurn)
                    i+=1
                    
                  t0 = time.perf_counter() # tiempo inicial
                  r = n.negociation(pafAgents, X)
                  tf = time.perf_counter() # tiempo final
                  turns.append([r[2], r[3], r[4]])
                  tim.append(tf - t0) # duración de la negociación
                  if r[2] == optima:
                    di.append(0)
                  elif r[2] != optima and r[2] == -1:
                    di.append(2)
                  elif r[2] != optima  and r[2] != -1:
                    di.append(1)
                    
                  # Calculo de cardinalidades R*, N*, I, R, N por agente
                  for a in pafAgents:
                      norm = float(len(a.Re) + len(a.Ne))
                      if a.sem == "R":
                          FPRj = 0 
                          FNRj = lenInt(a.I, a.Re) / norm
                          card.append([FNRj, FPRj])
                      elif a.sem == "RI":
                          FPRj = lenInt(a.I, a.Ne) / norm
                          FNRj = 0
                          card.append([FNRj, FPRj])
                          
                  if r[1] == True:
                      lst.append(r[2])
            
              agreements = len(lst) # número de agreements
              optimalAgreement = set(lst) # set de agreements  
              
              

              # MÉTRICA D
              D.append([getNumR(S), S, AT1[countat1], AT2[countat2], np.mean(di), np.std(di)])
              fileA.write(str(AT1[countat1][0])+" ")
              fileA.write(str(AT2[countat2][0])+" ")
              fileA.write(str(D[len(D)-1][0])+" ") # N_R
              fileA.write(str(L - D[len(D)-1][0])+" ") # N_i
              #for i in range(len(S)): # semánticas
              #    fileA.write(str(D[len(D)-1][1][i])+" ")
              #for i in range(len(S)):
              #    fileA.write(str(D[len(D)-1][2][i])+" ")
              #    fileA.write(str(D[len(D)-1][3][i])+" ")
              fileA.write(str(D[len(D)-1][4])+" ")
              fileA.write(str(D[len(D)-1][5])+" ")
              fileA.write(str(np.mean(tim))+" ")
              fileA.write(str(np.std(tim))+" ")
              Wn = []
              Wp = []
              for w in card:
                  Wn.append(w[0]) # neg
                  Wp.append(w[1]) # pos

              fileA.write(str(np.mean(Wn))+" ")
              fileA.write(str(np.std(Wn))+" ")
              fileA.write(str(np.mean(Wp))+" ")
              fileA.write(str(np.std(Wp))+"\n")

              lst = []

              order = stats.itemfreq(turns)
              for i in range(len(order)-1):
                  lst.append(list(order[i]))

              tur = []
              for e in lst:
                  tur.append(e[0])

              l = []
              for e in tur:
                  s = []
                  for k in turns:
                      if e == k[1]:
                          s.append(k[0])
                  l.append(s)

              d = []
              for x in l:
                  d.append([len(x), set(x)])

              fileA.close()
              del pafAgents
              del card
              del D
              del tim
              del turns
              del di
              del d
              del l
              del tur
              del lst
              del r
          countat1 += 1
      countat2 += 1

