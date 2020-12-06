#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools # for a powerset function implementation
#import arguments as ar # import arguments module
#import numpy as np
import random
from math import fabs

#librería para cfs
import networkx as nx
from networkx.algorithms.approximation import max_clique

##################################################################################
### DM ARGUMENTATION FRAMEWORK - Amgoud and Prade (2004)
##################################################################################

class CS: # commitment store
	def __init__(self):
		self.S = [] # contains the offers proposed by the agent and those it has accepted
		self.A = [] # is the set of arguments presented by the agent (argument supports)
		self.C = [] # is the set of challenges made by the agent 
		# otro
		self.R = []
		self.SN = []
		#self.M = []
		self.AS = []
		
	def add_ProposedOrAcceptedOffer(self, x):
		self.S.append(x)
	def add_ArgumentPresented(self, arg):
		self.A.append(arg)
	def add_ChallengePresented(self, challenge):
		self.C.append(challenge)
	def add_Refuse(self, ref):
		self.R.append(ref)


def numAtaquesReales(Ap, Ae):
	count=0
	for e in Ap:
		count+=len(e[3])
	for f in Ae:
		count+=len(f[1])
	return count
	
def modifyArgs(Ap, Ae, numAttacksToProcessInit):
	ATP = int(len(Ap)*len(Ae)+len(Ae)*(len(Ae)-1)/2) # ataques totales máx
	NAP = numAttacksToProcessInit # ataques a procesar inicialmente
	Re = numAtaquesReales(Ap, Ae) # ataques reales
	NumNe = fabs(ATP - Re) # no ataques reales
	#print("Args intactos:", Ae, Ap)
	
	#print("NUMNA", NumNe, "NUMRE", Re)
	if NAP >= ATP:
		ttt = [0, Re, NumNe, 0, 0]
		#print("NInit>=ATMax", NAP, ATP) #### borrar
		return Ae, Ap, ttt
		
	else:
		NumI = ATP - NAP # cantidad de ataques o no ataques no determinados
		NumIR = 0
		NumIN = 0
		#print("Primer loop, start...")
		for k in range(NumI):
			#print("Ok", k)
			p = random.random() # [0, 1)
			if p < 0.5:
				if NumIR < Re:
					# NOproceso ataque
					NumIR+=1
				elif NumIN < NumNe:
					NumIN+=1
			else:
				if NumIN < NumNe:
					#NO proceso un no ataque
					NumIN+=1
				elif NumIR < Re:
					NumIR+=1
		#print("Primer loop, end...")
		#print(NumI, NumIN, NumNe, NumIR, Re, "ok???") ##########3
		
		ttt = [NumI, Re, NumNe, NumIR, NumIN]
		#print(ttt, "ttt")
		
		#print(ttt) ###########
		#print("Ok", NumIR, NumIN)
		
		# con ataques reales
		T1 = []
		#sin ataques reales
		T2 = [] 
		for e in Ap:
			if len(e[3]) > 0:
				T1.append(e)
			else:
				T2.append(e)
		for e in Ae:
			if len(e[1]) > 0:
				T1.append(e)
			else:
				T2.append(e)
		
		#print("while loop 1 start..")	
		#print(T1, "T1 INIT")
		count=0
		while count < NumIR and len(T1) > 0:
			#print(count)
			i = random.randint(0, len(T1)-1) # indice
			#print(i, len(T1))
			#print(i, T[i])
			if len(T1[i])==3: #epistemico
				if len(T1[i][1])>0: # hay atacantes
					j = random.randint(0, len(T1[i][1])-1) # indice de atacante
					k = T1[i][1][j]
					T1[i][1].pop(j) 
					T1[i][2].append(k)
					count+=1
					if len(T1[i][1]) == 0: # si se quedó sin atacantes reales
						T2.append(T1[i]) # lo agrego a T2
						T1.pop(i) # lo saco de la lista
			else: #practico
				if len(T1[i][3])>0: # hay atacantes
					j = random.randint(0, len(T1[i][3])-1) # indice de atacante
					k = T1[i][3][j]
					T1[i][3].pop(j) 
					T1[i][5].append(k)
					count+=1
					if len(T1[i][3]) == 0: # si se quedó sin atacantes reales
						T2.append(T1[i]) # lo agrego a T2
						T1.pop(i) # lo saco de la lista
		
		#print(T1, "T1 FIN")
		#print("while loop 1 end...")	
		#print("ok1")
		
		T = []
		for e in T1:
			T.append(e)
		for e in T2:
			T.append(e)
			
		#print("while loop 2 start..")	
		count=0
		#print(count, NumIN, NumIR)
		
		# calculemos todos lo no ataques
		F=[]
		for e1 in T:
			for e2 in Ae:
				if len(e1) == len(e2):
					if e1[0] != e2[0]:
						if e1[0] not in e2[1] and e1[0] not in e2[2] and e2[0] not in e1[1] and e2[0] not in e1[2]:
							if (e2[0], e1[0]) not in F:
								F.append((e1, e2))
				elif len(e1)>len(e2):
					if e2[0] not in e1[3] and e2[0] not in e1[5]:
						F.append((e2, e1))
				else:
					if e1[0] not in e2[3] and e1[0] not in e2[5]:
						F.append((e1, e2))
						
		#print(len(F), NumIN, NumNe, NumIR, Re, NumI)
		#print(F)
		#print(T)
		
		if NumIN > 0 and len(F) > 0:
		    for i in range(NumIN):
			    #print(NumIN, i, "ok")
			    k = random.randint(0, len(F)-1) 
			    s = F[k]
			    F.pop(k)
			    for j in range(len(T)):
				    if T[j][0] == s[1]:
					    T[j][5].append(s[0][0])
				
		"""
		while count < NumIN:
			i = random.randint(0, len(T)-1) # epi y prac
			if len(T[i]) == 3:
				count1=0
				while count1 < 2:
					j = random.randint(0, len(Ae)-1) # epi
					if T[i][0] != Ae[j][0]: # si son distintos
						if T[i][0] not in Ae[j][1] and T[i][0] not in Ae[j][2] and Ae[j][0] not in T[i][1] and Ae[j][0] not in T[i][2]:
							T[i][2].append(Ae[j][0])
							count1 += 1		  
			else:
				count1 = 0
				while count1 < 2:
					j = random.randint(0, len(Ae)-1) # epi
					if Ae[j][0] not in T[i][3] and Ae[j][0] not in T[i][5]:
						T[i][5].append(Ae[j][0])
						count1 += 1
			count+=1
			
		""" 
		"""
		while count < NumIN: # num de no ataques que son puestos como ataques posibles
			i = random.randint(0, len(T)-1) # epi y prac
			j = random.randint(0, len(Ae)-1) # epi
			
			if len(T[i])==3 and T[i][0] != Ae[j][0]: # si es epist y el epist no es si mismo
				if Ae[j][0] not in T[i][1] and Ae[j][0] not in T[i][2]: #si no esta en los atacantes ni en los posibles
					if T[i][0] not in Ae[j][1] and T[i][0] not in Ae[j][2]:
						T[i][2].append(Ae[j][0])
						count+=1
			elif len(T[i])==6:
				if Ae[j][0] not in T[i][3] and Ae[j][0] not in T[i][5]:
					T[i][5].append(Ae[j][0])
					count+=1
			else:
				print("ERROR")
		"""
		#print("while loop 2 end...")
		
			
		AP = []
		AE = []
		for t in T:
			if len(t)==3:
				AE.append(t)
			else:
				AP.append(t)
		return AE, AP, ttt
		
