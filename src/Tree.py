from abc import ABC, abstractmethod
from math import sqrt
from random import randint
# Modelo fornecido pelo professor
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal_state):
        pass

# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial):
        self.domain = domain
        self.initial = initial

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent, energy=[], boost=[], direction=None, cost=0, heuristic=0): 
        self.state = state
        self.parent = parent
        self.direction=direction
        self.cost=cost
        self.heuristic=heuristic
        self.energy=energy
        self.boost=boost
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent.state) +"," + str(self.direction) + ","+ str(len(self.energy))+","+str(len(self.boost)) +"," + str(self.cost) +"," + str(self.heuristic)+")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, energy=None, boost=None, ghost=[], pastGhost=[]): 
        self.problem = problem
        self.ghost=ghost
        self.pastGhost=pastGhost
        root = SearchNode(problem.initial, None, energy, boost)
        self.open_nodes = [root]

    # procurar a solucao
    def search(self, getBoost):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            closestEnergy=self.problem.domain.getClosest(node.state, node.energy)
            lnewnodes = []
            act = self.problem.domain.runAway(self.problem.domain.actions(node.state),self.ghost)
            for a in act:
                newstate = self.problem.domain.result(node.state,a)
                if not self.is_parent(newstate, node):
                    energies=self.problem.domain.remainingEnergies(node.state, newstate, node.energy)
                    boosts=self.problem.domain.remainingBoosts(node.state, newstate,node.boost)

                    direct=self.problem.domain.getDirection(node.state,newstate) if node.direction==None else node.direction

                    lnewnodes += [SearchNode(newstate, node, energies, boosts, direct, node.cost+self.problem.domain.cost(a), self.problem.domain.heuristic(newstate, closestEnergy, energies, boosts, node.boost, self.ghost,a, getBoost))]
            self.add_to_open(lnewnodes)
            #print(self.open_nodes)
            return self.open_nodes[0].direction
        return None

    def searchGhost(self, eatableG):
        runG = self.ghost[:]
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            closestGhost=self.problem.domain.getClosest(node.state,eatableG)
            if closestGhost==[]:
                return None
            lnewnodes = []
            act=self.problem.domain.runAway(self.problem.domain.actions(node.state),runG)
            for a in act:
                newstate = self.problem.domain.result(node.state,a)
                if not self.is_parent(newstate, node):
                    direct=self.problem.domain.getDirection(node.state,newstate)
                    lnewnodes += [SearchNode(newstate,node, [], [],direct, node.cost+self.problem.domain.cost(a), self.problem.domain.heuristicGhost(newstate, eatableG, closestGhost,a))]
            self.add_to_open(lnewnodes)
            #print(self.open_nodes)
            return self.open_nodes[0].direction
        return None

    def is_parent(self, state, node):
        if node.parent is None:
            return False
        elif state==node.parent.state:
            return True
        else:
            return self.is_parent(state, node.parent)

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        self.open_nodes.extend(lnewnodes)
        self.open_nodes.sort(key=lambda x : x.heuristic+x.cost)



