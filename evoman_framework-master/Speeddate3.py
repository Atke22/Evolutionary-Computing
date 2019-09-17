# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 14:33:06 2019

@author: jorie_000
"""

import numpy as np

def speeddate (pop, numParing, numK):
    NumPossibleParents=len(pop[0]) #checken
    
    for j in range (0, numParing,1):
        p1 = np.random.randint(0,NumPossibleParents)
        fitp1 = pop[1,p1]
      
        k = np.empty((numK,2),dtype=float) #array met kandidaten
        for i in range (numK):
            k[i,0] = np.random.randint(0,NumPossibleParents)
            k[i,1] = fit[int(k[i,0])]
         
        h = k[k[:,1].argsort()[::-1]] #sorteert in descending order
        print (h)
        p2=h[0,0]
        print ('p2', p2)
        #kid = crossover (p1, p2)
        #kid ergens opslaan in de array of doet crossover functie dat?
    return p1,p2

z=np.array(([0,1,2,3,4],[3.3,2.2,4.1,1.4,5.3]))
speeddate (z, 3, 4)