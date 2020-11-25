#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def OptionsChallengeY(agent, currentOffer, r):
    """
    # Argue(currentOffer)
    r = agent.negociation.argue.preConditions(currentOffer, True) # Retorna res o False
    ##if r != False:
    ##    print("--Possibilities:", "True (Argue)")
    ##else:
    ##    print("--Possibilities:", r, "(Argue)")
    """ 
    if r == False: # si no hay argumentos que presentar, say nothing
        agent.cs.SN.append(True)
        ##print("--Pre-Conditions:", agent.name, "has no argument to present")
        ##print("--Post-Conditions: none")
        return "SayNothing"
    else:
        agent.negociation.argue.postConditions(currentOffer, True, r)
        ##print("--Pre-Conditions:", r.S, r.C, r.x, "is acceptable for", agent.name)
        ##print("--Post-Conditions: CS.A_t(", agent.name, ") = CS.A_t−1(", agent.name, ")U", r.S, r.C, r.x)
        return r



def OptionsChallengeX(agent, currentOffer, r):
    """
    # Argue(currentOffer)
    r = agent.negociation.argue.preConditions(currentOffer, True) # Retorna res o False
    
    ##if r != False:
    ##    print("--Possibilities:", "True (Argue)")
    ##else:
    ##    print("--Possibilities:", r, "(Argue)")
    """ 
    if r == False: # si no hay argumentos que presentar, say nothing
        agent.cs.SN.append(True)
        ##print("--Pre-Conditions:", agent.name, "has no argument to present")
        ##print("Post-Conditions: none")
        return "SayNothing"
    else:
        agent.negociation.argue.postConditions(currentOffer, True, r)
        ##print("--Pre-Conditions:", r.S, r.C, r.x, "is acceptable for", agent.name)
        ##print("--Post-Conditions: CS.A_t(", agent.name, ") = CS.A_t−1(", agent.name, ")U", r.S, r.C, r.x)
        return r
        
    
def OptionsChallengeYV(agent, currentOffer):
    r = agent.negociation.argue.preConditions(currentOffer, True)
    return (True, r)
        
def OptionsChallengeXV(agent, currentOffer):
    r = agent.negociation.argue.preConditions(currentOffer, True) # Retorna res o False
    return (True, r)
