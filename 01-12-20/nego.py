#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import random

from math import fabs

from moves import *



class D: # Dialogue
	def __init__(self):
		self.wfMoves = []

	def add_wfMove(self, M):
		self.wfMoves.append(M)

class M: # Well-founded move, M_k = <S_k , H_k , Move_k>
	def __init__(self, S, Move, act):
		self.S = S # agent which plays the move
		#self.H = H # set of agents to which the move is addressed
		self.Move = Move # is the uttered move
		self.moveAct = act

#######################################################################

# Return the set of agents to which the move is addressed 
#def Hearer(WellFoundedMove):
#	 return WellFoundedMove.H

# Create well-founded move
def createMove(S, Move, actStr):
	Mv = M(S, Move, actStr)
	return Mv
##########################################################
# Evaluate dialogue result -- reglas de terminación
def Result(firstS, agents, xCurrent):
	#lst = []
	#l = len(dialogue.wfMoves)
	c=0
	la = len(agents)
	
	for agent in agents:
		if xCurrent in agent.cs.S:
			c+=1
	if c==la:
		return "Success"

	count = 0
	for ag in agents: 
		if True in ag.cs.SN:
			count+=1
				 
	count1 = 0
	for ag in agents:
		if ag.name != firstS:
			#if xCurrent == ag.candidatesDecisionPrefOrder()[1][0]:
			if ag.compAltAcc(xCurrent)==True:
				count1+=1
				
	
	if count==la and count1==la-1:
		return "Success"
	elif count==la and count1!=la-1:
		return "Failure"

	return None

######################################################


	
# Dados los agentes y alternativas, genara un listado de los agentes que empezarán cada ronda de diálogo Di en la negociación N
def firstTurns(agents, X):
	la = len(agents)
	lx = len(X)
	fraccion = lx / la
	resto = lx % la
	turns = []
	ag = []
	
	ag = list(agents)
	
	# ordenamiento aleatorio
	np.random.shuffle(ag)
	"""
	for agent in agents:
		if agent.name == "Mary":
			m = agent
		elif agent.name == "Peter":
			p = agent
		elif agent.name == "John":
			j = agent
	ag = [m, j, p]
	"""
	
	if fraccion == 1: # num(X) == num(agents)
		return ag
	if fraccion > 1: # num(X) > num(agents)
		count = 0
		fraccion = lx // la
		while count < fraccion:
			for agent in ag:
				turns.append(agent)
			count += 1
		for i in range(0, resto):
			turns.append(ag[i])
		return turns
	if fraccion < 1: # num(X) < num(agents)
		for i in range(0, lx):
			turns.append(ag[i])
		return turns

######################################################################
# prepara y ejecuta el primer move M0 del dialogo D
def firstMove(agents, agSp, Dialogue, alternativasRestantes):
	#for ag in agents.difference({agSp}):
	#	 s = ag.get_Acc_CON_X()
	#	 for ss in s:
	#		 argsCON.add(ss)

	offer = agSp.negociation.offer.preConditions(alternativasRestantes) # pongo True si quiero info de los agentes
	# creo move
	M0 = createMove(agSp, offer, "Offer")
	
	##print("--Preferred:", agSp.candidatesDecisionPrefOrder()[1][0], agSp.candidatesDecisionPrefOrder()[0]) ###
	print(M0.S.name, M0.moveAct, M0.Move, "; Agent N° 0") ###
	
	# añado move
	Dialogue.add_wfMove(M0)
	# postconditions
	agSp.negociation.offer.postConditions(offer)
	
	return agSp
	


