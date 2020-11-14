#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

def OptionsAcceptXV(agent, currentOffer): # posibilidades revisadas
        #"AcceptX", "ChallengeY", "Argue", "Withdraw" 
        r1 = agent.negociation.acceptX.preConditions(currentOffer) # True o False
        r2 = agent.negociation.challengeY.preConditions(currentOffer) # T o F
        r3 = agent.negociation.argue.preConditions(currentOffer, True) # res o False
        #r4 = agent.negociation.withdraw.preConditions(currentOffer) # T o F
        
        possibleReplay = []
        
        if r1 == True:
            possibleReplay.append(1)
        
        if r2 == True:
            possibleReplay.append(2)
        
        if r3 != False:
            possibleReplay.append(3)
        
        #if r4 == True:
        #    possibleReplay.append(4)
        if len(possibleReplay) > 0:
            r = np.random.choice(possibleReplay, 1)[0]
            if r==3:
                r=r3
            return (True, r)
        else:
            return (False, -1)
        
            
def OptionsAcceptX(agent, currentOffer, r): # posibilidades revisadas
        if r == 1:
            if currentOffer not in agent.cs.S:
                #print("sddd")
                agent.negociation.acceptX.postConditions(currentOffer)
                ##print("--Pre-Conditions: the offer", currentOffer, "is the most preferred decision in X for", agent.name)
                ##print("--Post-Conditions: CS.S_t (", agent.name, ") = CS.S_t−1 (", agent.name, ") U {", currentOffer, "}.")
                return "AcceptX"
            else:
                ##print("--Pre-Conditions:", agent.name, "has already accepted the current offer", currentOffer)
                ##print("--Post-Conditions: none")
                return "SayNothing"
                    
        elif r == 2:
            agent.negociation.challengeY.postConditions(currentOffer)
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
                
        
