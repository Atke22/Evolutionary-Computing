import sys, os
# sys.path.insert(0, 'evoman') 
# from environment import Environment
# from demo_controller import player_controller
import numpy as np
import json
import matplotlib.pyplot as plt
# experiment_name = 'dummy_demo'
# if not os.path.exists(experiment_name):
#     os.makedirs(experiment_name)

# # # initializes environment with ai player using random controller, playing against static enemy
# # env = Environment(experiment_name=experiment_name,
# # 				  playermode="ai",
# # 				  player_controller=player_controller(),
# # 			  	  speed="normal",
# # 				  enemymode="static",
# # 				  level=2)

# # n_hidden = env.player_controller.n_hidden[0]
# # n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 # multilayer with 10 hidden neurons

# # n = np.zeros(n_vars) + 0.5

# def fitness(kid):
# 	f, pl, el, gt = env.play(pcont=kid)
# 	return f

# # fitness(n)

# def norm_fitness(fitness_list):
# 	mini = np.amin(fitness_list)
# 	fitness_list -= mini
# 	return fitness_list/np.sum(fitness_list)


# def mutation_N_weigths_max_mutate(kid, weigths_c, max_mutate):
# 	weigths_c = int(weigths_c)
# 	## can't loop using for...in, as choice returns new list
# 	for i in np.random.choice(kid.size, weigths_c,replace=False):
# 		kid[i] += np.random.uniform(-max_mutate, max_mutate)
# 		if kid[i] > 1:
# 			kid[i] = 1

# 		elif kid[i] < -1:
# 			kid[i] = -1
# 	return kid



# def save_data(kid_fitness_list, save_file):
# 	with open(save_file, 'a') as csvfile:
# 		new_line = ','.join(str(kid_fitness) for kid_fitness in kid_fitness_list)
# 		csvfile.write(new_line + '\n')


file_name = 'results/level_2_run_2.csv'

fitness = []
std = []
min_fit = []
max_fit = []

with open(file_name, 'r') as data_file:
	for line in data_file:
		henk = json.loads(line)
		fitness.append(np.average(henk['fitness']))
		std.append(np.std(henk['fitness']))
		min_fit.append(min(henk['fitness']))
		max_fit.append(np.average(sorted(henk['fitness'])[-10:]))


# plt.plot(range(len(fitness)), fitness)
# plt.errorbar(range(len(fitness)), fitness, std)
plt.plot(range(len(std)), std, 'o')

# plt.plot(range(len(min_fit)), min_fit, 'ro')
# plt.plot(range(len(max_fit)), max_fit, 'go')
# plt.plot(range(len(max_fit)), max_fit, 'go')


plt.show()

