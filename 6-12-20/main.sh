#!/bin/bash

# ESTO SIGNIFICAN LOS VALORES DE LOS PARÉNTESIS EN p1, p2 ,etc
# (numAg, N, M, val1, val2, numMaxGoals, numAlt, numMaxAp, numMaxEp, attacksDensity)
# numAg --> numero de agentes en la negociacion. Ej. 10
# N --> numero de iteraciones de la negociación con TAFs (NO PAFs). Ej. 50
# M --> numero de iteraciones de la negociación con PAFs (NO TAFs). Ej. 50
# val1 --> numero de ataques o no ataques a determinar con certeza inicialmente. Ej. [2] o [2, 4, 6], etc
# val2 --> numero de ataques o no ataques a determinar con certeza en los turnos. Ej. [2] o [2, 4, 6], etc
# numMaxGoals --> numero maximo de goals por agente. Ej. 2
# numAlt --> numero de alternativas en la negociacion. Ej. 3
# numMaxAp --> numero maximo de argumentos practicos por agente. Ej. 10
# numMaxEp --> numero maximo de argumentos epistemicos por agente. Ej. 3
# attacksDensity --> densidad de ataques por agente (0, 1). Ej. 0.7
# stepPropSem --> pasos para muestrear la proporcion de agentes negociadores con semánticas R y RI. Ej. 2

# ACA DECLARO DISTINTAS CONFIGURACIONES DE EXPERIMENTOS: p1, p2, p3, etc (¡EL CARACTER # REPRESENTA LINEAS COMENTADAS!)
declare -a p1=(20 50 50 "[5, 10]" "[1]" 2 3 6 2 0.8 1) # EXPERIMENTO 1
#declare -a p2=(20 50 50 "[5, 10]" "[2]" 2 3 10 4 0.5 1) # EXPERIMENTO 2
#declare -a p3=(20 50 50 "[8, 16]" "[2, 4]" 2 3 15 6 0.9 1) # EXPERIMENTO 3

#declare -a p4=(50 50 50 "[3, 5]" "[1]" 2 3 5 2 0.1 1) # EXPERIMENTO 1
#declare -a p5=(50 50 50 "[5, 10]" "[2]" 2 3 10 4 0.5 1) # EXPERIMENTO 2
#declare -a p6=(50 50 50 "[8, 16]" "[2, 4]" 2 3 15 6 0.9 1) # EXPERIMENTO 3

#declare -a p7=(100 50 50 "[3, 5]" "[1]" 2 3 5 2 0.1) # EXPERIMENTO 1
#declare -a p6=(100 50 50 "[5, 10]" "[2, 4]" 2 3 20 5 0.5 20) # EXPERIMENTO 2
#declare -a p7=(100 50 50 "[10, 20]" "[5, 8]" 2 3 30 10 0.9 20) # EXPERIMENTO 3
#declare -a p8=(100 50 50 "[5, 10]" "[2]" 2 3 10 4 0.5 20) # EXPERIMENTO 2
#declare -a p9=(100 50 50 "[8, 16]" "[2, 4]" 2 3 15 6 0.9 20) # EXPERIMENTO 3


# EJECUTO LOS EXPERIMENTOS (¡EL CARACTER # REPRESENTA LINEAS COMENTADAS!)
python3 exp.py "${p1[0]}" "${p1[1]}" "${p1[2]}" "${p1[3]}" "${p1[4]}" "${p1[5]}" "${p1[6]}" "${p1[7]}" "${p1[8]}" "${p1[9]}" "${p1[10]}" "${p1[11]}" &
#python3 exp.py "${p2[0]}" "${p2[1]}" "${p2[2]}" "${p2[3]}" "${p2[4]}" "${p2[5]}" "${p2[6]}" "${p2[7]}" "${p2[8]}" "${p2[9]}" "${p2[10]}" "${p2[11]}" &
#python3 exp.py "${p3[0]}" "${p3[1]}" "${p3[2]}" "${p3[3]}" "${p3[4]}" "${p3[5]}" "${p3[6]}" "${p3[7]}" "${p3[8]}" "${p3[9]}" "${p3[10]}" "${p3[11]}" &
#python3 exp.py "${p4[0]}" "${p4[1]}" "${p4[2]}" "${p4[3]}" "${p4[4]}" "${p4[5]}" "${p4[6]}" "${p4[7]}" "${p4[8]}" "${p4[9]}" "${p4[10]}" "${p4[11]}" &
#python3 exp.py "${p5[0]}" "${p5[1]}" "${p5[2]}" "${p5[3]}" "${p5[4]}" "${p5[5]}" "${p5[6]}" "${p5[7]}" "${p5[8]}" "${p5[9]}" "${p5[10]}" "${p5[11]}" &
#python3 exp.py "${p6[0]}" "${p6[1]}" "${p6[2]}" "${p6[3]}" "${p6[4]}" "${p6[5]}" "${p6[6]}" "${p6[7]}" "${p6[8]}" "${p6[9]}" "${p6[10]}" "${p6[11]}" &
#python3 exp.py "${p7[0]}" "${p7[1]}" "${p7[2]}" "${p7[3]}" "${p7[4]}" "${p7[5]}" "${p7[6]}" "${p7[7]}" "${p7[8]}" "${p7[9]}" "${p7[10]}" "${p7[11]}" &
#python3 exp.py "${p8[0]}" "${p8[1]}" "${p8[2]}" "${p8[3]}" "${p8[4]}" "${p8[5]}" "${p8[6]}" "${p8[7]}" "${p8[8]}" "${p8[9]}" "${p8[10]}" "${p8[11]}" &
#python3 exp.py "${p9[0]}" "${p9[1]}" "${p9[2]}" "${p9[3]}" "${p9[4]}" "${p9[5]}" "${p9[6]}" "${p9[7]}" "${p9[8]}" "${p9[9]}" "${p9[10]}" "${p9[11]}" &
wait
 



