#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 22:48:34 2022

@author: akseluhr
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

def county_speeding_violation(amera_data, location_data, sanction_data):
    camera_data_copy = camera_data.copy()
    location_data_copy = location_data.copy()
    merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
    vehicles_captured = merge_camera_location['MätplatsID'].value_counts()
    print(vehicles_captured)
    print(vehicles_captured.index[0])
    most_traffic = vehicles_captured.index[0]
    all_data_most_traffic = merge_camera_location.loc[merge_camera_location['MätplatsID'] == most_traffic]
    print("här ska d va 303 vid 07.00", all_data_most_traffic)
    all_data_most_traffic['Tid'] = pd.to_datetime(all_data_most_traffic['Tid'])
    print(all_data_most_traffic['Tid'].dt.hour)
    print(location_data_copy['Kommun'].dtypes)
    bins=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    bin_labels=['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    all_data_most_traffic = pd.cut(all_data_most_traffic['Tid'].dt.hour, bins, labels=bin_labels)
    #count_traffic = all_data_most_traffic['Tid'].value_counts()
    print(all_data_most_traffic)
    d = all_data_most_traffic.value_counts(sort=False)
    print(d)
    plt.bar(bin_labels, d)
    return 0

def most_speeding_violations():
    return 0

    
    

county_speeding_violation(camera_data, location_data, sanction_data)