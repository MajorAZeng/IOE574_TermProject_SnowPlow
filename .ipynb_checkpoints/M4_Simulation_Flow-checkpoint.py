# This is the Run File
from M0_Class_Map_Road import Map
from M1_Trip_Generation_Module import Generate_Trips
from M2_Plowing_Simulatoin_Module import Run_Snowplow_Simulation
from M3_Travel_Simulation_Module import Run_Travel_Simulation
from tqdm import tqdm
import copy

def Gen_Map_Trip_Assignment (map_info_path, trip_origin_path, trip_destination_path, simulation_hours):
    
    # Module 0
    # Create a based map
    M = Map(map_info_path)

    # Module 1
    # Generate trips
    Generate_Trips(M, trip_origin_path, trip_destination_path,simulation_hours)

    return M

    
def Run_Simulation(M,  snow_depth, simulation_hours,
                    plow_num, plow_start_points, plow_speed, num_reps):
    
    # Module 0
    # Experience a snow event
    M.Experience_Snow(snow_depth)
    
    # Set Up Record List
    Travel_Time_Record = []
    Plow_Time_Record = []
    # Run a number of 
    for _ in tqdm(range(int(num_reps))):

        # Deep Copy Map
        M_rep = copy.deepcopy(M)
        
        # Module 2
        # Simulation Plowing Time
        Run_Snowplow_Simulation(plow_num, plow_start_points, M_rep, plow_speed, simulation_hours)
        plow_time = M_rep.roads.plow_time
        
        # Module 3
        # Simulation Travel Time
        travel_time = Run_Travel_Simulation(M_rep)

        # Record
        Travel_Time_Record.append(travel_time)
        Plow_Time_Record.append(plow_time)

    return Travel_Time_Record, Plow_Time_Record





