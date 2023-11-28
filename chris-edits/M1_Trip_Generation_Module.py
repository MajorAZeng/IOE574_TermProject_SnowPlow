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
    #def find_shortest_path(graph, source, target):
    #    return nx.shortest_path(graph, source=source, target=target)


# ...

# Replace the line where you add the shortest_path to new_trip_data with the following:
#'shortest_path': shortest_path,

    # Generate random trips
    trips = []

    selected_households = locations.sample(n=3830)

    # Create a DataFrame to store all trip data
    all_trips_df = pd.DataFrame(columns=['start_latitude', 'start_longitude', 'destination_latitude', 'destination_longitude', 'shortest_path', 'duration'])
    # define findding shortest path
    def find_shortest_path(graph, source, target):
        path = nx.dijkstra_path(graph, source=source, target=target)
        return [(path[i], path[i+1]) for i in range(len(path) - 1)]
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
            # shortest_path = nx.dijkstra_path(G, source=start_node, target = end_node)
            # shortest_path_edges = []
            # for i in range(len(shortest_path) - 1):
            #     shortest_path_edges.append((shortest_path[i], shortest_path[i+1]))

            #shortest_path_edges = list(nx.utils.pairwise(shortest_path))
            if path_distance < min_distance:
                min_distance = path_distance
                closest_destination = destination
        end_point = Point(destionation.longitude, destination.latitude)
        end_node = nearest_node(G, end_point)
        shortest_path = nx.dijkstra_path(G, start_node, end_node)

        # Generate random trip duration with an average of 20 minutes
        trip_duration = max(1, round(random.normalvariate(20, 5)))
        # Create a return trip with the same locations but reversed
        return_trip = {
            'start_latitude': closest_destination.latitude,
            'start_longitude': closest_destination.longitude,
            'destination_latitude': location.latitude,
            'destination_longitude': location.longitude,
            'shortest_path': shortest_path,
            'duration': trip_duration
        }

        # Add the trip and return trip data to the DataFrame
        new_trip_data = {
            'start_latitude': location.latitude,
            'start_longitude': location.longitude,
            'destination_latitude': closest_destination.latitude,
            'destination_longitude': closest_destination.longitude,
            'shortest_path': shortest_path,
            'duration': trip_duration,
        }

        # Convert the dictionary to a DataFrame
        new_trip_df = pd.DataFrame(new_trip_data, index=[0])

        # convert return trip dictionary to DataFrame
        return_trip_df = pd.DataFrame(return_trip, index=[0])

        # Concatenate DataFrames
        all_trips_df = pd.concat([all_trips_df, new_trip_df], ignore_index=True)

        #all_trips_df = all_trips_df.append(return_trip, ignore_index=True)
        # we got a concat issue, so have to use that
        all_trips_df = pd.concat([all_trips_df, return_trip_df], ignore_index=True)

    # Return the DataFrame with all trip data to Map
    Map.trips = all_trips_df
