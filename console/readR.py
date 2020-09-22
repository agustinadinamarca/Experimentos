import arguments as ar

def readRest():
    F = open("argsAcc-R*.txt", "r")
    
    N = int(F.readline())
    LST = []
    lst = []
    
    t = F.readline().split()
    
    while t:
        if len(t)==1:
            lst.append(t[0])
        else:
            if t[0] == "PRO":
                S=set()
                count=3
                while count < len(t):
                    if t[count] == "2":
                        S.add((t[count+1], float(t[count+2])))
                        count+= 3
                    elif t[count] == "3":
                        S.add((t[count+1], t[count+2], float(t[count+3])))
                        count+= 4
                    lst.append(ar.ArgPRO(S, t[2], t[1], set()))
            else:
                    S=set()
                    count=3
                    while count<len(t):
                        if t[count] == "2":
                            S.add((t[count+1], float(t[count+2])))
                            count+= 3
                        elif t[count] == "3":
                            S.add((t[count+1], t[count+2], float(t[count+3])))
                            count+= 4
                    lst.append(ar.ArgCON(S, t[2], t[1], set()))
        t = F.readline().split()

    LST=[]
    c=0
    for i in range(N):
        L=[]
        
        while lst[c+1] != "#" and c+1 < len(lst)-1:
            L.append(lst[c+1])
            c+=1
        c+=1
        LST.append(L)
            
              

    #print(LST)
    return LST
    
readRest()
