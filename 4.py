#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 20:51:30 2022

@author: akseluhr
"""

import pandas as pd


def load_file(file_name):
    df = pd.read_csv(file_name, encoding='latin', sep=';')
    return df

def county_speeding_violation(camera_data, location_data, sanction_data):
    camera_data_copy = camera_data.copy()
    location_data_copy = location_data.copy()
    merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')

    sum_vehicles_per_road = merge_camera_location.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Antal fordon')
    print(sum_vehicles_per_road.head(20))
    county_speedings = merge_camera_location.where(merge_camera_location['Gällande Hastighet'] < merge_camera_location['Hastighet']).dropna()
    county_speedings = county_speedings.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Överträdelser (%)')
    print(county_speedings['Överträdelser (%)'].head(20))

    county_speedings['Överträdelser (%)'] = county_speedings['Överträdelser (%)'] / sum_vehicles_per_road['Antal fordon'] * 100
    county_speedings.sort_values(by='Överträdelser (%)', inplace=True, ascending=False)
    county_speedings.reset_index(inplace=True, drop=True)
    print(county_speedings.to_string())
    
camera_data = load_file('kameraData.csv')
location_data = load_file('platsData.csv')
sanction_data = load_file('pafoljd.csv')

county_speeding_violation(camera_data, location_data, sanction_data)