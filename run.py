import entity as ety
import tools as tl
import data_loader as load
import obs
import random
import plot
import copy
import os

class Simulation:
    def __init__(self, epoch, data_file, city_name, horizon, veh_num, ite):
        self.epoch = epoch
        self.data_file = data_file
        self.city_name = city_name
        self.horizon = horizon
        self.veh_num = veh_num
        self.ite = ite

        print('Initializing city map...')
        self.city = ety.Map(self.city_name)    #Initialize the city map
        self.city.set_base()
        self.poi_list = []
        #Load data
        poi_info, self.types = load.read_json(self.data_file, self.city_name)
        print('Building PoIs...')
        #Buiding pois
        for (seq, poi) in enumerate(poi_info, start=1):
            name = poi['name']
            loc = poi['location']
            type_code = poi['typecode']
            poi = ety.Poi(seq, name, loc, type_code, self.city.orig_g)
            poi.set_mislead(copy.deepcopy(self.types))
            self.poi_list.append(poi)
        print('Buiding PoIs ready.')
        print('Initialization completed.')

    def clear(self):
        #Clear the observed results in every poi
        for poi in self.poi_list:
            poi.clr()
        
    def run(self):
        self.clear()
        print('Puting vehicles...')
        #Generate vehicles and put to the city.
        w_range = self.city.w_range
        h_range = self.city.h_range
        veh_list = []
        for i in range(self.veh_num):
            seq = i+1
            #get location
            loc = tl.get_loc(self.poi_list, self.horizon, w_range, h_range)
            veh_list.append(ety.Vehicle(seq, loc, self.horizon))     #generate a vehicle
        print('Vehicles prepared.')
        print('Detecting...')
        #Observations for epoch times
        obs.obs_cir(self.poi_list, veh_list, self.epoch, self.horizon, w_range, h_range, self.types)
        print('Detectation completed')
        print('Calculating...')
        sort_poi = sorted(self.poi_list, key=lambda x:x.max_num, reverse=True)
        
        #Calculate pres
        P_list, R_list, k_list = tl.get_PR(sort_poi) #K*2
        print('Plotting')
        #Plot P-R curves
        plot.plot_PR(P_list, R_list, k_list)
        print('Loop completed')

    def start(self):
        for i in range(self.ite):
            print('The {}-th loop:'.format(i+1))
            self.run()

if __name__ == '__main__':
        param_file = './param.json'
        epoch, data_file, city_name, horizon, veh_num, ite = load.read_param(param_file)
        sim = Simulation(epoch, data_file, city_name, horizon, veh_num, ite)
        sim.start()
