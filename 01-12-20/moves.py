#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

### PRECONDICIONES ###

def replyToOfferPre(agent, currentOffer):

	# AcceptX
	r1 = agent.negociation.acceptX.preConditions(currentOffer) # Retorna True o False
	# RefuseX
	r2 = agent.negociation.refuse.preConditions(currentOffer) # Retorna True o False
	# ChallengeX
	r3 = agent.negociation.challengeX.preConditions(currentOffer) # Retorna True o False

	possibleReplay = []
	
	if r1 == True:
		possibleReplay.append(1)
		
	if r2 == True:
		possibleReplay.append(2)
		
	if r3 == True:
		possibleReplay.append(3)
	
	if len(possibleReplay) > 0:
	
		r = np.random.choice(possibleReplay, 1)[0]
		
		return (True, r)
		
	else:
		return (False, -1)
		
		
def replyToOfferPos(agent, currentOffer, r):

	if r == 1:
		agent.negociation.acceptX.postConditions(currentOffer)
		return "AcceptX"
		#if currentOffer not in agent.cs.S:
		#	 agent.negociation.acceptX.postConditions(currentOffer)
		#	 ##print("--Pre-Conditions: the offer", currentOffer, "is the most preferred decision in X for", agent.name)
		#	 ##print("--Post-Conditions: CS.S_t (", agent.name, ") = CS.S_t−1 (", agent.name, ") U {", currentOffer, "}.")
		#	 return "AcceptX"
		#else:
		#	 ##print("--Pre-Conditions:", agent.name, "has already accepted the current offer", currentOffer)
		#	 ##print("--Post-Conditions: none")
		#	 return "SayNothing"
			
	elif r == 2:
		agent.negociation.refuse.postConditions(currentOffer)
		##print("--Pre-Conditions:", agent.name, "has at least one argument against", currentOffer)
		##print("--Post-Conditions: none")
		return "RefuseX"
	
	elif r == 3:
		agent.negociation.challengeX.postConditions(currentOffer)
		##print("--Pre-Conditions: exists", agent.candidatesDecisionPrefOrder()[1][0], "that is preferred to", currentOffer)
		##print("--Post-Conditions: CS.C_t(", agent.name, ") = CS.C_t−1(", agent.name, ") ∪ {", currentOffer, "}")
		return "ChallengeX"
		
 ############################################################
 
def replyThirdPre(agent, X):
	# AcceptX
	r1 = agent.negociation.acceptX.preConditions(X) # Retorna True o False
	# Argue
	r2 = agent.negociation.argue.preConditions(X, True) # Retorna False o la estructura de un argumento
	# Challenge (X o Y) --> challengeX ahora es genérico (X, Accept, Refuse)
	r3 = agent.negociation.challengeX.preConditions(X) # Retorna True o False
	
	possibleReplay = []
	
	if r1 == True:
		possibleReplay.append(1)
		
	#if r2 != False:
	possibleReplay.append(2)
		
	if r3 == True:
		possibleReplay.append(3)
		
	if len(possibleReplay) > 0:
		r = np.random.choice(possibleReplay, 1)[0]
		if r == 2:
			r = r2
		return (True, r) # False o un argumento
	else:
		return (False, -1)
	
 
def replyThirdPos(agent, currentOffer, r):
	if r == 1:
		agent.negociation.acceptX.postConditions(currentOffer)
		return "AcceptX"
		
	elif r == 3:
		agent.negociation.challengeX.postConditions(currentOffer)
		return "ChallengeX"
		
	elif r == False or r == -1:
		agent.cs.SN.append(True)
		return "SayNothing"
		
	else:
		agent.negociation.argue.postConditions(currentOffer, True, r)
		return r
		
 #########################################################################
 
def replyMorePre(agent, X):
	# AcceptX
	r1 = agent.negociation.acceptX.preConditions(X) # Retorna True o False
	# Argue
	r2 = agent.negociation.argue.preConditions(X, True) # Retorna False o la estructura de un argumento
	# Challenge X o Y
	r3 = agent.negociation.challengeX.preConditions(X) # Retorna True o False --> X, Refuse, Accept, Argument
	# AcceptS
	l = []
	r4 = False
	#print(agent.cs.A, "Ok???", len(agent.cs.A))
	if len(agent.cs.A) > 0:
		for i in range(len(agent.cs.A)):
			l.append(i)
		k = np.random.choice(l, 1)[0]
		arg = agent.cs.A[k]
		#print("W")
		r4 = agent.negociation.acceptS.preConditions(arg=arg) # Retorna True o False
	
	#print(r1, r2, type(r2), r3, r4, "panorama")
	possibleReplay = []
	
	if r1 == True:
		possibleReplay.append(1)
		
	possibleReplay.append(2)
		
	if r3 == True:
		possibleReplay.append(3)
	
	if r4 == True:
		#print("OKKKK")
		possibleReplay.append(4)
	
	if len(possibleReplay) > 0:
		r = np.random.choice(possibleReplay, 1)[0]
		if r == 2:
			r = r2 # False o argumento
		if r == 4:
			r = [arg] # argumento
		return (True, r) # False o argumento o lista con argumento
	else:
		return (False, -1)
		
 
def replyMorePos(agent, currentOffer, r):
	if r == 1:
		agent.negociation.acceptX.postConditions(currentOffer)
		return "AcceptX"
		
	elif r == 3:
		agent.negociation.challengeX.postConditions(currentOffer)
		return "ChallengeX"
		
	elif isinstance(r, list):
		agent.negociation.acceptS.postConditions(r[0])
		return r
		
	elif r == False or r == -1:
		agent.cs.SN.append(True)
		return "SayNothing"
		
	else:
		agent.negociation.argue.postConditions(currentOffer, True, r)
		return r

 
 
 
