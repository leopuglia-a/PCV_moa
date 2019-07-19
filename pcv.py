# gerador de grafos
import random
import time

class GraphGenerator:

    def __init__(self, n):
        self.n = n
        self.cost={}
        self.graph = [[] for i in range(n)]
        self.gen_graph()

    def gen_graph(self):

        # adicionando am adjacente para todos os vertices
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if ((i,j) and (j,i)) not in self.cost:
                        custo = random.randint(1,100)
                        self.cost[(i,j)] = custo
                        self.cost[(j,i)] = custo
                    self.graph[i].append(j)

    def show_graph(self):
        for i in range(self.n):
            print('Adjacentes de %d:' %i, end=' ')
            for adj in self.graph[i]:
                print('(%d)%d -> ' %(self.cost[i,adj], adj), end=' ')


    def pcv_random(self, iterations):
        '''
            funcao geradora do caminho inicial
            gera um circuito aleatoriamente selecionando vertices  aleatoriamente
            adiciona o custo do ultimo elemento da lista do circuitos ao custo total
        '''
        best_circuit = []
        lowest_cost = None

        def gen_cir(best_circuit, lowest_cost):

            vertices = [ i for i in range(1, self.n)]
            circuit = [0]
            circuit_cost = 0

            while len(vertices) > 0:
                e = random.choice(vertices)
                vertices.remove(e)
                circuit_cost += self.cost[(circuit[-1], e)]
                circuit.append(e)

            circuit_cost += self.cost[(circuit[0],e)]

            if lowest_cost is None:
                best_circuit = circuit[:]
                lowest_cost = circuit_cost
                print('Circuito inicial: %s - Custo incial: %d' % (str(best_circuit), lowest_cost))
            else:
                if circuit_cost < lowest_cost:
                    best_circuit = circuit[:]
                    lowest_cost = circuit_cost

            return (best_circuit, lowest_cost)

        for i in range(iterations):
            best_circuit, lowest_cost = gen_cir(best_circuit, lowest_cost)

        print('Melhor circuito: %s - Custo: %d' % (str(best_circuit), lowest_cost))


generator = GraphGenerator(10)
generator.pcv_random(5)