""" 
# dado un dialogo D, retorna un posible move para agregar
def findLastMove(Dialogue, turnAg):
	a = Dialogue.wfMoves[0].S.name
	validMoves = []
	#print(turnAg.name)
	
	#prac = turnAg._Agent__Ap
	#acc = turnAg.get_acceptableArgs()
	#for u in prac:
	#	 if u[0] in acc and u[2] == Dialogue.wfMoves[0].Move:
	#		 print(u[0])
	
	c=1
	cc=0
	d = 0
	
	p = len(Dialogue.wfMoves)

	for i in range(0, p):
		if a != Dialogue.wfMoves[i].S.name:
			c+=1
			cc+=1
			d = 0
		else:
			#print(cc, "cc")
			if cc != 0:
				d += 1
				#print("break", cc, d)
				break
				
	#print("Ok1?", c, p, d, cc)
	
	if d==1:
		for i in range(1, p):
			e = Dialogue.wfMoves[i]
			if e.S.name != turnAg.name and e.moveAct != "SayNothing":
				k = existLeastOneTrue(e, e.Move, turnAg)
				#print(k)
				if k[0] == True:
					validMoves.append([e, k[1]])
	else:
		for i in range(0, p):
			e = Dialogue.wfMoves[i]
			if e.S.name != turnAg.name and e.moveAct != "SayNothing":
				k = existLeastOneTrue(e, e.Move, turnAg)
				#print(k)
				if k[0] == True:
					validMoves.append([e, k[1]]) 
	
	l = len(validMoves) # deberia tener sumpre al menos 1... 
	
	#print("Ok2?", l)
	
	if l > 0:
		i = random.randint(0, l - 1)
		return validMoves[i]
	
	else:			
		print("All False Move")
		## say nothing
		
		return None
		   
"""					

############################################################################


