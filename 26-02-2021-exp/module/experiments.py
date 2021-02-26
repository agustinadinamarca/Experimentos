
from module.synthetic import *
from module.negotiation import *
from module.metrics import *

from numpy import mean
from time import perf_counter

import copy

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


def set_synthetic_experiment_taf_agents(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value):
	taf_agents = create_agents(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value)
	return taf_agents

def get_taf_plus_agent(taf_agents_initial):
	taf_plus = get_major_agent_from_agents(taf_agents_initial)
	return taf_plus

def execute_negotiations_with_taf_agents(N, taf_agents):
	
	taf_agents_original = copy.deepcopy(taf_agents) # BORRAR
	X = -1
	for agent in taf_agents:
		X = agent.get_alternatives()
	
	lst = [] # almacena las alternativas ganadoras de cada agreement
	times = []

	print("Start", N, "negotiations with", len(taf_agents), "TAFs agents...")
		
	for i in range(N):
		t0 = perf_counter() # tiempo inicial
		#if are_equal_agents_sets(taf_agents, taf_agents_original):
		#	print("OK11")
		#print(len(taf_agents))
		result, taf_agents_final = negotiation(taf_agents, X) # [option, taf_agents_final]
		#print(len(taf_agents_final))
		#if are_equal_agents_sets(taf_agents, taf_agents_final) == False:
		#	print("OK22, intercambio")
		tf = perf_counter() # tiempo final
		
		#for ag in taf_agents:
		#	init = ag.get_all_arguments_structures()
		#	print(init, "\n")
		#	print(len(init))
		#print("taf_final")
		#for ag in taf_agents_final:
		#	f = ag.get_all_arguments_structures()
		#	print(f, "\n")
		#	print(len(f))
		if result != -1:
			lst.append(result)
			
		times.append(tf - t0) # duración de la negociación
		
		print("----- Progress:", int((i + 1) * 100 / N), "%" )
	
	print("End", N, "negotiations with", len(taf_agents), "TAFs agents...")
	mean_time_by_negotiation = mean(times)
	print("Average time by negotiation:", round(mean_time_by_negotiation, 3), "s")
	print("Total time", N, "negotiations:", round(sum(times), 3), "s") 
				
	agreements_number = len(lst) # cantidad de agreements
	optimal_agreements = set(lst) # set de soluciones óptimas

	return N, agreements_number, optimal_agreements, mean_time_by_negotiation, taf_agents_final
	
	
	
def save_taf_negotiation_results(name, N, agreements_number, optimal_agreements, mean_time_by_negotiation): 
	
	file_to_save = open(name, "w")
	file_to_save.write("TAFs Negotiations\n")
	file_to_save.write("Number of executions: "+ str(N) + "\n")
	file_to_save.write("Number of agreements: "+ str(agreements_number) + "\n")
	file_to_save.write("Optimal agreement: "+ str(optimal_agreements) + "\n")
	file_to_save.write("Average Time (1 execution):" + str(mean(mean_time_by_negotiation)) + "\n")
	
	file_to_save.close()
	
	
def save_synthetic_experiment_taf_agents(name, taf_agents):
	file_to_save = open(name, "w")
	file_to_save.write(str(len(taf_agents)) + "\n")
	file_to_save.write("Name\n")
	
	for ag in taf_agents:
		file_to_save.write(str(ag.name) + "\n")
		#file_to_save.write("Goals\n ")
		#for g in ag._Agent__G: 
		#	file_to_save.write(str(g[0])+" "+str(g[1])+"\n")

		file_to_save.write("Alternatives\n")
		X = ag.get_alternatives()
		
		for x in X:
			file_to_save.write(str(x) + " ")

		file_to_save.write("\nCandidates decisions preferred order\n")
		file_to_save.write(str(ag.candidate_decisions_descending_order_of_preference())+"\n")
		
		file_to_save.write("Practical Arguments\n")
		pab = ag.get_practical_base_structures()
		
		for e in pab:
			file_to_save.write(e[0]+" "+e[1]+" "+e[2]+" "+str(round(e[4], 2))+" ")
			for k in e[3]:
				file_to_save.write(k)
				file_to_save.write(" ")
			file_to_save.write("\n")
									
		file_to_save.write("Epistemic Arguments\n")
		eab = ag.get_epistemic_base_structures()
		
		for e in eab:
			file_to_save.write(e[0]+" ")
			for k in e[1]:
				file_to_save.write(k)
				file_to_save.write(" ")
			file_to_save.write("\n")

		file_to_save.write("Name\n")
	 
	file_to_save.close()
	

def get_number_semantics_r(semantics_list):
	count = 0
	for i in semantics_list:
		if i == True:
			count += 1
	return count

def get_alternatives_from_agents(agents):
	for ag in agents:
		return ag.get_alternatives()

