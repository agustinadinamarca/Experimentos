#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sintetic import createAgents
from nego import negociation
from time import perf_counter
from numpy import mean

def exp():
	numAg = 100
	sol = -1

	while sol != 1:
		t0 = perf_counter()
		agents = createAgents(numAg=numAg, numMaxGoals=2, numAlt=3, numMaxAp=5, numMaxEp=3, attacksDensity=0.4)
		tf = perf_counter()
		print("Example creation", tf - t0)
		
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

		# Cantidad de ejecuciones de la negociación
		N = 10

		#for a in agents:
		#	i = a.get_acceptableArgs()
		#	#print("i", i, len(i))
				
		for i in range(N):
			print(i+1)
			print("start")
			t0 = perf_counter() # tiempo inicial
			r = negociation(agents, X)
			tf = perf_counter() # tiempo final
			print("end")
			if r[0] == True:
				lst.append(r[1])
			print(tf-t0)
			times.append(tf - t0) # duración de la negociación
			
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
		
		sol = 1
		
	file1 = open("results-optimo.txt", "w")
	file1.write("Results without Ignorance Relation\n")
	file1.write("Number of executions: "+str(N)+"\n")
	file1.write("Number of agreements: "+str(agreements)+"\n")
	file1.write("Optimal agreement: "+str(optima)+"\n")
	file1.write("Average Time (1 execution):"+str(mean(times))+"\n")

	file1.close()
		
exp()
