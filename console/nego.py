#!/usr/bin/env python
# -*- coding: utf-8 -*-

import agentPaf as agent
import numpy as np
import arguments as ar
import numpy as np
from scipy import stats

import moveOffer as mo
import moveAcceptX as ax
import moveAcceptS as acs
import moveRefuse as ref
import moveArgue as ma
import moveChallenge as mcc

class N: # Negociation
    def __init__(self):
        self.dialogues = []
    def add_Dialogue(self, D):
        self.dialogues.append(D)

class D: # Dialogue
    def __init__(self):
        self.wfMoves = []

    def add_wfMove(self, M):
        self.wfMoves.append(M)

class M: # Well-founded move, M_k = <S_k , H_k , Move_k>
    def __init__(self, S, H, Move, act):
        self.S = S # agent which plays the move
        self.H = H # set of agents to which the move is addressed
        self.Move = Move # is the uttered move
        self.moveAct = act

#######################################################################

# Return the agent which plays the move
def Speaker(WellFoundedMove):
    return WellFoundedMove.S

# Return the set of agents to which the move is addressed 
def Hearer(WellFoundedMove):
    return WellFoundedMove.H

# Create well-founded move
def createMove(S, H, Move, actStr):
    Mv = M(S, H, Move, actStr)
    return Mv
##########################################################
# Evaluate dialogue result -- reglas de terminación
def Result(dialogue, agents, xCurrent):
    lst = []
    l = len(dialogue.wfMoves)
    for agent in agents:
        if xCurrent in agent.cs.S:
            lst.append(True)
        else:
            lst.append(False)
    if all(lst):
        return "Success"

    count = 0
    for ag in agents: 
        if True in ag.cs.SN:
            count+=1
                 
    count1 = 0
    for ag in agents:
        if ag.name != dialogue.wfMoves[0].S.name:
            #if xCurrent == ag.candidatesDecisionPrefOrder()[1][0]:
            if ag.compAltAcc(xCurrent)==True:
                count1+=1
    la = len(agents)
    if count==la and count1==la-1:
        return "Success"
    elif count==la and count1!=la-1:
        return "Failure"

    return None

######################################################


    
# Dados los agentes y alternativas, genara un listado de los agentes que empezarán cada ronda de diálogo Di en la negociación N
def firstTurns(agents, X):
    la = len(agents)
    lx = len(X)
    fraccion = lx / la
    resto = lx % la
    turns = []
    ag = []
    
    ag = list(agents)
    
    # ordenamiento aleatorio
    np.random.shuffle(ag)
    """
    for agent in agents:
        if agent.name == "Mary":
            m = agent
        elif agent.name == "Peter":
            p = agent
        elif agent.name == "John":
            j = agent
    ag = [m, j, p]
    """
    
    if fraccion == 1: # num(X) == num(agents)
        return ag
    if fraccion > 1: # num(X) > num(agents)
        count = 0
        fraccion = lx // la
        while count < fraccion:
            for agent in ag:
                turns.append(agent)
            count += 1
        for i in range(0, resto):
            turns.append(ag[i])
        return turns
    if fraccion < 1: # num(X) < num(agents)
        for i in range(0, lx):
            turns.append(ag[i])
        return turns

######################################################################
# prepara y ejecuta el primer move M0 del dialogo D
def firstMove(agents, agSp, Dialogue, alternativasRestantes):
    argsCON = set()
    for ag in agents.difference({agSp}):
        s = ag.get_Acc_CON_X()
        for ss in s:
            argsCON.add(ss)

    offer = agSp.negociation.offer.preConditions(argsCON, alternativasRestantes, False) # pongo True si quiero info de los agentes
    # creo move
    M0 = createMove(agSp, agents.difference({agSp}), offer, "Offer")
    
    ##print("--Preferred:", agSp.candidatesDecisionPrefOrder()[1][0], agSp.candidatesDecisionPrefOrder()[0])
    ##print(M0.S.name, M0.moveAct, M0.Move, "; Agent N° 0")
    
    # añado move
    Dialogue.add_wfMove(M0)
    # postconditions
    agSp.negociation.offer.postConditions(offer)
    
    return agSp
    
