import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller
import numpy as np


env = Environment(experiment_name=experiment_name,
				  playermode="ai",
				  player_controller=player_controller(),
			  	  speed="normal",
				  enemymode="static",
				  level=2)



pop_size = 10
gen_size = 3
min_weight = -1
max_weight = 1

n_hidden = env.player_controller.n_hidden[0]
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

start_pop = np.random.uniform(min_weight, max_weight, (pop_size, n_vars))

prin


