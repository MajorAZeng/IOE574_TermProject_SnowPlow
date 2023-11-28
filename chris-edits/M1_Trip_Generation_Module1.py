# Chris
# Major Revised
import geopandas as gpd
import pandas as pd
import numpy as np
import networkx as nx
from scipy.stats import norm
from shapely.geometry import Point

def Generate_Trips(Map, origins_file, destinations_file):
    # Read the map file
    graph = Map.graph

    # Read origin and destination CSV files
    origins = pd.read_csv(ori_path, names=['longitude', 'latitude'])
    destinations = pd.read_csv(des_path, names=['longitude', 'latitude'])


    trips_data = []
    for idx, origin in origins.iterrows():
        # Convert origin and destination latitudes and longitudes to Points
        origin_point = Point(origin['longitude'], origin['latitude'])

        # Find the closest node in the graph to the origin
        origin_node = nearest_node(graph, origin_point)

        # Initialize variables to hold closest destination and shortest path
        closest_destination = None
        shortest_path = None
        shortest_distance = float('inf')

        for idx, destination in destinations.iterrows():
            # Convert destination latitudes and longitudes to Points
            dest_point = Point(destination['longitude'], destination['latitude'])

            # Find the closest node in the graph to the destination
            dest_node = nearest_node(graph, dest_point)

            # Compute shortest path between origin_node and dest_node
            path = nx.shortest_path(graph, origin_node, dest_node, weight='distance')
            distance = nx.shortest_path_length(graph, origin_node, dest_node, weight='distance')

            # Update closest destination and shortest path if this destination is closer
            if distance < shortest_distance:
                shortest_distance = distance
                closest_destination = dest_node
                shortest_path = path

        # Generate random duration for the trip
        duration = max(0, np.random.normal(20, 5))

        # Append trip data to trips_data list
        trips_data.append({
            'origin_latitude': origin['latitude'],
            'origin_longitude': origin['longitude'],
            'destination_latitude': destinations.loc[closest_destination]['latitude'],
            'destination_longitude': destinations.loc[closest_destination]['longitude'],
            'shortest_path': shortest_path,
            'duration': duration
        })

    # Create DataFrame from trips_data
    trips_df = pd.DataFrame(trips_data)

    

def nearest_node(graph, point):
    # Find the nearest node in the graph to the given point
    distances = {}
    for idx, row in graph.iterrows():
        node = row.geometry
        distances[idx] = node.distance(point)
    closest_node_idx = min(distances, key=distances.get)
    return closest_node_idx


'''
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

    # Create a list to store all trips
    # Generate random trips
    trips = []

    selected_households = locations.sample(n=3830)

    # Create a DataFrame to store all trip data
    all_trips_df = pd.DataFrame(columns=['start_latitude', 'start_longitude', 'destination_latitude', 'destination_longitude', 'shortest_path', 'duration'])

    # Define finding the nearest node in the graph
    def nearest_node(graph, point):
        pos = {node: (data['geometry'][0], data['geometry'][1]) for node, data in graph.nodes(data=True)}
        tree = BallTree(np.array(list(pos.values())))
        dist, ind = tree.query([[point.x, point.y]], k=1)
        return list(pos.keys())[ind[0][0]]

    # Define finding the shortest path between two points
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

            if path_distance < min_distance:
                min_distance = path_distance
                closest_destination = destination

        end_point = Point(closest_destination.longitude, closest_destination.latitude)
        end_node = nearest_node(G, end_point)
        shortest_path = find_shortest_path(G, start_node, end_node)

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
'''