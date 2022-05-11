#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  7 17:58:15 2022

@author: akseluhr
"""
import pandas as pd
import numpy as np

# Function to read and return the csv file
def load_file(file_name):
    df = pd.read_csv(file_name, encoding='latin', sep=';')
    return df

# Function to read and store user input (county)
def user_input():
    inp = input("Enter county: ")
    return inp

camera_data = load_file('kameraData.csv')
location_data = load_file('platsData.csv')
sanction_data = load_file('pafoljd.csv')

# Function to read and print % of county speeding violation per road given a county
def county_speeding_violation(county, camera_data, location_data):
    
    if(county in location_data.values):
        # Copying for keeping the original DF intact
        camera_data_copy = camera_data.copy()
        location_data_copy = location_data.copy()
        
        # Filter on county (user input) to work with only requested data
        county_df = location_data_copy.loc[location_data_copy['Kommun'].str.contains(county)]
        
        # Preprocess: concats location and camera df to one for operations below
        merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
        
        # Get total vehicles per road (all roads)
        sum_vehicles_per_road = merge_camera_location.groupby('Kommun')['Vägnummer'].value_counts().reset_index(name='Antal fordon')
        
        # Get total vehicles per road (only current county which = user input)
        sum_vehicles_per_road_county = sum_vehicles_per_road.where(sum_vehicles_per_road['Kommun'] == county).dropna()
        sum_vehicles_per_road_county['Antal fordon'] = sum_vehicles_per_road_county['Antal fordon'].astype(int)
        sum_vehicles_per_road_county.sort_values(by='Vägnummer', inplace=True, ascending=True)
        
        # Create new DF for output
        county_speeding_analysis_df = pd.DataFrame(columns=['Vägnummer', 'Max hastighet (km/h)', 'Högsta uppmätta hastighet (km/h)', 'Överträdelser (%)', 'Tidpunkt'])
        
        # Filter on 'MätplatsID' which is unique for current county
        id_list = county_df['MätplatsID'].tolist()
        county_camera_data = merge_camera_location[merge_camera_location['MätplatsID'].isin(id_list)]
        
        # Take speedings which are greater than the legal velocity limit
        county_speedings = county_camera_data.where(county_camera_data['Gällande Hastighet'] < county_camera_data['Hastighet']).dropna()
        
        # Append speed limit to output DF
        county_speeding_analysis_df['Max hastighet (km/h)'] = county_speedings['Gällande Hastighet'].tolist()
    
        # Sum speedings per road for future division
        sum_speedings_per_road = county_speedings.groupby(by='Vägnummer').count()       
    
        # Append roadnumber and ALL measured speed to output DF
        county_speeding_analysis_df['Vägnummer'] = county_speedings['Vägnummer'].tolist()
        county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'] = county_speedings['Hastighet'].tolist()
        
        # Append time stamp to output DF
        date_time = county_speedings['Datum']+' '+county_speedings['Tid']
        county_speeding_analysis_df['Tidpunkt'] = date_time.tolist()
        
        # We don't want duplicates, hence dropping but keeping first occurance
        county_speeding_analysis_df.drop_duplicates(['Vägnummer'], keep='first', inplace=True)
        county_speeding_analysis_df.reset_index(drop=True, inplace=True)
    
        # Adjust ALL measured speed to max and append them to output DF 
        max_vel_measured = county_speeding_analysis_df.groupby(['Vägnummer'], sort=False)['Högsta uppmätta hastighet (km/h)'].max()
        county_speeding_analysis_df['Högsta uppmätta hastighet (km/h)'] = max_vel_measured.values
        
        # Calculate frequency of speedings and append to output DF
        sum_speedings_arr = np.array(sum_speedings_per_road['Hastighet'])
        sum_vehicles_arr = np.array(sum_vehicles_per_road_county['Antal fordon'])
        speedings_percente = sum_speedings_arr / sum_vehicles_arr * 100
        county_speeding_analysis_df['Överträdelser (%)'] = speedings_percente
    
        # Print output
        print(county_speeding_analysis_df.to_string())
        print("================================================================")
    else:
        print('Could not find county. Try again.')

def county_speeding_violation_sanctions(county, camera_data, location_data, sanction_data):
    
    if(county in location_data.values):
    
        # Copying for keeping the original DF intact
        camera_data_copy = camera_data.copy()
        location_data_copy = location_data.copy()
        sanction_data = sanction_data.copy()
        
        # Filter on county (user input) to work with only requested data
        county_df = location_data_copy.loc[location_data_copy['Kommun'].str.contains(county)]
        
        # Preprocess: concats location and camera df to one for operations below
        merge_camera_location = pd.merge(camera_data_copy, location_data_copy, left_on='MätplatsID', right_on='MätplatsID')
        
        # Create new DF for output
        county_speeding_analysis_df = pd.DataFrame(columns=['Vägnummer', 'Max hastighet (km/h)', 'Uppmätt Hastighet', 'Tidpunkt', 'Påföljd'])
        
        # Filter on 'MätplatsID' which is unique for current county
        id_list = county_df['MätplatsID'].tolist()
        county_camera_data = merge_camera_location[merge_camera_location['MätplatsID'].isin(id_list)]
        
        # Take speedings which are greater than the legal velocity limit
        county_speedings = county_camera_data.where(county_camera_data['Gällande Hastighet'] < county_camera_data['Hastighet']).dropna()
        
            
        # Append speed limit to output DF
        county_speeding_analysis_df['Max hastighet (km/h)'] = county_speedings['Gällande Hastighet'].tolist()
    
    
        # Append road number and ALL measured speedings to output DF
        county_speeding_analysis_df['Vägnummer'] = county_speedings['Vägnummer'].tolist()
        county_speeding_analysis_df['Uppmätt Hastighet'] = county_speedings['Hastighet'].tolist()
        
        # Append time stamp
        date_time = county_speedings['Datum']+' '+county_speedings['Tid']
        county_speeding_analysis_df['Tidpunkt'] = date_time.tolist()
        
        # Get sanction labels and threshold for comparison with speedings
        sanction_labels = sanction_data['Påföljd'].tolist()
        sanction_thresholds = sanction_data['Hastighetsöverträdelse (km/h)'].tolist()
    
        difference = 0.0
        sanction_list = []
        
        for a,b in zip(county_speeding_analysis_df['Max hastighet (km/h)'], county_speeding_analysis_df['Uppmätt Hastighet']):
            difference = b-a
            difference = round(difference)
    
            if (difference > 0 and difference <= sanction_thresholds[0]): # 0-30
                sanction_list.append(sanction_labels[0]) # Varning och böter
            elif (sanction_thresholds[0] < difference <= sanction_thresholds[1]): # 31-40
                sanction_list.append(sanction_labels[1]) # 2 mån
            elif (sanction_thresholds[1] < difference <= sanction_thresholds[2]): # 41-50
                sanction_list.append(sanction_labels[2]) # 3 mån
            elif (sanction_thresholds[2] < difference <= sanction_thresholds[3]): # 51-60
                sanction_list.append(sanction_labels[3]) # 4 mån
            elif (sanction_thresholds[3] < difference <= sanction_thresholds[4]): # 61-70
                sanction_list.append(sanction_labels[4]) # 5 mån
            elif (sanction_thresholds[4] < difference <= sanction_thresholds[5]): # 71-80
                sanction_list.append(sanction_labels[5]) # 6 mån
            elif (sanction_thresholds[5] < difference):  # 81 +
                sanction_list.append(sanction_labels[6]) # 8 mån
    
        # Append sanctions to final DF
        county_speeding_analysis_df['Påföljd'] = sanction_list
    
        # Print output
        print(county_speeding_analysis_df)
    else: 
        print('Could not find county. Please try again')


county = user_input()
county_trim = county.strip()
county_speeding_violation(county_trim, camera_data, location_data)
county_speeding_violation_sanctions(county_trim, camera_data, location_data, sanction_data)