import numpy as np
import random
import tools as tl
import copy

def damp(dist, h):     #Linear damping
    prob = dist/h
    return prob

def random_pick(item_list, prob_list):
    #Pick an item based on probability
    seed = random.uniform(0,1)
    cumulative_prob = 0.0
    for item, item_prob in zip(item_list, prob_list):
        cumulative_prob += item_prob
        if seed < cumulative_prob:
            break
    return item

def get_type(types): #Get some random types
    seed = random.randint(1, len(types))
    random.shuffle(copy.deepcopy(types))
    return types[:seed]
    
def random_type(p_type, type_list):
    seq = random.randint(0, len(type_list)-1)
    return [type_list[seq]]
    
def observe(veh, poi, types):
    dist = np.linalg.norm(tl.dik_minus(veh.loc, poi.loc))
    err_prob = damp(dist, veh.horizon)
    item_list = [0,1]
    prob_list = [err_prob, 1-err_prob]
    flag = random_pick(item_list, prob_list)
    if flag:
        return get_type(poi.type)
    #Is misled?
    mislead_f = random_pick(item_list, [1-poi.mislead_prob, poi.mislead_prob])
    if mislead_f:
        return poi.mislead_type
    else:
        #Not misked. Get a random type.
        type_list = poi.remove_type(copy.deepcopy(types))
        return random_type(poi.type, type_list)
    
def obs_cir(poi_list, veh_list, epoch, horizon, w_range, h_range, types):
    print('{} epoch toatlly.'.format(epoch))
    # Take EPOCH observations during the time period
    for i in range(epoch):
        print('The {}-th epoch:'.format(i+1))
        #Each vehicle observe the pois
        for veh in veh_list:
            #The vehicle moves
            veh.move(poi_list, w_range, h_range)
            if veh.seq % 200 == 0:
                print('Vehicle {}'.format(veh.seq))
            ob = veh.detect(poi_list, types)        #Store the observation results
            for poi_seq, ob_result in ob.items():
                for r in ob_result:
                    poi_list[poi_seq].rec_ob(r)
                
    print('Results collecting...')
    for poi in poi_list:
        if poi.ob_dict:
            max_ob = max(poi.ob_dict, key=poi.ob_dict.get)
            poi.max_ob = max_ob
            poi.max_num = poi.ob_dict[max_ob]
        else:
            poi.max_ob = None
            poi.max_num = 0
        
