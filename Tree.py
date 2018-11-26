
# Modulo: tree_search
# 
# Fornece um conjunto de classes para suporte a resolucao de 
# problemas por pesquisa em arvore:
#    SearchDomain  - dominios de problemas
#    SearchProblem - problemas concretos a resolver 
#    SearchNode    - nos da arvore de pesquisa
#    SearchTree    - arvore de pesquisa, com metodos para 
#                    a respectiva construcao
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2018,
#  Inteligência Artificial, 2014-2018

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
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
    def __init__(self,problem, energy=None, boost=None, ghost=[]): 
        self.problem = problem
        self.ghost=ghost
        root = SearchNode(problem.initial, None, energy, boost)
        self.open_nodes = [root]

    # obter o caminho (sequencia de estados) da raiz ate um no
    '''
    def get_path(self,node):
        if node.parent == None:
            return [node.direction]
        path = self.get_path(node.parent)
        path += [node.direction]
        return path 
    '''

    # procurar a solucao
    def search(self):
        while self.open_nodes != []:
            #for z in range(4):
            node = self.open_nodes.pop(0)

            closestEnergy=self.problem.domain.getClosest(node.state, node.energy)
            lnewnodes = []
            #self.problem.domain.runAway(self.problem.domain.actions(node.state),self.ghost)
            act=self.problem.domain.runAway(self.problem.domain.actions(node.state),self.ghost)
            for a in act:
                newstate = self.problem.domain.result(node.state,a)
                if not self.is_parent(newstate, node):
                    energies=self.problem.domain.remainingEnergies(node.state, newstate, node.energy)
                    boosts=self.problem.domain.remainingBoosts(node.state, newstate,node.boost)
                    #if z==0:
                    direct=self.problem.domain.getDirection(node.state,newstate)
                    #else:
                    #    direct=node.direction
                    lnewnodes += [SearchNode(newstate,node, energies, boosts, direct, node.cost+self.problem.domain.cost(a), self.problem.domain.heuristic(newstate, closestEnergy, energies, boosts, self.ghost))]
            self.add_to_open(lnewnodes)
                #print(lnewnodes)
                #if z==3:
            return self.open_nodes[0].direction
        return None


    def searchGhost(self, eatableG, runG):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            closestGhost=self.problem.domain.getClosest(node.state, eatableG)
            lnewnodes = []
            act=self.problem.domain.runAway(self.problem.domain.actions(node.state),runG)
            for a in act:
                newstate = self.problem.domain.result(node.state,a)
                if not self.is_parent(newstate, node):
                    direct=self.problem.domain.getDirection(node.state,newstate)
                    lnewnodes += [SearchNode(newstate,node, [], [],direct, node.cost+self.problem.domain.cost(a), self.problem.domain.heuristicGhost(newstate, closestGhost))]
            self.add_to_open(lnewnodes)
            print(self.open_nodes)
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

