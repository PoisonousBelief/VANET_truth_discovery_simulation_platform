#Define several entity
#including Map, Poi, and Vehicle
import json
import tools as tl
import random
import obs

class Map:
    def __init__(self, city):
        self.city = city
        edge_file = './edge/' + city + '.json'
        with open(edge_file, 'r') as f:
            self.edge = json.load(f, strict=False)
            
    def set_base(self):
        self.orig_g = [self.edge['left'], self.edge['down']]
        self.far_g = [self.edge['right'], self.edge['up']]
        self.orig = [0,0]
        self.far = tl.get_dik_coor(self.far_g, self.orig_g)
        self.w_range = self.far[0]      #The unit is meter
        self.h_range = self.far[1]

class Poi:
    def __init__(self, seq, name, loc, type_c, org):
        self.seq = seq  #Srart from 1
        self.name = name
        self.org = org
        self.loc = tl.get_dik_coor(tl.float_loc(loc), org)
        self.type = type_c  #list
        self.ob_dict = {}   #Stores all observations 
        self.mislead = False

    def remove_type(self, types):
        for t in self.type:
            types.remove(t)
        return types

    def set_mislead(self, types):
        self.mislead = True
        types = self.remove_type(types)
        self.mislead_type = obs.random_type(self.type, types) #list
        self.mislead_prob = random.uniform(0.0, 0.3)

    def rec_ob(self, ob):
        if ob in self.ob_dict.keys():
            self.ob_dict[ob] += 1
        else:
            self.ob_dict[ob] = 1

    def clr(self):
        self.ob_dict = {}
        self.max_ob = None
        self.max_num = 0

class Vehicle:
    def __init__(self, seq, ini_loc, horizon = 500):
        self.seq = seq      #Srart from 1
        self.loc = ini_loc
        self.horizon = horizon

    def move(self, poi_list, w_range, h_range):
        self.loc = tl.get_loc(poi_list, self.horizon, w_range, h_range)

    def rand_move(self, w_range, h_range):
        self.loc = tl.rand_loc(w_range, h_range)

    def detect(self, poi_list, types):     #Detect the PoI within the range and observ them
        ob_dict = {}
        #Determine whether the PoIs within the range
        detect_list = list(map(tl.in_horizon, poi_list, [self.loc]*len(poi_list), [self.horizon]*len(poi_list)))
        for (i, d_result) in enumerate(detect_list):
            if d_result[0]:
                ob_type = obs.observe(self, poi_list[i], types)
                ob_dict[i] = ob_type
        return ob_dict
