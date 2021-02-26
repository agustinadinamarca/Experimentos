#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import networkx as nx
import random

#import itertools 
from networkx.algorithms.approximation import max_clique

##################################################################################
### DM ARGUMENTATION FRAMEWORK - Amgoud and Prade (2004)
##################################################################################

#def powerset(iterable):
#	s = list(iterable)
#	return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))
	
class CommitmentStore:
	
	def __init__(self):
		self.offers_proposed = []
		self.arguments_presented = []
		self.challenges_made = []

		self.say_nothing = []
		self.external_arguments_added = []
		#self.R = []
		#self.AS = [] # AGUMENTOS QUE SE EMITIO UNA ACEPTABILIDAD O NO
		
	def __eq__(self, other):
		if isinstance(other, CommitmentStore):
			return self.offers_proposed == other.offers_proposed and self.arguments_presented == other.arguments_presented and self.challenges_made == other.challenges_made and self.say_nothing == other.say_nothing and self.external_arguments_added == other.external_arguments_added
		else:
			return False

	def reset(self):
		self.offers_proposed = []
		self.arguments_presented = []
		self.challenges_made = []
		self.say_nothing = []
		self.external_arguments_added = []

	def is_offer_accepted(self, current_offer):
		if current_offer in self.offers_proposed:
			return True
		else:
			return False
			
	def is_no_arguments_to_share(self):
		if True in self.say_nothing:
			return True
		else:
			return False

	def add_proposed_or_accepted_offer(self, offer):
		self.offers_proposed.append(offer)

	def add_argument_presented(self, argument):
		self.arguments_presented.append(argument)

	def get_argument_presented_from_index(self, index):
		if index >= 0 and index < len(self.arguments_presented):
			return self.arguments_presented[index]
		else:
			return -1

	def get_arguments_presented_number(self):
		return len(self.arguments_presented)

	def add_challenge_presented(self, challenge):
		self.challenges_made.append(challenge)
	#def add_Refuse(self, ref):
	#	self.R.append(ref)
	def add_no_arguments(self):
		self.say_nothing.append(True)
		
	def add_external_argument(self, argument_structure):
		self.external_arguments_added.append(argument_structure)

# Case: inconsistence bases y criterio bipolar de Amgoud and Prade 2009
# The framework computes the ‘best’ decision (if it exists)


# ki y kt ?????



def get_certain_attacks_number_agent(practical_base, epistemic_base):
	certain_attacks_number = 0

	for practical_argument in practical_base:
		certain_attacks_number += len(practical_argument[3])

	for epistemic_argument in epistemic_base:
		certain_attacks_number += len(epistemic_argument[1])

	return certain_attacks_number

def get_labels_from_arguments_list(arguments_list):
	labels = set()

	for argument in arguments_list:
		labels.add(argument[0])

	return labels

def get_certain_attacks_from_bases(practical_base, epistemic_base):
	all_attacks = []
	
	for practical_argument in practical_base:
		if len(practical_argument[3]) > 0:
			for label in practical_argument[3]:
				all_attacks.append((label, practical_argument[0]))
	
	for epistemic_argument in epistemic_base:
		if len(epistemic_argument[1]) > 0:
			for label in epistemic_argument[1]:
				all_attacks.append((label, epistemic_argument[0]))
	
	return all_attacks
	
def get_attacks_to_remove_set(number, all_set):
	num_attacks_set = len(all_set)
	# selección del conjunto de ataques seguros para pasar a indeterminados
	indices_list = []
	for i in range(num_attacks_set):
		indices_list.append(i)
	
	select_attacks_indices = random.sample(population=indices_list, k=number) # sin reemplazo
	
	attacks_to_be_remove = []
	
	for i in select_attacks_indices:
		attacks_to_be_remove.append(all_set[i])
	
	return attacks_to_be_remove
	
def attacks_to_indeterminated_method(attacks, epistemic_base, practical_base):
	
	eps = copy.deepcopy(epistemic_base)
	prs = copy.deepcopy(practical_base)
	
	le = len(eps)
	lp = len(prs)
	
	for attack in attacks:
		label1, label2 = attack
		
		if "ae" in label2:
			for i in range(le):
				if eps[i][0] == label2:
					arg = list(eps[i])
					arg[1].remove(label1)
					arg[2].append(label1)
					arg = tuple(arg)
					eps[i] = arg
					break
		else:
			for i in range(lp):
				if prs[i][0] == label2:
					arg = list(prs[i])
					arg[3].remove(label1)
					arg[5].append(label1)
					arg = tuple(arg)
					prs[i] = arg
					break
	
	return eps, prs
	
