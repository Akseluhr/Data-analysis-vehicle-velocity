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
    
    county_speeding_analysis_df = pd.DataFrame(columns=['Vägnummer', 'Max hastighet (km/h)', 'Högsta uppmätta hastighet (km/h)', 'Överträdelser (%)', 'Tidpunkt'])
    id_list = county_df['MätplatsID'].tolist()
    county_camera_data = merge_camera_location[merge_camera_location['MätplatsID'].isin(id_list)]
    county_speedings = county_camera_data.where(county_camera_data['Gällande Hastighet'] < county_camera_data['Hastighet']).dropna()
    county_speeding_analysis_df['Max hastighet (km/h)'] = county_speedings['Gällande Hastighet'].tolist()

    sum_speedings_per_road = county_speedings.groupby(by='Vägnummer').count()       

    county_speeding_analysis_df['Vägnummer'] = county_speedings['Vägnummer'].tolist()
    county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'] = county_speedings['Hastighet'].tolist()
    
    date_time = county_speedings['Datum']+' '+county_speedings['Tid']
    county_speeding_analysis_df['Tidpunkt'] = date_time.tolist()
    
    county_speeding_analysis_df.drop_duplicates(['Vägnummer'], keep='first', inplace=True)
    county_speeding_analysis_df.reset_index(drop=True, inplace=True)

    max_vel_measured = county_speeding_analysis_df.groupby(['Vägnummer'], sort=False)['Högsta uppmätta hastighet (km/h)'].max()
    county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'] = max_vel_measured.values
    
    county_speeding_analysis_df['Överträdelser (%)'] = sum_speedings_per_road['Hastighet'].tolist() / county_camera_data['Hastighet'].count() * 100
    county_speeding_analysis_df['Överträdelser (%)'].round(decimals=3)

    print(county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'])
   # print(county_speedings.groupby(by='Vägnummer').max())
    ##print('uniq',  len(county_speeding_analysis_df['Vägnummer']))
    #print(max_velocity_per_road_num['Hastighet'].tolist())

    print(county_speeding_analysis_df.to_string())
    #county_speeding_analysis_df = pd.DataFrame(columns=['Vägnummer', 'Max hastighet (km/h)', 'Överträdelser (%)', 'Högsta uppmätta hastighet (km/h)', 'Tidpunkt'])
   # county_speeding_analysis_df['Vägnummer'] = county_df['Vägnummer'].drop_duplicates().tolist()
   # county_speeding_analysis_df['Max hastighet (km/h)'] = county_speedings['Gällande Hastighet'].drop_duplicates().tolist()
   # print("hej: ", county_speedings['Hastighet'].count() / county_camera_data['Hastighet'].count())
   # county_speeding_analysis_df['Överträdelser (%)'] = 
   # max_velocity_per_id = county_speedings.groupby(by='MätplatsID').max()
   # county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'] = county_speedings['Hastighet'].drop_duplicates().tolist()
   # print(pd.merge(max_velocity_per_id, county_df, left_on='MätplatsID', right_on='MätplatsID'))
  #  merge_velocity_county = pd.merge(max_velocity_per_id, county_df, left_on='MätplatsID', right_on='MätplatsID')
   # merge_velocity_county.drop(columns=['MätplatsID', 'Kommun'], inplace=True)
   # max_velocity_per_road_num = merge_velocity_county.groupby(by='Vägnummer').max()
   # print(max_velocity_per_road_num)
   # county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'] = max_velocity_per_road_num['Hastighet'].tolist()
   # print(max_velocity_per_road_num['Datum'], "das")
   # print(max_velocity_per_road_num['Tid'],"ldas")
    
   # max_velocity_per_road_num.reset_index(drop=True, inplace=True)
   # print(max_velocity_per_road_num)
   # county_speeding_analysis_df['Tidpunkt'] = max_velocity_per_road_num['Datum']+' '+max_velocity_per_road_num['Tid']
    #print(county_speeding_analysis_df['Tidpunkt'])

    #merge_speedings_county = pd.merge(county_speedings, county_df, left_on='MätplatsID', right_on='MätplatsID')
   # sum_speedings_per_road = merge_speedings_county.groupby(by='Vägnummer').count()
   # county_speeding_analysis_df['Överträdelser (%)'] = sum_speedings_per_road['Hastighet'].tolist() / county_camera_data['Hastighet'].count() * 100
   # county_speeding_analysis_df['Överträdelser (%)'].round(decimals=3)
    
   # print(county_speeding_analysis_df['Överträdelser (%)'].round(decimals=3))
   # print(county_speeding_analysis_df)
    return 0

def most_speeding_violations():
    return 0

    
    
county = user_input()
county_speeding_violation(county, camera_data, location_data, sanction_data)