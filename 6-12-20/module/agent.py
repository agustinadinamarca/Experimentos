#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools # for a powerset function implementation
#import arguments as ar # import arguments module
import numpy as np
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
		self.AS = [] # AGUMENTOS QUE SE EMITIO UNA ACEPTABILIDAD O NO
		
	def add_ProposedOrAcceptedOffer(self, x):
		self.S.append(x)
	def add_ArgumentPresented(self, arg):
		self.A.append(arg)
	def add_ChallengePresented(self, challenge):
		self.C.append(challenge)
	def add_Refuse(self, ref):
		self.R.append(ref)
	def add_isEndArguments(self):
		self.SN.append(True)
		


# Case: inconsistence bases y criterio bipolar de Amgoud and Prade 2009
# The framework computes the ‘best’ decision (if it exists)

class Agent:
	def __init__(self, name, K, G, X, Ae, Ap, np):
		self.name = name # un label con el nombre del agente
		self.numAttacksToProcessByTurn = -1
		self.negoPer = np
		self.__K = K # Knowledge base
		self.__G = G # Goals base
		self.__X = X # Alternatives

		self.__Ap = Ap # Practical arguments
		self.__Ae = Ae # epistemic arguments
		#self.__arguments = self.get_AllArguments() # Practical and epistemic arguments
		
		#self.__undercuts = self.get_undercuts()
		#self.__attacks = self.get_attacks()
		#self.__stronglyUndercuts = self.get_stronglyUndercuts()
		#self.__stronglyAttacks = self.get_stronglyAttacks()
		#self.__accArgs = self.get_acceptableArgs()
		#self.__rejArgs = self.get_rejectedArgs()

		self.cs = CS() # commitment store for negociation
		self.negociation = Agent.Negociation(self)

	########################################
	# Retorna la base de conocimientos K especificada
	#def get_KnowledgeBase(self):
	#	return self.__K

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
					return a[1]
				else:
					return a[3]
		return []
						
	def getArg(self, arg):
		args = self.get_AllArguments()
		for a in args:
			if a[0] == arg:
				return a
		
	def get_Re(self):
		U = self.get_stronglyUndercuts()
		A = self.get_stronglyAttacks()	
		return U.union(A)
		
	def get_Ne(self):
		t = set()
		for ae in self.__Ae:
			for ap in self.__Ap:
				t.add((ae[0], ap[0]))
			for ae2 in self.__Ae:
				if ae[0]!=ae2[0]:
					t.add((ae[0], ae2[0]))
		Re = self.get_Re()
		for r in Re:
			if r in t:
				t.discard(r)
		return t
				
	#B strongly undercuts A (resp. B strongly attacks A) iff
	#B undercuts A (resp. B attacks A) and it is not the case
	#that A is preferred to B.
	def get_stronglyUndercuts(self):
		stronglyUndercuts = set()
		#print(self.__Ae)
		for e in self.__Ae:
			if len(e[1])>0:
				for f in e[1]:
					stronglyUndercuts.add((f, e[0]))
		return stronglyUndercuts

	def get_stronglyAttacks(self):
		stronglyAttacks = set()
		#print(self.__Ap)
		for e in self.__Ap:
			#print(len(e))
			#print(e[3], len(e[3]))
			if len(e[3])>0:
				for f in e[3]:
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
						lst.union(set(self.getAttackers(element)))
					if len(lst.intersection(E))==len(lst):
						return True
					else:
						return False
				else:
					return True
	
	# nueva (:
	def compute_cfs(self):
		N = list(self.allArguments())
		A = list(self.get_stronglyUndercuts().union(self.get_stronglyAttacks()))
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

		sU = self.get_stronglyUndercuts()
		sA = self.get_stronglyAttacks()
		
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










	# determina si es o no aceotable un arg externo
	def argExtIsAcceptable(self, arg):
		acc = self.get_acceptableArgs()

		if arg[0] in acc:
			return True
		else:
			return False
	
	def compAltChallenge(self, current):
		#lst = []
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
			#print("First")
			return False
		elif len(candidates) == 1 and current in candidates:
			return True
		else:
			print("Second")
			for x in candidates:
				if x != current:
					#print(x, current)
					r = self.get_Preferred(x, current)
					#print(r)
					if r != current and r != None:
						#print("WTF!")
						return False
			return True
		
	def metricBulshit(self, accTAFp):
		numApTAF = len(self.__Ap)
		# me fijo los acc del TAF local
		accTAF = self.get_acceptableArgs() # etiquetas
		# contador de bulshit
		count = 0
		
		# me fijo si no están en los accTAFp
		if len(accTAF) > 0:
			for u in accTAF:
				if u not in accTAFp:
					count += 1
		
		return float(count/numApTAF)
		
	class Negociation:
		def __init__(self, af):
			self.af = af
			# Speach acts
			self.offer = Agent.Negociation.Offer(self)
			self.challengeX = Agent.Negociation.ChallengeX(self)
			self.challengeY = Agent.Negociation.ChallengeY(self)
			self.argue = Agent.Negociation.Argue(self)
			self.acceptX = Agent.Negociation.AcceptX(self)
			self.acceptS = Agent.Negociation.AcceptS(self)
			self.refuse = Agent.Negociation.Refuse(self)
		
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
						return self.af.af.getArg(a) # retorna un argumento aceptable para el agente
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
				#if isinstance(res, ar.ArgPRO) or isinstance(res, ar.ArgCON):
					#res.__G = self.af.af._Agent__G
					#self.af.af._Agent__accArgs.add(res)	
				#self.af.af.cs.add_ArgumentPresented(res)
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
				return j
		return False
	else:
		return False
	

# Retorno todos los subconjuntos posibles dado un conjunto de elementos
def powerset(iterable):
	s = list(iterable)
	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))



def swap(A, x, y): # recibe una lista de alternativas candidatas, e índices de 2 de ellas distintas
	if x < len(A) and y < len(A):
		temp = A[x]
		A[x] = A[y]
		A[y] = temp



def is_defendedBySet(arg, E):
	Bs = arg[3]
	lst = []
	if len(E) >= 0:
		for element in Bs:
			at=set()
			if len(element)==3:
				at=set(element[1])
			else:
				at = set(element[3])
					
			if len(at.intersection(E))>0:
				lst.append(True)
			else:
				lst.append(False)
		if all(lst):
			return True
		else:
			return False
				

	
