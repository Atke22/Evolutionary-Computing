# imports framework
import sys
sys.path.insert(0, 'evoman')
from environment import Environment
from demo_controller import player_controller

# imports other libs
#import time
import numpy as np
#from math import fabs,sqrt
import glob, os


experiment_name = 'individual_demo'
if not os.path.exists(experiment_name):
    os.makedirs(experiment_name)

# initializes simulation in individual evolution mode, for single static enemy.
env = Environment(experiment_name=experiment_name,
                  enemies=[2],
                  playermode="ai",
                  player_controller=player_controller(),
                  enemymode="static",
                  level=2,
                  speed="fastest")




# de input van play in zijn de environment en bij pcont een array van alle weights voor de neurons. 

# dom_l = -1
# dom_u = 1
# npop = 2
# n_hidden = 10
# n_vars = (env.get_num_sensors()+1)*n_hidden + (n_hidden+1)*5 
# pop = np.random.uniform(dom_l, dom_u, (npop, n_vars))
# print pop
# print n_vars
# def simulation(env,x):
# 	print 'DIT IS X'
# 	if np.array_equal(x,pop[0]):
# 		print 'You got it :) '
# 	else:
# 		print 'but really??'
# 	print x
# 	f,p,e,t = env.play(pcont=pop[0])
# 	print 'f'
# 	print f
# 	print 'p'
# 	print p
# 	print 'e'
# 	print e
# 	print 't'
# 	print t
# 	return f

# def evaluate(x):
# 	return np.array(list(map(lambda y: simulation(env,y), x)))

# r = evaluate(pop)
# print r
# print pop[0]
#################### data storage ###############################

# how to save configurations of the weights ??? <<< numpy array :) 
# numerical weights to 'phenotype' <<< dit doet play al voor je


###################### evolution ###############################

# create offspring
## pair "Parents"
## mix "genes"

# mutations (random genes)

# selection
## remove (some of the) worst contestants
## maybe remove some random contestants of the middle mode

##################### other functions #########################

# save files with:
## the best contestants and their weights, run time, etc, etc.







