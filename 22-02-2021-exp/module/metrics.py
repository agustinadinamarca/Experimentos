#!/usr/bin/env python
# -*- coding: utf-8 -*-

# semantica r
#TP = R / (Re + Ne) --> R = [0, Re] --> TP = R / Re
#TN = N + I \int N+ = Ne / (Re + Ne) --> Ne = [0, Ne] --> TN = Ne / Ne
#FP = \emptyset = FP = 0
#FN = I \int Re / (Re + Ne) --> I int Re = [0, Re] --> FN = (I int Re) / Re
			
# semantica ri
#TP = Re / (Re + Ne) = 1
#TN = N / (Re + Ne)
#FP = In / (Re + Ne)
#FN = 0

import numpy as np

def get_re_taf(agent_taf):
	attacks = set(agent_taf.get_all_attacks())
	return attacks

def get_i_paf(agent_paf):
	practical = agent_paf.get_practical_base_structures()
	epistemic = agent_paf.get_epistemic_base_structures()
	#print(practical)
	#print(epistemic)
	epistemic_labels = agent_paf.get_epistemic_base_labels()

	possible_attacks = set()
	for argument in practical:
		if len(argument[5]) > 0:
			label = argument[0]
			for i in argument[5]:
				if i in epistemic_labels:
					possible_attacks.add((i, label))
	
	for argument in epistemic:
		if len(argument[2]) > 0:
			label = argument[0]
			for i in argument[2]:
				if i in epistemic_labels:
					possible_attacks.add((i, label))

	return possible_attacks

def get_r_paf(agent_paf):
	practical = agent_paf.get_practical_base_structures()
	epistemic = agent_paf.get_epistemic_base_structures()

	epistemic_labels = agent_paf.get_epistemic_base_labels()

	attacks = set()
	for argument in practical:
		if len(argument[3]) > 0:
			label = argument[0]
			for i in argument[3]:
				if i in epistemic_labels:
					attacks.add((i, label))
	
	for argument in epistemic:
		if len(argument[1]) > 0:
			label = argument[0]
			for i in argument[1]:
				if i in epistemic_labels:
					attacks.add((i, label))

	return attacks

# metric 1: FP, FN, TP, TN
def metric1(agent_taf, agent_paf):

	tp, tn, fp, fn = 0, 0, 0, 0

	r = get_r_paf(agent_paf)
	re = get_re_taf(agent_taf)
	i = get_i_paf(agent_paf)

	len_r = len(r)
	len_re = len(re)
	len_i = len(i)
	len_total = agent_taf.get_maximum_attacks_number()
	len_ne = len_total - len_re
	len_n = len_ne - (len_i - len(i.intersection(re)))


	if agent_paf.semantic_r == True:
		if len_re > 0:
			tp = float(len_r / len_re)
			tn = 1
			fp = 0
			fn = float(len(re.intersection(i)) / len_re)
		else:
			tp = 1
			tn = 1
			fp = 0
			fn = 0

	else:
		if len_ne > 0:
			tp = 1
			tn = len_n / len_ne
			fp = (len_i - len(i.intersection(re))) / len_ne
			fn = 0
		else:
			tp = 1
			tn = 1
			fp = 0
			fn = 0

	return tp, tn, fp, fn

def get_agent_from_agents(name, agents):
	for agent in agents:
		if agent.get_agent_name() == name:
			return agent
	return -1
	
def metric(agents_taf, agents_paf):
	TP = []
	TN = []
	FP = []
	FN = []
	
	for agent in agents_taf:
		agent_p = get_agent_from_agents(agent.get_agent_name(), agents_paf)
		tp, tn, fp, fn = metric1(agent, agent_p)
		TP.append(tp)
		TN.append(tn)
		FP.append(fp)
		FN.append(fn)
	
	return np.mean(TP), np.mean(TN), np.mean(FP), np.mean(FN)
	
	
def metric_bullshit(agents_paf, taf_plus):
	taf_plus_acceptable_arguments_labels = taf_plus.get_acceptable_arguments()

	bullshit = []

	for agent_paf in agents_paf:
		agent_paf_acceptable_arguments_labels = agent_paf.get_acceptable_arguments()
		if len(agent_paf_acceptable_arguments_labels) > 0:
			normalization_factor = len(agent_paf_acceptable_arguments_labels)
			acc_in_paf_but_not_in_taf_plus = len(agent_paf_acceptable_arguments_labels.difference(taf_plus_acceptable_arguments_labels))
			len_bullshit = float(acc_in_paf_but_not_in_taf_plus / normalization_factor)
		else:
			len_bullshit = 0

		bullshit.append(len_bullshit)

	mean_bullshit = np.mean(bullshit)
	std_bullshit = np.std(bullshit)

	return mean_bullshit, std_bullshit

def metric_global_wrongfully_cautious(agents_paf, taf_plus):
	taf_plus_acceptable_arguments_labels = taf_plus.get_acceptable_arguments()

	global_wrongfully_cautious = []

	for agent_paf in agents_paf:
		agent_paf_acceptable_arguments_labels = agent_paf.get_acceptable_arguments()
		if len(agent_paf_acceptable_arguments_labels) > 0:
			normalization_factor = len(taf_plus_acceptable_arguments_labels)
			taf_plus_self = set()
			for element in taf_plus_acceptable_arguments_labels:
				if agent_paf.name in element:
					taf_plus_self.add(element)
			acc_in_taf_plus_but_not_in_paf = len(taf_plus_self.difference(agent_paf_acceptable_arguments_labels))
			len_gwc = float(acc_in_taf_plus_but_not_in_paf / normalization_factor)
		else:
			len_gwc = 0

		global_wrongfully_cautious.append(len_gwc)

	mean_gwc = np.mean(global_wrongfully_cautious)
	std_gwc	 = np.std(global_wrongfully_cautious)

	return mean_gwc , std_gwc

def metric_local_wrongfully_cautious(agents_paf, agents_taf):
	agents_paf = list(agents_paf)
	agents_taf = list(agents_taf)
	
	agents_number = len(agents_paf)

	local_wrongfully_cautious = []
	#print(len(agents_paf), len(agents_taf), "????")
	for i in range(agents_number):
		agent_paf_acceptable_arguments = agents_paf[i].get_acceptable_arguments()
		agent_taf_acceptable_arguments = agents_taf[i].get_acceptable_arguments()
		if len(agent_taf_acceptable_arguments) > 0:
			normalization_factor = len(agent_taf_acceptable_arguments)
			acc_in_taf_but_not_in_paf = len(agent_taf_acceptable_arguments.difference(agent_paf_acceptable_arguments))
			len_lwc = float(acc_in_taf_but_not_in_paf / normalization_factor)
		else:
			len_lwc = 0

		local_wrongfully_cautious.append(len_lwc)

	
	mean_lwc = np.mean(local_wrongfully_cautious)
	std_lwc	 = np.std(local_wrongfully_cautious)

	return mean_lwc , std_lwc

