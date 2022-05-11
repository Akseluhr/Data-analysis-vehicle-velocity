#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:43:46 2022

@author: akseluhr
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def load_file(filename):
        data = pd.read_csv(filename, encoding= 'latin1', sep=';')
        return data
    
def mean_spead_per_hour(county, location_data, camera_data):
    
    if(county in location_data.values):
        # Copy origin DF
        location_data_copy = location_data.copy()
        camera_data_copy = camera_data.copy()
        
        # Merge on ID for future operations and match county with user input
        merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
        camera_location_update = merge_camera_location.drop(['Namn', 'Datum', 'MätplatsID'], axis=1)
        county_specific = camera_location_update.loc[camera_location_update['Kommun'] == county]
        
        # Adjust time stamp 
        county_specific['Tid'] = county_specific['Tid'].str.slice(stop = 2)
        
        mean_speed_per_h = np.zeros(18)
        roads = county_specific.drop_duplicates(subset = ['Vägnummer'])
        roads_num = roads['Vägnummer'].tolist()
        
        speed_limit_list = []
        mean_speed_roads_list = []
        
        # Calculating avarage speed per road and hour 
        # Appending speed limit, road number and measured speed for future plotting
        for j in range(len(roads_num)):
            mean_speed_per_h = np.zeros(18)
            per_road = county_specific.loc[county_specific['Vägnummer'] == roads_num[j]]
            speed_limit = per_road.drop_duplicates(subset = ['Gällande Hastighet'])
            speed_limit_list.append(speed_limit['Gällande Hastighet'].tolist())
            for i in range(11):
                per_road['Tid'] = per_road['Tid'].astype('int')
                per_hour = per_road.loc[per_road['Tid'] == i+7]
                mean_speed_per_h[7+i] = per_hour['Hastighet'].sum()/per_hour.shape[0]
            mean_speed_roads_list.append(mean_speed_per_h)
        
        return mean_speed_roads_list, speed_limit_list, roads_num
    else:
        print('County not found in the data. Please try again')
    

county = input('Enter county:')
county_trim = county.strip()
location_data = load_file('platsData.csv')
camera_data = load_file('kameraData.csv')
mean_speed_roads_list, speed_limit_list, roads_num = mean_spead_per_hour(county_trim, location_data, camera_data)

plt.figure()
x = np.arange(7, 18, 1)
i = 0
for road in mean_speed_roads_list:
    plt.plot(x, road[7:], label = 'Väg: {}, Hastighet: {}'.format(roads_num[i], speed_limit_list[i][:]))
    i +=1

plt.legend(loc='lower right',fancybox=True, shadow=True, fontsize=5)
klock_x= ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
plt.xticks(x, klock_x)
titel = 'Medelhastigheter uppmätta per vägnummer i {}s kommun i mätområdet 2021-09-11'.format(county_trim)
plt.title(titel)
plt.xlabel('Klockslag')
plt.ylabel('Medelhastighet km/h')
plt.grid(True)
plt.show()