# Case: inconsistence bases y criterio bipolar de Amgoud and Prade 2009
# The framework computes the ‘best’ decision (if it exists)

class Agent:
	def __init__(self, name, K, G, X, Ae, Ap, semanticRoRI, negoPer, numAttacksToProcessInit, numAttacksToProcessByTurn, S0):
		self.sem = semanticRoRI
		self.name = name # un label con el nombre del agente
		self.numAttacksToProcessInit = numAttacksToProcessInit
		self.numAttacksToProcessByTurn = numAttacksToProcessByTurn
		self.negoPer = negoPer
		self.__K = K # Knowledge base
		self.__G = G # Goals base
		self.__X = X # Alternatives
		self.__Ae = Ae
		self.__Ap = Ap
		#self.__Ar = self.get_AllArguments()
		self.Re = S0[1]
		self.Ne = S0[2]
		self.I = S0[0]
		self.N = S0[2] - S0[4]
		self.R = S0[1] - S0[3]
		self.Ir = S0[3]
		self.In = S0[4]
		 # epistemic arguments
		#self.__arguments = self.get_AllArguments() # Practical and epistemic arguments
		
		#self.__undercuts = self.get_undercuts()
		#self.__attacks = self.get_attacks()
		#self.__stronglyUndercuts = self.get_stronglyUndercuts()
		#self.__stronglyAttacks = self.get_stronglyAttacks()
		#self.__accArgs = self.get_acceptableArgs()
		#self.__rejArgs = self.get_rejectedArgs()

		self.cs = CS() # commitment store for negociation
		self.negociation = Agent.Negociation(self)


		
	def metric1(self):
		sem = self.sem
		R = self.R
		Re = self.Re
		Ne = self.Ne
		N = self.N
		I = self.I
		In = self.In
		Ir = self.Ir
		
		TP, TN, FP, FN = 0, 0, 0, 0
		
		if sem == "R":
			TP = R / (Re + Ne)
			TN = Ne / (Re + Ne)
			FP = 0
			FN = Ir / (Re + Ne)
			
		else:
			TP = Re / (Re + Ne)
			TN = N / (Re + Ne)
			FP = In / (Re + Ne)
			FN = 0
		
		return [TP, TN, FP, FN]
	   
	def getNum_I(self):
		Ae = self.__Ae
		Ap = self.__Ap
		
		count = 0
		
		for ae in Ae:
			count += len(ae[2])
			
		for ap in Ap:
			count += len(ap[5])
			
		return count
		
	def getNum_R(self):
		Ae = self.__Ae
		Ap = self.__Ap
		
		count = 0
		
		for ae in Ae:
			count += len(ae[1])
		for ap in Ap:
			count += len(ap[3])
		
		return count
		
	########################################
	# Retorna la base de conocimientos K especificada
	def get_KnowledgeBase(self):
		return self.__K

	# Retorna la base de objetivos G especificada
	def get_GoalsBase(self):
		return self.__G

	# Retorna el conjunto de alternativas X especificado
	def get_Alternatives(self):
		return self.__X

	# Retorna todos los argumentos prácticos dados K, G y X
	def get_PracticalArguments(self):
		return self.__Ap

	# Retorna todos los argumentos epistémicos dados K, G y X
	def get_EpistemicArguments(self):
		return self.__Ae

	# Retorna todos los argumentos dados K, G y X
	def get_AllArguments(self):
		T = self.__Ap + self.__Ae
		return T

	def allArguments(self):
		args = self.get_AllArguments()
		argsAll = set()
		for e in args:
			argsAll.add(e[0])
		return argsAll
	
	def getAttackers(self, arg):
		args = self.get_AllArguments()
		for a in args:
			if a[0]==arg:
				if len(a)==3:
					d=[]
					if len(a[1])>0:
						for e in a[1]:
							d.append(e)
					if len(a[2])>0:
						for e in a[2]:
							d.append(e)
					return d
				else:
					d=[]
					if len(a[3])>0:
						for e in a[3]:
							d.append(e)
					if len(a[5])>0:
						for e in a[5]:
							d.append(e)
					return d
		return []
					
	def getAttackersR(self, arg):
		args = self.get_AllArguments()
		for a in args:
			if a[0]==arg:
				if len(a)==3:
					return a[1]
				else:
					return a[3]
		return []
					
	def getArg(self, arg):
		args = self.get_AllArguments()
		for a in args:
			if a[0] == arg:
				return a
	#B strongly undercuts A (resp. B strongly attacks A) iff
	#B undercuts A (resp. B attacks A) and it is not the case
	#that A is preferred to B.
	def get_stronglyUndercuts(self, sem):
		stronglyUndercuts = set()
		#print(self.__Ae)
		if sem=="R":
			for e in self.__Ae:
				if len(e[1])>0:
					for f in e[1]:
						stronglyUndercuts.add((f, e[0]))
			return stronglyUndercuts
		if sem=="RI":
			for e in self.__Ae:
				if len(e[1])>0:
					for f in e[1]:
						stronglyUndercuts.add((f, e[0]))
						
				if len(e[2])>0:
					for f in e[2]:
						stronglyUndercuts.add((f, e[0]))
				
			return stronglyUndercuts
		

	def get_stronglyAttacks(self, sem):
		stronglyAttacks = set()
		#print(self.__Ap)
		if sem=="R":
			for e in self.__Ap:
				#print(len(e))
				#print(e[3], len(e[3]))
				if len(e[3])>0:
					for f in e[3]:
						#print(f)
						stronglyAttacks.add((f, e[0]))
						#print("ok")
			return stronglyAttacks
		if sem=="RI":
			for e in self.__Ap:
				#print(len(e))
				#print(e[3], len(e[3]))
				if len(e[3])>0:
					for f in e[3]:
						#print(f)
						stronglyAttacks.add((f, e[0]))
						#print("ok")
				if len(e[5])>0:
					for f in e[5]:
						#print(f)
						stronglyAttacks.add((f, e[0]))
						#print("ok")
						
			return stronglyAttacks
		

	#A set of arguments E defends an argument A if there
	#is some argument in E which strongly undercuts (resp.
	#strongly attacks) every argument B where B undercuts (resp. attacks) A and A cannot defend itself
	#against B.
	# ACEPTABLE --> si el conjunto E lo defiende de sus atacantes/undercuters
	def __is_defendedBySet(self, arg, E):

		Bs = self.getAttackers(arg)
		
		Bs = set(Bs)
		E = set(E)
		
		if len(Bs.intersection(E)) > 0:
			return False
		else:
			if len(E) >= 0:
				if len(Bs)>0:
					lst=set()
					for element in Bs:
						lst.union(set(self.getAttackersR(element)))
					if len(lst.intersection(E))==len(lst):
						return True
					else:
						return False
				else:
					return True
	# retorna conjunto de elementos que son atacados o undercutted
	#def __get_argsAttackedOrUndercutted(self):
	#	 lst=set()
	#	 for pair in self.__undercuts:
	#		 lst.add(pair[1])
	#	 for pair in self.__attacks:
	#		 lst.add(pair[1])
	#	 return lst

	def get_acceptableArgs(self): # esto es la semántica grounded  ##############################################
		S = self.compute_grounded_extensions()
		s = set()
		for i in S:
			for j in i:
				s.add(j)
		return s

	def __is_CandidateDecision(self, d):
		gA = self.get_acceptableArgs()
		for c in gA:
			a = self.getArg(c)
			if len(a)==6:
				if c == a[0] and a[2]== d:
					return True
		return False

	def get_CandidatesDecisions(self):
		candidates = []
		for x in self.__X:
			if self.__is_CandidateDecision(x) == True:
				candidates.append(x)
		return candidates

	# PRO Let d and d' ∈ D. d is preferred to d'
	#iff ∃ A ∈ S and Conclusion(A) = d such that ∀ A' ∈ S and Conclusion(A') = d'
	#, then min(LevelP (A), W eightP (A)) ≥ min(LevelP (A' ), W eightP (A')).

	# CON Let d, d 0 ∈ D. d is preferred to d 0 , denoted
	#d . O d 0 , iff ∃ A ∈ A O with Conclusion(A) = d such that ∀ B ∈
	#A O with Conclusion(B) = d 0 , then A is preferred to B.

	def __get_Acc_PRO(self, decision):
		argPro = []
		accArgs = self.get_acceptableArgs()
		for arg in accArgs:
			a = self.getArg(arg)
			if len(a) == 6 and a[1]=="P":
				if a[2] == decision:
					argPro.append(a)
		return argPro

	def __get_Acc_CON(self, decision):
		argCon = []
		accArgs = self.get_acceptableArgs()
		for arg in accArgs:
			a = self.getArg(arg)
			if len(a) == 6 and a[1]=="C":
				if a[2] == decision:
					argCon.append(a)
		return argCon
	"""
	def get_Acc_CON_X(self):
		args = set()
		for x in self.__X:
			s = self.__get_Acc_CON(x)
			for ss in s:
				args.add(ss)
		return args
	"""		
	def __is_Preferred_PRO_d1(self, argsProD1, argsProD2): # retorna "Primera", "Segunda" o "Equal"
		l1 = len(argsProD1)
		l2 = len(argsProD2)
		if l1 > 0 and l2 > 0:
			strengthsProD1 = []
			strengthsProD2 = []
			for element1 in argsProD1:
				strengthsProD1.append(element1[4])
			for element2 in argsProD2:
				strengthsProD2.append(element2[4])
			d1 = max(strengthsProD1)
			d2 = max(strengthsProD2)
			if d1 > d2:
				return "Primera"
			if d2 > d1:
				return "Segunda"
			if d1 == d2:
				if l1 > l2:
					return "Primera"
				elif l1 < l2:
					return "Segunda"
				else:
					return "Equal"

	def __is_Preferred_CON_d1(self, argsConD1, argsConD2):
		l1 = len(argsConD1)
		l2 = len(argsConD2)
		if l1 > 0 and l2 > 0:
			strengthsConD1 = []
			strengthsConD2 = []
			for element1 in argsConD1:
				strengthsConD1.append(element1[4])
			for element2 in argsConD2:
				strengthsConD2.append(element2[4])
			d1 = max(strengthsConD1)
			d2 = max(strengthsConD2)
			if d1 > d2:
				return "Primera"
			if d2 > d1:
				return "Segunda"
			if d1 == d2:
				if l1 > l2:
					return "Segunda"
				elif l1 < l2:
					return "Primera"
				else:
					return "Equal"

	def get_Preferred(self, d1, d2):
		d1PRO = self.__get_Acc_PRO(d1)
		d1CON = self.__get_Acc_CON(d1)
		d2PRO = self.__get_Acc_PRO(d2)
		d2CON = self.__get_Acc_CON(d2)

		# PARTE PRO
		statusPro = 0
		statusCon = 0

		if len(d1PRO)==0 and len(d2PRO)==0:
			statusPro = None
		if len(d1PRO)==0 and len(d2PRO)>0:
			statusPro = "Segunda"
		if len(d1PRO)>0 and len(d2PRO)==0:
			statusPro = "Primera"
		if len(d1PRO)>0 and len(d2PRO)>0:
			statusPro = self.__is_Preferred_PRO_d1(d1PRO, d2PRO)

		if len(d1CON)==0 and len(d2CON)==0:
			statusCon = None
		if len(d1CON)==0 and len(d2CON)>0:
			statusCon = "Primera"
		if len(d1CON)>0 and len(d2CON)==0:
			statusCon = "Segunda"
		if len(d1CON)>0 and len(d2CON)>0:
			statusCon = self.__is_Preferred_CON_d1(d1CON, d2CON)

		if statusPro == None and statusCon == None:
			return None

		if statusPro == None and statusCon != None:
			if statusCon=="Primera":
				return d1
			if statusCon=="Segunda":
				return d2
			if statusCon=="Equal":
				return None

		if statusCon == None and statusPro != None:
			if statusPro=="Primera":
				return d1
			if statusPro=="Segunda":
				return d2
			if statusPro=="Equal":
				return None

		if statusPro ==	 "Primera" and statusCon == "Primera":
			return d1

		if statusPro ==	 "Segunda" and statusCon == "Segunda":
			return d2
		
		if statusPro ==	 "Segunda" and statusCon == "Primera":
			return None

		if statusPro ==	 "Primera" and statusCon == "Segunda":
			return None

		if statusPro ==	 "Equal" and statusCon == "Equal":
			return None

		if statusPro ==	 "Equal" and statusCon == "Primera":
			return d1

		if statusPro ==	 "Equal" and statusCon == "Segunda":
			return d2

		if statusPro ==	 "Primera" and statusCon == "Equal":
			return d1

		if statusPro ==	 "Segunda" and statusCon == "Equal":
			return d2
			
	# nueva (:
	def compute_cfs(self):
		N = list(self.allArguments())
		A = list(self.get_stronglyUndercuts(self.sem).union(self.get_stronglyAttacks(self.sem)))
		G = nx.Graph()
		G.add_nodes_from(N)
	
		#Crear matriz de no_ataques
		aristas = []
	
		for i in range(0, len(N)):
			for j in range(i + 1, len(N)):
				
				no_ataque=True
				
				for r in A:
					if (r[0] == N[i] and r[1] == N[j]) or (r[0] == N[j] and r[1] == N[i]):
						no_ataque = False
						break
						
				if no_ataque:
					aristas.append((N[i],N[j]))
	  
		G.add_edges_from(aristas)
		
		C = nx.find_cliques(G)
		z=[]
		s = set()
		count = 0
		for c in C:
			count += 1
			k = powerset(c)
			z.append(len(c))
			for i in k:
				s.add(i)
		return s

	"""
	# Computa los conjuntos de argumentos que son cfs (subconjuntos de argumentos
	# que no se atacan entre sí).
	def compute_cfs(self):
			args = self.allArguments()
			pwr = powerset(args)
		
			sU = self.get_stronglyUndercuts(self.sem)
			sA = self.get_stronglyAttacks(self.sem)
			
			if len(sU) > 0:
				for x in sU:
				   x1 = x[0]
				   x2 = x[1]
				   todelete = []
				   for i in pwr:
					   if x1 in i and x2 in i:#if (x1 in i) and (x2 in i):
						   todelete.append(i)
				   for i in todelete:
					   pwr.remove(i)

			if len(sA) > 0:
				for x in sA:
					x1 = x[0]
					x2 = x[1]
					todelete = []
					for i in pwr:
						if x1 in i and x2 in i:#if (x1 in i) and (x2 in i):
							todelete.append(i)
					for i in todelete:
						pwr.remove(i)

			return set(pwr)

	"""
	
	def candidatesDecisionPrefOrder(self):
		X = self.get_CandidatesDecisions()
		if len(X) == 0:
			return ["equallyPreferred", self.__X]
		else:
			lst = self.__selectionSort(X) # lista de preferencias de mayor a menor, res None, [a,b]
			if lst == None:
				return ["equallyPreferred", self.__X]
			else:
				return ["prefOrder", lst]
			
	def __selectionSort(self, aList): # lista de alternativas candidatas
		l = len(aList)
		if l > 0:
			for i in range(l):
				least = i # índice de alternativa
				for k in range(i+1, l):
					a = self.get_Preferred(aList[k], aList[least]) 
					if a == aList[k]:
						least = k
					#if a == None:
					#	 return None

				swap(aList, least, i)
			return aList
		else:
			return None

	#############################
	# For each conflict free subset, if its attackers are
	# attacked (exhaustively) by a subset of that cfs, it is admissible
	# A conglict-free set of arguments S is ADMISIBLE iff each argument
	# in S is ACCEPTABLE with respect to S.

	def compute_admissibility(self, cfs):
		admissible = []
		if len(cfs) > 0:
			# tomo cada cf subset de cfs del AF
			for cfset in cfs:
				lst=[]
				if len(cfset) >= 0:
					for element in cfset:
						if self.__is_defendedBySet(element, cfset) == True:
							lst.append(True)
						else:
							lst.append(False)
					if all(lst):
						#admissible.append(cfset)
						if cfset == ():
							admissible.append(set())
						else:
							d = set()
							for k in cfset:
								#for kk in k:
									d.add(k)
							admissible.append(d)  


		return admissible

	# An admissible set S of arguments is called a complete extension iff
	# each argument, which is acceptable with respect to S, belongs to S.
	def compute_complete_extensions(self):
				arguments=self.allArguments()
				compl = []
				cfs = self.compute_cfs()
				if len(cfs)>0:
					adm = self.compute_admissibility(cfs)
					if len(adm)>0:
						for conj in adm:
							accArgs = set()
							for x in arguments:
								if self.__is_defendedBySet(x, conj) == True:
									accArgs.add(x)
							if len(accArgs.intersection(conj)) == len(accArgs) and len(accArgs.intersection(conj)) == len(conj):
								lst = []
								for x in accArgs:
									s = False
									if x in conj:
										s = True
									lst.append(s)
								if all(lst):
									compl.append(conj)
				return compl

	# E is the (unique) grounded extension of AF only if it is the smallest element	  
	# (with respect to set inclusion) among the complete extensions of S.
	def compute_grounded_extensions(self):
		grd = []
		compExt = self.compute_complete_extensions()
		count=0
		l = -99
		if len(compExt)>0:
			for conj in compExt:
				le = len(conj)
				if count == 0:
				   l = le
				else:
					if le < l:
						l = le
				count+=1
					
			for x in compExt:
				if len(x) == l:
					grd.append(x)

		return grd


	# incorporacion de argumento externo si este es aceptable
	def argExtIsAcceptable(self, arg):
		acc = self.get_acceptableArgs()
		if arg[0] in acc:
			return True
		else:
			return False
	
	def compAltChallenge(self, current):
		lst = []
		candidates = self.get_CandidatesDecisions()
		for x in candidates:
			if x != current:
				if self.get_Preferred(x, current) != current:
					return True
		return False
	
	def compAltAcc(self, current):
		candidates = self.get_CandidatesDecisions()
		if len(candidates) == 0:
		    return True
		elif current not in candidates:
		    return False
		elif len(candidates) == 1 and current in candidates:
		    return True
		else:
		    for x in candidates:
			    if x != current:
				    r = self.get_Preferred(x, current)
				    if r != current and r != None:
				        return False
		    return True
		
	class Negociation:
		def __init__(self, af):
			self.af = af
			# Speach acts
			self.offer = Agent.Negociation.Offer(self)
			self.challengeX = Agent.Negociation.ChallengeX(self)
			self.challengeY = Agent.Negociation.ChallengeY(self)
			self.argue = Agent.Negociation.Argue(self)
			#self.withdraw = Agent.Negociation.Withdraw(self)
			self.acceptX = Agent.Negociation.AcceptX(self)
			self.acceptS = Agent.Negociation.AcceptS(self)
			self.refuse = Agent.Negociation.Refuse(self)
			#self.sayNothing = Agent.Negociation.SayNothing(self)
		
		# OK---
		class Offer:
			def __init__(self, af):
				self.af = af
			def preConditions(self,alternativasRestantes): # conj de args CON de otros agentes, todos: g0 true o false
				cd = self.af.af.candidatesDecisionPrefOrder()
				
				for e in cd[1]:
					if e in alternativasRestantes:
						return e
				if len(alternativasRestantes) > 0:
					return alternativasRestantes[0]
				
				return None
				  
			def postConditions(self, x):
				self.af.af.cs.add_ProposedOrAcceptedOffer(x) # add offer to the commitment store of the agent
		# OK---
		class ChallengeX:
			def __init__(self, af):
				self.af = af
			def preConditions(self, currentOffer):
				if currentOffer not in self.af.af.cs.S:
					return True
				else:
					return False
				"""
				if currentOffer not in self.af.af.cs.C and currentOffer not in self.af.af.cs.S:
					r = self.af.af.compAltChallenge(currentOffer)
					if r == True:
						return True
					else:
						return False
				else:
					return False
				""" 
			def postConditions(self, currentOffer):
				self.af.af.cs.add_ChallengePresented(currentOffer)

		# OK---
		class ChallengeY: # y wff(L)
			def __init__(self, af):
				self.af = af
			def preConditions(self, y):
				if y not in self.af.af.cs.C:
					return True # Siempre se cumple
				else:
					return False

			def postConditions(self, y):
				self.af.af.cs.add_ChallengePresented(y)
				
		# OK--- completar
		class Argue:
			def __init__(self, af):
				self.af = af
			def preConditions(self, currentOffer, neg):
				# obtengo argumentos aceptables asociados a currentOffer (PRO y CON)
				#print("PRE ARGUE ---?")
				if neg == True:
					con = self.af.af._Agent__get_Acc_CON(currentOffer)
					pro = self.af.af._Agent__get_Acc_PRO(currentOffer)
					args = []
					
					if pro != set():
						for e in pro:
							args.append(e)
					if con != set():
						for e in con:
							args.append(e)
					#print(args,"OK?")
					
					#print("Debug-Args ACC TO PRESENT")
					#for e in args:
					#	 print(e.S, e.C, e.x, e)
						
						
					argsPresented = self.af.af.cs.A #list
					#print(argsPresented, "OK?")
					#print("Debug-ArgsPresented", argsPresented)
					#print("ok")
					a = searchArgs(argsPresented, args)
					#print("RESULT", a)
					if a != False:
						#print("aaa", a, self.af.af.getArg(a))
						return tuple(self.af.af.getArg(a)) # retorna un argumento aceptable para el agente
					else:
						return False # si no tengo argumentos

			def postConditions(self, currentOffer, neg, arg):
				self.af.af.cs.A.append(arg)
				#for k in self.af.af.cs.A:
				#	 print("0", k.S, k.C, k.x)
				"""
				argsPresented = set()
				for e in self.af.af.cs.A:
					argsPresented.add(e[0])
				con = self.af.af._Agent__get_Acc_CON(currentOffer)
				pro = self.af.af._Agent__get_Acc_PRO(currentOffer)
				args = set()
					
				if pro != set():
					for e in pro:
						args.add(e[0])
				if con != set():
					for e in con:
						args.add(e[0])
				
				if len(args.intersection(argsPresented)) == len(args):
					self.af.af.cs.SN.append(True)
				"""

		# OK---
		class AcceptX:
			def __init__(self, af):
				self.af = af
			def preConditions(self, currentOffer):
				if currentOffer not in self.af.af.cs.S:
					#cd = self.af.af.candidatesDecisionPrefOrder()
					#if cd[0] == "prefOrder":
					#		 if cd[1][0] == currentOffer:
					#			 return True
					#		 else:
					#			 return False
					#else:
					#	 return True # las alternativas son igual de preferidas
					r = self.af.af.compAltAcc(currentOffer)
					if r == True:
						return True
					else:
						return False
				else:
					return False
					
			def postConditions(self, x):
				self.af.af.cs.add_ProposedOrAcceptedOffer(x)

		class AcceptS:
			def __init__(self, af):
				self.af = af
			def preConditions(self, arg):
				# si el arg es aceptable lo incorporan los agentes a sus bases
				#arg.__G = self.af.af._Agent__G
				if arg not in self.af.af.cs.AS and self.af.af.name not in arg[0]:
					if self.af.af.argExtIsAcceptable(arg) == True:
						return True
					else:
						self.af.af.cs.AS.append(arg)
						return False
				else:
					return False

			def postConditions(self, res):
				self.af.af.cs.AS.append(res)
				return None
		# OK---
		class Refuse:
			def __init__(self, af):
				self.af = af
			# there exists an argument in the sense of definition 5 against x
			def preConditions(self, currentOffer):
				#if currentOffer not in self.af.af.cs.R:
					# si x no es mi preferida, me fijo si tengo args CON aceptables
					#cd = self.af.af.candidatesDecisionPrefOrder()
					#if cd[1][0] == currentOffer:
					if currentOffer in self.af.af.cs.S:
						return False # x es mi preferida, o me da lo mismo
					else:
						# busco si hay args en contra de currentOffer
						args = self.af.af._Agent__get_Acc_CON(currentOffer)
						
						lst = []
						for arg in args:
							if arg in self.af.af.cs.A: # support de args presentados
								lst.append(True)
							else:
								lst.append(False)
						if all(lst):
							return False # presento ya todos sus argumentos CON de la oferta, pierde turno
						else:
							return True # tiene al menos un argumento CON que puede agregar, no pierde el turno aun
						
			def postConditions(self, x):
				self.af.af.cs.add_Refuse(x)
				return None

##########################
### Otras funciones
##########################

def searchArgs(argsPresented, argsAcc):
	set1 = set()
	if len(argsPresented)>0:
		for e in argsPresented:
			set1.add(e[0])
	set2 = set()
	if len(argsAcc)>0:
		for e in argsAcc:
			set2.add(e[0])

	if len(set2)>0:
		for j in set2:
			#print(len(set1.intersection({j})),"par")
			if len(set1.intersection({j}))==0:
			    #print("ERROR???")
			    return j
		return False
	else:
		return False
	
# Retorno todos los subconjuntos posibles dado un conjunto de elementos
def powerset(iterable):
	s = list(iterable)
	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

def swap(A, x, y): # recibe una lista de alternativas candidatas, e índices de 2 de ellas distintas
	temp = A[x]
	A[x] = A[y]
	A[y] = temp

	
	
