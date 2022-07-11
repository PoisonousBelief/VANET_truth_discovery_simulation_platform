# Vehicular Ad-hoc Networks truth discovery simulation platform

This is a simulation platform aiming to simulate the process that finding out the true types of PoIs(Point of Interrest) according the observation results from the vehicles. This platform based on the National POI data of Amap(https://opendata.pku.edu.cn/dataset.xhtml?persistentId=doi:10.18170/DVN/WSXCNM). Using other dataset needs to modify related fields in the dataset or modify the code of data loader. This platform can implement simulations on all the cities in China.

## Prerequisites
- Python >= 3.6
- Numpy >= 1.14
- matplotlib >= 3.1

## Getting Stared

### Seting parameters
The parameters is in "param.json" file. The default parameters are as follows:   
{  
  "epoch":10,    
  "data_file":"../poidata.json",    
  "city_name":"上海市",  
  "horizon":500,   
  "veh_num":30000,   
  "ite":3  
 }  

### Giving the city boundary
You need to give the city boundary before simulation since this data is not recored in the dataset. Luckly, we have collected boundaries of several city. You can derectly implement simulations on these cities without searching the boundaries. The cities we have collected boundaries are : Beijing, Guangzhou, Shanghai, Shenzhen, Xi'an, Chongqing. If you wang to  implement simulations on other cities, here are a few things you need to be aware of:
1. The boundary files shoud be .json files and be put into the 'edge' folder. The file name must be writen in chinese such as '上海市.json'.
2. The values of boundaries are latitude or longitude represented in dotted decimal notation, such as:  
  {"left": 120.866,  
   "right": 122.2,  
   "up": 31.883,  
   "down": 30.666}    

### Start simulation
Derectly run the following script from the directory:
```
python run.py
```

*** Note that the names of the boundary files and the city name in the parameters should be written in Chinese, because this field in the dataset is written in Chinese! ***
