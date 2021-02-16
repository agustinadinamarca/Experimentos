#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from module.experiments_to_run import exp

number_agents = int(sys.argv[1])
alternatives_number = int(sys.argv[2])
maximum_number_practical_arguments = int(sys.argv[3])
maximum_number_epistemic_arguments = int(sys.argv[4])
maximum_attacks_density_value = float(sys.argv[5])
N = int(sys.argv[6])
step = int(sys.argv[7])
resource_boundness_density = float(sys.argv[8])

exp(number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, step, resource_boundness_density)
