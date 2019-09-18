import numpy as np
import copy
npop = 5
pop = [[1,1,1], [2,2,2], [3,3,3], [4,4,4], [5,5,5], [6,6,6], [7,7,7]]
fit_pop = [7, 6, 9, 3, 2, 10, 8]

dictionary = [{"weights": np.array([1,2,3]), "fitness": 4}, {"weights": np.array([1,2,3]), "fitness": 8}, {"weights": np.array([1,2,3]), "fitness": 1}]
# selects genomes to be killed
# individuals with the highest fitness values have the highest chance of survival
def roulette_wheel_survivor_selection(population, n_survivors):
    survivors = []
    #fit_survivors = []
    
    for survivor in range(n_survivors):
        sum_fitness = np.sum(make_fit_list(population))
        random_number = np.random.uniform(0, 1)
        c = 0
        
        for individual in population:
            c = c + individual['fitness']/sum_fitness
            if c >= random_number:
                survivors.append(copy.copy(individual))
                individual['fitness'] = 0
                break
    return survivors


def make_fit_list(data):
    return [i['fitness'] for i in data]



pop = roulette_wheel_survivor_selection(dictionary, 2)

print(pop)
#print(fit_pop)