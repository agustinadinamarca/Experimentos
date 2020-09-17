#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools # for a powerset function implementation
import arguments as ar # import arguments module
import numpy as np

###############################################################################
### DM ARGUMENTATION FRAMEWORK - Amgoud and Prade (2004)
###############################################################################

class CS: # commitment store
	def __init__(self):
		self.S = [] # contains the offers proposed by the agent and those it has accepted
		self.A = [] # is the set of arguments presented by the agent (argument supports)
		self.C = [] # is the set of challenges made by the agent 
		# otro
		self.R = []
		self.SN = []
		self.M = []
		
	def add_ProposedOrAcceptedOffer(self, x):
		self.S.append(x)
	def add_ArgumentPresented(self, arg):
		self.A.append(arg)
	def add_ChallengePresented(self, challenge):
		self.C.append(challenge)
	def add_Refuse(self, ref):
		self.R.append(ref)


# Case: inconsistence bases y criterio bipolar de Amgoud and Prade 2009
# The framework computes the ‘best’ decision (if it exists)

def isThere(pair, relations):
	for p in relations:
		if p[1].t == "E" and pair[1].t == "E":
			if p[0].H == pair[0].H and p[0].h == pair[0].h and p[1].H == pair[1].H and p[1].h == pair[1].h:
				return True
		elif p[1].t == "E" and pair[1].t == "P":
			if p[0].H == pair[0].H and p[0].h == p[0].h and p[1].S == pair[1].S and p[1].C == pair[1].C and p[1].x == pair[1].x:
				return True
		elif p[1].t == "E" and pair[1].t == "C":
			if p[0].H == pair[0].H and p[0].h == p[0].h and p[1].S == pair[1].S and p[1].C == pair[1].C and p[1].x == pair[1].x:
				return True
		
	return False
	
def funcUndercuts(relations, argEp):
	N = set()
	for a in argEp:
		for b in argEp:
			if a != b:
				#print("OK", isThere((a, b), relations))
				if isThere((a, b), relations)==False:
					#if ar.argPreferred(a, b) == a or ar.argPreferred(a, b) == "equal":
						#print("OK")
					N.add((a, b))
	return N
	
def funcAttacks(relations, argEp, argPr):
	N = set()
	for a in argEp:
		for b in argPr:
			#print(a, b, ar.argPreferred(a, b), isThere((a, b), relations))
			if isThere((a, b), relations)==False:
				#if ar.argPreferred(a, b) == a or ar.argPreferred(a, b) == "equal":
					#print("OK")
				N.add((a, b))
	return N
		
	
