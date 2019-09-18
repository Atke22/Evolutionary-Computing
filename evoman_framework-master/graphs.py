import numpy as np
import matplotlib.pyplot as plt
file = 'results/gen3_groteremutatie.csv'


with open(file, 'r') as data:
	for line in data:
		fitnesses = line.strip().split(",")
		fitnesses = [float(i) for i in fitnesses]
		average = np.average(fitnesses)
		std = np.std(fitnesses)
		print(average, std, max(fitnesses) )