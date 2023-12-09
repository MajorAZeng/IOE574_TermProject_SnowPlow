from M4_Simulation_Flow import Gen_Map_Trip_Assignment, Run_Case_Simulation
from M5_Post_Processing import Write_Log
import os
import time
import sys

def Run_Sim_5_Central_Cases(version_name, num_reps):

    # Start Timing
    start_time = time.time()
    print('[Run Start]')

    # General Parameters
    map_info_path = 'Data/AA_Map_Final.gpkg'
    trip_origin_path = 'Data/your_locations.csv'
    trip_destination_path = 'Data/your_destinations.csv'
    simulation_hours = 4
    plow_speed = 15

    # Create Result Folder
    os.makedirs('Result_'+version_name)
    log_file_name = 'Result_'+version_name+'/Run_Log.txt'

    # Scenario Set Up
    Write_Log(log_file_name, '== Setting Up Base Map and Trip Assignment ==')
    M = Gen_Map_Trip_Assignment(map_info_path, trip_origin_path, trip_destination_path, simulation_hours)
    Write_Log(log_file_name, 'time: '+str(round((time.time()-start_time)/60, 2))+' min')

    # Case 1: No Snow, No Plow
    case_num = '1'
    Write_Log(log_file_name, '== Run Case '+case_num+': No Snow, No Plow ==')
    # Other Parameters
    snow_depth = 0
    plow_num = 0
    plow_start_points = []
    # Run Case
    Run_Case_Simulation(version_name, num_reps, log_file_name,
                        M, simulation_hours, plow_speed,
                        case_num, snow_depth, plow_num, plow_start_points)
    Write_Log(log_file_name, 'time: '+str(round((time.time()-start_time)/60, 2))+' min')

    # Case 2: 4in Snow, No Plow
    case_num = '2'
    Write_Log(log_file_name, '== Run Case ' + case_num + ': 4in Snow, No Plow ==')
    # Other Parameters
    snow_depth = 4
    plow_num = 0
    plow_start_points = []
    # Run Case
    Run_Case_Simulation(version_name, num_reps, log_file_name,
                        M, simulation_hours, plow_speed,
                        case_num, snow_depth, plow_num, plow_start_points)
    Write_Log(log_file_name, 'time: '+str(round((time.time()-start_time)/60, 2))+' min')

    # Case 3: 4in Snow, 1 Plow from Downtown
    case_num = '3'
    Write_Log(log_file_name, '== Run Case ' + case_num + ': 4in Snow, 1 Plow from Downtown ==')
    # Other Parameters
    snow_depth = 4
    plow_num = 1
    plow_start_points = [151]
    # Run Case
    Run_Case_Simulation(version_name, num_reps, log_file_name,
                        M, simulation_hours, plow_speed,
                        case_num, snow_depth, plow_num, plow_start_points)
    Write_Log(log_file_name, 'time: '+str(round((time.time()-start_time)/60, 2))+' min')

    # Case 4: 4in Snow, 2 Plow from Downtown
    case_num = '4'
    Write_Log(log_file_name, '== Run Case ' + case_num + ': 4in Snow, 2 Plow from Downtown ==')
    # Other Parameters
    snow_depth = 4
    plow_num = 2
    plow_start_points = [151, 151]
    # Run Case
    Run_Case_Simulation(version_name, num_reps, log_file_name,
                        M, simulation_hours, plow_speed,
                        case_num, snow_depth, plow_num, plow_start_points)
    Write_Log(log_file_name, 'time: '+str(round((time.time()-start_time)/60, 2))+' min')

    # Case 5: 4in Snow, 2 Plow from Two Corners of AA
    case_num = '5'
    Write_Log(log_file_name, '== Run Case ' + case_num + ': 4in Snow, 2 Plow from Two Corners of AA ==')
    # Other Parameters
    snow_depth = 4
    plow_num = 2
    plow_start_points = [218, 141]
    # Run Case
    Run_Case_Simulation(version_name, num_reps, log_file_name,
                        M, simulation_hours, plow_speed,
                        case_num, snow_depth, plow_num, plow_start_points)
    Write_Log(log_file_name, 'time: ' + str(round((time.time() - start_time) / 60, 2)) + ' min')

    print('[Run End]')



if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python Run_Simulation_Central_Cases.py version_name number_reps")
        sys.exit(1)

    version_name = str(sys.argv[1])
    number_reps = int(sys.argv[2])

    Run_Sim_5_Central_Cases(version_name, number_reps)
