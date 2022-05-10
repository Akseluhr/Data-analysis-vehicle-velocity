#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:12:54 2022

@author: akseluhr
"""
import pandas as pd

# Function to read and return the csv file
def load_file(filename):
    data = pd.read_csv(filename, encoding= 'latin1', sep=';')
    return data

# Processes and prints number of cameras per county and road number
def camera_data(data):
    
    # Rename for proper column name w.r.t. the task
    location_data = data.rename(columns = {'MätplatsID':'Antal Kameror'})
    
    # Group by county and road number. Count() for counting instances per road number
    cameras_per_road = location_data.groupby(['Kommun', 'Vägnummer']).count()
    
    # Drop unnecessary column (Namn)
    cameras_per_road.drop(columns='Namn', axis=1, inplace=True)
    
    # Print results
    print('Hastighetsövervakning i Västra Götaland')
    print(cameras_per_road.to_string())
    


location_data = load_file('platsData.csv')
camera_data(location_data)
