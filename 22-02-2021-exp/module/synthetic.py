#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from module.agent import *
import copy

def get_major_agent_from_agents(agents):

	name = "MajorAgent"

	alternatives = set()
	practical_arguments = []
	epistemic_arguments = []

	for agent in agents:
		alternatives = agent.get_alternatives()
		practical_base = agent.get_practical_base_structures()
		epistemic_base = agent.get_epistemic_base_structures()
		for argument in agent.practical_base:
			practical_arguments.append(argument)
		for argument in agent.epistemic_base:
			epistemic_arguments.append(argument)

	major_agent = Agent("MajorAgent", alternatives, epistemic_arguments, practical_arguments, semantic_r=True)

	return major_agent


def create_agents(number_agents, alternatives_number, maximum_number_practical_arguments,
 maximum_number_epistemic_arguments, maximum_attacks_density_value):
	
	if number_agents >= 1 and alternatives_number >= 2 and isinstance(alternatives_number, int) and maximum_attacks_density_value >= 0 and maximum_attacks_density_value <= 1 and maximum_number_epistemic_arguments >= 1 and maximum_number_practical_arguments >= alternatives_number:

		agents = set()
	
		#goals_bases = create_goals_bases(number_agents, maximum_number_goals)

		alternatives = create_alternatives(alternatives_number)
		
		arguments, ext = create_arguments(number_agents, maximum_number_practical_arguments, maximum_number_epistemic_arguments,
		 maximum_attacks_density_value, alternatives)
		
		for i in range(number_agents):
			agent = Agent("Ag" + str(i + 1), alternatives, arguments[i][1], arguments[i][0], semantic_r=True)
			args_epistemic_number = len(arguments[i][1])
			args_practical_number = len(arguments[i][0])

			number_internal = args_practical_number * args_epistemic_number + args_epistemic_number * (args_epistemic_number - 1) / 2
			agent.maximum_attacks_number = ext[i] + number_internal
			agents.add(agent)
		
		return agents

	else:
		return -1
			 

def create_arguments(number_agents, maximum_number_practical_arguments, maximum_number_epistemic_arguments,
		 maximum_attacks_density_value, alternatives):

	arguments_bases = []

	for i in range(number_agents):

		alternatives_number = len(alternatives)

		practical_arguments_number = random.randint(alternatives_number, maximum_number_practical_arguments)
		epistemic_arguments_number = random.randint(1, maximum_number_epistemic_arguments)
		
		maximum_attacks_number = practical_arguments_number * epistemic_arguments_number + epistemic_arguments_number * (epistemic_arguments_number - 1) / 2
		
		attacks_density_value = random.uniform(0.1, maximum_attacks_density_value)

		attacks_number = round(maximum_attacks_number * attacks_density_value, 0)
		
		practical_arguments_base = []
		epistemic_arguments_base = []
		
		for j in range(practical_arguments_number):
			practical_arguments_base.append("ap" + str(j + 1) + "Ag" + str(i + 1))

		for j in range(epistemic_arguments_number):
			epistemic_arguments_base.append("ae" + str(j + 1) + "Ag" + str(i + 1))

		all_arguments = []

		for practical_argument in practical_arguments_base:
			all_arguments.append(practical_argument)

		for epistemic_argument in epistemic_arguments_base:
			all_arguments.append(epistemic_argument)

		attacks = set()
		count = 0

		while count < attacks_number:
			epistemic_argument_selected = random.choice(epistemic_arguments_base)
			argument_selected = random.choice(all_arguments)

			if epistemic_argument_selected != argument_selected:
				if (epistemic_argument_selected, argument_selected) not in attacks and (argument_selected, epistemic_argument_selected) not in attacks:
					attacks.add((epistemic_argument_selected, argument_selected))
					count += 1
		
		alternatives_list_variable = list(alternatives)
		alternatives_list = list(alternatives)

		if alternatives_number < practical_arguments_number:
			for j in range(practical_arguments_number - alternatives_number):
				alternatives_list_variable.append(random.choice(alternatives_list))
				
		practical_base = []
		index = 0

		for practical_argument_label in practical_arguments_base:

			type_label = random.choice(["P", "C"])
			certainty_value = random.random()

			practical_argument_structure = (practical_argument_label, type_label, alternatives_list_variable[index], [], certainty_value, [])

			for attack in attacks:
				if practical_argument_label == attack[1]:
					practical_argument_structure[3].append(attack[0])

			practical_base.append(practical_argument_structure)

			index += 1
			
		epistemic_base = []

		for epistemic_argument_label in epistemic_arguments_base:

			epistemic_argument_structure = (epistemic_argument_label, [], [])

			for attack in attacks:
				if epistemic_argument_label == attack[1]:
					epistemic_argument_structure[1].append(attack[0])

			epistemic_base.append(epistemic_argument_structure)
			
		arguments_bases.append([practical_base, epistemic_base])


	arguments_bases, ext = create_external_attacks(arguments_bases, maximum_attacks_density_value)

	return arguments_bases, ext

