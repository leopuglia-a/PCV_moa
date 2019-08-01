'''
    Problema do Caixeiro Viajante utilizando solucao inicial randomica
    e utilizando algoritmo genetico para otimizar a solucao
'''
import random
# import sys

class GraphGenerator:

    def __init__(self, n):
        self.n = n
        self.costs={}
        self.graph = [[] for i in range(n)]
        self.gen_graph()

    def gen_graph(self):

        # adicionando am adjacente para todos os vertices
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    if ((i,j) and (j,i)) not in self.costs:
                        custo = random.randint(1,100)
                        self.costs[(i,j)] = custo
                        self.costs[(j,i)] = custo
                    self.graph[i].append(j)

    def show_graph(self):
        for i in range(self.n):
            print('Adjacentes de %d:' %i, end=' ')
            for adj in self.graph[i]:
                print('(%d)%d -> ' %(self.costs[i,adj], adj), end=' ')

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
                circuit_cost += self.costs[(circuit[-1], e)]
                circuit.append(e)

            circuit_cost += self.costs[(circuit[0],e)]

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

    def pcv_genetic(self, pop_size, generations, tournament_size, prob_cross, prob_mutation):
        '''
            Gerar populacao, criando uma lista onde cada elemento eh um individuo
            Cada individuo eh um caminho possivel
        '''
        population = [] # populacao eh lista de listas (cada elemento eh um caminho)

        def gen_indivi():
            vertices = [i for i in range(1, self.n)]
            indivi = [0]
            while len(vertices) > 0:
                e = random.choice(vertices)
                vertices.remove(e)
                indivi.append(e)
            return indivi

        # funcao de fitness, avalicao da sua qualidade
        def get_cost(indivi):
            cost = 0
            for i in range(self.n -1):
                cost += self.costs[(indivi[i], indivi[i+1])]
            cost += self.costs[(indivi[-1], indivi[0])]
            return cost

        # gerando populacao inicial
        for i in range(pop_size):
            population.append(gen_indivi())

        #  a cada geracao
        for i in range(generations):
            # selecionar individuos por torneio
            for j in range(tournament_size):

                # chance de acontecer o crossover
                if random.random() <= prob_cross:

                    parent1, parent2 = None, None

                    # selecionar indices que nao sejam iguais
                    while True:
                        parent1 = random.randint(0, pop_size -1)
                        parent2 = random.randint(0, pop_size -1)
                        if parent1 != parent2:
                            break;

                    # pog para nao gerar vertices repetidos no cross over
                    valid_cross1 = [i for i in range(self.n)]
                    valid_cross2 = valid_cross1[:]
                    cross1, cross2 = [], []

                    # cruzamento de um ponto
                    while True:

                        ponto = random.randint(0, self.n -1 )

                        # nao seleciona corte nas extremidades
                        if ponto != 0 and ponto != (self.n -1):

                            # selecionar genes dos pais
                            for p in range(ponto):

                                # pog
                                if population[parent1][p] not in cross1:
                                    cross1.append(population[parent1][p])
                                    valid_cross1.remove(population[parent1][p])
                                else:
                                    e = random.choice(valid_cross1)
                                    cross1.append(e)
                                    valid_cross1.remove(e)

                                if population[parent2][p] not in cross2:
                                    cross2.append(population[parent2][p])
                                    valid_cross2.remove(population[parent2][p])
                                else:
                                    e = random.choice(valid_cross2)
                                    cross2.append(e)
                                    valid_cross2.remove(e)

                            for p in range(ponto, self.n):

                                # pog
                                if population[parent2][p] not in cross1:
                                    cross1.append(population[parent2][p])
                                    valid_cross1.remove(population[parent2][p])
                                else:
                                    e = random.choice(valid_cross1)
                                    cross1.append(e)
                                    valid_cross1.remove(e)

                                if population[parent1][p] not in cross2:
                                    cross2.append(population[parent1][p])
                                    valid_cross2.remove(population[parent1][p])
                                else:
                                    e = random.choice(valid_cross2)
                                    cross2.append(e)
                                    valid_cross2.remove(e)


                            break

                    # aplica a mutacao
                    if random.random() <= prob_mutation:
                        gene1, gene2 = None, None

                        while True:
                            gene1 = random.randint(0, self.n -1)
                            gene2 = random.randint(0, self.n -1)
                            if gene1 != gene2:
                                cross1[gene1], cross1[gene2] = cross1[gene2], cross1[gene1]
                                cross2[gene1], cross2[gene2] = cross2[gene2], cross2[gene1]
                                break;

                    # obtem fitness dos pais e dos filhos
                    fitness_parent1 = get_cost(population[parent1])
                    fitness_parent2 = get_cost(population[parent1])
                    fitness_cross1 = get_cost(cross1)
                    fitness_cross2 = get_cost(cross2)

                    # substitui melhor geracao e mantem populacao mesmo tamanho
                    if fitness_cross1 < fitness_parent1 or fitness_cross1 < fitness_parent2:
                        if fitness_cross1 < fitness_parent1:
                            population.pop(parent1)
                        else:
                            population.pop(parent2)
                        population.append(cross1)
                    elif fitness_cross2 < fitness_parent1 or fitness_cross2 < fitness_parent2:
                        if fitness_cross2 < fitness_parent1:
                            population.pop(parent1)
                        else:
                            population.pop(parent2)
                        population.append(cross2)

        # obtem o Melhor individiduo da populacao
        best_indivi = population[0][:]

        for indivi in range(1, pop_size):
            if get_cost(population[indivi]) < get_cost(best_indivi):
                best_indivi = population[indivi][:]
                # mostra onde houve alteracao
                print('Iter %d: Melhor circuito: %s - Custo: %d' % (indivi, str(best_indivi), get_cost(best_indivi)))

        print('Iter %d: Melhor circuito: %s - Custo: %d' % (i+ 1, str(best_indivi), get_cost(best_indivi)))

graph = GraphGenerator(20)
print('=====================  RANDOM  =====================')
graph.pcv_random(1000)
print('===================== GENÉTICO =====================')
graph.pcv_genetic(pop_size=1000, generations=1000, tournament_size=2, prob_cross=0.7, prob_mutation=0.2)