def pafs_negotiations(fname, number_agents, step, M, taf_agents, resource_boundness_density, taf_agents_final):
	
	data_to_save = open(fname, "w")
	data_to_save.write("Argumentation Problem")
	data_to_save.write("Decision-Making Algorithm\n")
	# nombres de las columnas
	data_to_save.write("num_agents_R num_agents_RI res_boundeness time_neg_mean time_neg_std FP_mean FP_std FN_mean FN_std TP_mean TP_std TN_mean TN_std bullshit_mean bullshit_std gwc_mean gwc_std lwc_mean lwc_std\n")
	#data_to_save.close()
	
	taf_plus = get_major_agent_from_agents(taf_agents)
	
	sc = get_semantics_configurations(number_agents)
	
	ssc = get_sample_semantics_configurations(number_agents, step, sc)
	taf_agents_original = copy.deepcopy(taf_agents) # borrar
	X = get_alternatives_from_agents(taf_agents)
	
	print("\nStart", len(ssc) * M, "negotiations with", number_agents, "PAFs agents...")
	count = 0
	for semantics_list in ssc:
		count += 1
		FP = []
		FN = []
		TP = []
		TN = []
		
		Bullshit = []
		GWC = []
		LWC = []
		
		time = []
		
		for i in range(M):
			np.random.shuffle(semantics_list)
			# comparar siempre taf_agents con su original
			#if are_equal_agents_sets(taf_agents_original, taf_agents) == True:
			#	print("OK1")
			paf_agents = create_paf_agents(taf_agents, resource_boundness_density, semantics_list)
			#if are_equal_agents_sets(paf_agents, taf_agents) != True:
			#	print("OK2, modificacion")
			# paf y taf distintos
			t0 = perf_counter() # tiempo inicial
			
			result, paf_agents_final = negotiation(set(paf_agents), X)
			#if are_equal_agents_sets(paf_agents_final, paf_agents) != True:
			#	print("OK3, intercambio", len(paf_agents_final), len(paf_agents))
			#print(len(paf_agents_final), len(paf_agents))
			# paf con paf final
			tf = perf_counter() # tiempo final
				  
			time.append(tf - t0)
			
			mean_bullshit, std_bullshit = metric_bullshit(paf_agents_final, taf_plus)
			mean_gwc, std_gwc = metric_global_wrongfully_cautious(paf_agents_final, taf_plus)
			mean_lwc, std_lwc = metric_local_wrongfully_cautious(paf_agents_final, taf_agents_final)
			tp, tn, fp, fn = metric(taf_agents_final, paf_agents_final)
			
			FP.append(fp)
			FN.append(fn)
			TP.append(tp)
			TN.append(tn)
			Bullshit.append(mean_bullshit)
			GWC.append(mean_gwc)
			LWC.append(mean_lwc)
			print("----- Progress:", count, "of", len(ssc), ": ", int((i + 1) * 100 / M), "%" )
		
		# info a guardar
		num_agents_R = get_number_semantics_r(semantics_list)
		num_agents_RI = number_agents - num_agents_R
		time_neg_mean = np.mean(time)
		time_neg_std = np.std(time)
		FP_mean = np.mean(FP)
		FP_std = np.std(FP)
		FN_mean = np.mean(FN)
		FN_std = np.std(FN)
		TP_mean = np.mean(TP)
		TP_std = np.std(TP)
		TN_mean = np.mean(TN)
		TN_std = np.std(TN)
		bullshit_mean = np.mean(Bullshit)
		bullshit_std = np.std(Bullshit)
		gwc_mean = np.mean(GWC)
		gwc_std = np.std(GWC)
		lwc_mean = np.mean(LWC)
		lwc_std = np.std(LWC)
		
		data_to_save.write(str(num_agents_R) + " ")
		data_to_save.write(str(num_agents_RI) + " ")
		data_to_save.write(str(resource_boundness_density) + " ")
		data_to_save.write(str(time_neg_mean) + " ")
		data_to_save.write(str(time_neg_std) + " ")
		data_to_save.write(str(FP_mean) + " ")
		data_to_save.write(str(FP_std) + " ")
		data_to_save.write(str(FN_mean) + " ")
		data_to_save.write(str(FN_std) + " ")
		data_to_save.write(str(TP_mean) + " ")
		data_to_save.write(str(TP_std) + " ")
		data_to_save.write(str(TN_mean) + " ")
		data_to_save.write(str(TN_std) + " ")
		
		data_to_save.write(str(bullshit_mean) + " ")
		data_to_save.write(str(bullshit_std) + " ")
		data_to_save.write(str(gwc_mean) + " ")
		data_to_save.write(str(gwc_std) + " ")
		data_to_save.write(str(lwc_mean) + " ")
		data_to_save.write(str(lwc_std) + "\n")

	data_to_save.close()
	
	print("End", len(ssc) * M, "negotiations with", number_agents, "PAFs agents...")
	
def get_semantics_configurations(number_agents):
	semantics_set = []
	
	for i in range(0, number_agents + 1):
		S = []
		if i == 0:
			for j in range(number_agents):
				S.append(False)
			semantics_set.append(S)
		else:
			for w in range(i):
				S.append(True)
				
			for k in range(i, number_agents):
				S.append(False)
				
			semantics_set.append(S)
	
	return semantics_set
	
	
def get_sample_semantics_configurations(number_agents, step, semantics_configurations):
	sample = []
	for i in range(0, len(semantics_configurations), step):
		sample.append(semantics_configurations[i])
		
	if semantics_configurations[len(semantics_configurations) - 1] not in sample:
		sample.append(semantics_configurations[len(semantics_configurations) - 1])
	
	return sample
