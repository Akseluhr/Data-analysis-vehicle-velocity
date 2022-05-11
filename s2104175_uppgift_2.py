#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 9 18:11:34 2022

@author: akseluhr
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# Function to read and return the csv file
def load_file(filename):
        data = pd.read_csv(filename, encoding= 'latin1', sep=';')
        return data

# Calculate total traffic (num of cars) per hour
def traffic_flow_per_hour(data):
    
    # Array for storing 
    n_traffic_per_hour = np.zeros(18)
    time_stamps = data['Tid']
    
    # Transforming timestamps to strings for slicing the hours
    slice_time= time_stamps.str.slice(stop = 2)
    
    # Transforming time (hours) to ints
    hours = np.asarray(slice_time).astype(int) 
    
    # Calculating total occurances for each hour 
    for value in hours:
            n_traffic_per_hour[value] = n_traffic_per_hour[value]+1
 
    # Plotting output
    x = np.arange(7, 18, 1)
    plt.plot(x, n_traffic_per_hour[7:],  color='red', marker='o')
    klock_x= ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    plt.xticks(x, klock_x)
    plt.title('Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11')
    plt.xlabel('Klockslag')
    plt.ylabel('Antal Fordon')
    plt.grid(True)
    plt.show()
        

df_kameraData = load_file('kameraData.csv')
traffic_flow_per_hour(df_kameraData)
