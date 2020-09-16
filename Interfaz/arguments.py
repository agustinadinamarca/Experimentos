#!/usr/bin/env python
# -*- coding: utf-8 -*-

####################
### Types of Arguments: EPISTEMIC AND PRÁCTICAL (PRO Y CON)
####################
class ArgPRO:
    def __init__(self, S, C, x, G):
        self.S = S # Support
        self.C = C # Consequences
        self.x = x # Conslusion (decision)
        self.__G = G
        self.t = "P"

    #####
    ### FUERZA ARGUMENTOS PRÁCTICOS PRO
    ####
    # The certainty level of the argument A is LevelP(A) = min{ρi | ki ∈ S and (ki, ρi) ∈ K}.
    # If S = ∅ then LevelP(A) = 1.
    def argPROLevel(self):
        lenS = list(self.S)
        if len(lenS) > 0: # S not {}
            temp = lenS[0][-1]
            for k in lenS:
                j = k[-1]
                if j < temp:
                    temp = j
            return temp
        else: # S = {}
            return 1   

    #The degree of satisfaction of the argument is WeightP(A) = n(β) with β = max{λj | (gj , λi) ∈
    # G and gj ∈/ C}.
    #If β = 1 then WeightP(A) = 0 and
    #if C = G then W eightP (A) = 1.
    def argPROWeight(self):
        # arg[1] == C in G; C is not empty
        Gdiffg = []
        for g in self.__G:
            for i in self.C:
                if i == g[0]:
                    Gdiffg.append(g)
                
        #Gdiffg = self.__G - self.C
        if len(Gdiffg)>0:
            temp = Gdiffg[0][1]
            for g in Gdiffg:
                j = g[1]
                if j > temp:
                    temp = j
            return reverseOrdMap(temp)
        else: # C == G, Gdiffg == {}
            return 1.00

    # Strength of an argument PRO:
    # <LevelP (A), W eightP (A)> 
    def argPROStrength(self):
        return (self.argPROLevel(), self.argPROWeight())


class ArgCON:
    def __init__(self, S, C, x, G):
        self.S = S # Support
        self.C = C # Consequences
        self.x = x # Conslusion (decision)
        self.__G = G
        self.t = "C"

    #####    
    ### FUERZA ARGUMENTOS PRÁCTICOS CON
    ####
    # The level of the argument is Level O (A) = m(φ)
    #such that φ = min{ρ i | k i ∈ S and (k i , ρ i ) ∈ K}. If S = ∅ then Level O (A) = 0.
    def argCONLevel(self):
        # arg[0] == S
        S = list(self.S)
        if len(S) > 0: # S not {}
            temp = S[0][-1]
            for k in S:
                j = k[-1]
                if temp < j:
                    temp = j
            return reverseOrdMap(temp)
        else: # S = {}
            return 0   

    #The degree of the argument is W eight O (A) = m(β) such
    #that β = max{λ j such that g j ∈ C and (g j , λ i ) ∈ G}
    def argCONWeight(self):
        # arg[1] == C in G; C is not empty
        priorities = []
        for g in self.C: # ahora g es un string
            for goal in self.__G:
                if g == goal[0]: # busco consecuente en G
                    priorities.append(goal[1])
        lp = len(priorities)
        if lp == 0:
            return 1 # si no hay consecuente en goals, le doy 0, osea beta = 1 (no importante)
        else:
            temp = priorities[0]
            if lp > 2:
                for k in priorities:
                    if k > temp:
                        temp = k
            return reverseOrdMap(temp)

    # Weakness of an argument CON:
    # <LevelP (A), W eightP (A)> 
    def argCONWeakness(self):
        return (self.argCONLevel(), self.argCONWeight())    

class ArgEp:
    def __init__(self, H, h):
        self.H = H # Support
        self.h = h # Conclusion
        self.t = "E"

    #####    
    ### FUERZA ARGUMENTOS EPISTÉMICOS
    ####
    # Argumento Epistémico (Argument in favor of a belief) An argument in favor of a belief is a pair A = <H, h>
    # H = Support(A) is the support of the argument, H in K and minimal
    # h = Conclusion(A) its conclusion. 
    def argEpStrength(self):
        H = list(self.H)
        if len(H) > 0: # H not {} con k1, k2, etc
            temp = H[0][-1]
            for k in H:
                j = k[-1]
                if j < temp:
                    temp = j
            return temp
        else: # H = {}
            return 1

##########################

#Then, strengths of arguments make it possible to compare pairs of arguments in Ap
#Let A and B be two arguments in A P. A is preferred to B,
#iff min(Level P (A), W eight P (A)) ≥ min(Level P (B), Weight P (B)).
def argPROPreferred(arg1, arg2):
    if min(arg1.argPROStrength()) > min(arg2.argPROStrength()):
        return arg1
    if min(arg2.argPROStrength()) > min(arg1.argPROStrength()):
        return arg2
    if min(arg2.argPROStrength()) == min(arg1.argPROStrength()):
        return "equal"

def argCONPreferred(arg1, arg2):
    if max(arg1.argCONWeakness()) > max(arg2.argCONWeakness()):
        return arg1
    if max(arg2.argCONWeakness()) > max(arg1.argCONWeakness()):
        return arg2
    if max(arg1.argCONWeakness()) == max(arg2.argCONWeakness()):
        return "equal"


def argEpPreferred(arg1, arg2):
    if arg1.argEpStrength() > arg2.argEpStrength():
        return arg1
    if arg2.argEpStrength() > arg1.argEpStrength():
        return arg2
    if arg1.argEpStrength() == arg2.argEpStrength():
        return "equal"


# mezclo arg epist y prácticos (len epistemicos 2 y len practicos 3)
def argPreferred(arg1, arg2):
    if arg1.t == "E" and arg2.t == "P":
        if arg1.argEpStrength() > arg2.argPROLevel():
            return arg1
        if arg2.argPROLevel() > arg1.argEpStrength():
            return arg2
        if arg2.argPROLevel() == arg1.argEpStrength():
            return "equal"

    if arg1.t == "P" and arg2.t == "E":
        if arg2.argEpStrength() > arg1.argPROLevel():
            return arg2
        if arg1.argPROLevel() > arg2.argEpStrength():
            return arg1
        if arg1.argPROLevel() == arg2.argEpStrength():
            return "equal"

    if arg1.t == "E" and arg2.t == "C":
        if arg1.argEpStrength() > arg2.argCONLevel():
            return arg1
        if arg2.argCONLevel() > arg1.argEpStrength():
            return arg2
        if arg2.argCONLevel() == arg1.argEpStrength():
            return "equal"

    if arg1.t == "C" and arg2.t == "E":
        if arg2.argEpStrength() > arg1.argCONLevel():
            return arg2
        if arg1.argCONLevel() > arg2.argEpStrength():
            return arg1
        if arg1.argCONLevel() == arg2.argEpStrength():
            return "equal"

# Dado beta en [0, 1], retorno el reverso. Ej. Si beta=0.2 --> reverseOrdMap(beta)=0.8
def reverseOrdMap(beta):
    if beta >=0 and beta <= 1:
        return 1 - beta
    else:
        return None