def all_attacks_minus_certain_attacks(practical_base, epistemic_base, certain_attacks_initial, external_epistemic_arguments_labels):
	practical_base_labels = get_labels_from_arguments_list(practical_base) # set
	epistemic_base_labels = list(get_labels_from_arguments_list(epistemic_base))# set
	
	all_attacks = []
	
	for ep in epistemic_base_labels:
		for pr in practical_base_labels:
			all_attacks.append((ep, pr))
	
	# arreglar pra que no haya 12 o 21, solo una posibilidad
	le = len(epistemic_base_labels)
	for i in range(le):
		for j in range(le):
			if j < i:
				l = [epistemic_base_labels[i], epistemic_base_labels[j]]
				random.shuffle(l)
				l = tuple(l)
				all_attacks.append(l)
	
	for ex in external_epistemic_arguments_labels:
		for ep in epistemic_base_labels:
			all_attacks.append((ex, ep))
		for pr in practical_base_labels:
			all_attacks.append((ex, pr))
			
	for element in certain_attacks_initial:
		a, b = element
		if (a, b) in all_attacks:
			all_attacks.remove((a, b))
		if (b, a) in all_attacks:
			all_attacks.remove((b, a))
		
	return all_attacks

def inteterminations_selection(set_non_attacks, number):
	indices = []
	for i in range(number):
		indices.append(i)
	
	selection = random.sample(population=indices, k=number) # sin reemplazo
	
	new_list = []
	for i in selection:
		new_list.append(set_non_attacks[i])
	return new_list
	
#def to_indeterminations(set_possible_indeterminations, number):
#	indeterminations = []
#	
#	indices = []
#	for i in range(number):
#		indices.append(i)
#		
#	random.sample(population=indices, k=number) # sin reemplazo

def make_indeterminations_in_bases(epistemic_base, practical_base, indeterminations_set):
	
	for attack in indeterminations_set:
		label1, label2 = attack
		
		if "ae" in label2:
			for i in range(len(epistemic_base)):
				if epistemic_base[i][0] == label2:
					arg = list(epistemic_base[i])
					arg[2].append(label1)
					arg = tuple(arg)
					epistemic_base[i] = arg
					break
		else:
			for i in range(len(practical_base)):
				if practical_base[i][0] == label2:
					arg = list(practical_base[i])
					arg[5].append(label1)
					arg = tuple(arg)
					practical_base[i] = arg
					break
	
	return epistemic_base, practical_base
				
	


