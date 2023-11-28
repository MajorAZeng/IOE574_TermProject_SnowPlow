# Riley

# Run simulation of all trips in both the road network with no snow and road network after a snowstorm to compare the two scenarios.

def run_simulation(graph, all_trips_df, road_network):
    trip_durations_storm = []
    trip_durations_clear = []

    # Loop through every trip from module 1
    for trip in all_trips_df.itertuples():
        trip_start_time = min(480, np.random.triangular(0, 240, 480))
        current_time_clear = trip_start_time
        current_time_storm = trip_start_time
        path_to_store = find_shortest_path(graph, nearest_node(graph, Point(trip.start_latitude, trip.start_longitude)), nearest_node(graph, Point(trip.destination_latitude, trip.destination_longitude)))
        path_from_store = find_shortest_path(graph, nearest_node(graph, Point(trip.destination_latitude, trip.destination_longitude)), nearest_node(graph, Point(trip.start_latitude, trip.start_longitude)))
        
        # Loop through every road taken to store
        # See if the road has been plowed at the current time and calculate travel time on that road based on the road's condition
        for i in range(0, len(path_to_store)-1):
            road = road_network.loc[road_network['osmid'] == graph.edges[path[i], path[i+1]]['osmid']]
            time_on_road_clear = 60*road['length'].array[0]/(1000*road['speed_kph'].array[0])
            if plowed:
                time_on_road_storm = 60*road['length'].array[0]/(1000*road['speed_kph'].array[0])
            else:
                time_on_road_storm = 60*road['length'].array[0]/(1000*road['speed_kph'].array[0])   
            current_time_clear += time_on_road_clear
            current_time_storm += time_on_road_storm

        # Add time spent in grocery store to the trip duration
        current_time_clear += trip.duration
        current_time_storm += trip.duration

        # Loop through every road taken to store
        # See if the road has been plowed at the current time and calculate travel time on that road based on the road's condition
        for i in range(0, len(path_from_storm)-1):
            road = road_network.loc[road_network['osmid'] == graph.edges[path[i], path[i+1]]['osmid']]
            time_on_road_clear = 60*road['length'].array[0]/(1000*road['speed_kph'].array[0])
            if plowed:
                time_on_road_storm = 60*road['length'].array[0]/(1000*road['speed_kph'].array[0])
            else:
                time_on_road_storm = 60*road['length'].array[0]/(1000*road['speed_kph'].array[0])   
            current_time_clear += time_on_road_clear
            current_time_storm += time_on_road_storm

        trip_durations_storm.append(current_time_storm - trip_start_time)
        trip_durations_clear.append(current_time_clear - trip_start_time)

    # Return 2 arrays: trip durations of residents on the road network after a storm and trip durations
    # of the same residents on clear roads
    return trip_durations_storm, trip_durations_clear
