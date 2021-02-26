#!/bin/bash

# ESTO SIGNIFICAN LOS VALORES DE LOS PARÉNTESIS EN p1, p2 ,etc
# (number_agents, alternatives_number, maximum_number_practical_arguments, maximum_number_epistemic_arguments, maximum_attacks_density_value, N, M, step, resource_boundness_density)

#number_agents --> numero de agentes en la negociacion. Ej. 10
#alternatives_number --> numero de alternativas en la negociacion. Ej. 3
#maximum_number_practical_arguments --> numero maximo de argumentos practicos por agente. Ej. 10
#maximum_number_epistemic_arguments --> numero maximo de argumentos epistemicos por agente. Ej. 3
#maximum_attacks_density_value --> valor de densidad de ataques máximo por agente. EJ. 0.4
#N --> numero de iteraciones de la negociación con TAFs y PAFs). Ej. 50
#step --> pasos para muestrear la proporcion de agentes negociadores con semánticas R y RI. Ej. 2 (STEP DEBE SER MENOR AL NÚMERO DE AGENTES!)
#resource_boundness_density --> densidad de resource boundness por agente. Ej. 0.3


# ACA DECLARO DISTINTAS CONFIGURACIONES DE EXPERIMENTOS: p1, p2, p3, etc (¡EL CARACTER # REPRESENTA LINEAS COMENTADAS!)
declare -a p1=(6 3 6 3 0.25 20 2 0.25) # EXPERIMENTO 1
declare -a p2=(6 3 6 3 0.25 30 2 0.50) # EXPERIMENTO 2
declare -a p3=(6 3 6 3 0.25 30 2 0.75) # EXPERIMENTO 3

declare -a p4=(6 3 6 3 0.50 30 2 0.25) # EXPERIMENTO 1
declare -a p5=(6 3 6 3 0.50 30 2 0.50) # EXPERIMENTO 2
declare -a p6=(6 3 6 3 0.50 30 2 0.75) # EXPERIMENTO 3

declare -a p7=(6 3 6 3 0.75 30 2 0.25) # EXPERIMENTO 1
declare -a p8=(6 3 6 3 0.75 30 2 0.50) # EXPERIMENTO 2
declare -a p9=(6 3 6 3 0.75 30 2 0.75) # EXPERIMENTO 3

# EJECUTO LOS EXPERIMENTOS (¡EL CARACTER # REPRESENTA LINEAS COMENTADAS!)
python3 main.py "${p1[0]}" "${p1[1]}" "${p1[2]}" "${p1[3]}" "${p1[4]}" "${p1[5]}" "${p1[6]}" "${p1[7]}" "${p1[8]}" &
python3 main.py "${p2[0]}" "${p2[1]}" "${p2[2]}" "${p2[3]}" "${p2[4]}" "${p2[5]}" "${p2[6]}" "${p2[7]}" "${p2[8]}" &
python3 main.py "${p3[0]}" "${p3[1]}" "${p3[2]}" "${p3[3]}" "${p3[4]}" "${p3[5]}" "${p3[6]}" "${p3[7]}" "${p3[8]}" &
python3 main.py "${p4[0]}" "${p4[1]}" "${p4[2]}" "${p4[3]}" "${p4[4]}" "${p4[5]}" "${p4[6]}" "${p4[7]}" "${p4[8]}" &
python3 main.py "${p5[0]}" "${p5[1]}" "${p5[2]}" "${p5[3]}" "${p5[4]}" "${p5[5]}" "${p5[6]}" "${p5[7]}" "${p5[8]}" &
python3 main.py "${p6[0]}" "${p6[1]}" "${p6[2]}" "${p6[3]}" "${p6[4]}" "${p6[5]}" "${p6[6]}" "${p6[7]}" "${p6[8]}" &
python3 main.py "${p7[0]}" "${p7[1]}" "${p7[2]}" "${p7[3]}" "${p7[4]}" "${p7[5]}" "${p7[6]}" "${p7[7]}" "${p7[8]}" &
python3 main.py "${p8[0]}" "${p8[1]}" "${p8[2]}" "${p8[3]}" "${p8[4]}" "${p8[5]}" "${p8[6]}" "${p8[7]}" "${p8[8]}" &
python3 main.py "${p9[0]}" "${p9[1]}" "${p9[2]}" "${p9[3]}" "${p9[4]}" "${p9[5]}" "${p9[6]}" "${p9[7]}" "${p9[8]}" &
wait
echo "All complete"



