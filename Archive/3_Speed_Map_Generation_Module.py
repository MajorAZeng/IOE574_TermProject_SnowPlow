# Major 
import numpy as np
from 0_Class_Map_Road import Map, Road, Intersection

def Simulate_Speed_Maps(geopackage_path, snow_depth, List_Plow_Maps):
    
    # Simulate a base map
    MP = Map(geopackage_path)

    # Simulation Snow Event
    for Rd in MP.roads:
        Rd.Experience_Snow(snow_depth)

    # Generate Plowed Speed Map
    List_Speed_Maps = [MP]
    # Create a speed map according to each plow map
    for Plow_Map in List_Plow_Maps:
        MP.timestamp  = Plow_Map.timestamp
        for road_num in Plow_Map.plowed:
            for Rd in MP.roads:
                if Rd.num == road_num:
                        Rd.Experience_Plow
        List_Speed_Maps.append(MP)








