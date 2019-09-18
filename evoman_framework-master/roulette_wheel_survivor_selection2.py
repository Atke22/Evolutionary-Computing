import numpy as np

npop = 5
pop = [[1,1,1], [2,2,2], [3,3,3], [4,4,4], [5,5,5], [6,6,6], [7,7,7]]
fit_pop = [7, 6, 9, 3, 2, 10, 8]


# selects genomes to be killed
# individuals with the highest fitness values have the highest chance of survival
def roulette_wheel_survivor_selection(pop, fit_pop, n_survivors):
    survivors = []
    fit_survivors = []
    
    for survivor in range(n_survivors):
        sum_fitness = np.sum(fit_pop)
        random_number = np.random.uniform(0, 1)
        c = 0
        
        for individual in range(len(pop)):
            c = c + fit_pop[individual]/sum_fitness
            if c >= random_number:
                survivors.append(pop[individual])
                fit_survivors.append(fit_pop[individual])
                pop.remove(pop[individual])
                fit_pop.remove(fit_pop[individual])
                break
    
    return survivors, fit_survivors

pop, fit_pop = roulette_wheel_survivor_selection(pop, fit_pop, npop)

print(pop)
print(fit_pop)