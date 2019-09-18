import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller
import numpy as np
import random as rand
import copy

experiment_name = 'dummy_demo'
if not os.path.exists(experiment_name):
	os.makedirs(experiment_name)


env = Environment(experiment_name=experiment_name,
				  playermode="ai",
				  player_controller=player_controller(),
				  speed="fastest",
				  enemymode="static",
				  level=2)


def fitness(kid):
	f, pl, el, gt = env.play(pcont=kid)
	if f < 0.000001:
		f = 0.000001
	return  f

def make_fit_list(data):
	return [i['fitness'] for i in data]

def make_kids_list(data):
	return [i['weights'] for i in data]

def sum_fit_list(data):
	return sum(make_fit_list(data))


def speeddate (pop, numParing, numK): #input is pop&fitness array, aantal koppeltje, aantal parents waaruit je selecteert
	
	NumPossibleParents=len(pop) 

	possible_parents = rand.sample(pop, k=numParing)
	for parent in possible_parents:
		desperate_people = rand.sample(pop, k=numK)
		# print(desperate_people)
		perfect_partner = sorted(desperate_people, key=lambda x: x['fitness'])[-1]
		# print(perfect_partner)
		kiddo1, kiddo2 = crossover_uniform(perfect_partner['weights'], parent['weights'])
		pop.extend([{
				'weights' : kiddo1,
				'fitness' : fitness(kiddo1)
				}, {
				'weights' : kiddo2,
				'fitness' : fitness(kiddo2)
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

def save_data(kid_list, save_file):
	with open(save_file, 'a') as csvfile:
		new_line = ','.join(str(kid['fitness']) for kid in kid_list)
		csvfile.write(new_line + '\n')


pop_size = 20
gen_number = 10
min_weight = -1
max_weight = 1

n_hidden = env.player_controller.n_hidden[0]
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

offspring_num = int(pop_size/4)
num_potential_partners = 4
## haha 
Jorien = 0.1 * n_vars
Inge = 0.1



start_pop = np.random.uniform(min_weight, max_weight, (pop_size, n_vars))

data = []

for kid in start_pop:
	fit = fitness(kid)
	data.append({
			'weights' : kid,
			'fitness' : fit
		})

for i in range(gen_number):
	
	# create new offspring 
	data = speeddate(data, offspring_num, num_potential_partners)
	
	# select which inididuals will go the next generation
	data = roulette_wheel_survivor_selection(data, pop_size)
	
	best_individual = sorted(data, key=lambda x: x['fitness'])[-1]
	print(best_individual['fitness'])



