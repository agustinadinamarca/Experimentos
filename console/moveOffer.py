#!/usr/bin/env python
# -*- coding: utf-8 -*-

import agent as agent
import arguments as ar
import numpy as np

def repliesToOffer(agent, currentOffer):
    # AcceptX
    r1 = agent.negociation.acceptX.preConditions(currentOffer) # Retorna True o False
    # RefuseX
    r2 = agent.negociation.refuse.preConditions(currentOffer) # Retorna True o False
    # ChallengeX
    r3 = agent.negociation.challengeX.preConditions(currentOffer) # Retorna True o False
    
    ##print("--Possibilities:", r1 , "(AcceptX),", r2, "(RefuseX),", r3, "(ChallengeX)")
    
    possibleReplay = []
    
    if r1 == True:
        possibleReplay.append("AcceptX")
        
    if r2 == True:
        possibleReplay.append("RefuseX")
        
    if r3 == True:
        possibleReplay.append("ChallengeX")
    
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
            
    elif r == "RefuseX":
        agent.negociation.refuse.postConditions(currentOffer)
        ##print("--Pre-Conditions:", agent.name, "has at least one argument against", currentOffer)
        ##print("--Post-Conditions: none")
        return "RefuseX"
    
    elif r == "ChallengeX":
        agent.negociation.challengeX.postConditions(currentOffer)
        ##print("--Pre-Conditions: exists", agent.candidatesDecisionPrefOrder()[1][0], "that is preferred to", currentOffer)
        ##print("--Post-Conditions: CS.C_t(", agent.name, ") = CS.C_t−1(", agent.name, ") ∪ {", currentOffer, "}")
        return "ChallengeX"
    

def repliesToOfferV(agent, currentOffer):
    # AcceptX
    r1 = agent.negociation.acceptX.preConditions(currentOffer) # Retorna True o False
    # RefuseX
    r2 = agent.negociation.refuse.preConditions(currentOffer) # Retorna True o False
    # ChallengeX
    r3 = agent.negociation.challengeX.preConditions(currentOffer) # Retorna True o False
    
    if r1 == True or r2 == True or r3 == True:
        return True
    else:
        return False
