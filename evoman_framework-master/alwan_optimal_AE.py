import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller
import numpy as np
import random as rand
import copy
import json

experiment_name = 'dummy_demo'
if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)



##########################################################
# variables



level = 3
pop_size = 100
gen_number = 500
min_weight = -1
max_weight = 1

env = Environment(experiment_name=experiment_name,
				  playermode="ai",
				  player_controller=player_controller(),
				  speed="fastest",
				  enemymode="static",
				  level=2,
				  enemies=[level])



n_hidden = env.player_controller.n_hidden[0]
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

offspring_num = int(pop_size/2)
num_potential_partners = int(pop_size/10)
## haha 
Jorien = 0.1 * n_vars
Inge = 0.2
best_fitness = 0




# end variables
##########################################################

def find_next_file():
	i = 0 
	file_name = 'results/level_' + str(level) + '_run_'
	while os.path.exists(file_name + str(i) + '.csv'):
		i+=1

	file_name += str(i) 
	return file_name + '.csv', file_name + '_weigths.csv', file_name + '_best.csv'


def fitness(kid):
	f, pl, el, gt = env.play(pcont=kid)
	if f < 0.000001:
		f = 0.000001
	return  f, pl, el, gt

def make_list(data,key):
	return [i[key] for i in data]

def sum_list(data, key):
	return sum(make_list(data,key))


def speeddate (pop, numParing, numK): #input is pop&fitness array, aantal koppeltje, aantal parents waaruit je selecteert
	
	for i in range(numParing):
		parent = sorted(rand.sample(pop, k=numK), key=lambda x: x['fitness'])[-1]
		perfect_partner = sorted(rand.sample(pop, k=numK), key=lambda x: x['fitness'])[-1]
		if np.array_equal(parent['weights'], perfect_partner['weights']):
			i-=1
			continue

		# print(perfect_partner)

		kiddo1, kiddo2 = crossover_uniform(perfect_partner['weights'], parent['weights'])
		fit, pl, el, gt = fitness(kiddo1)
		fit2, pl2, el2, gt2 = fitness(kiddo2)
		pop.extend([{
				'weights' : kiddo1,
				'fitness' : fit,
				'player_life' : pl,
				'enemy_life' : el,
				'game_time' : gt
				}, {
				'weights' : kiddo2,
				'fitness' : fit,
				'player_life' : pl2,
				'enemy_life' : el2,
				'game_time' : gt2
				}
		])

	return pop

def mutation_N_weigths_max_mutate(kid, weigths_c, max_mutate):
	weigths_c = int(weigths_c)
	## can't loop using for...in, as choice returns new list
	for i in np.random.choice(kid.size, weigths_c,replace=False):
		kid[i] += np.random.uniform(-max_mutate, max_mutate)
		if kid[i] > 1:
			kid[i] = 1

		elif kid[i] < -1:
			kid[i] = -1
	return kid



def crossover_uniform(mother, father):
	
	# every gene is iterated over
	child_size = mother.size
	for i in range(child_size):
		
		# a random number between 0 and 1 is chosen
		cross_choice = np.random.uniform(0,1)
		
		# when this number is greater than .5 the gene of the mother and father are switched
		if cross_choice > .5:
			mother_plh = mother[i]
			mother[i] = father[i]
			father[i] = mother_plh
	

	father_kiddo = mutation_N_weigths_max_mutate(father, Jorien, Inge)
	mother_kiddo = mutation_N_weigths_max_mutate(mother, Jorien, Inge)

	return mother_kiddo, father_kiddo

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



def save_best(best_individual):
	with open(best_file, 'w') as best:
		best.write(json.dumps(best_individual['weights'].tolist()))



def continue_old_run(weightsfile):
	data = []
	with open(weightsfile, 'r') as data_file:
		for line in data_file:
			kid = json.loads(line)
			np_array = np.asarray(kid['weights'])
			kid['weights'] = np_array
			data.append(kid)

	return data


start_pop = np.random.uniform(min_weight, max_weight, (pop_size, n_vars))

data = []


file_name, weights_file, best_file = find_next_file()


# weights_file = 'results/level_2_run_0_weigths.csv'



# data = continue_old_run(weights_file)


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
	data = speeddate(data, offspring_num, num_potential_partners)
	
	# select which inididuals will go the next generation
	data = roulette_wheel_survivor_selection(data, pop_size)
	
	fitness_std = np.std(make_list(data, 'fitness'))
	if fitness_std > 20:
		Jorien/=1.1
	elif fitness_std < 10:
		Jorien*=1.1
	if Jorien > n_vars:
		Jorien = n_vars

	best_individual = sorted(data, key=lambda x: x['fitness'])[-1]
	if best_individual['fitness'] > best_fitness:
		best_fitness = best_individual['fitness']
		save_best(best_individual)
	# print(best_individual['fitness'])
	save_data(data)