class Agent:
	def __init__(self, name, K, G, X, Ae, Ap, semanticRoRI, numAttacksToProcessInit, numAttacksToProcessByTurn):
		self.sem = semanticRoRI
		self.name = name # un label con el nombre del agente
		self.numAttacksToProcessInit = numAttacksToProcessInit
		self.numAttacksToProcessByTurn = numAttacksToProcessByTurn
		self.__K = K # Knowledge base
		self.__G = G # Goals base
		self.__X = X # Alternatives
		self.__Ap = Ap # Practical arguments
		self.__Ae = Ae # epistemic arguments
		self.__arguments = self.get_AllArguments() # Practical and epistemic arguments
		self.__undercuts = self.get_undercuts()
		self.__attacks = self.get_attacks()
		self.__stronglyUndercuts = self.get_stronglyUndercuts()
		self.__stronglyAttacks = self.get_stronglyAttacks()
		self.Re = self.set_PAF(numAttacksToProcessInit)[3]
		self.Ne = self.set_PAF(numAttacksToProcessInit)[4]
		self.R = self.set_PAF(numAttacksToProcessInit)[0]
		self.N = self.set_PAF(numAttacksToProcessInit)[1]
		self.I = self.set_PAF(numAttacksToProcessInit)[2]
		self.__accArgs = self.get_acceptableArgs()
		self.__rejArgs = self.get_rejectedArgs()
		self.cs = CS() # commitment store for negociation
		self.negociation = Agent.Negociation(self)
	### PAF
	def set_PAF(self, numAttacks):
		su = self.get_stronglyUndercuts()
		sa = self.get_stronglyAttacks()
		Ae = self.__Ae
		Ap = self.__Ap
		R = su
		if len(sa) > 0:
			for r in sa:
				R.add(r)
		Re = R # Re
		N = funcUndercuts(su, Ae)
		#print("###N", N)
		K = funcAttacks(sa, Ae, Ap)
		#print("###K",K)
		if len(K) > 0:
			for a in K:
				N.add(a)
		#N.union(K)
		#print("###N!", N)
		Ne = N # Ne
		T = N
		if len(R) > 0:
			for r in R:
				T.add(r)

		lst=[]
		for i in range(len(T)):
			lst.append(i)

		if len(lst) > numAttacks:
			y = np.random.choice(lst, numAttacks) # Acá tengo indices
		else:
			y = lst

		count=0
		Det = set()

		for e in T:
			if count in y:
				Det.add(e)
			count+=1

		# Actualizo R, N e I
		rR = set()
		rN = set()
		rI = set()

		for d in Det:
			if d in R:
				rR.add(d)
			if d in N:
				rN.add(d)
		for t in T:
			if t not in rR and t not in rN:
				rI.add(t)

		return rR, rN, rI, Re, Ne
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
		return self.get_PracticalArguments().union(self.get_EpistemicArguments())

	
	# UNDERCUTS entre epistemicos
	#A1 undercuts A2 iff ∃ h ∈ Support(A2) such that
	#Conclusion(A1) ≡ ¬ h. In other words, an argument is undercut iff there exists an argument for the
	#negation of an element of its support.
	def get_undercuts(self):
		undercuts = set()
		for arg1 in self.__Ae:
			for arg2 in self.__Ae:
				if arg1 != arg2:
					conclusion1 = arg1.h
					for h in arg2.H:
						if len(h) == 2: # fact
							k = "-"+h[0]
							k = k.replace('--', '')
							if conclusion1 == k:
								undercuts.add((arg1, arg2))
						#else: # rule
						#	 k = "-"+h[0]
						#	 k.replace('--', '')
						#	 if conclusion1 == k:
						#		 undercuts.add((arg1, arg2))
		return undercuts

	# ATTACKS epistemico a practico
	#A1 attacks A3 iff ∃h ∈ Support(A3) or ∃h ∈
	#Consequences(A3) such that Conclusion(A1) ≡ ¬h.
	def get_attacks(self):
		attacks = set()
		for arg1 in self.__Ae:
			conclusion1 = arg1.h
			for arg2 in self.__Ap:
				Sarg2 = arg2.S
				Carg2 = arg2.C
				for s in Sarg2:
					k = "-"+conclusion1
					k = k.replace('--', '')
					if s[0] == k:	  
						attacks.add((arg1, arg2))
				for c in Carg2:
					k = "-"+conclusion1
					k = k.replace('--', '')
					if c == k:
						attacks.add((arg1, arg2))
		return attacks

	 #B strongly undercuts A (resp. B strongly attacks A) iff
	#B undercuts A (resp. B attacks A) and it is not the case
	#that A is preferred to B.
	def get_stronglyUndercuts(self):
		stronglyUndercuts = set()
		for pair in self.__undercuts:
			res = ar.argEpPreferred(pair[0], pair[1])
			if res == pair[0] or res == "equal":
				stronglyUndercuts.add(pair)
		return stronglyUndercuts

	def get_stronglyAttacks(self):
		stronglyAttacks = set()
		for pair in self.__attacks:
			res = ar.argPreferred(pair[0], pair[1])
			if res == pair[0] or res == "equal":
				stronglyAttacks.add(pair)
		return stronglyAttacks

	# Retorna atacantes o undercuters (strong) de un argumento
	def __get_AttackersOrUndercutersOfArg(self, arg):
		lst = set()
		if self.sem == "R":
			for pair in self.R:
				if pair[1].t == "E" and arg.t == "E":
					if pair[1].H == arg.H and pair[1].h == arg.h:
						lst.add(pair[0])
				if pair[1].t == "P" and arg.t == "P":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
				if pair[1].t == "C" and arg.t == "C":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
			return lst
		elif self.sem == "RI":
			for pair in self.R:
				if pair[1].t == "E" and arg.t == "E":
					if pair[1].H == arg.H and pair[1].h == arg.h:
						lst.add(pair[0])
				if pair[1].t == "P" and arg.t == "P":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
				if pair[1] == "C" and arg.t == "C":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
			for pair in self.I:
				if pair[1].t == "E" and arg.t == "E":
					if pair[1].H == arg.H and pair[1].h == arg.h:
						lst.add(pair[0])
				if pair[1].t == "P" and arg.t == "P":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
				if pair[1].t == "C" and arg.t == "C":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
			return lst
		
	def __get_AttackersOrUndercutersOfArg_Reals(self, arg):
		lst = set()
		for pair in self.R:
			if pair[1].t == "E" and arg.t == "E":
				if pair[1].H == arg.H and pair[1].h == arg.h:
					lst.add(pair[0])
			if pair[1].t == "P" and arg.t == "P":
				if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
					lst.add(pair[0])
			if pair[1].t == "C" and arg.t == "C":
				if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
					lst.add(pair[0])
		return lst
		
	#A set of arguments E defends an argument A if there
	#is some argument in E which strongly undercuts (resp.
	#strongly attacks) every argument B where B undercuts (resp. attacks) A and A cannot defend itself
	#against B.
	# ACEPTABLE --> si el conjunto E lo defiende de sus atacantes/undercuters
	def __is_defendedBySet(self, arg, E):
		Bs = self.__get_AttackersOrUndercutersOfArg(arg) # reales o posibles
		lst = []
		if len(E) >= 0:
			for element in Bs:
				at = self.__get_AttackersOrUndercutersOfArg_Reals(element)
				if intersection(at, E):
					lst.append(True)
				else:
					lst.append(False)
			if all(lst):
				return True
			else:
				return False

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

	#The class R of rejected arguments. Such arguments
	#are undercut or attacked by acceptable ones.
	def get_rejectedArgs(self):
		lst=set()
		R = self.R
		I = self.I
		acc = self.__accArgs
		if self.sem == "R":
			for pair in R:
				if inTuple(pair[0], acc):
					lst.add(pair[1])

		if self.sem == "RI":
			for pair in R:
				if inTuple(pair[0], acc):
					lst.add(pair[1])
			for pair in I:
				if inTuple(pair[0], acc):
					lst.add(pair[1])
		return lst

	def get_abeyanceArgs(self):
		lst=set()
		for element in self.__arguments:
			if inTuple(element, self.__accArgs)==False and inTuple(element, self.__rejArgs)==False:
				lst.add(element)
		return lst

	def __is_CandidateDecision(self, d):
		for c in self.__accArgs:
			if c.t == "P" or c.t == "C":
				if c.x == d:
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
		argPro = set()
		for arg in self.__accArgs:
			if arg.t == "P":
				if arg.x == decision:
					argPro.add(arg)
		return argPro

	def __get_Acc_CON(self, decision):
		argCon = set()
		for arg in self.__accArgs:
			if arg.t == "C":
				if arg.x == decision:
					argCon.add(arg)
		return argCon

	def get_Acc_CON_X(self):
		args = set()
		for x in self.__X:
			s = self.__get_Acc_CON(x)
			for ss in s:
				args.add(ss)
		return args
			
	def __is_Preferred_PRO_d1(self, argsProD1, argsProD2): # retorna "Primera", "Segunda" o "Equal"
		l1 = len(argsProD1)
		l2 = len(argsProD2)
		if l1 > 0 and l2 > 0:
			strengthsProD1 = []
			strengthsProD2 = []
			for element1 in argsProD1:
				strengthsProD1.append(min(element1.argPROStrength()))
			for element2 in argsProD2:
				strengthsProD2.append(min(element2.argPROStrength()))
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
				strengthsConD1.append(max(element1.argCONWeakness()))
			for element2 in argsConD2:
				strengthsConD2.append(max(element2.argCONWeakness()))
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
		
		l1p = len(d1PRO)
		l2p = len(d2PRO)
		l1c = len(d1CON)
		l2c = len(d2CON)
		
		if l1p ==0 and l2p==0:
			statusPro = None
		if l1p==0 and l2p>0:
			statusPro = "Segunda"
		if l1p>0 and l2p==0:
			statusPro = "Primera"
		if l1p>0 and l2p>0:
			statusPro = self.__is_Preferred_PRO_d1(d1PRO, d2PRO)

		if l1c==0 and l2c==0:
			statusCon = None
		if l1c==0 and l2c>0:
			statusCon = "Primera"
		if l1c>0 and l2c==0:
			statusCon = "Segunda"
		if l1c>0 and l2c>0:
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


	# Computa los conjuntos de argumentos que son cfs (subconjuntos de argumentos
	# que no se atacan entre sí).
	def compute_cfs(self):
		pwr = powerset(self.__arguments)
		R = self.R
		I = self.I
		lr = len(R)
		if self.sem == "R":
			if lr > 0:
				for x in R:
					x1 = x[0]
					x2 = x[1]
					todelete = []
					for i in pwr:
						if inTuple(x1,i) and inTuple(x2,i):#if (x1 in i) and (x2 in i):
							todelete.append(i)
					for i in todelete:
						pwr.remove(i)
			return set(pwr)
		elif self.sem == "RI":
			if lr > 0:
				for x in R:
					x1 = x[0]
					x2 = x[1]
					todelete = []
					for i in pwr:
						if inTuple(x1,i) and inTuple(x2,i):#if (x1 in i) and (x2 in i):
							todelete.append(i)
					for i in todelete:
						pwr.remove(i)

			if len(I) > 0:
				for x in I:
					x1 = x[0]
					x2 = x[1]
					todelete = []
					for i in pwr:
						if inTuple(x1,i) and inTuple(x2,i):#if (x1 in i) and (x2 in i):
							todelete.append(i)
					for i in todelete:
						pwr.remove(i)
			return set(pwr)


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

	###############################

	def MorePreferredPROAcceptable(self, alternative):
		proAlt = [] # args acceptable PRO alternative
		# busco PRO accentable de alternative
		for arg in self.__accArgs:
			if arg.t == "P":
				if arg.x == alternative:
					proAlt.append(arg)
		# quiero el mejor argumento PRO
		if len(proAlt)>0:
			strengths = 0
			ele = 0
			for element in proAlt:
				res = min(element.argPROStrength())
				if strengths <= res:
					ele = element
					strengths = res
			return ele
		else:	 
			return None
	
	def LessPreferredCONAcceptable(self, alternative):
		conAlt = []
		# busco CON acceptable de alternative
		for arg in self.__accArgs:
			if arg.t == "C":
				if arg.x == alternative:
					conAlt.append(arg)
		# quiero el argumento CON menos fuerte
		if len(conAlt)>0:
			strengths = 0
			ele = 0
			for element in conAlt:
				res = max(element.argCONWeakness())
				if strengths >= res:
					ele = element
					strengths = res
			return ele
		else:	 
			return None
		
