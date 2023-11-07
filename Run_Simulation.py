# This is the Run File

# Import tool packages
import pandas as pd
import numpy as np
import scipy as sp
# Import all modeuls
import 0_Class_Map_Road
import 1_Trip_Generation_Module
import 2_Plowing_Simulatoin_Module
import 3_Speed_Map_Generation_Module
import 4_Travel_Simulation_Module
import 5_Post_Processing_Module
# 

def Run_Simulation_Once():

    # Create Base Map
    M = Map()
    M.Experience_Snow_Event()

    # Generate trips
    List_Trips = Trip_Generation_Module()

    # Generate Plowing Sequence
    List_of_PlowingMaps = Simulate_Plowing(plowing_sequence)

    # Generate Speed Maps
    List_of_SeedMaps = Simulate_Speed_Map(Map, plowing_simulation)

    # Simluation all Trips and record
    Trip_Records = Simulate_All_Trips(List_Trips, List_of_SeedMaps)

    return ...  # Some record of the simulation


# Code Block to repead simulaiton n times and record results


# Post processing 