# dado un dialogo D, retorna un posible move para agregar
def findLastMove(Dialogue, agents, turnAg):
    l = len(agents)
    dm = len(Dialogue.wfMoves)
    a = 1
    validMoves = []
    
    count = 0
    
    turnAg.cs.M = []
    
    for e in Dialogue.wfMoves:
        if a != turnAg.name and e.moveAct != "SayNothing": # si el move M no es una respuesta a si mismo
            if existLeastOneTrue(e, e.Move, turnAg, e.S) == True:
                turnAg.cs.M.append(1)
                validMoves.append(e)
            else:
                turnAg.cs.M.append(0)
                
    if len(validMoves)>0:
        m = np.random.choice(validMoves, 1)[0]
        return m
    
    else:           
        ##print("All False Move")
        return None
               
                
# Dado un move M, retorna True si al menos hay una posible respuesta (un move de respuesta) True  
def existLeastOneTrue(move, currentOffer, agent, offertAgent):
     if move.moveAct == "Offer":
        if mo.repliesToOfferV(agent, currentOffer) == True:
            return True
        else:
            return False
            
     if move.moveAct == "AcceptX":
        if ax.OptionsAcceptXV(agent, currentOffer, offertAgent) == True:
            return True
        else:
            return False
            
     if move.moveAct == "AcceptS":
        if acs.OptionsAcceptSV(agent, currentOffer, move.Move, offertAgent, move.Move) == True:
            return True
        else:
            return False
            
     if move.moveAct == "Argue":
        if ma.OptionsArgueV(agent, currentOffer, move.Move, offertAgent) == True:
            return True
        else:
            return False
            
     if move.moveAct == "RefuseX":
        if ref.OptionsRefuseV(agent, currentOffer, offertAgent) == True:
            return True
        else:
            return False
            
     if move.moveAct == "ChallengeX":
        if mcc.OptionsChallengeXV(agent, currentOffer, offertAgent) == True:
            return True
        else:
            return False
     
     if move.moveAct == "ChallengeY":
        if mcc.OptionsChallengeYV(agent, currentOffer, offertAgent, True) == True:
            return True
        else:
            return False

############################################################################


