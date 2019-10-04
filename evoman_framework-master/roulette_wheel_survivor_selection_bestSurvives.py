import numpy as np
import copy


dictionary = [{"weights": np.array([1,2,3]), "fitness": 4}, {"weights": np.array([4,5,6]), "fitness": 8}, {"weights": np.array([7,8,9]), "fitness": 1}]

# selects genomes to be killed
# individuals with the highest fitness values have the highest chance of survival
# best individual is always selected
def roulette_wheel_survivor_selection(population, n_survivors):
	survivors = []
	
	#add the best single individual to the survivors
	index_best_individual = 0
	for i in range(1, len(population)):
		if population[i]['fitness'] > population[index_best_individual]['fitness']:
			index_best_individual = i
	survivors.append(copy.copy(population[index_best_individual]))
	population[index_best_individual]['fitness'] = 0
	
	#the other survivors are determined using the roulette wheel
	for survivor in range(n_survivors-1):
		sum_fitness = sum_list(population, 'fitness')
		random_number = np.random.uniform(0, 1)
		c = 0
		
		for individual in population:
			c = c + individual['fitness']/sum_fitness
			if c >= random_number:
				survivors.append(copy.copy(individual))
				individual['fitness'] = 0
				break
	return survivors





def make_list(data,key):
	return [i[key] for i in data]

def sum_list(data, key):
	return sum(make_list(data,key))

pop = roulette_wheel_survivor_selection(dictionary, 2)
print(pop)

