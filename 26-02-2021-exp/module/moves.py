#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

def reply_offer_preconditions(agent, current_offer):

	reply_1 = agent.negotiation.accept_x.preconditions(current_offer) # Retorna True o False

	reply_2 = agent.negotiation.refuse_x.preconditions(current_offer) # Retorna True o False

	reply_3 = agent.negotiation.challenge_x.preconditions(current_offer) # Retorna True o False

	possible_replies = []
	
	if reply_1 == True:
		possible_replies.append(1) # AcceptX
		
	if reply_2 == True:
		possible_replies.append(2) # RefuseX
		
	if reply_3 == True:
		possible_replies.append(3) # ChallengeX
	
	if len(possible_replies) > 0:
		reply_chosen = random.choice(possible_replies)
	else:
		reply_chosen = -1
	
	return reply_chosen # 1, 2, 3 o -1
		
		
def reply_offer_postconditions(agent, current_offer, reply_chosen):

	if reply_chosen == 1:
		agent.negotiation.accept_x.postconditions(current_offer)
		return "AcceptX"
			
	elif reply_chosen == 2:
		agent.negotiation.refuse_x.postconditions()
		return "RefuseX"
	
	elif reply_chosen == 3:
		agent.negotiation.challenge_x.postconditions(current_offer)
		return "ChallengeX"

	else:
		return "SayNothing"
		
 ############################################################
 
def reply_argue_accept_challenge_preconditions(agent, current_offer):
	
	reply_1 = agent.negotiation.accept_x.preconditions(current_offer) # Retorna True o False
	
	reply_2 = agent.negotiation.argue_s.preconditions(current_offer) # Retorna False o la estructura de un argumento
	
	reply_3 = agent.negotiation.challenge_x.preconditions(current_offer) # Retorna True o False
	
	possible_replies = []
	
	if reply_1 == True:
		possible_replies.append(1)
		
	possible_replies.append(2)
		
	if reply_3 == True:
		possible_replies.append(3)
		
	if len(possible_replies) > 0:
		reply_chosen = random.choice(possible_replies)
		
		if reply_chosen == 2:
			if reply_2 == False:
				reply_chosen = -1
			else:
				reply_chosen = reply_2	
	else:
		reply_chosen = -1

	return reply_chosen
	
 
def reply_argue_accept_challenge_postconditions(agent, current_offer, reply_chosen):

	if reply_chosen == 1:
		agent.negotiation.accept_x.postconditions(current_offer)
		return "AcceptX"
		
	elif reply_chosen == 3:
		agent.negotiation.challenge_x.postconditions(current_offer)
		return "ChallengeX"
		
	elif reply_chosen == -1:
		agent.commitment_store.add_no_arguments()
		return "SayNothing"
		
	else:
		agent.negotiation.argue_s.postconditions(reply_chosen)
		return reply_chosen
		
 #########################################################################
 
def reply_all_preconditions(agent, current_offer):
	
	reply_1 = agent.negotiation.accept_x.preconditions(current_offer) # Retorna True o False
	
	reply_2 = agent.negotiation.argue_s.preconditions(current_offer) # Retorna False o la estructura de un argumento
	
	reply_3 = agent.negotiation.challenge_x.preconditions(current_offer) # Retorna True o False --> current_offer, Refuse, Accept, 
	
	
	indices_arguments_presented = []
	reply_4 = False

	cs_args_len = agent.commitment_store.get_arguments_presented_number()
	
	if cs_args_len > 0:
		for i in range(cs_args_len):
			indices_arguments_presented.append(i)
			
		index_argument_presented = random.choice(indices_arguments_presented)
		
		arg = agent.commitment_store.get_argument_presented_from_index(index_argument_presented)

		reply_4 = agent.negotiation.accept_s.preconditions(arg) # Retorna True o False
	

	possible_replies = []
	
	if reply_1 == True:
		possible_replies.append(1)
		
	possible_replies.append(2)
		
	if reply_3 == True:
		possible_replies.append(3)
	
	if reply_4 == True:
		possible_replies.append(4)
	
	if len(possible_replies) > 0:
		reply_chosen = random.choice(possible_replies)
		
		if reply_chosen == 2:
			if reply_2 == False:
				reply_chosen = -1
			else:
				reply_chosen = reply_2
			
		if reply_chosen == 4:
			reply_chosen = [arg] # argumento
			
	else:
		reply_chosen = -1
	
	return reply_chosen
		
 
def reply_all_postconditions(agent, current_offer, reply_chosen):

	if reply_chosen == 1:
		agent.negotiation.accept_x.postconditions(current_offer)
		return "AcceptX"
		
	elif reply_chosen == 3:
		agent.negotiation.challenge_x.postconditions(current_offer)
		return "ChallengeX"
		
	elif isinstance(reply_chosen, list):
		agent.negotiation.accept_s.postconditions(reply_chosen[0])
		return reply_chosen
		
	elif reply_chosen == -1:
		agent.commitment_store.add_no_arguments()
		return "SayNothing"
		
	else:
		agent.negotiation.argue_s.postconditions(reply_chosen)
		return reply_chosen

 
 
 