def negociation(agents, X):
    neg = N() # instancia de negociacion
    Xcurrent = list(X) # comienzo con todas las alternativas
    turnsDialogues = firstTurns(agents, X) # lista de los agentes que comenzaran un dialogo nuevo durante la negociacion
    count = 0
    agreement = False
    option = -1
    F = 0
    
    laa = len(agents)
    
    while len(Xcurrent) > 0 and agreement == False and count < laa: # en cada iteracion empieza un dialogo nuevo
        ##print("####################")
        ##print("### DIALOGUE N°", count+1)
        ##print("####################")
        Dialogue = D() # dialogo vacio
        agSp = turnsDialogues[count] # este agente inicia el dialogo
        listAg = [agSp]
        l = agents.difference({agSp})
        # ordenamiento aleatorio
        np.random.shuffle(list(l))
        
        for ag in l:
            listAg.append(ag)

        ##for e in listAg:
        ##    print("###", e.name)
        ##print(agSp, type(agSp))
        agSp = firstMove(agents, agSp, Dialogue, Xcurrent) # primer move
        listAg[0] = agSp
 
        ###
        ##for ag in listAg:
        ##    print(ag.name)
        ##    for e in ag._Agent__accArgs:
        ##        if isinstance(e, ar.ArgPRO):
        ##            print(e.S, e.C, e.x, "pro")
        ##        if isinstance(e, ar.ArgCON):
        ##            print(e.S, e.C, e.x, "con")
                    
        status = True # para que ocurran nuevos moves en el dialogo
        j = 1
        
        while status == True:
            # itero para cada agente
            turnAg = listAg[j]
            # creo move
            nm = newMove(turnAg, Dialogue, listAg)
            
            listAg = nm[1]
            
            ##if nm[0].moveAct == "Argue" or nm[0].moveAct == "AcceptS":
            ##    print(nm[0].S.name, nm[0].moveAct, "(", nm[0].Move.S, nm[0].Move.C, nm[0].Move.x, ")", j)
            ##else:
            ##    print(nm[0].S.name, nm[0].moveAct, nm[0].Move, "; Agent N°", j)
                
            
            ####################### TABLITA ##################
            for ag in listAg:
                ch = False
                sn = False
                
                if Dialogue.wfMoves[0].Move in ag.cs.C:
                    ch = True
                if True in ag.cs.SN:
                    sn = True
                    
                ##print("### ", ag.name, "ACCEPTX", ag.cs.S, "CHALLENGEX", ch, "REFUSE", len(ag.cs.R), "SAYNOTHING", sn)
                
            # evaluo si D == Success o D == Failure
            result = Result(Dialogue, agents, Dialogue.wfMoves[0].Move) # Dialogue.wfMoves[0].Move es offer
            
            # añado D a instancia Negociacion si D == Success o D == Failure
            if result == "Success" or result == "Failure":
            
                
                ##print("\n### Result(Dialogue) =", result, "\n") # imprimo resultado del dialogo D
                
                neg.add_Dialogue(Dialogue) # añado D a instancia negociacion neg
                status = False # cierro la iteración while
                count += 1 # para que sea el turno de otro agente de empezar el siguiente dialogo D
                
                for agent in listAg: # vacio commitment stores cs excepto componente de argumentos (así dice el paper)
                        agent.cs.S = []
                        agent.cs.A = [] # Componente argumentos A, no la vacío
                        agent.cs.C = []
                        agent.cs.SN = []
                        ##print(agent.name)
                        ##for m in agent._Agent__accArgs:
                        ##    if isinstance(m, ar.ArgPRO):
                        ##        print(m.S, m.C, m.x, "PRO", min(m.argPROStrength()))
                        ##    elif isinstance(m, ar.ArgCON):
                        ##        print(m.S, m.C, m.x, "CON", max(m.argCONWeakness()))
                        ##    else:
                        ##        print(m.H, m.h, "Ep")
                        
                        
                        
                        
                Xcurrent.remove(Dialogue.wfMoves[0].Move) #remuevo alternativa para que no se empiece un D con la misma
                
                #if Dialogue.wfMoves[len(Dialogue.wfMoves)-1].moveAct == "Withdraw":
                    # se termina la negociacion y vacio commitment stores cs totalmente
                #    for agent in agents:
                #        agent.cs.S = []
                #        agent.cs.A = []
                #        agent.cs.C = []
                #    return [neg, agreement] # retorno objeto negociacion neg y agreement == False
                
                if result == "Success": # si en particular D == succcess
                    option = Dialogue.wfMoves[0].Move # guardo alternativa "ganadora"
                    agreement = True # cambio estado de agreement a True
                    
            #agente siguiente para un nuevo move
            if j == laa - 1:
                j = 0
            else:
                j += 1
                

    r = 0
    if agreement == False:
        r = "NOT AGREEMENT"
    else:
        r = "AGREEMENT"
        
    ##print("##########################################")
    ##print("### NEGOCIATION RESULT:", r)
    ##print("##########################################")
    
    s=""
    for element in turnsDialogues:
        if element.name == "Ag1":
            s = s+"Ag1"
        if element.name == "Ag2":
            s = s+"Ag2"
        if element.name == "Ag3":
            s = s+"Ag3"
        
    return [neg, agreement, option, s, neg.dialogues[0].wfMoves[0].Move] # retorno la negociación (con diálogos) y si se alcanzó o no un acuerdo
        
#####################################################



