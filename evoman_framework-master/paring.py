import numpy as np
from random import randrange



def paring_regular(mother, father):
	child = mother
	mix_len = child.size / 2
	child[mix_len:] = father[mix_len:]
	return child

def paring_random(mother,father):
	child = mother
	child_len = child.size
	mix_len = child_len / 2
	is_changed = np.zeros(child.size)
	change_count = 0
	while change_count < mix_len:
		loc = randrange(child_len)
		if is_changed[loc] == 0:
			is_changed[loc] = 1
			child[loc] = father[loc]
			change_count += 1	
	return child

def crossover1(mother, father):
	cross_point = randrange(1,mother.size-1) # could also be exactly at middle
	print mother, father
	child1 = np.concatenate((mother[:cross_point],father[cross_point:]))
	print mother, father
	child2 = np.concatenate((father[:cross_point],mother[cross_point:]))
	return child1, child2

def crossover_uniform(mother, father):
	child_size = mother.size
	for i in range(child_size):
		cross_choice = randrange(2)
		if cross_choice == 1:
			mother_plh = mother[i]
			mother[i] = father[i]
			father[i] = mother_plh
	return mother, father




mother = np.empty(10)
mother.fill(2)

#print mother

father = np.empty(10)
father.fill(3)

#print father

#print paring_regular(mother, father)
#print paring_random(mother, father)
#print crossover1(mother, father)
print crossover_uniform(mother, father)


# dit is gemaakt voor 1 kind per ouders, veel "standaard" crossover algoritmes maken 2 kinderen per ouders.
# ideeen: de functies houden nu aan dat precies de helft van de waarden van elke ouder wordt overgenomen (mix_len), maar dit zou evt ook nog verandert kunnen worden (betere individuen hebben meer invloed op de offspring van de ouders)

# https://pdfs.semanticscholar.org/3bda/cac99759ca1c71e241b815ea50226b05af70.pdf
# https://en.wikipedia.org/wiki/Crossover_(genetic_algorithm)
# https://pdfs.semanticscholar.org/bcac/ca28249e967e1c3b8af0d257ec76aa0ec312.pdf <<--- vergelijkt crossover voor neural networks