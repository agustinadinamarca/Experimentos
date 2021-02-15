#!/bin/bash

# ESTO SIGNIFICAN LOS VALORES DE LOS PARÉNTESIS EN p1, p2 ,etc
# (number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, M, step, resource_boundness_densities)

#number_agents --> numero de agentes en la negociacion. Ej. 10
#alternatives_number --> numero de alternativas en la negociacion. Ej. 3
#maximum_number_practical_arguments --> numero maximo de argumentos practicos por agente. Ej. 10
#maximum_number_epistemic_arguments --> numero maximo de argumentos epistemicos por agente. Ej. 3
# maximum_attacks_density_value --> valor de densidad de ataques máximo por agente. EJ. 0.4
#N --> numero de iteraciones de la negociación con TAFs y PAFs). Ej. 50
#step --> pasos para muestrear la proporcion de agentes negociadores con semánticas R y RI. Ej. 2
#resource_boundness_densities --> lista de densidad de resource boundness por agente. Ej. [0.5, 0.3, 0.2]


# ACA DECLARO DISTINTAS CONFIGURACIONES DE EXPERIMENTOS: p1, p2, p3, etc (¡EL CARACTER # REPRESENTA LINEAS COMENTADAS!)
declare -a p1=(4 3 8 4 0.5 5 2 "[0.2, 0.4, 0.3, 0.6]") # EXPERIMENTO 1
#declare -a p2=(4 3 8 4 0.5 5 2 "[0.2, 0.4, 0.3, 0.6]") # EXPERIMENTO 2
#declare -a p3=(4 3 8 4 0.5 10 2 "[0.2, 0.4, 0.3, 0.6]") # EXPERIMENTO 3

# EJECUTO LOS EXPERIMENTOS (¡EL CARACTER # REPRESENTA LINEAS COMENTADAS!)
python3 main.py "${p1[0]}" "${p1[1]}" "${p1[2]}" "${p1[3]}" "${p1[4]}" "${p1[5]}" "${p1[6]}" "${p1[7]}" "${p1[8]}" #&
#python3 main.py "${p2[0]}" "${p2[1]}" "${p2[2]}" "${p2[3]}" "${p2[4]}" "${p2[5]}" "${p2[6]}" "${p2[7]}" "${p2[8]}" #&
#python3 main.py "${p3[0]}" "${p3[1]}" "${p3[2]}" "${p3[3]}" "${p3[4]}" "${p3[5]}" "${p3[6]}" "${p3[7]}" "${p3[8]}"
wait
 



