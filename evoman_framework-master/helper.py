import numpy as np
import random as rand
import copy
import json



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



def continue_old_run(weightsfile):
	data = []
	with open(weightsfile, 'r') as data_file:
		for line in data_file:
			kid = json.loads(line)
			np_array = np.asarray(kid['weights'])
			kid['weights'] = np_array
			data.append(kid)

	return data


def make_list(data,key):
	return [i[key] for i in data]

def sum_list(data, key):
	return sum(make_list(data,key))