###############################

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
				compl = []
				cfs = self.compute_cfs()
				if len(cfs)>0:
					adm = self.compute_admissibility(cfs)
					if len(adm)>0:
						for conj in adm:
							accArgs = set()
							for x in self.__arguments:
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
				#print type(conj), len(conj)
				if count == 0:
				   l = len(conj)
				else:
					lc = len(conj)
					if lc < l:
						l = lc
				count+=1
					
			for x in compExt:
				if len(x) == l:
					grd.append(x)

		return grd

	# incorporacion de argumento externo si este es aceptable
	def argExtIsAcceptable(self, arg):
		ApPrima = self._Agent__Ap
		AePrima = self._Agent__Ae
		
		if arg.t == "P" or arg.t == "C":
			ApPrima.add(arg)
		else:
			AePrima.add(arg)
		
		if is_defendedBySet(arg, self._Agent__accArgs, AePrima, ApPrima, self.R, self.I, self.sem) == True:
			return True
		else:
			return False

	def compAltChallenge(self, current):
		lst = []
		candidates = self.get_CandidatesDecisions()
		for x in candidates:
			if x != current:
				r = self.get_Preferred(x, current)
				lst.append(r)
			
		for l in lst:
			if l != current:
				return True
				
		return False
	
	def compAltAcc(self, current):
		lst = []
		candidates = self.get_CandidatesDecisions()
		for x in candidates:
			if x != current:
				r = self.get_Preferred(x, current)
				lst.append(r)
		
		m=[]
		for l in lst:
			if l == current or l == None:
				m.append(True)
			else:
				m.append(False)
		if all(m):
			return True
		else:
			return False
		
	class Negociation:
		def __init__(self, af):
			self.af = af
			# Speach acts
			self.offer = Agent.Negociation.Offer(self)
			self.challengeX = Agent.Negociation.ChallengeX(self)
			self.challengeY = Agent.Negociation.ChallengeY(self)
			self.argue = Agent.Negociation.Argue(self)
			self.withdraw = Agent.Negociation.Withdraw(self)
			self.acceptX = Agent.Negociation.AcceptX(self)
			self.acceptS = Agent.Negociation.AcceptS(self)
			self.refuse = Agent.Negociation.Refuse(self)
			self.sayNothing = Agent.Negociation.SayNothing(self)
		
		# OK---
		class Offer:
			def __init__(self, af):
				self.af = af
			def preConditions(self, argsCONOtherAgents, alternativasRestantes, go): # conj de args CON de otros agentes, todos: g0 true o false
				cd = self.af.af.candidatesDecisionPrefOrder()
				if cd[0] == "prefOrder" and go == True:
					argsCon = checkArgsCON(cd[1][0], argsCONOtherAgents)
					if argsCon==False and cd[1][0] in alternativasRestantes:
						return cd[1][0]
					else:
						return cd[1][1]
				elif cd[0] == "prefOrder" and go == False:
					for e in cd[1]:
						if e in alternativasRestantes:
							return e
					if len(alternativasRestantes) > 0:
						return alternativasRestantes[0]
					
				elif cd[0] == "equallyPreferred" and go == True:
					r = np.random.choice(cd[1][0], cd[1][1], 1)[0]
					argsCon = checkArgsCON(r, argsCONOtherAgents)
					if argsCon==False and r in alternativasRestantes:
						return r
					else:
						if r == cd[1][0]:
							return cd[1][1]
						else:
							return cd[1][0]
							
				elif cd[0] == "equallyPreferred" and go == False:
					for e in cd[1]:
						if e in alternativasRestantes:
							return e
					if len(alternativasRestantes) > 0:
						return alternativasRestantes[0]
							
				
				  
			def postConditions(self, x):
				self.af.af.cs.add_ProposedOrAcceptedOffer(x) # add offer to the commitment store of the agent
		# OK---
		class ChallengeX:
			def __init__(self, af):
				self.af = af
			def preConditions(self, currentOffer):
				if currentOffer not in self.af.af.cs.C:
				
				#	 cd = self.af.af.candidatesDecisionPrefOrder() # obtengo decisiones candidatas
				#	 if cd[0] == "prefOrder":
				#		 if cd[1][0] != currentOffer:
				#			 return True # existe decision mas preferida distinta a la actual
				#		 else:
				#			 return False # la preferida es la actual
				#	 else: # todas las alternativas dan lo mismo
				#		 return False # me dan lo mismo, asi que no la desafio
				#else:
				#	 return False
				
					r = self.af.af.compAltChallenge(currentOffer)
					if r == True:
						return True
					else:
						return False
				else:
					return False
					
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

				if neg == True:
					con = self.af.af._Agent__get_Acc_CON(currentOffer)
					pro = self.af.af._Agent__get_Acc_PRO(currentOffer)
					args = set()
					
					if pro != set():
						for e in pro:
							args.add(e)
					if con != set():
						for e in con:
							args.add(e)
					
					
					#print("Debug-Args ACC TO PRESENT")
					#for e in args:
					#	 print(e.S, e.C, e.x, e)
						
					argsPresented = self.af.af.cs.A #list
					#print("Debug-ArgsPresented", argsPresented)
					a = searchArgs(argsPresented, args)
					if a != False:
						return a # retorna un argumento aceptable para el agente
					else:
						return False # si no tengo argumentos

			def postConditions(self, currentOffer, neg, arg):
				self.af.af.cs.A.append(arg)
				#for k in self.af.af.cs.A:
				#	 print("0", k.S, k.C, k.x)

		# OK---
		class Withdraw:
			def __init__(self, af):
				self.af = af
			def preConditions(self, currentOffer):
				"""
				lst = []
				for x in self.af.af._Agent__X:
					s = []
					con = self.af.af._Agent__get_Acc_CON(x)
					if len(con) > 0:
						for arg in con:
							if arg.argCONWeight() == 0:
								s.append(True)
							s.append(False)
					else:
						s.append(False)
					if any(s):
						lst.append(True)
					else:
						lst.append(False)
				if all(lst):
					return True
				else:
					return False
				"""
				return False
					
			def postConditions(self):
				return None
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
				arg.__G = self.af.af._Agent__G
				if self.af.af.argExtIsAcceptable(arg) == True:
					return True
				else:
					return False

			def postConditions(self, res):
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
					if self.af.af.compAltAcc(currentOffer)==True:
						return False # x es mi preferida, o me da lo mismo
					else:
						# busco si hay args en contra de currentOffer
						args = self.af.af._Agent__get_Acc_CON(currentOffer)
						
						lst = []
						for arg in args:
							if arg.S in self.af.af.cs.A: # support de args presentados
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

		# This move allows an agent to miss its turn if it has
		#already accepted the current offer, or it has no argument to present.
		#This move has no effect on the dialogue.
		class SayNothing: # OK
			def __init__(self, af):
				self.af = af
			def preConditions(self, currentOffer):
				# Ya acepto la oferta o fue quien oferto
				if currentOffer in self.af.af.cs.S:
					return True # Puede perder el turno
				else:
					# No tiene argumentos que agregar
					args = self.af.af._Agent__get_Acc_PRO(currentOffer)
					args1 = self.af.af._Agent__get_Acc_CON(currentOffer)
					for a in args1:
						args.append(a)
					lst = []
					for arg in args:
						if arg in self.af.af.cs.A: # support de args presentados
							lst.append(True)
						else:
							lst.append(False)
					if all(lst):
						return True # presento ya todos sus argumentos CON de la oferta, pierde turno
					else:
						return False # tiene al menos un argumento CON que puede agregar, no pierde el turno aun

			def postConditions(self):
				return None

