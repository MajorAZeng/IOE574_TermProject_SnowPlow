# Kate

import numpy as np
from numpy.random import multinomial
import random
from datetime import datetime
from datetime import timedelta

class Plow_Map:
    def __init__(self, roads):
        self.roads = roads
        self.snow_levels = ['zero', 'light', 'medium', 'heavy']
        self.plowed = set()  # Store plowed roads
        self.timestamp = 0
    
    def plow_one_street(self, road_num):
        self.plowed.add(road_num)
        self.timestamp = datetime.now()


def simulate_plowing(plow_map, plow_vehicles):
    PM = Plow_Map()
    plowed_roads = []  # Store plowed roads and timestamps

    while len(plow_map.plowed) < len(plow_map.roads):
        snow_levels_list = plow_map.simulate_snow_levels()

        # Vehicles status (0: idle, 1: busy)
        idle_vehicles = [vehicle for vehicle, status in plow_vehicles.items() if status == 0]

        for vehicle in idle_vehicles:
            if snow_levels_list:
                # Check if there are school roads to prioritize
                school_roads = [road for road in snow_levels_list if road['road_num'] == 'school_road']
                if school_roads:
                    road_to_plow = school_roads[0]
                else:
                    # Sort roads based on snow level priority: heavy, medium, light
                    snow_levels_list.sort(key=lambda x: plow_map.snow_levels.index(x['snow_level']), reverse=True)
                    road_to_plow = snow_levels_list[0]

                plow_vehicles[vehicle] = 1

                # Simulate plowing the road
                hours = plow_time_needed(vehicle, road_to_plow['road_num'], plow_map)
                finish_plowing_timestamp = plow_map.timestamp + timedelta(hours)
                plow_vehicles[vehicle] = 0

                plowed_roads.append({'road_num': road_to_plow['road_num'], 'timestamp': finish_plowing_timestamp})

                # Update plow_map with the plowed road
                plow_map.plow_one_street(road_to_plow['road_num'])

    return plowed_roads


def plow_time_needed(vehicle, road_num, plow_map):

    road_info = next(road for road in plow_map.roads if road.num == road_num) # from end_1 to end_2

    speed = simulate_plowing_speed()
    distance = road_info.distance
    time_needed = distance / speed

    return time_needed

def simulate_snow_levels(roads, plowed):
    snow_levels_list = []

    for road in roads:
        if road.num not in plowed:
            probabilities = calculate_snow_probabilities()
            snow_level_index = np.argmax(multinomial(1, probabilities))
            snow_level = ['zero', 'light', 'medium', 'heavy'][snow_level_index]

            snow_levels_list.append({'road_num': road.num, 'snow_level': snow_level})

    return snow_levels_list

def calculate_snow_probabilities():
    # Probability of snow level
    zero_prob = 0.4
    light_prob = 0.3
    mid_prob = 0.2
    heavy_prob = 0.1

    # Normalize probabilities to sum to 1
    total_prob = zero_prob + light_prob + mid_prob + heavy_prob
    probabilities = [zero_prob / total_prob, light_prob / total_prob, mid_prob / total_prob, heavy_prob / total_prob]

    return probabilities

def simulate_plowing_speed():
    average_speed = 35
    speed_std = 5
    return max(1, round(random.normalvariate(average_speed, speed_std)))
