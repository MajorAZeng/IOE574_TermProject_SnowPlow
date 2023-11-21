# Kate

import geopandas as gpd
import networkx as nx
import pandas as pd
import numpy as np
from numpy.random import multinomial
import random
from datetime import datetime
from datetime import timedelta


class Plow_Map:
    def __init__(self, roads):
        self.roads = roads
        self.plowed = set()  # Store plowed roads
        self.timestamp = datetime.now()

    def plow_one_street(self, road_num):
        self.plowed.add(road_num)
        self.timestamp = datetime.now()


def simulate_plowing_speed():
    average_speed = 35
    speed_std = 5
    return max(1, round(random.normalvariate(average_speed, speed_std)))


def plow_time_needed(road_num, plow_map):
    road_info = next((road for road in plow_map.roads if road.num == road_num), None)
    
    if road_info is not None:
        speed = simulate_plowing_speed()
        distance = road_info.distance
        time_needed = distance / speed
        return time_needed
    else:
        return 0


# Plow school first
def plow_sequence_1(plow_map):
    school_roads = [road for road in plow_map.roads if 'school' in road.name.lower() and road.num not in plow_map.plowed]
    
    if school_roads:
        return min(school_roads, key=lambda road: plow_time_needed(road.num, plow_map))
    else:
        unplowed_roads = [road for road in plow_map.roads if road.num not in plow_map.plowed]
        return min(unplowed_roads, key=lambda road: plow_time_needed(road.num, plow_map))
    

#Plow hospital first
def plow_sequence_2(plow_map):
    hospital_roads = [road for road in plow_map.roads if 'hospital' in road.name.lower() and road.num not in plow_map.plowed]
    
    if hospital_roads:
        return min(hospital_roads, key=lambda road: plow_time_needed(road.num, plow_map))
    else:
        unplowed_roads = [road for road in plow_map.roads if road.num not in plow_map.plowed]
        return min(unplowed_roads, key=lambda road: plow_time_needed(road.num, plow_map))


def simulate_plowing(plow_map, plow_vehicles, sequence):
    all_plowed_roads = {}  # Store plowed roads and timestamps for each sequence

    for strategy_function in sequence:
        plow_map.reset()  
        plow_vehicles.reset()  

        plowed_roads = []  # Store plowed roads and timestamps
        while len(plow_map.plowed) < len(plow_map.roads):
            # Vehicles status (0: idle, 1: busy)
            idle_vehicles = [vehicle for vehicle, status in plow_vehicles.items() if status == 0]

            for vehicle in idle_vehicles:
                road_to_plow = sequence(plow_map, vehicle)

                if road_to_plow:
                    plow_vehicles[vehicle] = 1 

                    hours = plow_time_needed(road_to_plow.num, plow_map)
                    finish_plowing_timestamp = plow_map.timestamp + timedelta(hours)
                    plow_vehicles[vehicle] = 0 

                    plowed_roads.append({'road_num': road_to_plow.num, 'timestamp': finish_plowing_timestamp})

                    plow_map.plowed.add(road_to_plow.num)

        all_plowed_roads[sequence.__name__] = plowed_roads

    return all_plowed_roads