def negociation(agents, X):
	#neg = N() # instancia de negociacion
	Xcurrent = list(X) # comienzo con todas las alternativas
	turnsDialogues = firstTurns(agents, X) # lista de los agentes que comenzaran un dialogo nuevo durante la negociacion
	count = 0
	agreement = False
	option = -1
	F = 0
	
	laa = len(agents)
	
	while len(Xcurrent) > 0 and agreement == False and count < laa: # en cada iteracion empieza un dialogo nuevo
		##print("####################")
		##print("### DIALOGUE N°", count+1)
		##print("####################")
		
		Dialogue = D() # dialogo vacio
		agSp = turnsDialogues[count] # este agente inicia el dialogo
		listAg = [agSp]
		l = agents.difference({agSp})
		# ordenamiento aleatorio
		np.random.shuffle(list(l))
		
		for ag in l:
			listAg.append(ag)

		##for e in listAg:
		##	  print("###", e.name)
		##print(agSp, type(agSp))
		agSp = firstMove(agents, agSp, Dialogue, Xcurrent) # primer move
		index = 1
		listAg[0] = agSp
 
		xcurr = Dialogue.wfMoves[0].Move
		firstS = Dialogue.wfMoves[0].S.name
		###
		##for ag in listAg:
		##	  print(ag.name)
		##	  for e in ag._Agent__accArgs:
		##		  if isinstance(e, ar.ArgPRO):
		##			  print(e.S, e.C, e.x, "pro")
		##		  if isinstance(e, ar.ArgCON):
		##			  print(e.S, e.C, e.x, "con")
					
		status = True # para que ocurran nuevos moves en el dialogo
		j = 1
		
		while status == True:
			# itero para cada agente
			turnAg = listAg[j]
			# creo move#############################################################
			#nm = newMove(turnAg, Dialogue, listAg)
			index+=1
			
			nm = newMove(turnAg, xcurr, listAg, index, Dialogue)
			
			listAg = nm[1]
			
			##if nm[0].moveAct == "Argue" or nm[0].moveAct == "AcceptS": ##
			##	  print(nm[0].S.name, nm[0].moveAct, nm[0].Move, j) ##
			##else:
			##	  print(nm[0].S.name, nm[0].moveAct, nm[0].Move, "; Agent N°", j) ##
				
			print(nm[0].moveAct, nm[0].Move, nm[0].S.name)
			#for w in listAg:
			#	print(w.name, w.cs.A)
			####################### TABLITA ##################
			#for ag in listAg:
			#	 ch = False
			#	 sn = False
			#	 
			#	 if Dialogue.wfMoves[0].Move in ag.cs.C:
			#		 ch = True
			#	 if True in ag.cs.SN:
			#		 sn = True
					
				##print("### ", ag.name, "ACCEPTX", ag.cs.S, "CHALLENGEX", ch, "REFUSE", len(ag.cs.R), "SAYNOTHING", sn)
			if nm[0].moveAct == "AcceptX" or nm[0].moveAct == "Argue" or nm[0].moveAct == "SayNothing":
				# evaluo si D == Success o D == Failure
				result = Result(firstS, agents, xcurr) # Dialogue.wfMoves[0].Move es offer
				#print("???")
				
				# añado D a instancia Negociacion si D == Success o D == Failure
				if result == "Success" or result == "Failure":
					#print("END")
					
					##print("\n### Result(Dialogue) =", result, "\n") # imprimo resultado del dialogo D
					
					#neg.add_Dialogue(Dialogue) # añado D a instancia negociacion neg
					status = False # cierro la iteración while
					count += 1 # para que sea el turno de otro agente de empezar el siguiente dialogo D
					
					for agent in listAg: # vacio commitment stores cs excepto componente de argumentos (así dice el paper)
							agent.cs.S = []
							agent.cs.A = [] # Componente argumentos A, no la vacío
							agent.cs.C = []
							agent.cs.SN = []
							agent.cs.AS = []
							#print(agent.get_acceptableArgs())
							##print(agent.name)
							##for m in agent._Agent__accArgs:
							##	  if isinstance(m, ar.ArgPRO):
							##		  print(m.S, m.C, m.x, "PRO", min(m.argPROStrength()))
							##	  elif isinstance(m, ar.ArgCON):
							##		  print(m.S, m.C, m.x, "CON", max(m.argCONWeakness()))
							##	  else:
							##		  print(m.H, m.h, "Ep")
							
							
							
							
					Xcurrent.remove(xcurr) #remuevo alternativa para que no se empiece un D con la misma
					
					#if Dialogue.wfMoves[len(Dialogue.wfMoves)-1].moveAct == "Withdraw":
						# se termina la negociacion y vacio commitment stores cs totalmente
					#	 for agent in agents:
					#		 agent.cs.S = []
					#		 agent.cs.A = []
					#		 agent.cs.C = []
					#	 return [neg, agreement] # retorno objeto negociacion neg y agreement == False
					
					if result == "Success": # si en particular D == succcess
						option = xcurr # guardo alternativa "ganadora"
						agreement = True # cambio estado de agreement a True
					
			#if nm[0].moveAct == "SayNothing":
			#	Dialogue.wfMoves.pop()
			#agente siguiente para un nuevo move
			if j == laa - 1:
				j = 0
			else:
				j += 1
				

	#r = 0
	#if agreement == False:
	#	 r = "NOT AGREEMENT"
	#else:
	#	 r = "AGREEMENT"
		
	##print("##########################################")
	##print("### NEGOCIATION RESULT:", r)
	##print("##########################################")
	
	#for element in turnsDialogues:
	#	 if element.name == "Ag1":
	#		 s = s+"Ag1"
	#	 if element.name == "Ag2":
	#		 s = s+"Ag2"
	#	 if element.name == "Ag3":
	#		 s = s+"Ag3"
	
	
	return [agreement, option, listAg, Dialogue] # retorno la negociación (con diálogos) y si se alcanzó o no un acuerdo
		
#####################################################



