# Riley

import numpy as np

def Run_Travel_Simulation(M):
    trip_durations = []

    # Loop through every trip from module 1
    for trip in M.trips:
        current_time = trip['trip_start_time']

        # Loop through every road taken to store
        # See if the road has been plowed at the current time and calculate travel time on that road based on the road's condition
        for elem in trip['path_to_store']:
            road = M.roads.iloc[elem,]
            if road['plow_time'] < current_time:
                time_on_road = 60*road['length']/(0.8*np.random.normal(road['normal_speed'], road['normal_speed']/10))
            else:
                time_on_road = 60*road['length']/(0.8*np.random.normal(road['speed_after_snow'], road['speed_after_snow']/10))
            current_time += time_on_road

        # Add time spent in grocery store to the trip duration
        current_time += trip['duration']
        # Add time spent getting from home to nearest node on the way to grocery and from nearest node to home on the way back
        current_time +=  2*np.random.triangular(1, 3, 7)        
        
        for elem in trip['path_from_store']:
            road = M.roads.iloc[elem,]
            if road['plow_time'] < current_time:
                time_on_road = 60*road['length']/(0.8*np.random.normal(road['normal_speed'], road['normal_speed']/10))
            else:
                time_on_road = 60*road['length']/(0.8*np.random.normal(road['speed_after_snow'], road['speed_after_snow']/10))
            current_time += time_on_road

        trip_durations.append(current_time - trip['trip_start_time'] - trip['duration'])
    
    
    return trip_durations

