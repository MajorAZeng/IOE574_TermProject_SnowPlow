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
    locations = pd.read_csv(ori_path, names=['latitude', 'longitude'])
    destinations = pd.read_csv(des_path, names=['latitude', 'longitude'])

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

        # Find shortest path to and from the store
        end_node = nearest_node(G, Point(closest_destination.longitude, closest_destination.latitude))
        path_to_store = find_shortest_path(G, start_node, end_node)
        path_from_store = find_shortest_path(G, end_node, start_node)
        
        # Generate random trip duration with an average of 20 minutes
        trip_duration = max(1, round(random.normalvariate(20, 5)))
        # Create a return trip with the same locations but reversed
        return_trip = {
            'start_latitude': closest_destination.latitude,
            'start_longitude': closest_destination.longitude,
            'destination_latitude': location.latitude,
            'destination_longitude': location.longitude,
            'shortest_path': path_from_store,
            'duration': trip_duration
        }
        Map.trips.append(return_trip)

        # Add the trip and return trip data to the DataFrame
        new_trip_data = {
            'start_latitude': location.latitude,
            'start_longitude': location.longitude,
            'destination_latitude': closest_destination.latitude,
            'destination_longitude': closest_destination.longitude,
            'shortest_path': path_to_store,
            'duration': trip_duration,
        }
        Map.trips.append(new_trip_data)