def addArg(agents, turnAg, res):
	#print("en add arg...")
	for ag in agents:
		if ag.name != turnAg.name:
			if len(res)==6:
				res = list(res)
				res[3] = []
				res[5] = []
				res[4] = random.random() # si es práctico, le pongo un nuevo peso
				res = tuple(res)
				if res not in ag._Agent__Ap:
					# añado ataques
					Ae = ag._Agent__Ae # obtengo args epistemicos
					for e in Ae:
						d = random.random() # genero numero aleatorio entre 0 y 1
						if d < ag.negoPer: # negoPer = 0.5 de ataques
							res[3].append(e[0]) # lo añado como atacante
					
					
					if ag.numAttacksToProcessByTurn > 0: #(si es Paf, distorciono)
						#print("in process by turn...")
						NAT = len(ag._Agent__Ae) # numero de epistémicos
						NaRe = len(res[3]) # numero de ataques reales (recién agregados)
						NunN = NAT - NaRe # numero de no ataques reales
						
						count = 0
						c1 = 0
						c2 = 0
						# numero de ataques a determinar (como ataque o no ataque con certeza)
						while count < ag.numAttacksToProcessByTurn:
							p = random.random() # numero aleatorio entre [0, 1)
							
							if p < float(NaRe/NAT):
								if c1 < NaRe:
									c1 += 1 # numero de ataques reales a determinar con certeza
								elif c2 < NunN:
									c2 += 1
							else:
								if c2 < NunN:
									c2 += 1 # numero de no ataques reales a determinar con certeza
									# esto era un bug...
								elif c1 < NaRe:
									c1 += 1
							count += 1
						#print(c2, NunN, c1, NaRe)
						
						k = fabs(NaRe - c1) # numero de ataques reales que no se pueden determinar
						kk = fabs(NunN - c2) # numero de no ataques reales que no se pueden determinar
						
						ag.Re += NaRe # agrego ataques reales del argumento 
						ag.Ne += NunN # agrego no ataques reales del argumento
						ag.I += NAT - ag.numAttacksToProcessByTurn # numero de ataques o no ataques no determinados con certeza
						ag.N += c2
						ag.R += c1 
						ag.Ir += k 
						ag.In += kk 
		
						# otro bug era la repitencia...
						count1 = 0
						res = list(res)
						while count1 < k and len(res[3]) > 0:
							x = random.randint(0, len(res[3]) - 1) # numero que representa un indice
							n = res[3][x] # elemento que está en el índice x
							res[5].append(n) # pasa a ser no determinado
							res[3].pop(x) # lo remuevo de los determinados (le paso el indice)
							count1 += 1
							
						count2 = 0
						while count2 < kk:
							x = random.randint(0, NAT - 1) # numero 0 y cantidad de epistémicos, es un índice
							w = ag._Agent__Ae[x]
							if w[0] not in res[3] and w[0] not in res[5]:
								res[5].append(w[0]) # coloco ataques posibles
								count2 += 1
						res = tuple(res)
						
					# lo agreso a los argumentos
					ag._Agent__Ap.append(res)
					# para que el agente no presente un arg presentado por otro (NO ESTÁ FUNCIONANDO)
					ag.cs.A.append(res)

	#print("Finish add Args..")
	return agents
						  