def modify_agent_arguments_bases(practical_base, epistemic_base, external_epistemic_arguments_set, resource_boundness_density=0):
	
	internal_practical_arguments_number = len(practical_base)
	internal_epistemic_arguments_number = len(epistemic_base)
	external_epistemic_arguments_number = len(external_epistemic_arguments_set)
	internal_arguments_number = internal_practical_arguments_number + internal_epistemic_arguments_number
	internal_arguments = practical_base + epistemic_base
	internal_epistemic_arguments_labels = get_labels_from_arguments_list(epistemic_base)


	certain_attacks_number = get_certain_attacks_number_agent(practical_base, epistemic_base)
	maximum_relations_number = internal_practical_arguments_number * internal_epistemic_arguments_number + internal_epistemic_arguments_number * (internal_epistemic_arguments_number - 1) / 2 + internal_practical_arguments_number * external_epistemic_arguments_number + internal_epistemic_arguments_number * external_epistemic_arguments_number
	maximum_relations_number = int(maximum_relations_number)
	certain_non_attacks_number = int(maximum_relations_number - certain_attacks_number)
	# cantidad de relaciones que no puedo procesar
	certain_non_deteminations_number = int(round(maximum_relations_number * resource_boundness_density, 0))

	#print(internal_practical_arguments_number)
	#print(internal_epistemic_arguments_number)
	#print(external_epistemic_arguments_number)
	#print(internal_arguments_number)
	#print(internal_arguments)
	#print(internal_epistemic_arguments_labels)
	#print(certain_attacks_number)
	#print(maximum_relations_number)
	#print(certain_non_attacks_number)
	#print(certain_non_deteminations_number)

	# ataques seguros a remover y colocar como indeterminados
	attacks_to_indeterminated = 0
	if certain_non_deteminations_number > certain_attacks_number:
		attacks_to_indeterminated = random.randint(0, certain_attacks_number)
	else:
		attacks_to_indeterminated = random.randint(0, certain_non_deteminations_number)
	  
	# no ataques seguros a colocar como indeterminados
	non_attacks_to_indeterminated = certain_non_deteminations_number - attacks_to_indeterminated

	# lista de ataques en el sistema
	attacks_set = get_certain_attacks_from_bases(practical_base, epistemic_base)
	num_attacks_set = len(attacks_set)
	# selección del conjunto de ataques seguros para pasar a indeterminados
	attacks_to_remove = get_attacks_to_remove_set(attacks_to_indeterminated, attacks_set)
	
	# genero ataques totales y filtro los ataques seguros iniciales (para el otro paso)
	modify = all_attacks_minus_certain_attacks(practical_base, epistemic_base, attacks_set, external_epistemic_arguments_set)
	
	# ejecución en un for-loop de una función que remueve ataque especificado y lo pasa a indeterminado
	#print(attacks_to_remove, "ok???")
	#print(attacks_to_remove, epistemic_base, practical_base)
	#print("to remove:", attacks_to_remove)
	#print("attack set", attacks_set)
	
	# ataques que no existen?????????
	epistemic_base_new, practical_base_new = attacks_to_indeterminated_method(attacks_to_remove, epistemic_base, practical_base)

	# agragar indeterminaciones de no ataques sin agregar las previamente modificadas
	#print("certain_attacks_number", certain_attacks_number)
	#print("maximum_relations_number", maximum_relations_number)
	#print("certain_non_attacks_number", certain_non_attacks_number)
	#print("attacks_to_indeterminated", attacks_to_indeterminated)
	#print("certain_non_deteminations_number", certain_non_deteminations_number)
	#print(len(modify), non_attacks_to_indeterminated, "ok")
	
	# el número de non_attacks_to_indeterminated es a veces mayor a lo que hay en modify
	#print("modify", len(modify))
	#print("nat", non_attacks_to_indeterminated)
	#print("nat menor o igual a modify???")
	to_modify = inteterminations_selection(modify, non_attacks_to_indeterminated)

	epistemic_base_final, practical_base_final = make_indeterminations_in_bases(epistemic_base_new, practical_base_new, to_modify)

	return practical_base_final, epistemic_base_final



