# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 11:56:18 2025

@author: A R Fogg
"""

import os
import json

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

import numpy as np

data_dir = os.path.join("C:"+os.sep,
                        r"Users\Alexandra\Documents\irish_citizen_science_auroral_project\data")



def read_summary_admin_actions():
    
    json_f = os.path.join(data_dir, "admin_actions.json")
    


    with open(json_f) as f:
        data = json.load(f)

    # Sort per county data
    d_sorted = dict(sorted(data['counties'].items(), key=lambda x: x[1], reverse=True))

    counties = np.array(list(d_sorted.keys()))
    n_photos = np.array(list(d_sorted.values()))

    return data, counties, n_photos

def read_county_borders():
    
    json_f = os.path.join(data_dir, "counties_geojson", "counties.geojson")


    gdf = gpd.read_file(json_f)
    
    return gdf
    
def read_rep_census():
    
    rep = os.path.join(data_dir, "population",
                       "rep_census_2022.csv")
                       #"rep_ire_census_2022_pop_by_county.csv")
    
    rep_df = pd.read_csv(rep)
    
    rep_total_pop = rep_df['VALUE'].iloc[0]
    

    # Counties without seperate city/county council values
    county = []
    pop = []
    for i in [1] + list(range(6, 17)) + list(range(19,23)) + list(range(25, 32)):
        county.append(rep_df['Administrative Counties'].iloc[i].split()[0])
        pop.append(rep_df['VALUE'].iloc[i])


    # 2, 3, 4, 5 rows are the four Dublin councils
    dub_pop = rep_df['VALUE'].iloc[2] + rep_df['VALUE'].iloc[3] + \
        rep_df['VALUE'].iloc[4] + rep_df['VALUE'].iloc[5]
    county.append('Dublin')
    pop.append(dub_pop)
    
    # 17, 18 rows are the Cork rows
    cork_pop = rep_df['VALUE'].iloc[17] + rep_df['VALUE'].iloc[18]
    county.append('Cork')
    pop.append(cork_pop)
    
    # 23, 24 rows are the Galway rows
    gal_pop = rep_df['VALUE'].iloc[23] + rep_df['VALUE'].iloc[24]
    county.append('Galway')
    pop.append(gal_pop)
    
    rep_pop_df = pd.DataFrame({'County': county, 'Population': pop})    

    return rep_pop_df

def read_ni_census():
    
    ni = os.path.join(data_dir, "population", "ni_census_2021.csv")
    
    ni_df = pd.read_csv(ni)
    
    county = []
    pop = []
    for i in range(len(ni_df)):
        if ni_df['County Label'].iloc[i] == "Derry/Londonderry":
            county.append("Derry")
        else:
            county.append(ni_df['County Label'].iloc[i])
        pop.append(ni_df['Count'].iloc[i])
    
    ni_pop_df = pd.DataFrame({'County': county, 'Population': pop})

    return ni_pop_df

def combined_pop():
    
    rep_pop_df = read_rep_census()
    ni_pop_df = read_ni_census()
    
    comb_df = pd.concat([rep_pop_df, ni_pop_df])
    comb_df = comb_df.sort_values('County').reset_index(drop=True)
    
    return comb_df