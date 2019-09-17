import numpy as np

npop = 10
#pop = np.random.uniform(0, 1, (npop, 2))
pop = [[1,1,1], [2,2,2], [3,3,3], [4,4,3], [5,5,5]]
#pop = np.array([[1,1,1], [2,2,2], [3,3,3], [4,4,3], [5,5,5]])
#fit_pop = np.random.uniform(1, 11, npop)
fit_pop = [7, 6, 9, 3, 2]
#fit_pop = np.array([7, 6, 9, 3, 2])

offspring = [[6,6], [7,7]]
#offspring = np.array([[6,6], [7,7]])
fit_offspring = [10, 8]
#fit_offspring = np.array([10, 8])

#print(fit_pop)



# selects genomes to be killed and replaces them by offspring
# individuals with the highest fitness values have the highest chance of survival
def roulette_wheel_survivor_selection(pop, fit_pop, offspring, fit_offspring):
    survivors = []
    fit_survivors = []
    n_survivors = len(pop) - len(offspring)
    
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
                #np.delete(pop, individual, 0)
                fit_pop.remove(fit_pop[individual])
                #np.delete(fit_pop, individual, 0)
                break
    
    pop = survivors + offspring
    #pop = np.concatenate((survivors, offspring), axis=0)
    fit_pop = fit_survivors + fit_offspring
    #fit_pop = np.concatenate((fit_survivors, fit_offspring), axis=0)
    return pop, fit_pop

pop, fit_pop = roulette_wheel_survivor_selection(pop, fit_pop, offspring, fit_offspring)

print(pop)
print(fit_pop)