class Agent:
	def __init__(self, agent_name, alternatives, epistemic_base, practical_base, semantic_r=True):
		self.name = agent_name
		self.alternatives = alternatives
		self.epistemic_base = epistemic_base
		self.practical_base = practical_base
		self.commitment_store = CommitmentStore()
		self.negotiation = Agent.Negotiation(self)
		self.semantic_r = semantic_r
		# PRUEBA
		self.epistemic_labels = Agent.get_epistemic_base_labels(self)
		self.practical_labels = Agent.get_practical_base_labels(self)
		self.all_arguments_labels = Agent.get_all_arguments_labels(self)
	
	def get_agent_name(self):
		return self.name

	def get_ep_labels(self):
		return self.epistemic_labels

	def get_pr_labels(self):
		return self.practical_labels

	def get_all_labels(self):
		return self.all_arguments_labels

	def get_alternatives(self):
		return self.alternatives

	def get_practical_base_structures(self):
		return self.practical_base
		
	def get_epistemic_base_structures(self):
		return self.epistemic_base

	def get_maximum_attacks_number(self):
		num_p = len(self.get_practical_base_structures())
		num_e = len(self.get_epistemic_base_structures())
		
		r = num_p * num_e + num_e * (num_e - 1) / 2
		return int(r)
		
	def add_argument_structure_to_base(self, argument_structure):
		if len(argument_structure) > 3:
			self.practical_base.append(argument_structure)
		else:
			self.epistemic_base.append(argument_structure)

	def get_practical_base_labels(self):
		practical_labels = set()

		for argument in self.practical_base:
			practical_labels.add(argument[0])

		return practical_labels

	def get_epistemic_base_labels(self):
		epistemic_labels = set()

		for argument in self.epistemic_base:
			epistemic_labels.add(argument[0])

		return epistemic_labels

	def get_commitment_store(self):
		return self.commitment_store

	def get_all_arguments_structures(self):
		pb = self.practical_base
		eb = self.epistemic_base
		arguments = pb + eb
		return arguments

	def is_label_in_arguments_base(self, argument_label):
		arguments = self.all_arguments_labels
		if argument_label in arguments:
			return True
		else:
			return False

	def get_all_arguments_labels(self):
		epistemic_labels = self.get_ep_labels()
		practical_labels = self.get_pr_labels()

		arguments_labels = epistemic_labels.union(practical_labels)

		return arguments_labels
	
	def get_argument_structure_from_label(self, argument_label):
		if "ap" in argument_label:
			practical_base = self.get_practical_base_structures()

			for practical_argument in practical_base:
				if practical_argument[0] == argument_label:
					return practical_argument

			return -1
		else:
			epistemic_base = self.get_epistemic_base_structures()

			for epistemic_argument in epistemic_base:
				if epistemic_argument[0] == argument_label:
					return epistemic_argument

			return -1

	def get_certain_attacked_labels_set_from_argument_label(self, argument_label):
		attacked_set = set()
		
		if self.is_label_in_arguments_base(argument_label) == True:
			epistemic_base = self.get_epistemic_base_structures()
			practical_base = self.get_practical_base_structures()
			
			for argument_structure in epistemic_base:
				if argument_label in argument_structure[1]:
					attacked_set.add(argument_structure[0])
	
			for argument_structure in practical_base:
				if argument_label in argument_structure[3]:
					attacked_set.add(argument_structure[0])
				
		return attacked_set

	def get_attackers_of_argument_label(self, argument_label, semantic_r=True):
		argument_structure = self.get_argument_structure_from_label(argument_label)

		if semantic_r == True:
			if len(argument_structure) == 3:
				real_attackers = set()
				for label in argument_structure[1]:
					if self.is_label_in_arguments_base(label) == True:
						real_attackers.add(label)

				return real_attackers
			else:
				real_attackers = set()
				for label in argument_structure[3]:
					if self.is_label_in_arguments_base(label) == True:
						real_attackers.add(label)

				return real_attackers

		else:
			if len(argument_structure) == 3:
				real_attackers = set()
				for label in argument_structure[1]:
					if self.is_label_in_arguments_base(label) == True:
						real_attackers.add(label)
				for label in argument_structure[2]:
					if self.is_label_in_arguments_base(label) == True:
						real_attackers.add(label)

				return real_attackers

			else:
				real_attackers = set()
				for label in argument_structure[3]:
					if self.is_label_in_arguments_base(label) == True:
						real_attackers.add(label)
				for label in argument_structure[5]:
					if self.is_label_in_arguments_base(label) == True:
						real_attackers.add(label)

				return real_attackers

	def get_certain_attacked_set(self, attacker_set):
		attacked_set = set()

		if attacker_set != set():
			for argument_label in attacker_set:
				attacked_set_of_argument = self.get_certain_attacked_labels_set_from_argument_label(argument_label)
				attacked_set = attacked_set.union(attacked_set_of_argument)
			return attacked_set

		else:
			return attacked_set 

	def get_undercuts(self):
		undercuts = set()
		epistemic_base = self.get_epistemic_base_structures()

		if self.semantic_r == True:
			for epistemic_argument in epistemic_base:
				if len(epistemic_argument[1]) > 0:
					for attacker_label in epistemic_argument[1]:
						if self.is_label_in_arguments_base(attacker_label) == True:
							undercuts.add((attacker_label, epistemic_argument[0]))
		else:
			for epistemic_argument in epistemic_base:
				if len(epistemic_argument[1]) > 0:
					for attacker_label in epistemic_argument[1]:
						if self.is_label_in_arguments_base(attacker_label) == True:
							undercuts.add((attacker_label, epistemic_argument[0]))

				if len(epistemic_argument[2]) > 0:
					for attacker_label in epistemic_argument[2]:
						if self.is_label_in_arguments_base(attacker_label) == True:
							undercuts.add((attacker_label, epistemic_argument[0]))

		return undercuts

	def get_attacks(self):
		attacks = set()
		practical_base = self.get_practical_base_structures()

		if self.semantic_r == True:
			for practical_argument in practical_base:
				if len(practical_argument[3]) > 0:
					for attacker_label in practical_argument[3]:
						if self.is_label_in_arguments_base(attacker_label) == True:
							attacks.add((attacker_label, practical_argument[0]))
		else:
			for practical_argument in practical_base:
				if len(practical_argument[3]) > 0:
					for attacker_label in practical_argument[3]:
						if self.is_label_in_arguments_base(attacker_label) == True:
							attacks.add((attacker_label, practical_argument[0]))

				if len(practical_argument[5]) > 0:
					for attacker_label in practical_argument[5]:
						if self.is_label_in_arguments_base(attacker_label) == True:
							attacks.add((attacker_label, practical_argument[0]))

		return attacks

	def get_all_attacks(self):
		undercuts = copy.copy(self.get_undercuts())
		attacks = copy.copy(self.get_attacks())

		all_attacks = copy.copy(undercuts.union(attacks))

		return all_attacks

	def get_maximal_cfs(self):
		all_arguments_labels = list(self.all_arguments_labels)
		arguments_number = len(all_arguments_labels)
		all_attacks = list(self.get_all_attacks())

		graph = nx.Graph()
		graph.add_nodes_from(all_arguments_labels)
	
		links = []
	
		for i in range(0, arguments_number):
			for j in range(i + 1, arguments_number):
				
				no_attack = True
				
				for attack in all_attacks:
					if (attack[0] == all_arguments_labels[i] and
					 attack[1] == all_arguments_labels[j]) or (attack[0] == all_arguments_labels[j] and
					  attack[1] == all_arguments_labels[i]):
						no_attack = False
						break
						
				if no_attack == True:
					links.append((all_arguments_labels[i], all_arguments_labels[j]))
	  
		graph.add_edges_from(links)
		
		maximum_cliques = nx.find_cliques(graph)

		cliques_list = []

		for clique in maximum_cliques:
			cliques_list.append(set(clique))
			
		return cliques_list


	def get_acceptable_arguments(self):
		maximal_cfs = self.get_maximal_cfs()
		maximal_admisibles_sets = self.maximal_admisible_cfs(maximal_cfs) #extensiones preferidas
		
		acceptable_arguments = set()

		for admisible_set in maximal_admisibles_sets:
			acceptable_arguments = acceptable_arguments.union(admisible_set)

		return acceptable_arguments


	def is_candidate_decision(self, decision):
		acceptable_arguments = self.get_acceptable_arguments()

		for acceptable_argument_label in acceptable_arguments:
			acceptable_argument_structure = self.get_argument_structure_from_label(acceptable_argument_label)

			if len(acceptable_argument_structure) == 6:
				if acceptable_argument_label == acceptable_argument_structure[0] and acceptable_argument_structure[2]== decision:
					return True

		return False

	def get_candidate_decisions(self):
		candidates_decisions = []

		for alternative in self.alternatives:
			if self.is_candidate_decision(alternative) == True:
				candidates_decisions.append(alternative)

		return candidates_decisions


	def is_acceptable_argument(self, argument_structure):
		acceptable_arguments = self.get_acceptable_arguments()

		if argument_structure[0] in acceptable_arguments:
			return True

		else:
			return False
	
	def get_acceptable_pro_of_decision(self, decision):
		acceptable_arguments_pro_decision = []
		acceptable_arguments = self.get_acceptable_arguments()

		for argument_label in acceptable_arguments:
			argument_structure = self.get_argument_structure_from_label(argument_label)

			if len(argument_structure) == 6 and argument_structure[1] == "P" and argument_structure[2] == decision:
				acceptable_arguments_pro_decision.append(argument_structure)

		return acceptable_arguments_pro_decision

	def get_acceptable_con_of_decision(self, decision):
		acceptable_arguments_con_decision = []
		acceptable_arguments = self.get_acceptable_arguments()

		for argument_label in acceptable_arguments:
			argument_structure = self.get_argument_structure_from_label(argument_label)

			if len(argument_structure) == 6 and argument_structure[1] == "C" and argument_structure[2] == decision:
				acceptable_arguments_con_decision.append(argument_structure)

		return acceptable_arguments_con_decision
	
	def get_preferred_decision_from_arguments_pro(self, arguments_pro_decision1, arguments_pro_decision2):
		arguments_pro_decision1_number = len(arguments_pro_decision1)
		arguments_pro_decision2_number = len(arguments_pro_decision2)

		if arguments_pro_decision1_number > 0 and arguments_pro_decision2_number > 0:
			strengths_arguments_pro_decision1 = []
			strengths_arguments_pro_decision2 = []

			for argument_pro_decision1 in arguments_pro_decision1:
				strengths_arguments_pro_decision1.append(argument_pro_decision1[4])
			
			for argument_pro_decision2 in arguments_pro_decision2:
				strengths_arguments_pro_decision2.append(argument_pro_decision2[4])
			
			maximum_strength_decision1 = max(strengths_arguments_pro_decision1)
			maximum_strength_decision2 = max(strengths_arguments_pro_decision2)

			if maximum_strength_decision1 > maximum_strength_decision2:
				return "Primera"

			elif maximum_strength_decision2 > maximum_strength_decision1:
				return "Segunda"

			else:
				if arguments_pro_decision1_number > arguments_pro_decision2_number:
					return "Primera"

				elif arguments_pro_decision1_number < arguments_pro_decision2_number:
					return "Segunda"

				else:
					return "Equal"
		else:
			if arguments_pro_decision1_number > 0 and arguments_pro_decision2_number == 0:
				return "Primera"

			else:
				return "Segunda"

	def get_preferred_decision_from_arguments_con(self, arguments_con_decision1, arguments_con_decision2):
		arguments_con_decision1_number = len(arguments_con_decision1)
		arguments_con_decision2_number = len(arguments_con_decision2)

		if arguments_con_decision1_number > 0 and arguments_con_decision2_number > 0:

			weaknesses_arguments_con_decision1 = []
			weaknesses_arguments_con_decision2 = []
			
			for argument_con_decision1 in arguments_con_decision1:
				weaknesses_arguments_con_decision1.append(argument_con_decision1[4])

			for argument_con_decision2 in arguments_con_decision2:
				weaknesses_arguments_con_decision2.append(argument_con_decision2[4])

			maximum_weakness_decision1 = max(weaknesses_arguments_con_decision1)
			maximum_weakness_decision2 = max(weaknesses_arguments_con_decision2)

			if maximum_weakness_decision1 > maximum_weakness_decision2:
				return "Primera"

			elif maximum_weakness_decision2 > maximum_weakness_decision1:
				return "Segunda"

			else:
				if arguments_con_decision1_number > arguments_con_decision2_number:
					return "Segunda"

				elif arguments_con_decision1_number < arguments_con_decision2_number:
					return "Primera"

				else:
					return "Equal"

		else:
			if arguments_con_decision1_number > 0 and arguments_con_decision2_number == 0:
				return "Segunda"

			else:
				return "Primera"



	def get_preferred_decision(self, decision1, decision2):
		arguments_pro_decision1 = self.get_acceptable_pro_of_decision(decision1)
		arguments_con_decision1 = self.get_acceptable_con_of_decision(decision1)
		arguments_pro_decision2 = self.get_acceptable_pro_of_decision(decision2)
		arguments_con_decision2 = self.get_acceptable_con_of_decision(decision2)

		status_pro = 0
		status_con = 0

		arguments_pro_decision1_number = len(arguments_pro_decision1)
		arguments_pro_decision2_number = len(arguments_pro_decision2)
		arguments_con_decision1_number = len(arguments_con_decision1)
		arguments_con_decision2_number = len(arguments_con_decision2)

		if arguments_pro_decision1_number == 0 and arguments_pro_decision2_number == 0:
			status_pro = None
		elif arguments_pro_decision1_number == 0 and arguments_pro_decision2_number > 0:
			status_pro = "Segunda"
		elif arguments_pro_decision1_number > 0 and arguments_pro_decision2_number == 0:
			status_pro = "Primera"
		elif arguments_pro_decision1_number > 0 and arguments_pro_decision2_number > 0:
			status_pro = self.get_preferred_decision_from_arguments_pro(arguments_pro_decision1, arguments_pro_decision2)

		if arguments_con_decision1_number == 0 and arguments_con_decision2_number == 0:
			status_con = None
		elif arguments_con_decision1_number == 0 and arguments_con_decision2_number > 0:
			status_con = "Primera"
		elif arguments_con_decision1_number > 0 and arguments_con_decision2_number == 0:
			status_con = "Segunda"
		elif arguments_con_decision1_number > 0 and arguments_con_decision2_number > 0:
			status_con = self.get_preferred_decision_from_arguments_con(arguments_con_decision1, arguments_con_decision2)

		if status_pro == None and status_con == None:
			return None
		elif status_pro == None and status_con != None:
			if status_con == "Primera":
				return decision1
			elif status_con == "Segunda":
				return decision2
			elif status_con == "Equal":
				return None
		elif status_con == None and status_pro != None:
			if status_pro == "Primera":
				return decision1
			elif status_pro == "Segunda":
				return decision2
			elif status_pro == "Equal":
				return None
		elif status_pro == "Primera" and status_con == "Primera":
			return decision1
		elif status_pro == "Segunda" and status_con == "Segunda":
			return decision2
		elif status_pro == "Segunda" and status_con == "Primera":
			return None
		elif status_pro == "Primera" and status_con == "Segunda":
			return None
		elif status_pro == "Equal" and status_con == "Equal":
			return None
		elif status_pro == "Equal" and status_con == "Primera":
			return decision1
		elif status_pro == "Equal" and status_con == "Segunda":
			return decision2
		elif status_pro == "Primera" and status_con == "Equal":
			return decision1
		elif status_pro == "Segunda" and status_con == "Equal":
			return decision2


	def candidate_decisions_descending_order_of_preference(self):

		candidate_decisions = self.get_candidate_decisions()

		if len(candidate_decisions) == 0:
			return ["equallyPreferred", self.alternatives]

		else:
			preference_list = self.selection_sort(candidate_decisions) # lista de preferencias de mayor a menor, res None, [a,b]

			if preference_list == None:
				return ["equallyPreferred", self.alternatives]
			else:
				return ["prefOrder", preference_list]
			
	def selection_sort(self, list_to_order): # lista de alternativas candidatas
		list_to_order_len = len(list_to_order)

		if list_to_order_len > 0:
			for i in range(list_to_order_len):
				least = i # índice de alternativa
				for k in range(i + 1, list_to_order_len):
					a = self.get_preferred_decision(list_to_order[k], list_to_order[least]) 
					if a == list_to_order[k]:
						least = k

				swap(list_to_order, least, i)

			return list_to_order

		else:
			return None


	def is_now_acceptable_offer(self, current_offer):
		candidates_decisions = self.get_candidate_decisions()
		candidates_decisions_number = len(candidates_decisions)

		if candidates_decisions_number == 0:
			return True

		elif current_offer not in candidates_decisions:
			return False

		elif candidates_decisions_number == 1 and current_offer in candidates_decisions:
			return True

		else:
			for decision in candidates_decisions:
				if decision != current_offer:
					preferred = self.get_preferred_decision(decision, current_offer)

					if preferred != current_offer and preferred != None:
						return False
			return True

	"""
	def __is_defendedBySet(self, arg, E):
		Bs = self.get_attackers_of_argument_label(arg)
		
		Bs = set(Bs)
		E = set(E)
		
		if len(Bs.intersection(E)) > 0:
			return False
		else:
			if len(E) >= 0:
				if len(Bs)>0: # si tiene atacantes externos
					s = True
					for element in Bs:
						at = set(self.get_attackers_of_argument_label(element))					
						if at.intersection(E)==set():
							s = False
							break
					if s== True:
						return True
					else:
						return False
				else:
					return True # si no hay atacantes, lo defiente
	"""			
	# Retorna conjuntos admisibles maximales dados los cfs maximales
	def maximal_admisible_cfs(self, maximal_cfs):

		attacks = self.get_all_attacks()

		maximal_admisible_sets = []

		for cfs in maximal_cfs:

			cfs = set(cfs)
			admisible_set = copy.copy(cfs)

			while len(admisible_set) >= 0:
				to_delete = set()

				for argument in admisible_set:
						#comp = args.difference(admis) # complemento del cfs --- admis no cfs
					argument_attakers = self.get_attackers_of_argument_label(argument, semantic_r=False) # argumentos que atacan a el elemento "x" de "admis"

					admisible_set_without_argument = admisible_set.difference({argument}) # cfs sin "x" --- admis no cfs

					certain_attacked_set = self.get_certain_attacked_set(admisible_set_without_argument)# argumentos a los que ataca "cfs" sin "x"

					if len(argument_attakers) > 0: # si hay al menos un argumento externo a cfs que ataca a x
						if argument_attakers.intersection(certain_attacked_set) != argument_attakers:
							to_delete.add(argument)

				if to_delete == set(): 
					break

				else:
					admisible_set = copy.copy(admisible_set.difference(to_delete))
				
			if admisible_set not in maximal_admisible_sets and admisible_set != set():
				maximal_admisible_sets.append(admisible_set)
					
		#necesito quedarme con los qque satisfacen lema 10 (elimino subconjuntos de uqellos)
		to_remove = []
		
		for s1 in maximal_admisible_sets:
			for s2 in maximal_admisible_sets:
				if s1 != s2:
					if s1 == s2.intersection(s1):
						if s1 not in to_remove:
							to_remove.append(s1)
						
		for k in to_remove:
			maximal_admisible_sets.remove(k)

		return maximal_admisible_sets

	class Negotiation:
		def __init__(self, af):
			self.af = af

			self.offer_x = Agent.Negotiation.OfferX(self)
			self.challenge_x = Agent.Negotiation.ChallengeX(self)
			self.challenge_y = Agent.Negotiation.ChallengeY(self)
			self.argue_s = Agent.Negotiation.ArgueS(self)
			self.accept_x = Agent.Negotiation.AcceptX(self)
			self.accept_s = Agent.Negotiation.AcceptS(self)
			self.refuse_x = Agent.Negotiation.RefuseX(self)
		
		class OfferX:
			def __init__(self, af):
				self.af = af
			def preconditions(self, remaining_alternatives):
				cd = self.af.af.candidate_decisions_descending_order_of_preference()
				
				for e in cd[1]:
					if e in remaining_alternatives:
						return e
				if len(remaining_alternatives) > 0:
					return remaining_alternatives[0]
				
				return None
				  
			def postconditions(self, offer):
				self.af.af.commitment_store.add_proposed_or_accepted_offer(offer) 

		class ChallengeX:
			def __init__(self, af):
				self.af = af

			def preconditions(self, current_offer):
				if current_offer not in self.af.af.commitment_store.offers_proposed:
					return True
				else:
					return False

			def postconditions(self, current_offer):
				self.af.af.commitment_store.add_challenge_presented(current_offer)

		class ChallengeY:
			def __init__(self, af):
				self.af = af

			def preconditions(self, argument_or_offer):
				if argument_or_offer not in self.af.af.commitment_store.challenges_made:
					return True
				else:
					return False

			def postconditions(self, argument_or_offer):
				self.af.af.commitment_store.add_challenge_presented(argument_or_offer)
				
		class ArgueS:
			def __init__(self, af):
				self.af = af

			def preconditions(self, current_offer):

				con_arguments = self.af.af.get_acceptable_con_of_decision(current_offer)
				pro_arguments = self.af.af.get_acceptable_pro_of_decision(current_offer)

				all_arguments_acceptable = con_arguments + pro_arguments
		
				arguments_presented = self.af.af.commitment_store.arguments_presented

				argument_to_present_label = search_argument_to_share(arguments_presented, all_arguments_acceptable)

				if argument_to_present_label != False:
					return self.af.af.get_argument_structure_from_label(argument_to_present_label)

				else:
					return False

			def postconditions(self, argument_structure):
				self.af.af.commitment_store.add_argument_presented(argument_structure)

		class AcceptX:
			def __init__(self, af):
				self.af = af
			
			def preconditions(self, current_offer):
				if current_offer not in self.af.af.commitment_store.offers_proposed:

					status = self.af.af.is_now_acceptable_offer(current_offer)

					if status == True:
						return True

					else:
						return False
				else:
					return False
					
			def postconditions(self, current_offer):
				self.af.af.commitment_store.add_proposed_or_accepted_offer(current_offer)

		class AcceptS:
			def __init__(self, af):
				self.af = af

			def preconditions(self, argument_structure):
				if argument_structure not in self.af.af.commitment_store.external_arguments_added and self.af.af.name not in argument_structure[0]:
					if self.af.af.is_acceptable_argument(argument_structure) == True:
						return True
					else:
						self.af.af.commitment_store.add_external_argument(argument_structure)
						return False
				else:
					return False

			def postconditions(self, argument_structure):
				self.af.af.commitment_store.add_external_argument(argument_structure)

		class RefuseX:
			def __init__(self, af):
				self.af = af

			def preconditions(self, current_offer):
					if current_offer in self.af.af.commitment_store.offers_proposed:
						return False

					else:
						arguments_con = self.af.af.get_acceptable_con_of_decision(current_offer)
						
						status = True

						for argument in arguments_con:
							if argument not in self.af.af.commitment_store.arguments_presented:
								status = False
								break

						if status == True:
							return False

						else:
							return True
						
			def postconditions(self):
				#self.af.af.commitment_store.add_Refuse(current_offer)
				return None


##########################
### Otras funciones
##########################

def get_arguments_labels_set_from_structures_list(arguments_structures_list):
	labels = set()

	if arguments_structures_list != []:
		for argument_structure in arguments_structures_list:
			labels.add(argument_structure[0])

	return labels

def search_argument_to_share(arguments_presented, acceptable_arguments):

	arguments_presented_labels_set = get_arguments_labels_set_from_structures_list(arguments_presented)
	arguments_acceptable_labels_set = get_arguments_labels_set_from_structures_list(acceptable_arguments)

	if len(arguments_acceptable_labels_set) > 0:
		for j in arguments_acceptable_labels_set:
			if len(arguments_presented_labels_set.intersection({j})) == 0:
				return j
		return False
	else:
		return False



def swap(A, x, y): # recibe una lista de alternativas candidatas, e índices de 2 de ellas distintas
	if x < len(A) and y < len(A):
		temp = A[x]
		A[x] = A[y]
		A[y] = temp

				

