# Chris
# Major Revised

import geopandas as gpd
import networkx as nx
import pandas as pd
from shapely.geometry import Point
from sklearn.neighbors import BallTree
import numpy as np
import random


def Generate_Trips(Map, ori_path, des_path):

    # Load your locations and destinations from CSV files
    locations = pd.read_csv(ori_path, names=['longitude', 'latitude'])
    destinations = pd.read_csv(des_path, names=['longitude', 'latitude'])

    # Load the graph from the map-
    G = Map.graph
   
    # Function to find the nearest node in the graph
    def nearest_node(graph, point):
        pos = {node: (data['geometry'][0], data['geometry'][1]) for node, data in graph.nodes(data=True)}
        tree = BallTree(np.array(list(pos.values())))
        dist, ind = tree.query([[point.x, point.y]], k=1)
        return list(pos.keys())[ind[0][0]]

    # Function to find the shortest path between two points
    def find_shortest_path(graph, source, target):
        return nx.shortest_path(graph, source=source, target=target, weight='length')

    # Generate random trips
    trips = []

    selected_households = locations.sample(n=3830)

    # Create a DataFrame to store all trip data
    all_trips_df = pd.DataFrame(columns=['start_latitude', 'start_longitude', 'destination_latitude', 'destination_longitude', 'distance', 'duration', 'return_distance'])

    # Generate trips
    for location in selected_households.itertuples():
        start_point = Point(location.longitude, location.latitude)
        start_node = nearest_node(G, start_point)

        closest_destination = None
        min_distance = float('inf')

        for destination in destinations.itertuples():
            end_point = Point(destination.longitude, destination.latitude)
            end_node = nearest_node(G, end_point)

            path_distance = nx.shortest_path_length(G, source=start_node, target=end_node, weight='length')

            if path_distance < min_distance:
                min_distance = path_distance
                closest_destination = destination

        # Generate random trip duration with an average of 20 minutes
        trip_duration = max(1, round(random.normalvariate(20, 5)))
        # Create a return trip with the same locations but reversed
        return_trip = {
            'start_latitude': closest_destination.latitude,
            'start_longitude': closest_destination.longitude,
            'destination_latitude': location.latitude,
            'destination_longitude': location.longitude,
            'distance': min_distance,
            'duration': trip_duration,
            'return_distance': min_distance  # Assuming return distance is the same as the original trip distance
        }

        # Add the trip and return trip data to the DataFrame
        new_trip_data = {
            'start_latitude': location.latitude,
            'start_longitude': location.longitude,
            'destination_latitude': closest_destination.latitude,
            'destination_longitude': closest_destination.longitude,
            'distance': min_distance,
            'duration': trip_duration,
            'return_distance': min_distance
}

        # Convert the dictionary to a DataFrame
        new_trip_df = pd.DataFrame(new_trip_data, index=[0])

        # Concatenate DataFrames
        all_trips_df = pd.concat([all_trips_df, new_trip_df], ignore_index=True)

        '''
        all_trips_df = all_trips_df.append({
            'start_latitude': location.latitude,
            'start_longitude': location.longitude,
            'destination_latitude': closest_destination.latitude,
            'destination_longitude': closest_destination.longitude,
            'distance': min_distance,
            'duration': trip_duration,
            'return_distance': min_distance
        }, ignore_index=True)
        '''

        #all_trips_df = all_trips_df.append(return_trip, ignore_index=True)
        # we got a concat issue, so have to use that
        all_trips_df = pd.concat([all_trips_df, return_trip], ignore_index=True)

    # Return the DataFrame with all trip data to Map
    Map.trips = all_trips_df
