# Kate 
# Fack by Major

from M0_Class_Map_Road import Map
import random
import numpy as np

def run_snowplow_simulation(num_plows, start_nodes, plow_speed, map_instance, duration_minutes):
    # Ensure there are as many start nodes as plows
    if len(start_nodes) != num_plows:
        raise ValueError("Number of start nodes must match the number of plows")

    # Initialize snowplows
    snowplows = [{'current_node': start_node, 'plowed_edges': []} for start_node in start_nodes]

    def calculate_travel_time(length, speed):
        return length / speed

    def choose_edge(current_node):
        edges = list(map_instance.graph.edges(current_node, data=True))
        unplowed_edges = [edge for edge in edges if map_instance.roads.loc[map_instance.roads['road_id'] == edge[2]['roadid'], 'plow_time'].iloc[0] == np.inf]

        if unplowed_edges:
            chosen_edge = random.choice(unplowed_edges)
            # print(f"Snowplow at node {current_node}: Choosing unplowed edge {chosen_edge}")
            return chosen_edge
        else:
            if edges:
                chosen_edge = random.choice(edges)
                # print(f"Snowplow at node {current_node}: All edges plowed, choosing random edge {chosen_edge}")
                return chosen_edge
            else:
                # print(f"Snowplow at node {current_node}: No edges available, stuck")
                return None

    current_time = 0  # Start at time 0

    while current_time < duration_minutes:  # Convert hours to minutes for comparison
        for plow in snowplows:
            edge = choose_edge(plow['current_node'])
            if edge:
                road_id = edge[2]['roadid']
                map_instance.roads.loc[map_instance.roads['road_id'] == road_id, 'plow_time'] = current_time
                map_instance.roads.loc[map_instance.roads['road_id'] == road_id, 'inches_of_snow'] = 0
                plow['current_node'] = edge[1] if plow['current_node'] == edge[0] else edge[0]
                plow['plowed_edges'].append((edge[0], edge[1]))
                travel_time = calculate_travel_time(edge[2]['weight'], plow_speed)
                current_time += travel_time
                # print(f"Snowplow moved to node {plow['current_node']}, current time (minutes): {current_time}")

    return snowplows
    
# # Define start nodes for snowplows
# start_node = 133
# start_nodes = [133]  # Replace with actual start nodes
        
# # Create a Map instance
# map_instance = Map('AA_Map_Final.gpkg')
# map_instance.Experience_Snow(4)

# # Initialize snowplows
# snowplows = [Snowplow(start_node, map_instance) for start_node in start_nodes]

# # Simulate snowplowing
# current_time = datetime.now()
# for _ in range(100):  # Number of iterations
#     for plow in snowplows:
#         travel_time = plow.plow()
#         # Here you can update current_time based on travel_time if needed    

# # Example usage
# map_info_path = 'AA_Map_Final.gpkg'
# snow_depth = 4
# start_nodes = [1, 2, 3]  # Example start nodes
