# Chris
# Major Revised

import geopandas as gpd
import networkx as nx
import pandas as pd
from shapely.geometry import Point
from sklearn.neighbors import BallTree
import numpy as np
import random


def generate_trips():
    # Load the road network data using GeoPandas
    road_network = gpd.read_file("network_shapefile/edges.shp")

    # Load your locations and destinations from CSV files
    locations = pd.read_csv("your_locations.csv", names=['longitude', 'latitude'])
    destinations = pd.read_csv("your_destinations.csv", names=['longitude', 'latitude'])

    # Create a graph from the road network data
    G = nx.Graph()
    for row in road_network.itertuples():
        G.add_edge(row[11], row.to, weight=row.length, osmid=row.osmid)
        pos = {
            row[11]: (row.geometry.bounds[0], row.geometry.bounds[1]),
            row.to: (row.geometry.bounds[2], row.geometry.bounds[3])
        }
        nx.set_node_attributes(G, pos, 'geometry')

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
        all_trips_df = all_trips_df.append({
            'start_latitude': location.latitude,
            'start_longitude': location.longitude,
            'destination_latitude': closest_destination.latitude,
            'destination_longitude': closest_destination.longitude,
            'distance': min_distance,
            'duration': trip_duration,
            'return_distance': min_distance
        }, ignore_index=True)

        all_trips_df = all_trips_df.append(return_trip, ignore_index=True)

    # Return the DataFrame with all trip data
    return all_trips_df

# Call the function to generate trips and store the result in a variable
generated_trips = generate_trips()

# Display or save the DataFrame with all trip data
print(generated_trips)


'''
# Load the road network data using GeoPandas
# Is there an easy way to make the road map generated by 0_Class_Map_Road into a .shp?
road_network = gpd.read_file("network_shapefile/edges.shp")

# Load your locations and destinations from CSV files
locations = pd.read_csv("your_locations.csv", names=['longitude', 'latitude'])
destinations = pd.read_csv("your_destinations.csv", names=['longitude', 'latitude'])

# Create a graph from the road network data
G = nx.Graph()

for row in road_network.itertuples():
    G.add_edge(row[11], row.to, weight=row.length, osmid = row.osmid)
    pos = {row[11]: (row.geometry.bounds[0], row.geometry.bounds[1]), row.to: (row.geometry.bounds[2], row.geometry.bounds[3])}
    nx.set_node_attributes(G, pos, 'geometry')



# Function to find the nearest node in the graph
def nearest_node(graph, point):
    pos = {node: (data['geometry'][0], data['geometry'][1]) for node, data in G.nodes(data=True)}
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
    all_trips_df = all_trips_df.append({
        'start_latitude': location.latitude,
        'start_longitude': location.longitude,
        'destination_latitude': closest_destination.latitude,
        'destination_longitude': closest_destination.longitude,
        'distance': min_distance,
        'duration': trip_duration,
        'return_distance': min_distance
        
    }, ignore_index=True)

    all_trips_df = all_trips_df.append(return_trip, ignore_index=True)

# Display or save the DataFrame with all trip data
print(all_trips_df)

'''




'''

def Trip_Generation_Module():

This is a function that generate all trips


    # define trip parametes

    # random select housholds 
    # create housefold_trip object for each of them
    
    # return a list of hosehold_trip objects 
    # determine route based on distance- network x package
   

    


# trip routing is in there
class Household_Trip():
    
    This object contains all information about trip of a hosuehold


    def __init__(self, inputs...):
    # create the base strucion 
    self.hosuehold_num = 
    self.household_loc
    self.trip_start_time = 
    self.stay_duration = 
    self.route = 

    def simulation(self, inputs...):
'''
