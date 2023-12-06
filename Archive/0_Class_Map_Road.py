# Graham 
import geopandas as gpd

class Map:
    def __init__(self, geopackage_path):
        self.roads = self._load_roads(geopackage_path)
        self.intersections = self._load_intersections(geopackage_path)
        self.timestamp = 0

    def _load_roads(self, geopackage_path):
        roads_gdf = gpd.read_file(geopackage_path, layer='edges')  # Use 'edges' for the roads layer
        print(roads_gdf.head())
        print(roads_gdf.iterrows()) 
        roads = []
        for _, row in roads_gdf.iterrows():
            road_num = row['osmid']  # Adjust to the actual identifier field           
            end1 = row['from']  # Adjust field names as necessary
            end2 = row['to']
            end_locations = (row['geometry'].coords[0], row['geometry'].coords[-1])
            traffic_flow = row.get('traffic_flow', 0)  # Default to 0 if not present
            max_speed = row.get('maxspeed', '25')  # Default to '25' if not present
            if isinstance(max_speed, str):
                # Split the string by space and take the numeric parts
                speed_values = [int(s) for s in max_speed.split() if s.isdigit()]
                # Take the maximum of the speed values if there are multiple, otherwise use the single value or default
                max_speed = max(speed_values) if speed_values else 25
            else:
                max_speed = int(max_speed)
            current_speed = max_speed  # Initialize current speed to max speed
            lanes = row.get('lanes', '1')  # Assuming '1' is the default value
            if isinstance(lanes, str):
                # Remove any leading/trailing brackets and quotes
                lanes = lanes.strip("[]'\" ")
                # Remove any remaining quotes from the string
                lanes = lanes.replace("'", "").replace('"', '')
                # Check if the resulting string is empty
                if lanes == '':
                    lanes = 1  # Default to 1 if the string is empty
                else:
                    if ',' in lanes:
                        # If there are multiple values, take the first one after splitting
                        lanes = int(lanes.split(',')[0])
                    else:
                        # If there's only one value, convert it directly to int
                        lanes = int(lanes)
#             lanes = row.get('lanes', 1)  # Default to 1 if not present
            road_name = row.get('name', 'Unknown')  # Replace 'name' with the actual field for road names
            road_length = row.get('length', 0)  # Replace 'length' with the actual field name if different
            road = Road(road_num, end1, end2, end_locations, traffic_flow, max_speed, lanes, road_name, road_length)
            roads.append(road)
        return roads

    def _load_intersections(self, geopackage_path):
        intersections_gdf = gpd.read_file(geopackage_path, layer='nodes')  # Use 'nodes' for the intersections layer
        intersections = []
        for _, row in intersections_gdf.iterrows():
            intersection_id = row['osmid']  # Adjust to the actual identifier field
            latitude = row['y']  # Adjust field names as necessary
            longitude = row['x']
            # The connected roads would need to be determined based on your data's structure
            # This might involve a spatial join or lookup to the 'edges' layer
            connected_roads = ['to', 'from']  # Placeholder, you'll need to implement this based on your data
            intersection = Intersection(intersection_id, latitude, longitude, connected_roads)
            intersections.append(intersection)
        return intersections

class Road:
    def __init__(self, road_num, end1, end2, end_locations, traffic_flow, max_speed, lanes):
        self.num = road_num
        self.end1 = end1
        self.end2 = end2
        self.end_locations = end_locations
        self.traffic_flow = traffic_flow  # vehicles per hour
        self.max_speed = max_speed
        self.current_speed = max_speed
        self.lanes = lanes
        self.name = name
        self.length = length
        self.is_plowed = True  # Assume road is initially plowed
        self.kj = 220  # Jam density (vehicles per mile per lane)

    def Experience_Snow(self, inches_of_snow):
        '''
        Reduce the road's current speed by 12% per inch of snow if not plowed.
        '''
        if not self.is_plowed:
            snow_effect = (1 - 0.12) ** inches_of_snow
            self.current_speed *= snow_effect

    def Experience_Plow(self):
        '''
        Set the road as plowed, which removes the snow's effect on speed.
        '''
        self.is_plowed = True
        self.current_speed = self.max_speed  # Reset speed to max as snow is cleared

    def update_traffic_flow(self, new_traffic_flow):
        '''
        Update the number of cars on the road segment.
        '''
        self.traffic_flow = new_traffic_flow
        self.update_speed_due_to_traffic()

    def update_speed_due_to_traffic(self):
        '''
        Update the road's current speed based on traffic flow using Greenshield’s equation.
        '''
        k = self.traffic_flow / (self.lanes * 60)  # Convert vehicles per hour to vehicles per minute per lane
        self.current_speed = self.max_speed - (self.max_speed / self.kj) * k
        self.current_speed = max(self.current_speed, 0)  # Ensure speed doesn't go negative

# # Example usage:
# road = Road(road_num=1, end1='A', end2='B', end_locations=[(0,0), (1,1)], traffic_flow=100, max_speed=60, lanes=2)
# print(f"Original speed: {road.current_speed}")

# # Experience snow
# road.Experience_Snow(inches_of_snow=4)
# print(f"Speed after 4 inches of snow: {road.current_speed}")

# # Experience plow
# road.Experience_Plow()
# print(f"Speed after plowing: {road.current_speed}")

# # Update traffic flow and calculate new speed
# road.update_traffic_flow(new_traffic_flow=300)  # 300 vehicles per hour
# print(f"Speed with updated traffic flow: {road.current_speed}")


class Intersection:
    def __init__(self, intersection_id, latitude, longitude, connected_roads):
        self.id = intersection_id
        self.latitude = latitude
        self.longitude = longitude
        self.connected_roads = connected_roads


M = Map('nonresidential_network_geopackage.gpkg')