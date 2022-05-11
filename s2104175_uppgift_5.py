#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 22:48:34 2022

@author: akseluhr
"""

import pandas as pd
import matplotlib.pyplot as plt

def load_file(file_name):
    df = pd.read_csv(file_name, encoding='latin', sep=';')
    return df

def most_speeding_violation(camera_data, location_data):
    
    # Copying data, keeping original DF intact
    camera_data_copy = camera_data.copy()
    location_data_copy = location_data.copy()
    
    # Mege on ID from both tables for feasible operations
    merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
    
    # Finding the area with the most captured vehicles for plotting later
    vehicles_captured = merge_camera_location['MätplatsID'].value_counts()
    most_traffic = vehicles_captured.index[0]
    
    # Get all data from this area by filtering on ID for this county
    all_data_most_traffic = merge_camera_location.loc[merge_camera_location['MätplatsID'] == most_traffic]
    print(all_data_most_traffic)
    # Transform to datetime
    all_data_most_traffic['Tid'] = pd.to_datetime(all_data_most_traffic['Tid'])
    
    # Get most trafficed area for title plot
    county = all_data_most_traffic['Kommun'].values[0]
    road = all_data_most_traffic['Vägnummer'].values[0]

    # Bins and labels for the time
    # All time data will be put in the corresponding bin. 
    # E.g. if dt.hour = 8, it will be put in the 8th bin
    bins=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    bin_labels=['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    all_data_most_traffic = pd.cut(all_data_most_traffic['Tid'].dt.hour, bins, labels=bin_labels)
    
    # Sort = false to keep the chronological (w.r.t. time) order. 
    most_trafic = all_data_most_traffic.value_counts(sort=False)

    # Plotting output
    plt.bar(bin_labels, most_trafic)
    title = 'Totalt antal fordon som kamerorna registrerar i '+ county + ' på väg: '+ road+'. Datum: 2021-09-11.'
    plt.title(title)
    plt.xlabel('Klockslag')
    plt.ylabel('Antal Fordon')
    
    
camera_data = load_file('kameraData.csv')
location_data = load_file('platsData.csv')
most_speeding_violation(camera_data, location_data)