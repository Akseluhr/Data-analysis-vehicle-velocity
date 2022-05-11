#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 20:51:30 2022

@author: akseluhr
"""

import pandas as pd

# Function to read and return the csv file
def load_file(file_name):
    df = pd.read_csv(file_name, encoding='latin', sep=';')
    return df

# Function that outputs all speeding violations for each road number in %
def all_county_speeding_violation(camera_data, location_data):
    
    # Copying the data
    camera_data_copy = camera_data.copy()
    location_data_copy = location_data.copy()
    
    # Merging on ID for easier operations
    merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')

    # Counting all vehicles per road and grouping the data based on county and road number
    sum_vehicles_per_road = merge_camera_location.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Antal fordon')
    
    # Get county speedings per county and road number
    county_speedings = merge_camera_location.where(merge_camera_location['Gällande Hastighet'] < merge_camera_location['Hastighet']).dropna()
    county_speedings = county_speedings.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Överträdelser (%)')

    # Calculate the percentage of speedings per county and road numnber. Descending sort.
    county_speedings['Överträdelser (%)'] = county_speedings['Överträdelser (%)'] / sum_vehicles_per_road['Antal fordon'] * 100
    county_speedings.sort_values(by='Överträdelser (%)', inplace=True, ascending=False)
    county_speedings.reset_index(inplace=True, drop=True)
    print(county_speedings.to_string())
    
camera_data = load_file('kameraData.csv')
location_data = load_file('platsData.csv')
all_county_speeding_violation(camera_data, location_data)