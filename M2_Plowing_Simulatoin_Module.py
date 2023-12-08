# Kate 
# Fack by Major

import random
import numpy as np

def Run_Snowplow_Simulation(num_plows, start_nodes, map_instance, base_plow_speed, sim_hours):
    if num_plows == 0:
        return []
    
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
            return chosen_edge
        else:
            if edges:
                chosen_edge = random.choice(edges)
                return chosen_edge
            else:
                return None

    current_time = 0  # Start at time 0


    while current_time < sim_hours*60:  # Direct comparison with minutes
        for plow in snowplows:
            plow_speed = max(1, np.random.normal(loc=base_plow_speed, scale=5))
            edge = choose_edge(plow['current_node'])
            if edge:
                road_id = edge[2]['roadid']
                travel_time = calculate_travel_time(edge[2]['weight'], plow_speed)

                # Check if the road has not been plowed yet
                if map_instance.roads.loc[map_instance.roads['road_id'] == road_id, 'plow_time'].iloc[0] == np.inf:
                    # Update road plow_time and print the update
                    map_instance.roads.loc[map_instance.roads['road_id'] == road_id, 'plow_time'] = current_time

                # Update snowplow position and plowed edges
                plow['current_node'] = edge[1] if plow['current_node'] == edge[0] else edge[0]
                plow['plowed_edges'].append((edge[0], edge[1]))

                # Update current time
                current_time += travel_time

    return snowplows
