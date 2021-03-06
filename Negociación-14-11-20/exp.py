#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sintetic import createAgents
from nego import negociation
from time import perf_counter
from numpy import mean

#from nego import negociation
from scipy import stats
from time import perf_counter
from agentPaf import Agent, modifyArgs
import numpy as np
from read2 import readFile
from math import fabs

################################
### SETTINGS
################################
global numAg# número de agentes
global N # cantidad de ejecuciones de negociación (agentes con TAF)
global M # numero de ejecuciones de negociacion (agentes con PAF)
global val1 # valor de ataques y no ataques a determinar inicialmente
global val2 #  valor de ataques y no ataques a determinar por turnos
global numMaxGoals # numero max de goals por agente
global numAlt # numero de alternativas
global numMaxAp # numero max de argumentos practicos por agente
global numMaxEp # numero max de argumentos practicos por agente
global attacksDensity # densidad de ataques por agente

numAg = 5 # número de agentes
N = 1 # cantidad de ejecuciones de negociación (agentes con TAF)
M = 1 # numero de ejecuciones de negociacion (agentes con PAF)
val1= [5] # valor de ataques y no ataques a determinar inicialmente
val2 = [2] #  valor de ataques y no ataques a determinar por turnos
numMaxGoals=2
numAlt=3
numMaxAp=5
numMaxEp=3
attacksDensity=0.4
################################
	
def exp():

	
	sol = -1

	while sol != 1:
		t0 = perf_counter()
		agents = createAgents(numAg, numMaxGoals, numAlt, numMaxAp, numMaxEp, attacksDensity)
		tf = perf_counter()
		print("Example creation:", tf - t0, "s")
		
		# Genero archivo con el ejemplo de sistema de agentes negociadores
		fileI = open("exp-example.txt", "w")

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
			fileI.write("Practical Arguments\n")

			for e in ag._Agent__Ap:
				fileI.write(e[0]+" "+e[1]+" "+e[2]+" "+str(round(e[4], 2))+" ")
				for k in e[3]:
					fileI.write(k)
					fileI.write(" ")
				fileI.write("\n")
									
			fileI.write("Epistemic Arguments\n")
	  
			for e in ag._Agent__Ae:
				fileI.write(e[0]+" ")
				for k in e[1]:
					fileI.write(k)
					fileI.write(" ")
				fileI.write("\n")
					
				

			fileI.write("Name\n")
	 
		fileI.close()

		# Ejecuto la negociación N veces

		lst = [] # almacena las alternativas ganadoras de cada agreement
		times = []

		#for a in agents:
		#	i = a.get_acceptableArgs()
		#	#print("i", i, len(i))
		print("Start", N, "negociations with", numAg, "agents...")
		
		for i in range(N):
			#print("start")
			t0 = perf_counter() # tiempo inicial
			r = negociation(agents, X)
			tf = perf_counter() # tiempo final
			#print("end")
			if r[0] == True:
				lst.append(r[1])
			#print(tf-t0)
			times.append(tf - t0) # duración de la negociación
		print("End negociations...")
		print("Average time:", mean(times), "s")	
			#for a in agents:
			#	i = a.get_acceptableArgs()
			#	#print("f", i, len(i))
				
		agreements = len(lst) # cantidad de agreements
		optimalAgreement = set(lst) # set de soluciones óptimas
		sol = len(set(lst)) # num
		
		optima = -1
		if agreements > 0:
			optima = lst[0] ### guardo la solución optima (si esta es 1)
		else:
			optima = None

	file1 = open("results-optimo.txt", "w")
	file1.write("Results without Ignorance Relation\n")
	file1.write("Number of executions: "+str(N)+"\n")
	file1.write("Number of agreements: "+str(agreements)+"\n")
	file1.write("Optimal agreement: "+str(optima)+"\n")
	file1.write("Average Time (1 execution):"+str(mean(times))+"\n")

	file1.close()
	


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

def getAccRe(agentName, agentsSet):
	for ag in agentsSet:
		if ag[0] == agentName:
			return [ag[1], ag[2]] 
			
###########################################
# CASO CON IGNORANCE RELATION
# En cada agente se puede especificar:
# + semántica (R o RI)
# + número de ataques a procesar antes de que el agente comience a negociar
# + número de ataques a procesar al recibir un argumento durante la negociación

