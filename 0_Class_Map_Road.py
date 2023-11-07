class Map():
    '''
    This is a class of map object.
    Each map object carries information about all road segments and their travel speed.
    There are various methods to manipulate the map (updating travel seepd or so.)
    '''
    # chris comment to see if the change works

    def __init__(self):
        '''
        This method creat a brand new base map, which contains all it's road segments, with initial no snow condition speed.
        It's a collectoin of may road objects. 
        '''

    def Experience_Snow_Event(self, snow_depth=4):
        '''
        Thus method update all road speed with a snow event. 
        By defult the snow depth is 4 inch. Additional argument input can change the depth. 
        '''
    
    def Experience_Plow_Event(self, plow_section):
        '''
        This method update the map on a specific segment as if plowing has been completed on that segment
        '''




class Road():
    '''
    This is a class of road object
    Each raod object carries all relevant info
    '''

    def __init__(self, road_num, end1, end2, end_locations, traffic_flow, max_speed, current_speed...):
        '''
        This method create a new road segment with given properties
        '''
        self.num = road_num
        ...
      
    def Experience_Snow(self):
        '''
        how raod should be updated after a snow event
        '''

    def Experience_Plow(self):
        '''
        how raod should be updated after a snow event
        '''