"""								
def newMove(turnAg, Dialogue, agents):
	WWW = findLastMove(Dialogue, turnAg) # 1 move
	##print("\n--The following move is a reply to the move:", lastMoveAdded.moveAct)
	current = Dialogue.wfMoves[0].Move # oferta actual
	offertAgent = Dialogue.wfMoves[0].S # agente que ofertó primero

	#dif = []
	
	#for a in agents:
	#	 if a != turnAg:
	#		 dif.append(a)
	lastMoveAdded = WWW[0]
	
	if lastMoveAdded.moveAct == "Offer":
		res = mo.repliesToOffer(turnAg, lastMoveAdded.Move, WWW[1])
		if res != "SayNothing":
			Mi = createMove(turnAg, lastMoveAdded.Move, res)
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg 
			return [Mi, agents]		   
		else:
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg	   
			return [Mi, agents] # retono move agregado

	if lastMoveAdded.moveAct == "ChallengeX":
		#res = repliesToChallengeX(turnAg, lastMoveAdded.Move, offertAgent)
		res = mcc.OptionsChallengeX(turnAg, current, WWW[1])
		if res == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
			return [Mi, agents]
		else:
			Mi = createMove(turnAg, res, "Argue")
			Dialogue.add_wfMove(Mi)
			#print(res)
			agents = addArg(agents, turnAg, res)
			
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
			
			return [Mi, agents]


	if lastMoveAdded.moveAct == "Argue":
		#print("???", lastMoveAdded.Move, WWW[1])
		res = ma.OptionsArgue(turnAg, current, lastMoveAdded.Move, WWW[1])
		if res == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg	 
			return [Mi, agents]
			
		elif res == "ChallengeY" or res == "AcceptS":
			if res == "ChallengeY": 
				Mi = createMove(turnAg, lastMoveAdded.Move, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg	 
				return [Mi, agents]
			else:
				Mi = createMove(turnAg, lastMoveAdded.Move, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg	 
				return [Mi, agents]
				
		elif res == "AccepX":
			Mi = createMove(turnAg, current, res)
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
					return [Mi, agents]
			
		else:
			Mi = createMove(turnAg, res, "Argue")
			agents = addArg(agents, turnAg, res)
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
				
			return [Mi, agents]

	if lastMoveAdded.moveAct == "RefuseX":
		res = ref.OptionsRefuse(turnAg, current, WWW[1])
		if res == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg	  
			return [Mi, agents]
		else:
			if res != "AcceptX" and res != "ChallengeX" and res != "SayNothing":
				Mi = createMove(turnAg, res, "Argue")
				agents = addArg(agents, turnAg, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg
				return [Mi, agents]
				
			else:
				Mi = createMove(turnAg, lastMoveAdded.Move, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg	 
				return [Mi, agents]

	if lastMoveAdded.moveAct == "AcceptS":
		res = acs.OptionsAcceptS(turnAg, current, WWW[1])
		
		if res == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
			return [Mi, agents]
		else:
			if res == "ChallengeY": 
				Mi = createMove(turnAg, lastMoveAdded.Move, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg
				return [Mi, agents]
			else:
				if res != "AcceptX" and res!= "ChallengeY":
					Mi = createMove(turnAg, res, "Argue")
					agents = addArg(agents, turnAg, res)
					Dialogue.add_wfMove(Mi)
					for ag in agents:
						if ag.name == turnAg.name:
							ag = turnAg
					return [Mi, agents]
				else:
					 if res == "AcceptX":
						 Mi = createMove(turnAg, current, res)
						 Dialogue.add_wfMove(Mi)
						 for ag in agents:
							 if ag.name == turnAg.name:
								 ag = turnAg
						 return [Mi, agents]
					 else:
						 Mi = createMove(turnAg, lastMoveAdded.Move, res) 
						 Dialogue.add_wfMove(Mi)
						 for ag in agents:
							 if ag.name == turnAg.name:
								 ag = turnAg
						 return [Mi, agents]


	if lastMoveAdded.moveAct == "ChallengeY":
		res = mcc.OptionsChallengeY(turnAg, current, WWW[1])
		if res == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
				
			return [Mi, agents]
		else:
			Mi = createMove(turnAg, res, "Argue")
			Dialogue.add_wfMove(Mi)
		   
			agents = addArg(agents, turnAg, res)

			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg
				
			return [Mi, agents]

	if lastMoveAdded.moveAct == "AcceptX":
		res = ax.OptionsAcceptX(turnAg, lastMoveAdded.Move, WWW[1])
		
		if res == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", "SayNothing")
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg 
			return [Mi, agents]
			
		elif res!= "ChallengeY" and res!="AcceptX":
			Mi = createMove(turnAg, res, "Argue")
			agents = addArg(agents, turnAg, res)
			Dialogue.add_wfMove(Mi)
			for ag in agents:
				if ag.name == turnAg.name:
					ag = turnAg	   
			return [Mi, agents]
		else:
			if res == "ChallengeY":
				Mi = createMove(turnAg, lastMoveAdded.moveAct+lastMoveAdded.Move, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg
				return [Mi, agents]
			else:
				Mi = createMove(turnAg, lastMoveAdded.Move, res)
				Dialogue.add_wfMove(Mi)
				for ag in agents:
					if ag.name == turnAg.name:
						ag = turnAg	  
				return [Mi, agents]

"""
"""
# Dado un move M, retorna True si al menos hay una posible respuesta (un move de respuesta) True  
def existLeastOneTrue(moveAct, currentOffer, agent, arg):
	 if moveAct == "Offer":
		 return mo.repliesToOfferV(agent, currentOffer)
			
	 if moveAct == "AcceptX":
		 return ax.OptionsAcceptXV(agent, currentOffer)
			
	 if moveAct == "AcceptS":
		 return acs.OptionsAcceptSV(agent, currentOffer, arg)
			
	 if moveAct == "Argue":
		 return ma.OptionsArgueV(agent, currentOffer, arg)
			
	 if moveAct == "RefuseX":
		 return ref.OptionsRefuseV(agent, currentOffer)
			
	 if moveAct == "ChallengeX":
		 return mcc.OptionsChallengeXV(agent, currentOffer)
	 
	 if moveAct == "ChallengeY":
		 return mcc.OptionsChallengeYV(agent, currentOffer)

"""
def newMove(turnAg, X, agents, index, Dialogue): # index es un número entre 2 y más

	if index == 2:
		# Precondiciones, se opta por una respuesta
		res1 = replyToOfferPre(agent=turnAg, currentOffer=X) # --> (True, r) o (False, -1), donde r es un número natural
		# Se ejecutan poscondiciones
		res2 = replyToOfferPos(agent=turnAg, currentOffer=X, r=res1[1])
		# Creo move
		Mi = createMove(turnAg, X, res2) # agente creador, contenido, moveAct (OK)
		# Añado move
		Dialogue.add_wfMove(Mi)
			
		for ag in agents:
			if ag.name == turnAg.name:
				ag = turnAg 
		return [Mi, agents] 
		
	
	if index == 3:
		res1 = replyThirdPre(agent=turnAg, X=X)
		res2 = replyThirdPos(agent=turnAg, currentOffer=X, r=res1[1]) # act, SayNothing o argumento
		#print("respuesta", res2, type(res2))
		if res2 == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", res2) # agente creador, contenido, moveAct (OK)
		elif res2 == "AcceptX" or res2 == "ChallengeX":
			Mi = createMove(turnAg, X, res2) # agente creador, contenido, moveAct (OK)
		else:
			Mi = createMove(turnAg, res2, "Argue") # agente creador, contenido, moveAct (OK)
			agents = addArg(agents, turnAg, res2)
		
		Dialogue.add_wfMove(Mi)
			
		for ag in agents:
			if ag.name == turnAg.name:
				ag = turnAg 
		return [Mi, agents] 
	
	else:
		res1 = replyMorePre(agent=turnAg, X=X)
		res2 = replyMorePos(agent=turnAg, currentOffer=X, r=res1[1]) # act, SayNothing, argument
		#print("respuesta", res2, type(res2))
		if res2 == "SayNothing":
			Mi = createMove(turnAg, "SayNothing", res2) # agente creador, contenido, moveAct (OK)
		elif res2 == "AcceptX" or res2 == "ChallengeX":
			Mi = createMove(turnAg, X, res2) # agente creador, contenido, moveAct (OK)
		elif isinstance(res2, list):
			#print("ME ESTÁS JODIENDO???")
			Mi = createMove(turnAg, res2[0], "AcceptS") # agente creador, contenido, moveAct (OK)
		else:
			Mi = createMove(turnAg, res2, "Argue") # agente creador, contenido, moveAct (OK)
			agents = addArg(agents, turnAg, res2)
		
		Dialogue.add_wfMove(Mi)
			
		for ag in agents:
			if ag.name == turnAg.name:
				ag = turnAg 
		return [Mi, agents] 
	
	
	