def addArg(agents, turnAg, res):
    for ag in agents:
        if ag.name != turnAg.name:
            if res.t == "P" or res.t == "C":
                res.__G = ag._Agent__G
                if res not in ag._Agent__Ap:
                    ag._Agent__Ap.add(res)
                    if ag.numAttacksToProcessByTurn > 0: #(si es Paf, distorciono)
                        Ae = ag._Agent__Ae

                        # selecciono args aleatoriamente 
                        # determino ataque o no ataque
                        # el resto intedeterminado

                        # a los argumentos epistémicos les asocio un índice
                        lst = []
                        for i in range(len(Ae)):
                            lst.append(i)

                        if len(lst) > ag.numAttacksToProcessByTurn:
                            y = np.random.choice(lst, ag.numAttacksToProcessByTurn)
                        else:
                            y = lst

                        count=0
                        Det = set() # Ae de argumentos bien determinados

                        for e in Ae:
                            if count in y: # lista de índices de algunos Ae
                                Det.add(e)
                            count+=1
                        # los guardo a los correctos en los set correspondientes
                        for e in Det:
                            if agent.is_stronglyAttacked(res, e)==True:
                                ag.R.add((e, res))
                                ag.Re.add((e, res))
                            else:
                                ag.N.add((e, res))
                                ag.Ne.add((e, res))
                        # ver si es atacado o no y añadirlo a R o N
                        # para todos los arg en Ae que no estan en R o N añadir a I
                        for k in Ae:
                            if (k, res) not in ag.R and (k, res) not in ag.N:
                                ag.I.add((k, res))
                                if agent.is_stronglyAttacked(res, k)==True:
                                    ag.Re.add((e, res))
                                else:
                                    ag.Ne.add((e, res))

                    for e in res.S:
                        ag._Agent__K.add(e)
                if ag.argExtIsAcceptable(res) == True:
                    ag._Agent__accArgs.add(res)
                    ag.cs.A.append(res)
    return agents
                          
                                
