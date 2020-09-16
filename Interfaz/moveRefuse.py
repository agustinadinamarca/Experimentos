
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import agent as agent
import numpy as np
import arguments as ar

def OptionsRefuseV(agent, currentOffer, offertAgent):
    #"AcceptX", "ChallengeX", "Argue", "Withdraw"
    r1 = agent.negociation.acceptX.preConditions(currentOffer) # True o False
    r2 = agent.negociation.challengeX.preConditions(currentOffer) # T o F
    r3 = agent.negociation.argue.preConditions(currentOffer, True) # res o False
    r4 = agent.negociation.withdraw.preConditions(currentOffer) # T o F
    
    if r1 == True or r2 == True or r4 == True or r3 != False:
        return True
    else:
        return False
        
def OptionsRefuse(agent, currentOffer, offertAgent):
    #"AcceptX", "ChallengeX", "Argue", "Withdraw"
    r1 = agent.negociation.acceptX.preConditions(currentOffer) # True o False
    r2 = agent.negociation.challengeX.preConditions(currentOffer) # T o F
    r3 = agent.negociation.argue.preConditions(currentOffer, True) # res o False
    r4 = agent.negociation.withdraw.preConditions(currentOffer) # T o F
    
    ##if r3 != False:
    ##    print("--Possibilities:", r1, "(AcceptX),", r2, "(ChallengeX),", "True (Argue),", r4, "(Withdraw)")
    ##else:
    ##    print("--Possibilities:", r1, "(AcceptX),", r2, "(ChallengeX),", r3, "(Argue),", r4, "(Withdraw)")
      
    possibleReplay = []
    
    if r1 == True:
        possibleReplay.append("AcceptX")
      
    if r2 == True:
        possibleReplay.append("ChallengeX")
        
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
      
      
    elif r == "ChallengeX":
        agent.negociation.challengeX.postConditions(currentOffer)
        ##print("--Pre-Conditions: exists", agent.candidatesDecisionPrefOrder()[1][0], "that is preferred to", currentOffer)
        ##print("--Post-Conditions: CS.C_t(", agent.name, ") = CS.C_t−1(", agent.name, ") ∪ {", currentOffer, "}")
        return "ChallengeX"
       
    elif r == "Withdraw":
        ##print("--Pre-Conditions: ∀x ∈ X, there is an argument with maximal strength against x")
        ##print("--Post-Conditions: Result(Dialogue) = failure and ∀i, CS_t (a_i ) = ∅")
        return "Withdraw"
      
