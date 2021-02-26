#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from math import fabs
from module.moves import *
import copy

class Move:
	def __init__(self, creator, content, label):
		self.creator = creator
		self.content = content
		self.label = label
	
def create_move(creator, content, label):
	new_move = Move(creator, content, label)
	return new_move


# Dados los agentes y alternativas, genara un listado 
#de los agentes que empezarán cada ronda de diálogo Di en la negociación N
def first_turn_per_dialogue(agents_list, number_offers):

	turns = []

	number_agents = len(agents_list)

	fraction = number_offers / number_agents
	remainder = number_offers % number_agents

	random.shuffle(agents_list)
	
	if fraction == 1: # num(X) == num(agents)
		return agents_list

	elif fraction > 1: # num(X) > num(agents)
		count = 0
		fraction = number_offers // number_agents

		while count < fraction:
			for agent in agents_list:
				turns.append(agent)
			count += 1

		for i in range(remainder):
			turns.append(agents_list[i])
		
		return turns

	else: # fraction < 1, num(X) < num(agents)
		for i in range(number_offers):
			turns.append(agents_list[i])

		return turns

######################################################################

def first_move_dialogue(first_speaker, remaining_alternatives):

	offer_proposed = first_speaker.negotiation.offer_x.preconditions(remaining_alternatives) # pongo True si quiero info de los agentes

	move_created = create_move(first_speaker, offer_proposed, "Offer")

	first_speaker.negotiation.offer_x.postconditions(offer_proposed)
	
	return move_created
	

def new_move(creator, current_offer, agents, move_index): # index es un número entre 2 y más

	if move_index == 2:
		reply_chosen = reply_offer_preconditions(creator, current_offer) # 1, 2, 3 o -1
		reply_label = reply_offer_postconditions(creator, current_offer, reply_chosen) # label

		move_created = create_move(creator, current_offer, reply_label)
		
	elif move_index == 3:
		reply_chosen = reply_argue_accept_challenge_preconditions(creator, current_offer) # 1, arg, 3 o -1
		reply_label = reply_argue_accept_challenge_postconditions(creator, current_offer, reply_chosen)

		if reply_label == "SayNothing":
			move_created = create_move(creator, "SayNothing", reply_label)

		elif reply_label == "AcceptX" or reply_label == "ChallengeX":
			move_created = create_move(creator, current_offer, reply_label)

		else:
			move_created = create_move(creator, reply_label, "Argue")
			# AÑADO ARGUMENTO A LOS DEMÁS AGENTES
			agents = add_argument(agents, creator, reply_label)
	
	else:
		reply_chosen = reply_all_preconditions(creator, current_offer) # -1, 1, arg, 3, [arg]
		reply_label = reply_all_postconditions(creator, current_offer, reply_chosen)

		if reply_label == "SayNothing":
			move_created = create_move(creator, "SayNothing", reply_label)

		elif reply_label == "AcceptX" or reply_label == "ChallengeX":
			move_created = create_move(creator, current_offer, reply_label)

		elif isinstance(reply_label, list):
			move_created = create_move(creator, reply_label[0], "AcceptS")
		
		else:
			move_created = create_move(creator, reply_label, "Argue")
			# AÑADO ARGUMENTOS A OTROS AGENTES
			agents = add_argument(agents, creator, reply_label)

			
	for agent in agents:
		if agent.name == creator.name:
			agent = creator

	return [move_created, agents]

#####################################################
def add_argument(agents, creator_agent, argument_structure):
	for agent in agents:
		if agent.name != creator_agent.name:
			if len(argument_structure)==6:
				argument_structure = list(argument_structure)
				argument_structure[4] = random.random() # si es práctico, le pongo un nuevo peso
				argument_structure = tuple(argument_structure)

			# para que el agente no argumentente un arg presentado por otro (NO ESTÁ FUNCIONANDO)
			agent.commitment_store.add_argument_presented(argument_structure)
			agent.commitment_store.add_external_argument(argument_structure)
			agent.add_argument_structure_to_base(argument_structure)
			agent.practical_labels.add(argument_structure[0])

	return agents
