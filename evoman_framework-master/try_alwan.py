import sys, os
# sys.path.insert(0, 'evoman') 
# from environment import Environment
# from demo_controller import player_controller
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob

algorithms = ['alg1', 'alg2']
boxplot_data = []
for alg in algorithms:
	for level in range(1,4):
		runs = glob.glob('results/'+ str(alg) + '/*/level_' + str(level) + '*[0-9].csv')
		if not runs:
			runs = glob.glob('results/'+ str(alg) + '/*/Alg1_enemy' + str(level) + '*[0-9].csv')

		fitness = []
		max_fitness = []
		for run in runs:
			with open(run, 'r') as run_data:
				i = 0
				for line in run_data:
					henk = json.loads(line)
					if len(fitness) == i:
						fitness.append([np.average(henk['fitness'])])
						max_fitness.append([max(henk['fitness'])])

					else:
						fitness[i].append(np.average(henk['fitness']))
						max_fitness[i].append(max(henk['fitness']))
					i+=1

		if fitness:
			# std = [np.std(i) for i in fitness]
			# average_fitness = [np.average(i) for i in fitness]
			# average_max_fitness = [np.average(i) for i in max_fitness]
			# std_max = [np.std(i) for i in max_fitness]
			# plt.title('Algorithm: ' + alg[-1] + ', level: ' + str(level))
			# plt.errorbar(range(len(average_fitness)), average_fitness, std)
			# plt.errorbar(range(len(average_max_fitness)), average_max_fitness, std_max)
			# plt.xlabel('Generation')
			# plt.ylabel('Fitness')
			# plt.show()
			boxplot_data.append([max_fitness[-1], alg[-1], str(level)])
boxplot_data = sorted(boxplot_data, key=lambda x: x[2])
max_fitness_1 = [i[0] for i in boxplot_data if i[1] == '1']
max_fitness_2 = [i[0] for i in boxplot_data if i[1] == '2']
positions_1 = [int(i[2])*5  for i in boxplot_data if i[1] == '1']
positions_2 = [1 + int(i[2])*5  for i in boxplot_data if i[1] == '2']

labels = ['level ' + i[2] for i in boxplot_data if i[1] == '2']
label_positions = [i - 0.5 for i in positions_2]

for i in range(len(max_fitness_1)):

	boxplot1 = plt.boxplot(max_fitness_1[i], widths=0.5, positions=[0], patch_artist=True)
	boxplot2 = plt.boxplot(max_fitness_2[i], widths=0.5, positions=[1], patch_artist=True)
	for box in boxplot1['boxes']:
		box.set_facecolor('black')

	for box in boxplot2['boxes']:
		box.set_facecolor('blue')


	blue_patch = mpatches.Patch(color='blue', label='Algorithm 2')
	black_patch = mpatches.Patch(color='black', label='Algorithm 1')
	plt.legend(handles=[black_patch, blue_patch])

	plt.xticks([])
	plt.ylabel('Fitness')
	plt.show()

# print(max_fitness_1)



# scatter_pos_1 = [positions_1[i] for i in range(len(max_fitness_1)) for j in max_fitness_1[i]]
# scatter_pos_2 = [positions_2[i] for i in range(len(max_fitness_2)) for j in max_fitness_2[i]]

# print(scatter_pos_2)
# print(max_fitness_2)
# plt.scatter(scatter_pos_1, max_fitness_1)
# plt.scatter(scatter_pos_2, max_fitness_2)







# jorien  = 0
# inge = 100
# for level in range(1,4):
# 	i = 0
# 	file_name = 'results/level_' + str(level) + '_run_' + str(i) +'.csv'
# 	if not os.path.exists(experiment_name):
# 		i+=1

# 		fitness = []
# 		std = []
# 		min_fit = []
# 		max_fit = []
# 		max_fit_10 = []
# 		min_el = []
# 		max_pl = []
# 		game_time = []
# 		with open(file_name, 'r') as data_file:
# 			for line in data_file:
# 				henk = json.loads(line)
# 				fitness.append(np.average(henk['fitness']))
# 				std.append(np.std(henk['fitness']))
# 				min_fit.append(min(henk['fitness']))
# 				min_el.append(min(henk['enemy_life']))
# 				max_pl.append(max(henk['player_life'])/100)
# 				i = henk['player_life'].index(max(henk['player_life']))
# 				game_time.append(henk['game_time'][i]/1000)
# 				max_fit_10.append(np.average(sorted(henk['fitness'])[-10:]))
# 				max_fit.append(sorted(henk['fitness'])[-1])

# 		plt.plot(range(len(fitness)), fitness)
# 		# plt.errorbar(range(len(fitness)), fitness, std)
# 		# plt.plot(range(len(std)), std)
# 		# plt.plot(range(len(game_time)), game_time)
# 		# plt.plot(range(len(max_pl)), max_pl)
# 		# plt.title('maximum player life')
# 		# plt.plot(range(len(min_fit)), min_fit, 'ro')
# 		plt.plot(range(len(max_fit)), max_fit, 'go')
# 		print(max(max_fit))

# 		plt.show()

