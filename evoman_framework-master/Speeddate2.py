# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 19:08:38 2019

@author: jorie_000
"""
import numpy as np

def speeddate (list, fit, numDood):
    numDood = numDood
    NumPossibleParents=len(list)-numDood
    
    np.sort(list) #order list
    for j in range (0, numDood,1):
        p1 = np.random.randint(0,NumPossibleParents)
        fitp1 = fit[p1]
        
        k = np.empty((4,2),dtype=float) #array met kandidaten
        k[0,0] = np.random.randint(0,NumPossibleParents)
        k[0,1] = fit[int(k[0,0])]
        k[1,0] = np.random.randint(0,NumPossibleParents)
        k[1,1] = fit[int(k[1,0])]
        k[2,0] = np.random.randint(0,NumPossibleParents)
        k[2,1] = fit[int(k[2,0])]
        k[3,0] = np.random.randint(0,NumPossibleParents)
        k[3,1] = fit[int(k[3,0])]
        
        
        print(k)
        h = k[k[:,1].argsort()[::-1]] #sorteert in descending order
        print (h)
        p2=h[0,0]
        print ('p2', p2)
        #kid = crossover (p1, p2)
        #kid ergens opslaan in de array of doet crossover functie dat?
    return k

z=[0,1,2,3,4,5]
fit = [.6,0.5,.4,.3,.2,.1]
speeddate (z, fit, 3)