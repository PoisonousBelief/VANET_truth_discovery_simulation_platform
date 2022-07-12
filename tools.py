import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import datetime
import random
import os

lng_unit = 111111
lat_unit = 111320

def float_loc(string):
    s_lng, s_lat = string.split(',')
    return [float(s_lng), float(s_lat)]
    
def get_dik_coor(sph_coor, org):     #Trigonometric method
    lng = float(sph_coor[0])
    lat = float(sph_coor[1])
    lat_radian = lat * math.pi / 180
    x = (lng - org[0]) * lng_unit * math.cos(lat_radian)
    y = (lat - org[1]) * lat_unit
    return [x, y]

def get_dik_x(x):
    x = float(x)
    x1 = x * math.pi / 180
    dikaerX = (W / 2) + (W / (2 * math.pi)) * x1
    return dikaerX

def get_dik_y(y):
    y = float(y)
    y1 = y * math.pi / 180
    y1 = 1.25 * math.log(math.tan(0.25 * math.pi + 0.4 * y1))
    dikaerY = (H / 2) + (H / (2 * Mill)) * y1
    return dikaerY

def dik_minus(dik_1, dik_2):    #dik1-dik2
    x = dik_1[0] - dik_2[0]
    y = dik_1[1] - dik_2[1]
    return [x, y]

def in_horizon(poi, v_loc, horiz):
    p_loc = poi.loc
    dist = np.linalg.norm(dik_minus(p_loc, v_loc))
    if dist <= horiz:
        tag = poi.seq
    else:
        tag = 0
    return (tag, dist)
    
def rand_loc(w_range, h_range):
    x = random.uniform(0, w_range)
    y = random.uniform(0, h_range)
    loc = [x, y]
    return loc

def prox_put(poi, horizon):
    loc_x, loc_y = poi.loc
    sigma = horizon*1.2
    x = random.gauss(loc_x, sigma)
    y = random.gauss(loc_y, sigma)
    return x, y

def get_loc(poi_list, horizon, w_range, h_range):
    #Mix the two puting methods
    thresh = 0.7
    is_prox = random.uniform(0,1)
    if is_prox < thresh:    #Random putting
        loc = rand_loc(w_range, h_range)
    else:
        #The PoIs are randomly selected by gaussian distribution
        #Then putting vehicles to nearby PoI.
        mean = len(poi_list)//2
        sigma = len(poi_list)//5
        prox_poi_seq = int(random.gauss(mean, sigma))
        prox_poi_seq = min(max(0, prox_poi_seq),len(poi_list)-1)
        loc = prox_put(poi_list[prox_poi_seq], horizon)
    return loc

def PR(poi_list, k):
    tp = 0
    fp = 0
    fn = 0
    tn = 0
    for poi in poi_list:
        valid_ob = [x for x in poi.ob_dict.keys() if poi.ob_dict[x]>=k] #All observations greater than k
        negat_ob = [x for x in poi.ob_dict.keys() if poi.ob_dict[x]<k]
        for ob in valid_ob:
            if ob in poi.type:
                tp += 1
            else:
                fp += 1
        for ob in negat_ob:
            if ob in poi.type:
                fn += 1
            else:
                tn += 1
    P = tp / (tp+fp)
    R = tp / (tp+fn)
    return P, R

def get_PR(sort_poi):
    P_list = []
    R_list = []
    max_k = sort_poi[0].max_num
    #Arrange k from largest to smallest and calculate P and R for each k
    k_list = [x for x in range(max_k, 0, -1)]
    for k in k_list:
        P, R = PR(sort_poi, k)
        P_list.append(P)
        R_list.append(R)
    #Save into the log file
    k_array = np.array(k_list)
    P_array = np.array(P_list)
    R_array = np.array(R_list)
    loc_m = np.concatenate((np.expand_dims(k_array,axis=0), np.expand_dims(P_array,axis=0), np.expand_dims(R_array,axis=0)), axis=0)
    if not os.path.exists('./log/'):
        os.mkdir('./log/')
    log_name = './log/P-R_log_' + datetime.date.today().strftime('%m_%d_%Y_') + datetime.datetime.now().strftime('%H_%M_%S_%f')
    np.savetxt( log_name + '.txt', loc_m, fmt='%s', delimiter='\t')
    return P_list, R_list, k_list
