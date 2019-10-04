#############################################################
#															#
# Evolutionary Algorithm 2								 	#
# Inge Bieger, Jorien Lokker, Alwan Rashid, Atke Visser  	#
#															#
#############################################################


# imports framwork
import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller

# imports other libraries
import numpy as np
import random as rand
import copy
import json

# creates directory
experiment_name = 'dummy_demo'
if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)


# do you want to continue your old run?
continue_run = False
continue_file = 'results/'


# initialises the framework. enemy number can be changed accordingly

enemy = 2

env = Environment(experiment_name=experiment_name,
				  playermode="ai",
				  player_controller=player_controller(),
				  speed="fastest",
				  enemymode="static",
				  level=2,
				  enemies = [2])




# calculates the number of weights per agent
n_hidden = env.player_controller.n_hidden[0] 
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 

best_fitness = 0
min_weight = -1
max_weight = 1


# parameter settings of the algorithm
pop_size = 100
gen_number = 100
runs = 10
mutation_rate = 0.1
parent_fraction = 0.5
partner_fraction = 0.1
mutation_value = 0.2

paring_num = int(pop_size * parent_fraction)
num_potential_partners = int(pop_size * partner_fraction)




# runs simulations and returns the fitness, game time, enemy life and player life 
def fitness(kid):
	fit, pl, el, gt = env.play(pcont=kid)
	if fit < 0.000001:
		fit = 0.000001
	return  fit, pl, el, gt

# selects parents and creates offspring
def speeddate (pop, num_paring, num_selection): 
	
	# selects numParing parents
	for i in range(num_paring):
		
		# selects a random sample of numK agents and chooses the best to be a parent (twice)
		parent1 = sorted(rand.sample(pop, k=num_selection), key=lambda x: x['fitness'])[-1]
		parent2 = sorted(rand.sample(pop, k=num_selection), key=lambda x: x['fitness'])[-1]
		
		# checks that parents are not equal to each other and selects other parents otherwise
		if np.array_equal(parent1['weights'], parent2['weights']):
			i-=1
			continue

		# generates two offspring for from a parent pair
		offsprings = crossover_uniform(parent1['weights'], parent2['weights'])
		
		for offspring in offsprings: 
			# finds fitness of the offspring
			fit, pl, el, gt = fitness(offspring)
		
		
		# adds offspring to population
			pop.extend([{
					'weights' : offspring,
					'fitness' : fit,
					'player_life' : pl,
					'enemy_life' : el,
					'game_time' : gt
					}
			])

	# returns new population
	return pop

# makes two offspring from two parents
def crossover_uniform(parent1, parent2):
	parent1 = copy.deepcopy(parent1)
	parent2 = copy.deepcopy(parent2)
	# iterates over every gene
	child_size = parent1.size
	for i in range(child_size):
		
		# randomly switches genes of parent 1 and parent 2 with a chance of 50%
		cross_choice = np.random.uniform(0,1)
		
		if cross_choice > .5:
			parent1_placeholder = parent1[i]
			parent1[i] = parent2[i]
			parent2[i] = parent1_placeholder
	
	# mutates the weights of the offspring
	offspring1 = mutation(parent1, mutation_count, mutation_value)
	offspring2 = mutation(parent2, mutation_count, mutation_value)

	return offspring1, offspring2

# gives mutation to agent
def mutation(agent, mut_count, mut_value):
	mut_count = int(mut_count)
	agent = copy.deepcopy(agent)
	# selects mut_count weights of agent
	for i in np.random.choice(agent.size, mut_count,replace=False):
		
		# changes value of weight by random number between -mut_value and +mut_value 
		agent[i] += np.random.uniform(-mut_value, mut_value)
		
		# normalises weights between -1 and 1
		if agent[i] > 1:
			agent[i] = 1

		elif agent[i] < -1:
			agent[i] = -1
	
	return agent

# selects which individuals survive for the next generation
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
		
		# calculates the total fitness of the population
		sum_fitness = sum_list(population, 'fitness')
		
		# generates the pointer on the roulettewheel
		random_number = np.random.uniform(0, 1)
		c = 0
		
		# places every individual on the roulette wheel
		for individual in population:
			
			# the size of the individual is its fraction of the total fitness
			c = c + individual['fitness']/sum_fitness
			
			# adds individual to survivor, when the pointer is on the same location as the individual   
			if c >= random_number:
				survivors.append(copy.copy(individual))
				individual['fitness'] = 0
				break
	
	return survivors


# makes a list values of a certain key in a dictionary list
def make_list(data,key):
	return [i[key] for i in data]

# calcuates the sum of all the values of a of a certain key in a dictionary list
def sum_list(data, key):
	return sum(make_list(data,key))

# finds suitable name for the csv file of a run
def find_next_file():
	i = 0 
	file_name = 'results/level_' + str(enemy) + '_run_'
	while os.path.exists(file_name + str(i) + '.csv'):
		i+=1

	file_name += str(i) 
	return file_name + '.csv', file_name + '_weigths.csv', file_name + '_best.csv'

# saves data of a generation
def save_data(kid_list):
	keys = list(kid_list[0].keys())
	keys.remove('weights')
	data = {}	

	with open(file_name, 'a') as csvfile:
		for key in keys:
			data[key] = make_list(kid_list, key)

		csvfile.write(json.dumps(data) + '\n')


	with open(weights_file, 'w') as weightsfile:
		for kid in kid_list:
			a = kid['weights'].tolist()
			kid['weights'] = a
			weightsfile.write(json.dumps(kid) + '\n')
			np_array = np.asarray(kid['weights'])
			kid['weights'] = np_array


# save the weights of the best individual
def save_best(best_individual):
	with open(best_file, 'w') as best:
		best.write(json.dumps(best_individual['weights'].tolist()))


# opens previous file
def continue_old_run(weightsfile):
	data = []
	with open(weightsfile, 'r') as data_file:
		for line in data_file:
			kid = json.loads(line)
			np_array = np.asarray(kid['weights'])
			kid['weights'] = np_array
			data.append(kid)

	return data



for i in range(runs):
	
	# creates random weigts for population
	start_pop = np.random.uniform(min_weight, max_weight, (pop_size, n_vars))
	file_name, weights_file, best_file = find_next_file()

	if continue_run:
		data = continue_old_run(weights_file)

	data = []
	
	# assigns the weights to the starting population and finds the phenotype and fitness
	for kid in start_pop:
		fit, pl, el, gt = fitness(kid)

		data.append({
				'weights' : kid,
				'fitness' : fit,
				'player_life' : pl,
				'enemy_life' : el,
				'game_time' : gt
			})

	save_data(data)


	mutation_count = int(mutation_rate * n_vars)
	best_fitness = 0
	
	# creates new generation
	for i in range(gen_number):
		
		# create new offspring 
		data = speeddate(data, paring_num, num_potential_partners)
		
		# select which inididuals will go the next generation
		data = roulette_wheel_survivor_selection(data, pop_size)
		

		# alters the mutation_count based on the standard deviation of the generation
		fitness_std = np.std(make_list(data, 'fitness'))
		if fitness_std > 20:
			mutation_count/=1.1
		elif fitness_std < 10:
			mutation_count*=1.1
		if mutation_count > n_vars:
			mutation_count = n_vars

		# stores the weights of the best agent
		best_individual = sorted(data, key=lambda x: x['fitness'])[-1]
		if best_individual['fitness'] > best_fitness:
			best_fitness = best_individual['fitness']
			save_best(best_individual)
		
		# stores the data of the generation
		save_data(data)



