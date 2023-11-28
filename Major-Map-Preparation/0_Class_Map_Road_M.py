# Graham
# Major Revised

import geopandas as gpd
import networkx as nx
import numpy as np

class Map():
    
    def __init__(self,geopackage_path):
        self.roads = self._load_roads(geopackage_path)
        self.graph = self._load_graph(geopackage_path)
        
    def _load_roads(self,geopackage_path):
        # load map info
        roads_gdf = gpd.read_file(geopackage_path, layer='edges')
        # find traffic flow as vehicles per minute per lane
        roads_gdf['traffic_flow'] = roads_gdf['aadt']/roads_gdf['lanes']/12/60 
        # calculate current speed
        roads_gdf['normal_speed'] = roads_gdf['max_speed'] - (roads_gdf['max_speed'] / 220 ) * roads_gdf['traffic_flow']
        return roads_gdf
    
    def _load_graph(self, geopackage_path):
        
        # Load Info
        roads_gdf = gpd.read_file(geopackage_path, layer='edges')
        nodes_gdf = gpd.read_file(geopackage_path, layer='nodes')
        
        # Create a graph from the road network data
        G = nx.Graph()
        for i,row in roads_gdf.iterrows():
            G.add_edge(row['node1_id'], row['node2_id'], weight=row['length'], roadid=row['road_id'])
            pos = {
            row['node1_id']: nodes_gdf.loc[row['node1_id'],'geometry'],
            row['node2_id']: nodes_gdf.loc[row['node2_id'],'geometry']
            }
            nx.set_node_attributes(G, pos, 'geometry')
    
    
    def Experience_Snow(self, inches_of_snow=4):
        '''
        Reduce the road max speed by 12% per inch of snow if not plowed.
        Set all roads plow time to inf
        '''
        snow_effect = (1 - 0.12) ** inches_of_snow
        self.roads['speed_after_snow'] = self.roads['normal_speed']* snow_effect
        self.roads['plow_time'] = np.inf
        
 