##########################
### Otras funciones
##########################

def searchArgs(argsPresented, argsAcc):
		if len(argsAcc)>0:
			for j in argsAcc:
				#print(j.S, j.C, j.x, j) ###
				if intersection([j], argsPresented)==False:
					#print(argsPresented)
					return j
			return False
		else:
			return False
						
def existXtoOffer(candidateDesicionsAgent, argsCONOtherAgents):
	for d in candidateDesicionsAgent:
		if checkArgsCON(d, argsCONOtherAgents) == False:
			return [True, d] # la mas preferida y con args no fuertes en contra
	return False

def checkArgsCON(x, argsConOtherAgents): # checkeo si tiene tiene args en CON fuertes de otros agentes (degree == 0)
	
	if len(argsConOtherAgents) > 0:
		for arg in argsConOtherAgents:
			if arg.x == x and arg.argCONWeight() == 0:
				return True
		return False
	else:
		return False

# Retorno todos los subconjuntos posibles dado un conjunto de elementos
def powerset(iterable):
	s = list(iterable)
	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))


def inTuple(x, tup):
	for i in tup:
		if i.t == "C" and x.t == "C":
			if x.S==i.S and x.C==i.C and x.x == i.x:
				return True
		if i.t == "P" and x.t == "P":
			if x.S==i.S and x.C==i.C and x.x == i.x:
				return True
		if i.t == "E" and x.t == "E":
			if x.H==i.H and x.h==i.h:
				return True
	return False