def newMove(turnAg, Dialogue, agents):
    lastMoveAdded = findLastMove(Dialogue, agents, turnAg) # 1 move
    ##print("\n--The following move is a reply to the move:", lastMoveAdded.moveAct)
    current = Dialogue.wfMoves[0].Move # oferta actual
    offertAgent = Dialogue.wfMoves[0].S # agente que ofertó primero

    dif = []
    
    for a in agents:
        if a != turnAg:
            dif.append(a)
        
    
    if lastMoveAdded.moveAct == "Offer":
        res = mo.repliesToOffer(turnAg, lastMoveAdded.Move)
        if res != "SayNothing":
            Mi = createMove(turnAg, dif, lastMoveAdded.Move, res)
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg 
            return [Mi, agents]        
        else:
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg    
            return [Mi, agents] # retono move agregado

    if lastMoveAdded.moveAct == "ChallengeX":
        #res = repliesToChallengeX(turnAg, lastMoveAdded.Move, offertAgent)
        res = repliesToChallengeX(turnAg, current, offertAgent)
        if res == "SayNothing":
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg
            return [Mi, agents]
        else:
            Mi = createMove(turnAg, dif, res, "Argue")
            Dialogue.add_wfMove(Mi)
           
            agents = addArg(agents, turnAg, res)
            
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg
            
            return [Mi, agents]


    if lastMoveAdded.moveAct == "Argue":
        res = repliesToArgue(turnAg, current, lastMoveAdded.Move, offertAgent)
        if res == "SayNothing":
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg  
            return [Mi, agents]
            
        elif res == "ChallengeY" or res == "AcceptS":
            if res == "ChallengeY": 
                Mi = createMove(turnAg, dif, lastMoveAdded.Move, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg  
                return [Mi, agents]
            else:
                Mi = createMove(turnAg, dif, lastMoveAdded.Move, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg  
                return [Mi, agents]
                        
        else:
            Mi = createMove(turnAg, dif, res, "Argue")
            agents = addArg(agents, turnAg, res)
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg
                
            return [Mi, agents]

    if lastMoveAdded.moveAct == "RefuseX":
        res = repliesToRefuse(turnAg, current, offertAgent)
        if res == "SayNothing":
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg   
            return [Mi, agents]
        else:
            if res != "AcceptX" and res != "ChallengeX" and res!= "Withdraw" and res != "SayNothing":
                Mi = createMove(turnAg, dif, res, "Argue")
                agents = addArg(agents, turnAg, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg
                return [Mi, agents]
                
            else:
                Mi = createMove(turnAg, dif, lastMoveAdded.Move, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg  
                return [Mi, agents]

    if lastMoveAdded.moveAct == "AcceptS":
        res = repliesToAcceptS(turnAg, current, lastMoveAdded.Move, offertAgent, lastMoveAdded.Move)
        
        if res == "SayNothing":
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg
            return [Mi, agents]
        else:
            if res == "ChallengeY": 
                Mi = createMove(turnAg, dif, lastMoveAdded.Move, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg
                return [Mi, agents]
            else:
                if res != "AcceptX" and res!= "ChallengeY" and res != "Withdraw":
                    Mi = createMove(turnAg, dif, res, "Argue")
                    agents = addArg(agents, turnAg, res)
                    Dialogue.add_wfMove(Mi)
                    for ag in agents:
                        if ag.name == turnAg.name:
                            ag = turnAg
                    return [Mi, agents]
                else:
                     if res == "AcceptX":
                        Mi = createMove(turnAg, dif, current, res)
                        Dialogue.add_wfMove(Mi)
                        for ag in agents:
                            if ag.name == turnAg.name:
                                ag = turnAg
                        return [Mi, agents]
                     else:
                        Mi = createMove(turnAg, dif, lastMoveAdded.Move, res) 
                        
                        Dialogue.add_wfMove(Mi)
                        for ag in agents:
                            if ag.name == turnAg.name:
                                ag = turnAg
                        return [Mi, agents]


    if lastMoveAdded.moveAct == "ChallengeY":
        neg = True
        res = repliesToChallengeY(turnAg, current, offertAgent, neg)
        if res == "SayNothing":
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg
                
            return [Mi, agents]
        else:
            Mi = createMove(turnAg, dif, res, "Argue")
            Dialogue.add_wfMove(Mi)
           
            agents = addArg(agents, turnAg, res)

            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg
                
            return [Mi, agents]

    if lastMoveAdded.moveAct == "AcceptX":
        res = repliesToAcceptX(turnAg, lastMoveAdded.Move, offertAgent)
        
        if res == "SayNothing":
            Mi = createMove(turnAg, dif, "SayNothing", "SayNothing")
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg 
            return [Mi, agents]
            
        elif res != "Withdraw" and res!= "ChallengeY" and res!="AcceptX":
            Mi = createMove(turnAg, dif, res, "Argue")
            agents = addArg(agents, turnAg, res)
            Dialogue.add_wfMove(Mi)
            for ag in agents:
                if ag.name == turnAg.name:
                    ag = turnAg    
            return [Mi, agents]
        else:
            if res == "ChallengeY":
                Mi = createMove(turnAg,dif, lastMoveAdded.moveAct+lastMoveAdded.Move, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg
                return [Mi, agents]
            else:
                Mi = createMove(turnAg, dif, lastMoveAdded.Move, res)
                Dialogue.add_wfMove(Mi)
                for ag in agents:
                    if ag.name == turnAg.name:
                        ag = turnAg   
                return [Mi, agents]
        
###############################################################################
def repliesToAcceptX(agent, currentOffer, offertAgent):
    return ax.OptionsAcceptX(agent, currentOffer, offertAgent)

def repliesToAcceptS(agent, currentOffer, y, offertAgent, arg):
    return acs.OptionsAcceptS(agent, currentOffer, y, offertAgent, arg)

def repliesToChallengeY(agent, currentOffer, offertAgent, neg):
    return mcc.OptionsChallengeY(agent, currentOffer, offertAgent, neg)

def repliesToRefuse(agent, currentOffer, offertAgent):
    return ref.OptionsRefuse(agent, currentOffer, offertAgent)

def repliesToArgue(agent, currentOffer, arg, offertAgent):
    return ma.OptionsArgue(agent, currentOffer, arg, offertAgent)

def repliesToChallengeX(agent, currentOffer, offertAgent):
    return mcc.OptionsChallengeX(agent, currentOffer, offertAgent)