def get_remaining_bases(current_bases, arguments_bases):
	remaining_bases = []

	for agent_bases in arguments_bases:
		if current_bases != agent_bases:
			remaining_bases.append(agent_bases)

	return remaining_bases

def get_epistemic_labels_from_remaining_bases(remaining_bases):
	epistemic_labels = []

	for bases in remaining_bases:
		for argument_structure in bases[1]:
			epistemic_labels.append(argument_structure[0])
	
	return epistemic_labels

def get_arguments_number(agent_arguments_bases):

	practical_arguments_number = len(agent_arguments_bases[0])
	epictemic_arguments_number = len(agent_arguments_bases[1])
	
	return practical_arguments_number + epictemic_arguments_number

def is_already_attacked(argument_structure_seggested, external_epictemic_label):
	if len(argument_structure_seggested) == 3:
		if external_epictemic_label in argument_structure_seggested[1]:
			return True
		else:
			return False
	else:
		if external_epictemic_label in argument_structure_seggested[3]:
			return True
		else:
			return False

def get_all_arguments_from_agent_bases(agent_bases):

	arguments = []

	for practical_argument in agent_bases[0]:
		arguments.append(practical_argument)
	
	for epistemic_argument in agent_bases[1]:
		arguments.append(epistemic_argument)

	return arguments

def select_possible_argument_to_be_attacked(agent_bases):

	arguments = get_all_arguments_from_agent_bases(agent_bases)
	arguments_number = len(arguments)

	if arguments_number > 0:
		index = random.randint(0, arguments_number - 1) 
		return arguments[index]
	else:
		return -1


def is_mutual_attack(label_argument_to_be_attacked, argument_structure_that_wants_to_attack):
	if len(argument_structure_that_wants_to_attack) != 3:
		return False
	else:
		if label_argument_to_be_attacked in argument_structure_that_wants_to_attack[1]:
			return True
		else:
			return False

def get_argument_structure_from_label(remaining_bases, argument_label):
	for bases in remaining_bases:
		for argument in bases[0]:
			if argument_label == argument[0]:
				return argument

		for argument in bases[1]:
			if argument_label == argument[0]:
				return argument

	return -1

def add_effective_attack(argument_structure, attack_label, agent_bases):

	if isinstance(attack_label, str):
			
		if len(argument_structure) == 3:
			argument_label = argument_structure[0]

			for argument in agent_bases[1]:
				if argument[0] == argument_label:
					r = list(argument)
					r[1].append(attack_label)
					argument = tuple(r)
					return agent_bases

			return -1

		elif len(argument_structure) == 6:
			argument_label = argument_structure[0]

			for argument in agent_bases[0]:
				if argument[0] == argument_label:
					r = list(argument)
					r[3].append(attack_label)
					argument = tuple(r)
					return agent_bases
			return -1

		else:
			return -1

	else:
		return -1
			

	

"""
def maximum_number_non_attacks(arguments_bases_agents, bases):
	for agent_bases in arguments_bases_agents:
		if bases == agent_bases:
			remaining_bases = get_remaining_bases(bases, arguments_bases_agents)
			epistemic_labels_from_remaining_bases = get_epistemic_labels_from_remaining_bases(remaining_bases)
			argument_number_current_bases = get_arguments_number(agent_bases)
			external_arguments_number = len(epistemic_labels_from_remaining_bases)
			maximum_attacks_number_from_external_arguments = argument_number_current_bases * external_arguments_number

			return maximum_attacks_number_from_external_arguments
"""