"""
def add_argument(agents, creator_agent, argument):

	for ag in agents:
		if ag.name != creator_agent.name:
			if len(argument)==6:
				argument = list(argument)
				argument[3] = []
				argument[5] = []
				argument[4] = random.random() # si es práctico, le pongo un nuevo peso
				argument = tuple(argument)
				if argument not in ag._Agent__Ap:
					# añado ataques
					pp = random.random()
					Ae = ag._Agent__Ae # obtengo args epistemicos
					for e in Ae:
						d = random.random() # genero numero aleatorio entre 0 y 1
						if d < pp: # negoPer = 0.5 de ataques
							argument[3].append(e[0]) # lo añado como atacante
					
					
					if ag.numAttacksToProcessByTurn > -1: #(si es Paf, distorciono)
						#print("in process by turn...")
						NAT = len(ag._Agent__Ae) # numero de epistémicos
						NaRe = len(argument[3]) # numero de ataques reales (recién agregados)
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
						argument = list(argument)
						while count1 < k and len(argument[3]) > 0:
							x = random.randint(0, len(argument[3]) - 1) # numero que repargumententa un indice
							n = argument[3][x] # elemento que está en el índice x
							argument[5].append(n) # pasa a ser no determinado
							argument[3].pop(x) # lo remuevo de los determinados (le paso el indice)
							count1 += 1
							
						count2 = 0
						while count2 < kk:
							x = random.randint(0, NAT - 1) # numero 0 y cantidad de epistémicos, es un índice
							w = ag._Agent__Ae[x]
							if w[0] not in argument[3] and w[0] not in argument[5]:
								argument[5].append(w[0]) # coloco ataques posibles
								count2 += 1
						argument = tuple(argument)
						
					# lo agargumento a los argumentos
					ag._Agent__Ap.append(argument)
					# para que el agente no pargumentente un arg presentado por otro (NO ESTÁ FUNCIONANDO)
					ag.commitment_store.arguments_presented.append(argument)

	#print("Finish add Args..")
	return agents
"""


def negotiation(agents, X):
	remaining_alternatives = list(X)
	number_offers = len(X)
	number_agents = len(agents)
	agents_c = copy.deepcopy(agents)
	agents_list = copy.deepcopy(list(agents))
	agreement_status = False
	count = 0 # num_iteration
	global sn 
	sn = set()
	
	option = -1 # WTF

	initial_turn_per_dialogue = first_turn_per_dialogue(agents_list, number_offers)

	while len(remaining_alternatives) > 0 and agreement_status == False and count < number_agents: # en cada iteracion empieza un dialogo nuevo
		
		move_count = 0
		initiator_agent = initial_turn_per_dialogue[count] # este agente inicia el dialogo

		agent_list_dialogue = [initiator_agent]
		#print(len(agents_c), type(agents_c),"agent_c", initiator_agent.name)
		#if initiator_agent in agents_c:
		#	print("OK")
		remaining_agents = set()
		for ag in agents_c:
			if ag.name != initiator_agent.name:
				remaining_agents.add(ag)
		#remaining_agents = agents_c.difference({initiator_agent})
		#for ag in remaining_agents:
		#	print(ag.name)
		random.shuffle(list(remaining_agents))
		for agent in remaining_agents:
			agent_list_dialogue.append(agent)
		#print(len(agent_list_dialogue), "agent_ldial")
		move_index = 1
		first_move = first_move_dialogue(initiator_agent, remaining_alternatives) # primer move
		
		move_count += 1 # hay 1 move
		agent_list_dialogue[0] = first_move.creator
		current_alternative = first_move.content
		#print(current_alternative)
		initiator_name = first_move.creator.name
		dialogue_status = True
		index_next_agent = 1
		moves_labels_in_round = set()
		
		while dialogue_status == True:
			
			if index_next_agent == 0:
				moves_labels_in_round = set() # la vacío al empezar una ronda nueva
			
			creator = agent_list_dialogue[index_next_agent]

			move_index += 1
			move_created_agents = new_move(creator, current_alternative, agent_list_dialogue, move_index)
			move_created = move_created_agents[0]
			#print("m ", move_created.label, creator.name, move_created.content)
			
			moves_labels_in_round.add(move_created.label) # añado movimientos depor ronda
			
			move_count += 1

			agent_list_dialogue = move_created_agents[1]

			result = 0

			if move_created.label == "AcceptX" and move_count >= number_agents:
				count1 = 0
				
				for agent in agent_list_dialogue:
					if agent.commitment_store.is_offer_accepted(current_alternative):
						count1 += 1

				if count1 == number_agents:
					result = "Success"
			# modificar
			#if move_created.label == "SayNothing":
			#	count2 = 0

			#	for agent in agent_list_dialogue: 
			#		if agent.commitment_store.is_no_arguments_to_share():
			#			count2 += 1

			#	if count2 == number_agents:
			#		result = "Failure"

			if index_next_agent == number_agents - 1:
				if "Argue" in moves_labels_in_round:
					sn = set()
			
			if move_created.label == "SayNothing":
				sn.add(creator.name)
				
			if len(sn) == number_agents:
				sn = set()
				result = "Failure"
			
			if move_created.label == "Argue":
				count3 = 0

				for agent in agent_list_dialogue:
					if agent.name != initiator_name:
						if agent.is_now_acceptable_offer(current_alternative) == True:
							count3 += 1

				if count3 == number_agents - 1:
					result = "Success"
			
			
			if result == "Success" or result == "Failure":

				dialogue_status = False

				count += 1 # para que sea el turno de otro agente de empezar el siguiente dialogo D
					
				for agent in agent_list_dialogue:
					agent.commitment_store.reset()

				remaining_alternatives.remove(current_alternative)
					
				if result == "Success":
					option = current_alternative # guardo alternativa "ganadora"
					agreement_status = True # cambio estado de agreement a True
					
			if index_next_agent == number_agents - 1:
				index_next_agent = 0
			else:
				index_next_agent += 1
	
	return option, agent_list_dialogue				   
	
	
	
