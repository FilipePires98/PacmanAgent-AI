from Tree import *
from math import sqrt

class Pacman(SearchDomain):
    def __init__(self,mapa):
        self.nodes=self.findNodes([(x,y) for x in range(mapa.size[0]) for y in range(mapa.size[1]) if not mapa.is_wall((x,y))])
        self.mapa=mapa

    def actions(self,state):
        actlist = []
        act=self.possibleAction(state)
        return act

    def result(self,state,action):
        (C1,C2) = action
        if C1==state:   
            return C2

    def cost(self, action):
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        (C1,C2) = action
        cost=0
        direction=self.getDirection(C1,C2)
        aux=C1
        while aux!=C2:
            cost+=1
            if direction=='a':
                aux=((xOut if (aux[0]-1==-1) else (aux[0]-1)),aux[1])
            if direction=='d':
                aux=((aux[0]+1)%xOut,aux[1])
            if direction=='w':
                aux=(aux[0],(yOut if (aux[1]-1)==-1 else (aux[1]-1)))
            if direction=='s':
                aux=(aux[0],(aux[1]+1)%yOut)
        return cost



    def heuristic(self,state, closestEnergy, energies, boosts, ghosts):
        return (len(energies)*10+len(boosts)*20) + self.costFromTo(state, closestEnergy)
    

    def heuristicGhost(self,state, closestGhost):
        return self.costFromTo(state, closestGhost)

    # aux functions
    
    def runAway(self, actions, ghosts):
        if ghosts==[]:
            return actions
        print("act", actions)
        aux=[x for x in actions if not self.ghostInPath(x, ghosts)]
        print(aux)
        act=[x for x in aux if min([abs(x[1][0]-g[0])+abs(x[1][1]-g[1]) for g in ghosts])>3]
        if act==[]:
            dists=[min([abs(x[1][0]-g[0])+abs(x[1][1]-g[1]) for g in ghosts]) for x in aux]
            act=[actions[dists.index(max(dists))]]
        print("a", act)
        return act


    def ghostInPath(self, action, ghosts):
        ret=False
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        s1,s2=action
        aux=s1
        run=True
        while run:
            if aux==s2:
                run=False
                break
            if s1[0]==s2[0]:
                if s1[1]>s2[1]:
                    if list(aux) in ghosts:
                        ret=True
                        run=False
                        break
                    aux=(aux[0], yOut if (aux[1]-1)==-1 else (aux[1]-1))
                else:
                    if list(aux) in ghosts:
                        ret= True
                        run=False
                        break
                    aux=(aux[0], (aux[1]+1)%yOut)
            if s1[1]==s2[1]:
                if s1[0]>s2[0]:
                    if list(aux) in ghosts:
                        ret= True
                        run=False
                        break
                    aux=(xOut if (aux[0]-1)==-1 else (aux[0]-1), aux[1])
                else:
                    if list(aux) in ghosts:
                        ret= True
                        run=False
                        break
                    aux=((aux[0]+1)%xOut, aux[1])
        return ret


    '''
    def runAway(self, actions, ghosts):
        # for each action and each gost, get danger level (1=very danger, 4=safe)
        aux = []
        for i,a in enumerate(actions):
            aux.append([])
            for j,g in enumerate(ghosts):
                cost = self.costFromTo(a[1],g)
                if cost>3:
                    aux[i].append(4)
                else:
                    aux[i].append(cost)

        # for each action, get most dangerous level
        aux2 = []
        for i,n in enumerate(aux):
            aux2.append(min(aux[i])) #sum(aux[i])/len(ghosts)

        # if all 4 actions dangerous, return the least bad, else return the safe ones (4)
        retval = []
        if 4 not in aux2:
            best = max(aux2)
            for i,a in enumerate(aux2):
                if a == best:
                    retval.append(actions[i])
        else:
            for i,a in enumerate(aux2):
                if a == 4:
                    retval.append(actions[i])
        return retval
    '''

    def costFromTo(self, state1, state2):
        #print(state1,state2)
        aux=[(state1,0)]
        while state2 not in [x[0] for x in aux]:
            st=aux.pop(0)
            actions=self.possibleAction(st[0])
            visitedstates=[y[0] for y in aux]
            aux+=[(x[1], st[1]+sqrt((st[0][0]-x[1][0])**2 + (st[0][1]-x[1][1])**2)) for x in actions if x[1] not in visitedstates]
        return [x[1] for x in aux if x[0]==state2][0]

    def findNodes(self, allPositions):
        n = []
        for p1 in allPositions:
            if (p1[0]+1, p1[1]) in allPositions and (p1[0], p1[1]+1) in allPositions:
                n.append(p1)
            elif (p1[0]-1, p1[1]) in allPositions and (p1[0], p1[1]+1) in allPositions:
                n.append(p1)
            elif (p1[0]+1, p1[1]) in allPositions and (p1[0], p1[1]-1) in allPositions:
                n.append(p1)
            elif (p1[0]-1, p1[1]) in allPositions and (p1[0], p1[1]-1) in allPositions:
                n.append(p1)
        return list(set(n))

    def getDirection(self, state1, state2):
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        if state1[0]==state2[0]:
            y=state1[1]
            for i in range(abs(state1[1]-state2[1])+1):
                if self.mapa.is_wall((state1[0],(y+i)%yOut)):
                    return 'w'
                if (state1[0],(y+i)%yOut)==state2:
                    return 's'
            return 'w'
        if state1[1]==state2[1]:
            x=state1[0]
            for i in range(abs(state1[0]-state2[0])+1):
                if self.mapa.is_wall(((x+i)%xOut,state1[1])):
                    return 'a'
                if ((x+i)%xOut,state1[1])==state2:
                    return 'd'
            return 'a'

    def possibleAction(self, state1):
        dir1=state1
        dir2=state1
        dir3=state1
        dir4=state1
        d1=True
        d2=True
        d3=True
        d4=True
        verify=True
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        aux=[]
        while verify:
            #print(aux, dir1, dir2, dir3,dir4)
            if d1==False and d2==False and d3==False and d4==False:
                verify=False
            if d1:
                dir1=((dir1[0]+1)%xOut, dir1[1])
                if self.mapa.is_wall(dir1):
                    d1=False
                if dir1 in self.nodes:
                    d1=False
                    aux+=[(state1,dir1)]
            if d2:
                dir2=((xOut if (dir2[0]-1==-1) else dir2[0]-1), dir2[1])
                if self.mapa.is_wall(dir2):
                    d2=False
                if dir2 in self.nodes:
                    d2=False
                    aux+=[(state1,dir2)]
            if d3:
                dir3=(dir3[0], (dir3[1]+1)%yOut)
                if self.mapa.is_wall(dir3):
                    d3=False
                if dir3 in self.nodes:
                    d3=False
                    aux+=[(state1,dir3)]
            if d4:
                dir4=(dir4[0], (yOut if (dir4[1]-1==-1) else dir4[1]-1))
                if self.mapa.is_wall(dir4):
                    d4=False
                if dir4 in self.nodes:
                    d4=False
                    aux+=[(state1,dir4)]
        return aux

    def remainingEnergies(self, node, state, energy):
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        direction=self.getDirection(node,state)
        path=[]
        aux=node
        while aux!=state:
            path.append(aux)
            if direction=='a':
                aux=((xOut if (aux[0]-1==-1) else (aux[0]-1)),aux[1])
            if direction=='d':
                aux=((aux[0]+1)%xOut,aux[1])
            if direction=='w':
                aux=(aux[0],(yOut if (aux[1]-1==-1) else (aux[1]-1)))
            if direction=='s':
                aux=(aux[0],(aux[1]+1)%yOut)
        return [x for x in energy if tuple(x) not in path]

    def remainingBoosts(self, node, state,boost):
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        direction=self.getDirection(node, state)
        path=[]
        aux=node
        while aux!=state:
            path.append(aux)
            if direction=='a':
                aux=((xOut if (aux[0]-1==-1) else (aux[0]-1)),aux[1])
            if direction=='d':
                aux=((aux[0]+1)%xOut,aux[1])
            if direction=='w':
                aux=(aux[0],(yOut if (aux[1]-1)==-1 else (aux[1]-1)))
            if direction=='s':
                aux=(aux[0],(aux[1]+1)%yOut)
        return [x for x in boost if tuple(x) not in path]

    def isNode(self, state):
        return state in self.nodes


    '''
    def getClosest(self, state, Energies):
        minimo=min([sqrt((state[0]-x[0])**2 + (state[1]-x[1])**2) for x in Energies])
        Energy=[x for x in Energies if sqrt((state[0]-x[0])**2 + (state[1]-x[1])**2)==minimo][0]
        return Energy
    '''

    def getClosest(self, state, states):
        minimo=min([(abs(state[0]-x[0])+abs(state[1]-x[1])) for x in states])
        Energy=[x for x in states if (abs(state[0]-x[0])+abs(state[1]-x[1]))==minimo][0]
        minimo2=min([(abs(Energy[0]-x[0])+abs(Energy[1]-x[1])) for x in self.nodes])
        node=[x for x in self.nodes if (abs(Energy[0]-x[0])+abs(Energy[1]-x[1]))==minimo2][0]
        return node
