# This is the Run File
from M0_Class_Map_Road import Map
from M1_Trip_Generation_Module import Generate_Trips
from M2_Plowing_Simulatoin_Module import Fack_Plow_Simulation

def Run_Simulation_Once(map_info_path, snow_depth, trip_origin_path, trip_destination_path):

    
    # Create a based map
    M = Map(map_info_path)
    # Experience a snow event
    M.Experience_Snow(snow_depth)

    # Generate trips
    Generate_Trips(M,trip_origin_path, trip_destination_path)

    # Simulation Plowing Time
    Fack_Plow_Simulation(M)

    # Simluation all Trips and record
    # 

    return ...  # Some record of the simulation


# Code Block to repead simulaiton n times and record results


# Post processing 







