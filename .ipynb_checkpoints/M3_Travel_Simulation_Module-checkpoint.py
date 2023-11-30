# Riley

# Run simulation of all trips in both the road network with no snow and road network after a snowstorm to compare the two scenarios.

#M = Map('AA_Map_Final.gpkg')
#M.Experience_Snow()
#graph = M.graph
#Generate_Trips(M, 'your_locations.csv', 'your_destinations.csv')

def Run_Travel_Simulation(M):
    trip_durations = []

    # Loop through every trip from module 1
    for trip in M.trips:
        current_time = trip['trip_start_time']
        #path_to_store = find_shortest_path(graph, nearest_node(graph, Point(trip.start_longitude, trip.start_latitude)), nearest_node(graph, Point(trip.destination_longitude, trip.destination_latitude)))
        #path_from_store = find_shortest_path(graph, nearest_node(graph, Point(trip.destination_longitude, trip.destination_latitude)), nearest_node(graph, Point(trip.start_longitude, trip.start_latitude)))
        
        # Loop through every road taken to store
        # See if the road has been plowed at the current time and calculate travel time on that road based on the road's condition
        for elem in trip['path_to_store']:
            road = M.roads.iloc[elem,]
            if road['plow_time'] < current_time:
                time_on_road = 60*road['length']/road['normal_speed']
            else:
                time_on_road = 60*road['length']/road['speed_after_snow']
            current_time += time_on_road

        # Add time spent in grocery store to the trip duration
        current_time += trip['duration']        
        
        for elem in trip['path_from_store']:
            road = M.roads.iloc[elem,]
            if road['plow_time'] < current_time:
                time_on_road = 60*road['length']/road['normal_speed']
            else:
                time_on_road = 60*road['length']/road['speed_after_snow']
            current_time += time_on_road
        
        trip_durations.append(current_time - trip['trip_start_time'])
    
    
    return trip_durations

# simulate_one_day = run_simulation(M, graph)