def intersection(set1, set2):
	l1 = len(set1)
	l2 = len(set2)
	if l1 > 0 and l2 > 0:
		for x in set1:
			for i in set2:
				if x.t == "C" and i.t == "C":
					if x.S==i.S and x.C==i.C and x.x == i.x:
						return True
				if x.t == "P" and i.t == "P":
					if x.S==i.S and x.C==i.C and x.x == i.x:
						return True
				if x.t == "E" and i.t == "E":
					if x.H==i.H and x.h==i.h:
						return True
		return False
	if l1 ==0 and l2 ==0:
		return True	   
	else:
		return False
	 
def swap(A, x, y): # recibe una lista de alternativas candidatas, e índices de 2 de ellas distintas
	temp = A[x]
	A[x] = A[y]
	A[y] = temp


def intLen(set1, set2):
	if len(set1) > 0 and len(set2) > 0:
		l=0
		for x in set1:
			for i in set2:
				if x.t == "C" and i.t == "C":
					if x.S==i.S and x.C==i.C and x.x == i.x:
						l+=1
				if x.t == "P" and i.t == "P":
					if x.S==i.S and x.C==i.C and x.x == i.x:
						l+=1
				if x.t == "E" and i.t == "E":
					if x.H==i.H and x.h==i.h:
						l+=1
		return l
	else:
		return 0


