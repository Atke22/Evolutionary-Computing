import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller
import numpy as np

experiment_name = 'dummy_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# # initializes environment with ai player using random controller, playing against static enemy
# env = Environment(experiment_name=experiment_name,
# 				  playermode="ai",
# 				  player_controller=player_controller(),
# 			  	  speed="normal",
# 				  enemymode="static",
# 				  level=2)

# n_hidden = env.player_controller.n_hidden[0]
# n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

# n = np.zeros(n_vars) + 0.5

def fitness(kid):
	f, pl, el, gt = env.play(pcont=kid)
	return f

# fitness(n)

def norm_fitness(fitness_list):
	mini = np.amin(fitness_list)
	fitness_list -= mini
	return fitness_list/np.sum(fitness_list)


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



def save_data(kid_fitness_list, save_file):
	with open(save_file, 'a') as csvfile:
		new_line = ','.join(str(kid_fitness) for kid_fitness in kid_fitness_list)
		csvfile.write(new_line + '\n')
