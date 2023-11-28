# Kate 
# Fack by Major

from M0_Class_Map_Road import Map
from datetime import datetime, timedelta
import random
import numpy as np

# Load geopackage
gdf_edges = gpd.read_file('AA_Map_Final.gpkg', layer='edges')

# Create a graph from the edges
G = nx.Graph()
for _, row in gdf_edges.iterrows():
    G.add_edge(row['node1_id'], row['node2_id'], length=row['length'])

class Snowplow:
    def __init__(self, start_node, map_instance, speed=30):
        self.current_node = start_node
        self.map = map_instance
        self.speed = speed
        self.plowed_edges = []

    def calculate_travel_time(self, length):
        return length / self.speed

    def choose_edge(self):
        edges = list(self.map.graph.edges(self.current_node, data=True))
        unplowed_edges = [edge for edge in edges if self.map.roads.loc[self.map.roads['road_id'] == edge[2]['roadid'], 'plow_time'].iloc[0] == np.inf]

        if unplowed_edges:
            chosen_edge = random.choice(unplowed_edges)
            return chosen_edge
        else:
            if edges:
                chosen_edge = random.choice(edges)
                return chosen_edge
            else:
                return None

    def plow(self):
        edge = self.choose_edge()
        if edge:
            road_id = edge[2]['roadid']
            self.map.roads.loc[self.map.roads['road_id'] == road_id, 'plow_time'] = datetime.now()
            self.map.roads.loc[self.map.roads['road_id'] == road_id, 'inches_of_snow'] = 0
            self.current_node = edge[1] if self.current_node == edge[0] else edge[0]
            self.plowed_edges.append((edge[0], edge[1]))
            travel_time = self.calculate_travel_time(edge[2]['weight'])
            return travel_time
        return 0
