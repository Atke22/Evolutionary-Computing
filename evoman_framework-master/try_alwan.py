import sys, os
sys.path.insert(0, 'evoman') 
from environment import Environment
from demo_controller import player_controller
import numpy as np

experiment_name = 'dummy_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# initializes environment with ai player using random controller, playing against static enemy
env = Environment(experiment_name=experiment_name,
				  playermode="ai",
				  player_controller=player_controller(),
			  	  speed="normal",
				  enemymode="static",
				  level=2)

n_hidden = env.player_controller.n_hidden[0]
n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

n = np.zeros(n_vars)+0.5

a = env.play(pcont=n)

