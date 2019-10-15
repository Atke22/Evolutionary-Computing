import sys, os
# sys.path.insert(0, 'evoman') 
# from environment import Environment
# from demo_controller import player_controller
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import glob
from scipy import stats
henk2 = []
algorithms = ['alg1', 'alg2']
for alg in algorithms:
	average_fitness = []
	fit_std = []
	maximum = []
	minimum = []
	runs = glob.glob('results/' + alg +  '/*/*general*[0-9].csv')
	for run in runs:
		fitness = []
		std = []
		maxi = []
		mini = []
		with open(run, 'r') as data_file:
			lines = data_file.read().splitlines()
			for line in lines:
				henk = json.loads(line)
				fitness.append(np.average(henk['fitness']))
				std.append(np.std(henk['fitness']))
				maxi.append(max(henk['fitness']))
				mini.append(min(henk['fitness']))


		for i in range(len(fitness)):
			if i < len(average_fitness):
				average_fitness[i].append(fitness[i])
				fit_std[i].append(std[i])
				maximum[i].append(maxi[i])
				minimum[i].append(mini[i])

			else:
				average_fitness.append([fitness[i]])
				fit_std.append([std[i]])
				maximum.append([maxi[i]])
				minimum.append([mini[i]])

		last_line = lines[-1]
		henk = json.loads(last_line)
		for fitness in henk['fitness']:
			henk2.append([run, fitness])
	average_fitness = [np.average(i) for i in average_fitness]
	fit_std = [np.average(i) for i in fit_std]
	maximum = [np.average(i) for i in maximum]
	minimum = [np.average(i) for i in minimum]

	plt.errorbar(range(len(average_fitness)), average_fitness, fit_std, alpha=0.5, label=alg)
	plt.plot(range(len(maximum)), maximum, 'o', label=alg)
	plt.plot(range(len(maximum)), minimum, 'o', label=alg)
plt.legend()
plt.show()

piet = sorted(henk2, key=lambda x: x[1])
print(piet[-10:])

# positions_1 = [int(i[2])*5  for i in boxplot_data if i[1] == '1']
# positions_2 = [1 + int(i[2])*5  for i in boxplot_data if i[1] == '2']

# labels = ['level ' + i[2] for i in boxplot_data if i[1] == '2']
# label_positions = [i - 0.5 for i in positions_2]

# for i in range(len(max_fitness_1)):

# 	boxplot1 = plt.boxplot(max_fitness_1[i], widths=0.5, positions=[0], patch_artist=True)
# 	boxplot2 = plt.boxplot(max_fitness_2[i], widths=0.5, positions=[1], patch_artist=True)
# 	for box in boxplot1['boxes']:
# 		box.set_facecolor('black')

# 	for box in boxplot2['boxes']:
# 		box.set_facecolor('blue')


# 	blue_patch = mpatches.Patch(color='blue', label='Algorithm 2')
# 	black_patch = mpatches.Patch(color='black', label='Algorithm 1')
# 	plt.legend(handles=[black_patch, blue_patch])

# 	plt.xticks([])
# 	plt.ylabel('Fitness')
# 	plt.show()

# ttest_data = []
# for i in range(len(max_fitness_1)):
# 	print(max_fitness_1[i])
# 	print(max_fitness_2[i])
# 	W1, p1 = stats.shapiro(max_fitness_1[i])
# 	W2, p2 = stats.shapiro(max_fitness_2[i])
# 	st, p = stats.ttest_ind(max_fitness_1[i], max_fitness_2[i])
# 	stn, pn = stats.mannwhitneyu(max_fitness_1[i], max_fitness_2[i])

# 	ttest_data.append({'shapiro1': [W1, p1], 'shapiro2': [W2, p2] , 'ttest': [st,p], 'mannwhitneyu': [stn, pn] })

# # print(ttest_data)
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

