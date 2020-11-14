#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def OptionsArgueV(agent, currentOffer, arg): # revisado
        # Accept(S)
        r1 = agent.negociation.acceptS.preConditions(arg) # Retorna True o False
        # Challenge(y)
        r2 = agent.negociation.challengeY.preConditions(arg) # Retorna True (siempre se cumple)
        # Argue
        r3 = agent.negociation.argue.preConditions(currentOffer, True) # Retorna res o False
        #print(r3, "eee")
        possibleReplay = []
        
        if r1 == True:
            possibleReplay.append(1)
        
        if r2 == True:
            possibleReplay.append(2)
        
        if r3 != False:
            possibleReplay.append(3)
           
        if len(possibleReplay) > 0:
            r = np.random.choice(possibleReplay, 1)[0]
            if r==3:
                r=r3
            return (True, r)
        else:
            return (False, -1)
        

            
def OptionsArgue(agent, currentOffer, arg, r):
        if r == 1:
            agent.negociation.acceptS.postConditions(arg)
            ##print("--Pre-Conditions: S is acceptable for", agent.name)
            ##print("--Post-Conditions: CS.A_t (", agent.name, ") = CS.A_t−1 (", agent.name, ") U S")
            return "AcceptS"
            
        elif r == 2:
            agent.negociation.challengeY.postConditions(arg)
            ##print("--Pre-Conditions: there is no condition.")
            ##print("--Post-Conditions: CS.C_t(", agent.name, ") = CS.C_t−1(", agent.name, ") U {y}")
            return "ChallengeY"
            
        else:
            if r != False:
                agent.negociation.argue.postConditions(currentOffer, True, r)
                ##print("--Pre-Conditions:", r3.S, r3.C, r3.x, "is acceptable for", agent.name)
                ##print("--Post-Conditions: CS.A_t(", agent.name, ") = CS.A_t−1(", agent.name, ")U", r3.S, r3.C, r3.x)
                return r
            else:
                agent.cs.SN.append(True)
                ##print("--Pre-Conditions:", agent.name, "has no argument to present")
                ##print("--Post-Conditions: none")
                return "SayNothing"

