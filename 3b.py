#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 20:02:40 2022

@author: akseluhr
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:58:15 2022

@author: akseluhr
"""
import pandas as pd
import numpy as np
import matplotlib as plt
import csv

#santion_data_df = pd.read_csv("Users/Akseluhr/Documents/GitHub/Data-analysis-vehicle-velocity/pafoljd.csv")

print("hej")

def load_file(file_name):
    df = pd.read_csv(file_name, encoding='latin', sep=';')
    return df

def user_input():
    inp = input("Enter county: ")
    print(inp)
    return inp

camera_data = load_file('kameraData.csv')
location_data = load_file('platsData.csv')
sanction_data = load_file('pafoljd.csv')

def county_speeding_violation(county, camera_data, location_data, sanction_data):
    camera_data_copy = camera_data.copy()
    location_data_copy = location_data.copy()
    county_df = location_data_copy.loc[location_data_copy['Kommun'].str.contains(county)]
    merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
    
    county_speeding_analysis_df = pd.DataFrame(columns=['Vägnummer', 'Max hastighet (km/h)', 'Uppmätt Hastighet', 'Tidpunkt', 'Påföljd'])
    id_list = county_df['MätplatsID'].tolist()
    county_camera_data = merge_camera_location[merge_camera_location['MätplatsID'].isin(id_list)]
    county_speedings = county_camera_data.where(county_camera_data['Gällande Hastighet'] < county_camera_data['Hastighet']).dropna()
    county_speeding_analysis_df['Max hastighet (km/h)'] = county_speedings['Gällande Hastighet'].tolist()

    county_speeding_analysis_df['Vägnummer'] = county_speedings['Vägnummer'].tolist()
    county_speeding_analysis_df['Uppmätt Hastighet'] = county_speedings['Hastighet'].tolist()
    
    date_time = county_speedings['Datum']+' '+county_speedings['Tid']
    county_speeding_analysis_df['Tidpunkt'] = date_time.tolist()
    

    sanction_labels = sanction_data['Påföljd'].tolist()
    sanction_thresholds = sanction_data['Hastighetsöverträdelse (km/h)'].tolist()

    difference = 0.0

    sanction_list = []
    for a,b in zip(county_speeding_analysis_df['Max hastighet (km/h)'], county_speeding_analysis_df['Uppmätt Hastighet']):
        difference = b-a
        difference = round(difference)

        # 0-30
        if (difference > 0 and difference <= sanction_thresholds[0]):
            # Varning och böter
            sanction_list.append(sanction_labels[0])
        # 31-40
        elif (sanction_thresholds[0] < difference <= sanction_thresholds[1]):
            # 2 mån
            sanction_list.append(sanction_labels[1])
        # 41-50
        elif (sanction_thresholds[1] < difference <= sanction_thresholds[2]):
            # 3 mån
            sanction_list.append(sanction_labels[2])
        # 51-60
        elif (sanction_thresholds[2] < difference <= sanction_thresholds[3]):
            # 4 mån
            sanction_list.append(sanction_labels[3])
        # 61-70
        elif (sanction_thresholds[3] < difference <= sanction_thresholds[4]):
            # 5 mån
            sanction_list.append(sanction_labels[4])
        # 71-80
        elif (sanction_thresholds[4] < difference <= sanction_thresholds[5]):
            # 6 mån
            sanction_list.append(sanction_labels[5])
        # 81 +
        elif (sanction_thresholds[5] < difference):
            # 8 mån
            sanction_list.append(sanction_labels[6])

    county_speeding_analysis_df['Påföljd'] = sanction_list
    print(county_speeding_analysis_df['Uppmätt Hastighet'].nlargest(5))
    print(county_speeding_analysis_df.loc[county_speeding_analysis_df['Uppmätt Hastighet'] == 144.0].to_string())
    print(county_speeding_analysis_df)
    return 0

def most_speeding_violations():
    return 0

county = user_input()
county_speeding_violation(county, camera_data, location_data, sanction_data)