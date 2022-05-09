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


camera_data = load_file('kameraData.csv')
location_data = load_file('platsData.csv')
sanction_data = load_file('pafoljd.csv')

def county_speeding_violation(camera_data, location_data, sanction_data):
    camera_data_copy = camera_data.copy()
    location_data_copy = location_data.copy()
    merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
    #merge_camera_location = merge_camera_location.groupby(by='Vägnummer').size().unstack(fill_value=0)
    print(merge_camera_location)
   # county_df = location_data_copy.loc[location_data_copy['Kommun'].str.contains(county)]

    #id_list = county_df['MätplatsID'].tolist()

    
    county_speedings = merge_camera_location.where(merge_camera_location['Gällande Hastighet'] < merge_camera_location['Hastighet']).dropna()
    print(county_speedings)
    sum_vehicles_per_road = merge_camera_location.groupby(by='Vägnummer').count()      
    sum_vehicles_per_road.sort_values(by='Hastighet', inplace=True, ascending=False)
    print(sum_vehicles_per_road)
    county_speedings = county_speedings.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Överträdelser (%)')
    county_speedings.sort_values(by='Överträdelser (%)', inplace=True, ascending=False)
    print(county_speedings)
    county_speedings.reset_index(inplace=True, drop=True)
   # county_camera_data = merge_camera_location[merge_camera_location['MätplatsID'].isin(id_list)]

    
   # county_speedings['Överträdelser (%)'] = camera_data_copy['Hastighet'].count() * 100
    
    county_speedings['Överträdelser (%)'] = county_speedings['Överträdelser (%)'] / sum_vehicles_per_road['Hastighet']
    print(county_speedings)
  #  county_speedings['Överträdelser (%)'] = county_speedings['Hastighet'].tolist() / camera_data_copy['Hastighet'].count() * 100
   # county_speedings['Överträdelser (%)'].round(decimals=3)

county_speeding_violation(camera_data, location_data, sanction_data)