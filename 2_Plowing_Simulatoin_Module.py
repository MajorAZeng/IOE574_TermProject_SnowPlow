# Kate

import geopandas as gpd
import networkx as nx
import pandas as pd
import numpy as np
from geopy.distance import geodesic
import random
from datetime import datetime
from datetime import timedelta
from 0_Class_Map_Road import Map, Road, Intersection

class Plow_Map:
    def __init__(self, roads):
        self.roads = roads
        self.plowed = set()  # Store plowed roads
        self.timestamp = 0

    def plow_one_street(self, road_num):
        self.plowed.add(road_num)
        self.timestamp = datetime.now()


def simulate_plowing_speed():
    average_speed = 35
    speed_std = 5
    return max(1, round(random.normalvariate(average_speed, speed_std)))


def plow_time_needed(road_num, plow_map, speed_func=simulate_plowing_speed):
    road_info = next((road for road in plow_map.roads if road.num == road_num), None)
    
    if road_info is not None:
        speed = speed_func()
        distance = road_info.distance
        time_needed = distance / speed
        return time_needed
    else:
        return 0


# Plow school first
def plow_sequence_1(plow_map):
    plow_map = Plow_Map(roads=map.roads)
    school_roads = [road for road in plow_map.roads if 'school' in road.name.lower() and road.num not in plow_map.plowed]
    
    if school_roads:
        chosen_road = min(school_roads, key=lambda road: plow_time_needed(road.num, plow_map))
        plow_map.plow_one_street(chosen_road.num)
        
        unplowed_roads = [road for road in plow_map.roads if road.num not in plow_map.plowed]
        nearest_unplowed_road = min(unplowed_roads, key=lambda road: geodesic((chosen_road.latitude, chosen_road.longitude), (road.latitude, road.longitude)).km)
        
        nearby_high_traffic_roads = [road for road in unplowed_roads if geodesic((nearest_unplowed_road.latitude, nearest_unplowed_road.longitude), (road.latitude, road.longitude)).km <= 2 and road.traffic_volume > 30]
        
        if nearby_high_traffic_roads:
            chosen_road = min(nearby_high_traffic_roads, key=lambda road: plow_time_needed(road.num, plow_map))
            plow_map.plow_one_street(chosen_road.num)
        else:
            plow_map.plow_one_street(nearest_unplowed_road.num)

# Plow hospital first
def plow_sequence_2(plow_map):
    plow_map = Plow_Map(roads=map.roads)
    hospital_roads = [road for road in plow_map.roads if 'hospital' in road.name.lower() and road.num not in plow_map.plowed]
    
    if hospital_roads:
        chosen_road = min(hospital_roads, key=lambda road: plow_time_needed(road.num, plow_map))
        plow_map.plow_one_street(chosen_road.num)
        
        unplowed_roads = [road for road in plow_map.roads if road.num not in plow_map.plowed]
        nearest_unplowed_road = min(unplowed_roads, key=lambda road: geodesic((chosen_road.latitude, chosen_road.longitude), (road.latitude, road.longitude)).km)
        
        nearby_high_traffic_roads = [road for road in unplowed_roads if geodesic((nearest_unplowed_road.latitude, nearest_unplowed_road.longitude), (road.latitude, road.longitude)).km <= 2 and road.traffic_volume > 30]
        
        if nearby_high_traffic_roads:
            chosen_road = min(nearby_high_traffic_roads, key=lambda road: plow_time_needed(road.num, plow_map))
            plow_map.plow_one_street(chosen_road.num)
        else:
            plow_map.plow_one_street(nearest_unplowed_road.num)


def simulate_plowing(plow_map, plow_vehicles, sequences, max_iterations=1000):
    all_plowed_roads = {}  # Store plowed roads and timestamps for each sequence

    for sequence in sequences:
        plowed_roads = []  # Store plowed roads and timestamps
        iteration = 0

        while len(plow_map.plowed) < len(plow_map.roads) and iteration < max_iterations:
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

            iteration += 1

        all_plowed_roads[sequence.__name__] = plowed_roads

    return all_plowed_roads


plow_map = Plow_Map(roads=map.roads)

simulate_plowing(plow_map, plow_vehicles, sequences)
