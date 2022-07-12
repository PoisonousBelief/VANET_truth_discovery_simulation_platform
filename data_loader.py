import json

def read_json(json_file, city_name):
    f = open(json_file, encoding='utf-8')
    data = json.load(f, strict=False)
    poi_list = []
    type_list = []
    for poi in data:
        if poi['cityname'] == city_name:
            typecodes = poi['typecode'].split('|')
            for code in typecodes:
                type_list.append(code)
            poi['typecode'] = typecodes
            poi_list.append(poi)
    f.close()
    type_list = list(set(type_list))    #Remove Duplicates
    return poi_list, type_list

def read_param(param_file):
    f = open(param_file, encoding='utf-8')
    param_dict = json.load(f, strict=False)
    f.close()
    return param_dict.values()
