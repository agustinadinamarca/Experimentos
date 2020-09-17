#!/usr/bin/env python
# -*- coding: utf-8 -*-

import agent as agent
import numpy as np
import arguments as ar

def OptionsArgueV(agent, currentOffer, arg, offertAgent): # revisado
        support = arg
        # Accept(S)
        r1 = agent.negociation.acceptS.preConditions(support) # Retorna True o False
        # Challenge(y)
        r2 = agent.negociation.challengeY.preConditions(support) # Retorna True (siempre se cumple)
        # Argue
        r3 = agent.negociation.argue.preConditions(currentOffer, True) # Retorna res o False
        
        if r1 == True or r2 == True or r3 != False:
            return True
        else:
            return False
            
def OptionsArgue(agent, currentOffer, arg, offertAgent):
        support = arg
        # Accept(S)
        r1 = agent.negociation.acceptS.preConditions(support) # Retorna True o False
        # Challenge(y)
        r2 = agent.negociation.challengeY.preConditions(support) # Retorna True (siempre se cumple)
        # Argue
        r3 = agent.negociation.argue.preConditions(currentOffer, True) # Retorna res o False
        
        ##if r3 != False:
        ##    print("--Possibilities:", r1, "(AcceptS),", r2, "(ChallengeY),", "True (Argue)")
        ##else:
        ##    print("--Possibilities:", r1, "(AcceptS),", r2, "(ChallengeY),", r3, "(Argue)")
        
        possibleReplay = []
        
        if r1 == True:
            possibleReplay.append("AcceptS")
        
        if r2 == True:
            possibleReplay.append("ChallengeY")
        
        if r3 != False:
            possibleReplay.append("Argue")
           
        r = np.random.choice(possibleReplay, 1)[0]
        
        if r == "AcceptS":
            agent.negociation.acceptS.postConditions(support)
            ##print("--Pre-Conditions: S is acceptable for", agent.name)
            ##print("--Post-Conditions: CS.A_t (", agent.name, ") = CS.A_t−1 (", agent.name, ") U S")
            return "AcceptS"
            
        elif r == "ChallengeY":
            agent.negociation.challengeY.postConditions(support)
            ##print("--Pre-Conditions: there is no condition.")
            ##print("--Post-Conditions: CS.C_t(", agent.name, ") = CS.C_t−1(", agent.name, ") U {y}")
            return "ChallengeY"
            
        elif r == "Argue":
            if r3 != False:
                agent.negociation.argue.postConditions(currentOffer, True, r3)
                ##print("--Pre-Conditions:", r3.S, r3.C, r3.x, "is acceptable for", agent.name)
                ##print("--Post-Conditions: CS.A_t(", agent.name, ") = CS.A_t−1(", agent.name, ")U", r3.S, r3.C, r3.x)
                return r3
            else:
                agent.cs.SN.append(True)
                ##print("--Pre-Conditions:", agent.name, "has no argument to present")
                ##print("--Post-Conditions: none")
                return "SayNothing"

