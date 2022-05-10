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
def traffic_flow_per_hour(kamera):
    
    # Array for storing 
    antal = np.zeros(18)
    tider = kamera['Tid']
    print(tider)
    
    # Transforming timestamps to strings and taking the hours
    slct= tider.str.slice(stop = 2)
    print(slct)
    
    # Transforming 
    timme = np.asarray(slct).astype(int)
    print(len(timme))      
    for value in timme:
            antal[value] = antal[value]+1
        
    plt.plot(x, antal[7:],  color='red', marker='o')
    klock_x= ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
    plt.xticks(x, klock_x)
    plt.title('Totalt antal fordon som kamerorna registrerar i mätområdet 2021-09-11')
    plt.xlabel('Klockslag')
    plt.ylabel('Antal Fordon')
    plt.grid(True)
    plt.show()
        

df_kameraData = load_file('kameraData.csv')
x = np.arange(7, 18, 1)
traffic_flow_per_hour(df_kameraData)