def create_external_attacks(arguments_bases, maximum_attacks_density_value):

	max_ext_attacks_number = []

	for i in range(len(arguments_bases)):
		remaining_bases = get_remaining_bases(arguments_bases[i], arguments_bases)
		epistemic_labels_from_remaining_bases = get_epistemic_labels_from_remaining_bases(remaining_bases)
		argument_number_current_bases = get_arguments_number(arguments_bases[i])
		external_arguments_number = len(epistemic_labels_from_remaining_bases)
		maximum_attacks_number_from_external_arguments = argument_number_current_bases * external_arguments_number
		attacks_density_value = random.random() * maximum_attacks_density_value
		attacks_to_add_number = round(attacks_density_value * maximum_attacks_number_from_external_arguments, 0)

		max_ext_attacks_number.append(maximum_attacks_number_from_external_arguments)

		effective_attacks_added_number = 0

		while effective_attacks_added_number < attacks_to_add_number:
			# tomo un argumento al azar de los restantes
			external_argument_label_selected = random.choice(epistemic_labels_from_remaining_bases)
			
			possible_argument_structure_to_be_attacked = select_possible_argument_to_be_attacked(arguments_bases[i])
			possible_argument_label_to_be_attacked = possible_argument_structure_to_be_attacked[0]
			# checkeo que no repita ese mismo ataque
			attack_status = is_already_attacked(possible_argument_structure_to_be_attacked, external_argument_label_selected)
			#checkeo que si se agraga a un epistemic, no exista el ataue mutuo
			external_argument_structure_selected = get_argument_structure_from_label(remaining_bases, external_argument_label_selected)
			mutual_status = is_mutual_attack(possible_argument_label_to_be_attacked, external_argument_structure_selected)
			# lo incorporo como ataque a un practico o epistemico en la base corriente
			if attack_status == False and mutual_status == False:
				# añado ataque
				arguments_bases[i] = add_effective_attack(possible_argument_structure_to_be_attacked, external_argument_label_selected, arguments_bases[i])
				effective_attacks_added_number += 1

	return arguments_bases, max_ext_attacks_number

def create_alternatives(number_alternatives):

	if number_alternatives >= 0 and isinstance(number_alternatives, int):

		alternatives = set()

		for i in range(number_alternatives):
			alternatives.add("X" + str(i + 1)) 
		
		return alternatives

	else:
		return -1

"""
def create_goals_bases(number_bases, maximum_number_goals_per_base):

	if number_bases > 0 and maximum_number_goals_per_base > 0:

		bases = []

		for i in range(number_bases):
			real_number_goals = random.randint(1, maximum_number_goals_per_base)

			single_base = set()

			indices = list(np.random.choice(maximum_number_goals_per_base, real_number_goals, replace=False))

			for j in range(real_number_goals):
				importance_value = random.uniform(0.1, 1)
				single_base.add(("g" + str(indices[j] + 1), round(importance_value, 2)))

			bases.append(single_base)

		return bases

	else:
		return -1
"""


def create_paf_agent(agent, resource_boundness_density, semantic_r, external_epistemic_arguments_list):
	practical_base = agent.get_practical_base_structures()
	epistemic_base = agent.get_epistemic_base_structures()
	#goals_base = agent.get_goals_base()
	agent_name = agent.get_agent_name()
	alternatives = agent.get_alternatives()


	# modifico bases segun kinit y kturn
	new_practical_base, new_epistemic_base = modify_agent_arguments_bases(practical_base, epistemic_base, external_epistemic_arguments_list, resource_boundness_density)
	
	return Agent(agent_name, alternatives, new_epistemic_base, new_practical_base, semantic_r)

def create_paf_agents(taf_agents, resource_boundness_density, semantics_r):
	paf_agents = []
	number_agents = len(taf_agents)
	taf_agents = copy.deepcopy(list(taf_agents))
	arguments_bases = []
	for i in range(number_agents):
		arguments_bases.append([taf_agents[i].get_practical_base_structures(), taf_agents[i].get_epistemic_base_structures()])
		
	for i in range(number_agents):
		current_bases = [taf_agents[i].get_practical_base_structures(), taf_agents[i].get_epistemic_base_structures()]

		remaining_bases_list = get_remaining_bases(current_bases, arguments_bases)
		external_epistemic_arguments_labels_list = get_epistemic_labels_from_remaining_bases(remaining_bases_list)
		paf_agent = create_paf_agent(taf_agents[i], resource_boundness_density, semantics_r[i], external_epistemic_arguments_labels_list)
		paf_agents.append(paf_agent)
	
	return paf_agents