################################### checkear para argumentos externos
def get_undercuts_new(AePrima):
	undercuts = set()
	for arg1 in AePrima:
		for arg2 in AePrima:
			if arg1 != arg2:
				conclusion1 = arg1.h
				for h in arg2.H:
					if len(h) == 2: # fact
						k = "-"+h[0]
						k = k.replace('--', '')
						if conclusion1 == k:
							undercuts.add((arg1, arg2))
	return undercuts

def get_attacks_new(AePrima, ApPrima):
		attacks = set()
		if len(AePrima)>0:
			for arg1 in AePrima:
				conclusion1 = arg1.h
				for arg2 in ApPrima:
					Sarg2 = arg2.S
					Carg2 = arg2.C
					for s in Sarg2:
						k = "-"+conclusion1
						k = k.replace('--', '')
						if s[0] == k:	  
							attacks.add((arg1, arg2))
					for c in Carg2:
						k = "-"+conclusion1
						k = k.replace('--', '')
						if c == k:
							attacks.add((arg1, arg2))
		return attacks
		
def get_stronglyUndercuts_new(AePrima):
		undercuts = get_undercuts_new(AePrima)
		stronglyUndercuts = set()
		for pair in undercuts:
			res = ar.argEpPreferred(pair[0], pair[1])
			if res == pair[0] or res == "equal":
				stronglyUndercuts.add(pair)
		return stronglyUndercuts

