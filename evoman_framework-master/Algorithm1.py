#############################################################
#															#
# Evolutionary Algorithm 1							 	#
# Inge Bieger, Jorien Lokker, Alwan Rashid, Atke Visser  	#
#															#
#############################################################

# imports framework
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
continue_file = ''

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
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

best_fitness = 0
min_weight = -1
max_weight = 1

# parameter settings of the algorithm
pop_size = 10
gen_number = 10
runs = 10
mutation_rate = 0.1
parent_fraction = 0.5
partner_fraction = 0.1
mutation_value = 0.2

paring_num = int(pop_size * parent_fraction)
num_potential_partners = int(pop_size * partner_fraction)




# runs simulations and returns the fitness, game time, enemy life and player life
def fitness(kid):
	f, pl, el, gt = env.play(pcont=kid)
	if f < 0.000001:
		f = 0.000001
	return  f, pl, el, gt

# selects parents and creates offspring
def speeddate (pop, num_paring, numK): #input is pop&fitness array, aantal koppeltje, aantal parents waaruit je selecteert

    # Choose a random parent and a random partner for this parent
	possible_parents = rand.sample(pop, k=num_paring)
	for parent in possible_parents:
		parent_partner = rand.choice(pop)
		
		# if the parent is the same as the partner, choose another partner
		while np.array_equal(parent['weights'], parent_partner['weights']):
			parent_partner = rand.choice(pop)
		
        # generates two offspring for from a parent pair
		offsprings = crossover_uniform(parent_partner['weights'], parent['weights'])
        
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

	return pop

# gives mutation to agent
def mutation(agent, mut_count, mut_value):
	mut_count = int(mut_count)
	
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



# makes two offspring from two parents
def crossover_uniform(parent1, parent2):
	
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
	offspring1 = mutation(parent1, mutation_rate, mutation_value)
	offspring2 = mutation(parent2, mutation_rate, mutation_value)

	return offspring1, offspring2

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
    
	for i in range(gen_number):
    	
    	# create new offspring 
		print(type(data))
		data = speeddate(data, paring_num, num_potential_partners)
    	
    	# select which inididuals will go the next generation
		data = roulette_wheel_survivor_selection(data, pop_size)
    	
		# stores the weights of the best agent
		best_individual = sorted(data, key=lambda x: x['fitness'])[-1]
		if best_individual['fitness'] > best_fitness:
			best_fitness = best_individual['fitness']
			save_best(best_individual)
        
    	# print(best_individual['fitness'])
		save_data(data)