#Meu dominio
class Pacman(SearchDomain):
    def __init__(self,mapa):
        self.nodes=self.findNodes([(x,y) for x in range(mapa.size[0]) for y in range(mapa.size[1]) if not mapa.is_wall((x,y))])
        self.mapa=mapa

    #acoes para determinado estado
    def actions(self,state):
        actlist = []
        act=self.possibleAction(state)
        return act

    #resultado da acao
    def result(self,state,action):
        (C1,C2) = action
        if C1==state:   
            return C2

    #custo de um resultante de uma acao
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

    #heuristica ate ao objetico
    def heuristic(self,state, closestEnergy, energies,remboosts, boosts, ghosts,act, getBoost):
        if getBoost and boosts!=[]:
            return (len(energies)*5+len(remboosts)) + self.costFromTo(state, self.getClosest(state, boosts)) if not self.ghostInPath(act,boosts) else 0
        else:
            return (len(energies)*10+len(remboosts)) + self.costFromTo(state, closestEnergy)

    #heuristica caso o objetivo seja comer um fantasma
    def heuristicGhost(self,state, eatableG, closestGhost,act):
        ghst=[list(x) for x in eatableG if abs(x[0]-closestGhost[0])+abs(x[1]-closestGhost[1])==min(abs(y[0]-closestGhost[0])+abs(y[1]-closestGhost[1]) for y in eatableG)]
        cst=self.costFromTo(state, closestGhost)
        notInPath=1000+cst if not self.ghostInPath(act, ghst) else cst
        return notInPath




    # aux functions
    
    #algoritmo para fugir dos fantasmas
    def runAway(self, actions, ghosts):
        if ghosts==[]:
            return actions
        aux=[x for x in actions if not self.ghostInPath(x, ghosts)]
        if len(aux)==0:
            aux=actions
        act=[x for x in aux if min([abs(x[1][0]-g[0])+abs(x[1][1]-g[1]) for g in ghosts])>1]
        if act==[]:
            dists=[min([abs(x[1][0]-g[0])+abs(x[1][1]-g[1]) for g in ghosts]) for x in aux]
            act=[actions[dists.index(max(dists))]]
        return act


    #algoritmo para verificacao se algum fantasma se encontra na acao pertendida
    def ghostInPath(self, action, ghosts):
        ret=False
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1
        s1,s2=action
        aux=s1
        direction=self.getDirection(s1,s2)
        while aux!=s2:
            if list(aux) in ghosts:
                ret=True
                break
            if direction=='a':
                aux=((xOut if (aux[0]-1==-1) else (aux[0]-1)),aux[1])
            if direction=='d':
                aux=((aux[0]+1)%xOut,aux[1])
            if direction=='w':
                aux=(aux[0],(yOut if (aux[1]-1)==-1 else (aux[1]-1)))
            if direction=='s':
                aux=(aux[0],(aux[1]+1)%yOut)
        if list(s2) in ghosts:
            ret=True
        return ret


    #retorna o custo real de ir de um n?? para o outro tendo que o n?? de destino ser um cruzamento(isto ??, pertencer ?? lista nodes)
    def costFromTo(self, state1, state2):
        aux=[(state1,0)]
        while state2 not in [x[0] for x in aux]:
            st=aux.pop(0)
            actions=self.possibleAction(st[0])
            visitedstates=[y[0] for y in aux]
            aux+=[(x[1], st[1]+sqrt((st[0][0]-x[1][0])**2 + (st[0][1]-x[1][1])**2)) for x in actions if x[1] not in visitedstates]
        return [x[1] for x in aux if x[0]==state2][0]

    #funcao que dado todo o mapa calcula todos os n??s, isto ??, todos os cruzamentos e intercecoes
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

    #dados duas posicoes devolve a direcao necessaria para ir da posicao 1 ate a posicao 2
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

    #retorna todas as acoes possiveis para uma dada posicao(maximo de 4, wasd)
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


    #retorna as energias restantes depois de um movimento
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

    #retorna os boosts restantes depois de um movimento
    def remainingBoosts(self, node, state, boost):
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


    #verifica se ?? um node, isto e, pertence a lista nodes
    def isNode(self, state):
        return state in self.nodes


    #retorna o node mais proximo do state mais proximo pertencente a lista de states fornecido
    def getClosest(self, state, states):
        minimo=min([(abs(state[0]-x[0])+abs(state[1]-x[1])) for x in states])
        Energy=[x for x in states if (abs(state[0]-x[0])+abs(state[1]-x[1]))==minimo][0]
        minimo2=min([(abs(Energy[0]-x[0])+abs(Energy[1]-x[1])) for x in self.nodes])
        aux=[x for x in self.nodes if (abs(Energy[0]-x[0])+abs(Energy[1]-x[1]))==minimo2]
        node=aux[randint(0,len(aux)-1)]
        return node

    #verifica se a posicao e segura, isto e, se nao existe ghosts a sua volta
    def d8(self, cell, ghosts):
        if (cell[0], cell[1]+1) in ghosts:
            return False
        if (cell[0], cell[1]-1) in ghosts:
            return False
        if (cell[0]+1, cell[1]) in ghosts:
            return False
        if (cell[0]-1, cell[1]) in ghosts:
            return False
        if (cell[0]+1, cell[1]+1) in ghosts:
            return False
        if (cell[0]+1, cell[1]-1) in ghosts:
            return False
        if (cell[0]-1, cell[1]+1) in ghosts:
            return False
        if (cell[0]-1, cell[1]-1) in ghosts:
            return False

        return True

    #verifica se o ghost esta numa zona segura, no caso, se nao se encontra nas margens
    def ghostInSafeZone(self,ghost):
        xIn=0
        yIn=0
        xOut=self.mapa.size[0]-1
        yOut=self.mapa.size[1]-1

        if(ghost[0]==xIn or ghost[0]==xOut or ghost[1]==yIn or ghost[1]==yOut):
            return True

        return False