def get_stronglyAttacks_new(AePrima, ApPrima):
		attacks = get_attacks_new(AePrima, ApPrima)
		stronglyAttacks = set()
		for pair in attacks:
			res = ar.argPreferred(pair[0], pair[1])
			if res == pair[0] or res == "equal":
				stronglyAttacks.add(pair)
		return stronglyAttacks

def get_AttackersOrUndercutersOfArg_new(arg, AePrima, ApPrima, R, I, sem):
		#stronglyUndercuts = get_stronglyUndercuts_new(AePrima)
		#stronglyAttacks = get_stronglyAttacks_new(AePrima, ApPrima)
		
		lst = set()
		lr = len(R)
		if sem == "R" and lr > 0:
			for pair in R:
				#print(pair[1])
				if pair[1].t == "E" and arg.t == "E":
					if pair[1].H == arg.H and pair[1].h == arg.h:
						lst.add(pair[0])
				if pair[1].t == "P" and arg.t == "P":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
				if pair[1].t == "C" and arg.t == "C":
					if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
						lst.add(pair[0])
			return lst
		elif sem == "RI":
			if lr > 0:
				for pair in R:
					#print(pair[1])
					if pair[1].t == "E" and arg.t == "E":
						if pair[1].H == arg.H and pair[1].h == arg.h:
							lst.add(pair[0])
					if pair[1].t == "P" and arg.t == "P":
						if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
							lst.add(pair[0])
					if pair[1].t == "C" and arg.t == "C":
						if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
							lst.add(pair[0])
			if len(I) > 0:
				for pair in I:
					if pair[1].t == "E" and arg.t == "E":
						if pair[1].H == arg.H and pair[1].h == arg.h:
							lst.add(pair[0])
					if pair[1].t == "P" and arg.t == "P":
						if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
							lst.add(pair[0])
					if pair[1].t == "C" and arg.t == "C":
						if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
							lst.add(pair[0])
			return lst
		else:
			return lst


