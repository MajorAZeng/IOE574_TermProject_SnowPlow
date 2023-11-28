# Kate 
# Fack by Major

import numpy.random as random

def Fack_Plow_Simulation(Map):

        Map.roads['plow_time'] = random.uniform(low=0, high=12*60, size=len(Map.roads))