def exp1():

    fname = "metric-d.txt"
    
    agentsF = readFile()

    optima = get_optima()

    Ag = list(agentsF)
    
    #accRe=[]
    #for a in Ag:
    #	accRe.append([a.name, len(a._Agent__Ap), set(a.get_acceptableArgs())])
    	
    L = len(Ag)
    X = Ag[0]._Agent__X
    
    # Semánticas: R o RI
    SSet = []
    for i in range(0, 1):
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
    #val1 = [5]

    for k in val1:
        at1 = []
        for i in range(L):
            at1.append(k) # especifico valor de número de ataques a procesar
        AT1.append(at1)
    # Número de ataques a procesar durante la negociación
    AT2 = []
    #3
    #val2 = [2]#1, 3, 5]
    for k in val2:
        at2 = []
        for i in range(L):
            at2.append(k) # especifico valor de número de ataques a procesar
        AT2.append(at2)

    countQ = 0

    countat2 = 0

    #print(len(SSet), len(AT1), len(AT2))
    
    fileA = open(fname, "w")
    fileA.write("Argumentation Problem: "+"exp-example.txt "+"generated using sintetic.py\n")
    fileA.write("Decision-Making Algorithm:\n")
    fileA.write("k_Init k_Turn N_R N_I Davg Dstd TimeAvg TimeStd TP TN FP FN TPstd TNstd FPstd FNstd\n")
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

              for i in range(L):
                  k = Ag[i]
                  # agent PAF
                  
                  AE, AP, ttt = modifyArgs(Ap=k._Agent__Ap, Ae=k._Agent__Ae, numAttacksToProcessInit=AT1[countat1][i])
                  nn = Agent(name=k.name, K=set(), G=k._Agent__G, X=k._Agent__X,
                             Ae=AE, Ap=AP, semanticRoRI=S[i], negoPer=0.4,
                             numAttacksToProcessInit=AT1[countat1][i],
                             numAttacksToProcessByTurn=AT2[countat2][i], S0=ttt)
                             
                  print("o")
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

              fileA = open(fname, "a+")
              countQ += 1
              
              lst = []
              tim = [] # lista de tiempos de ejecución
              di = [] # métrica d por ejecución
              
              FP = []
              FN = []
              TP = []
              TN = []

              #M = 1 # número de ejecuciones
              print("Start")
              for i in range(M):
                  np.random.shuffle(S)
                  i=0
                  for w1 in pafAgents:
                    w1.sem = S[i]
                    i+=1
                  	  
                  t0 = perf_counter() # tiempo inicial
                  r = negociation(pafAgents, X)
                  tf = perf_counter() # tiempo final
                  
                  tim.append(tf - t0) # duración de la negociación
                  
                  for a in pafAgents:
                    tp, tn, fp, fn = a.metric1() #[TP, TN, FP, FN]
                    TP.append(tp)
                    TN.append(tn)
                    FP.append(fp)
                    FN.append(fn)
                    
                  if r[1] == optima:
                    di.append(0)
                  elif r[1] != optima and r[1] == -1:
                    di.append(2)
                  elif r[1] != optima and r[1] != -1:
                    di.append(1)
                    
              print("Finish --- ", np.mean(tim)*M) 
              agreements = len(lst) # número de agreements
              optimalAgreement = set(lst) # set de agreements  
              
              fileA.write(str(AT1[countat1][0])+" ") # k init
              fileA.write(str(AT2[countat2][0])+" ") # k turn
              fileA.write(str(getNumR(S))+" ") # N_R
              fileA.write(str(L - getNumR(S))+" ") # N_i
              fileA.write(str(np.mean(di))+" ")
              fileA.write(str(np.std(di))+" ")
              fileA.write(str(np.mean(tim))+" ")
              fileA.write(str(np.std(tim))+" ")
              fileA.write(str(np.mean(TP))+" ")
              fileA.write(str(np.mean(TN))+" ")
              fileA.write(str(np.mean(FP))+" ")
              fileA.write(str(np.mean(FN))+" ")
              fileA.write(str(np.std(TP))+" ")
              fileA.write(str(np.std(TN))+" ")
              fileA.write(str(np.std(FP))+" ")
              fileA.write(str(np.std(FN))+"\n")
              #fileA.write(str(np.mean(neg))+" ")
              #fileA.write(str(np.std(neg))+" ")
              #fileA.write(str(np.mean(pos))+" ")
              #fileA.write(str(np.std(pos))+"\n")
              del pafAgents
              del tim
              del di
              
              fileA.close()
              
          countat1 += 1
      countat2 += 1
      		
exp()
exp1()
