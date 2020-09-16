#!/usr/bin/env python
# -*- coding: utf-8 -*-

import agent as agent
import arguments as ar
import numpy as np

def OptionsAcceptXV(agent, currentOffer, offertAgent): # posibilidades revisadas
        #"AcceptX", "ChallengeY", "Argue", "Withdraw" 
        r1 = agent.negociation.acceptX.preConditions(currentOffer) # True o False
        r2 = agent.negociation.challengeY.preConditions(currentOffer) # T o F
        r3 = agent.negociation.argue.preConditions(currentOffer, True) # res o False
        r4 = agent.negociation.withdraw.preConditions(currentOffer) # T o F
        
        if r1 == True or r2 == True or r4 == True or r3 != False:
            return True
        else:
            return False
            
def OptionsAcceptX(agent, currentOffer, offertAgent): # posibilidades revisadas
        #"AcceptX", "ChallengeY", "Argue", "Withdraw" 
        r1 = agent.negociation.acceptX.preConditions(currentOffer) # True o False
        r2 = agent.negociation.challengeY.preConditions(currentOffer) # T o F
        r3 = agent.negociation.argue.preConditions(currentOffer, True) # res o False
        r4 = agent.negociation.withdraw.preConditions(currentOffer) # T o F
        
        ##if r3 != False:
        ##    print("--Possibilities:", r1, "(AcceptX),", r2, "(ChallengeY),", "True (Argue),", r4, "(Withdraw)")
        ##else:
        ##    print("--Possibilities:", r1, "(AcceptX),", r2, "(ChallengeY),", r3, "(Argue),", r4, "(Withdraw)")
        
        possibleReplay = []
        
        if r1 == True:
            possibleReplay.append("AcceptX")
        
        if r2 == True:
            possibleReplay.append("ChallengeY")
        
        if r3 != False:
            possibleReplay.append("Argue")
        
        if r4 == True:
            possibleReplay.append("Withdraw")
        
        r = np.random.choice(possibleReplay, 1)[0]
        
        if r == "AcceptX":
            if currentOffer not in agent.cs.S:
                agent.negociation.acceptX.postConditions(currentOffer)
                ##print("--Pre-Conditions: the offer", currentOffer, "is the most preferred decision in X for", agent.name)
                ##print("--Post-Conditions: CS.S_t (", agent.name, ") = CS.S_t−1 (", agent.name, ") U {", currentOffer, "}.")
                return "AcceptX"
            else:
                ##print("--Pre-Conditions:", agent.name, "has already accepted the current offer", currentOffer)
                ##print("--Post-Conditions: none")
                return "SayNothing"
                    
        elif r == "ChallengeY":
            agent.negociation.challengeY.postConditions(currentOffer)
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
                
        elif r == "Withdraw":
            ##print("--Pre-Conditions: ∀x ∈ X, there is an argument with maximal strength against x")
            ##print("--Post-Conditions: Result(Dialogue) = failure and ∀i, CS_t (a_i ) = ∅")
            return "Withdraw"
        
