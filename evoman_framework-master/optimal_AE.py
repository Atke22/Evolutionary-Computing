import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller
import numpy as np

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
	return  f

def make_fit_list(data):
	return [i['fitness'] for i in data]

def sum_fit_list(data):
	return sum(make_fit_list(data))

pop_size = 10
gen_size = 3
min_weight = -1
max_weight = 1

n_hidden = env.player_controller.n_hidden[0]
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons
start_pop = np.random.uniform(min_weight, max_weight, (pop_size, n_vars))

data = []

for kid in start_pop:
	fit = fitness(kid)
	data.append({
			'weights' : kid,
			'fitness' : fit
		})


print(make_fit_list(data))
print(sum_fit_list(data))