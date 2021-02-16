#!/usr/bin/env python
# -*- coding: utf-8 -*-

from module.experiments import *
from datetime import datetime
import os

def get_agent_from_name(name, agents):
	for agent in agents:
		if agent.name == name:
			return agent
	return -1
	
def are_equal_arguments_set(args1, args2):
	if len(args1) != len(args2):
		return False
	else:	
		for arg in args1:
			if arg not in args2:
				return False
	return True
	
# si dos conjuntos de agents son iguales
def are_equal_agents_sets(agent_set_1, agent_set_2):
	for agent1 in agent_set_1:
		agent2 = get_agent_from_name(agent1.name, agent_set_2)
		args_1 = agent1.get_all_arguments_structures()
		args_2 = agent2.get_all_arguments_structures()
		status = are_equal_arguments_set(args_1, args_2)
		if status == False:
			return False
	return True

def exp(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, step, resource_boundness_density):
	#number_agents = 3
	#alternatives_number = 3
	#maximum_number_practical_arguments = 5
	#maximum_number_epistemic_arguments = 3
	#maximum_attacks_density_value = 0.3
	#N = 3
	# Returns a datetime object containing the local date and time
	dto = datetime.now()
	
	if not os.path.exists('results'):
		os.makedirs('results')

	cwd = os.getcwd() 
	name1 = str(cwd)+"/results/"+str(dto.day)+"-"+str(dto.month)+"-"+str(dto.year)+"-"+str(dto.hour)+"-"+str(dto.minute)+"-"+str(dto.second)+"__synthetic.csv"
	name2 = str(cwd)+"/results/"+str(dto.day)+"-"+str(dto.month)+"-"+str(dto.year)+"-"+str(dto.hour)+"-"+str(dto.minute)+"-"+str(dto.second)+"__negotiation_taf_optimal.csv"
	fname = str(cwd)+"/results/"+str(dto.day)+"-"+str(dto.month)+"-"+str(dto.year)+"-"+str(dto.hour)+"-"+str(dto.minute)+"-"+str(dto.second)+"__metrics.csv"
	#step = 2
	#M = 3
	#resource_boundness_densities = [0.3, 0.4, 0.2]
	##################################3
	
	status = False

	while status == False:
		taf_agents = set_synthetic_experiment_taf_agents(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value)
		#taf_agents_original = copy.deepcopy(taf_agents)
		save_synthetic_experiment_taf_agents(name1, taf_agents)
		
		taf_plus = get_taf_plus_agent(taf_agents)
	
		N, agreements_number, optimal_agreements, mean_time_by_negotiation, taf_agents_final = execute_negotiations_with_taf_agents(N, taf_agents)
	
		save_taf_negotiation_results(name2, N, agreements_number, optimal_agreements, mean_time_by_negotiation)
		
		if len(optimal_agreements) == 1 and agreements_number == N:
			status = True
	
	#print("equal?", are_equal_agents_sets(taf_agents_original, taf_agents))
	# recibe el taf_agents original...
	pafs_negotiations(fname, number_agents, step, N, taf_agents, resource_boundness_density, taf_agents_final)