def get_AttackersOrUndercutersOfArg_new_(arg, AePrima, ApPrima, R):
		#stronglyUndercuts = get_stronglyUndercuts_new(AePrima)
		#stronglyAttacks = get_stronglyAttacks_new(AePrima, ApPrima)
		
		lst = set()

		for pair in R:
			if pair[1].t == "E" and arg.t == "E":
				if pair[1].H == arg.H and pair[1].h == arg.h:
					lst.add(pair[0])
			if pair[1].t == "P" and arg.t == "P":
				if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
					lst.add(pair[0])
			if pair[1].t == "C" and arg.t == "C":
				if pair[1].S == arg.S and pair[1].C == arg.C and pair[1].x == arg.x:
					lst.add(pair[0])
		return lst



def is_defendedBySet(arg, E, AePrima, ApPrima, R, I, sem):
		Bs = get_AttackersOrUndercutersOfArg_new(arg, AePrima, ApPrima, R, I, sem)
		lst = []
		if len(E) >= 0:
			if len(Bs) > 0:
				for element in Bs:
					at = get_AttackersOrUndercutersOfArg_new_(element, AePrima, ApPrima, R)
					if intersection(at, E):
						lst.append(True)
					else:
						lst.append(False)
				if all(lst):
					return True
				else:
					return False
			else:
				return True
				

def is_attacked(prac, epi):
			conclusion1 = epi.h
			Sarg2 = prac.S
			Carg2 = prac.C
			for s in Sarg2:
				k = "-"+conclusion1
				k = k.replace('--', '')
				if s[0] == k:	  
					return True
			for c in Carg2:
				k = "-"+conclusion1
				k = k.replace('--', '')
				if c == k:
					return True
			return False

def is_stronglyAttacked(prac, epi):
	if is_attacked(prac, epi)==True:
		res = ar.argPreferred(prac, epi)
		if res == epi or res == "equal":
			return True
	return False
	
