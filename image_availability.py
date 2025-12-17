# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 12:00:45 2025

@author: A R Fogg
"""

import os
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt

import read_data

fontsize = 10

county_names = np.array(["Antrim", "Armagh", "Carlow", "Cavan", "Clare",
                         "Cork", "Derry", "Donegal", "Down", "Dublin",
                         "Fermanagh", "Galway", "Kerry", "Kildare", "Kilkenny",
                         "Laois", "Leitrim", "Limerick", "Longford", "Louth",
                         "Mayo", "Meath", "Monaghan", "Offaly", "Roscommon",
                         "Sligo", "Tipperary", "Tyrone", "Waterford",
                         "Westmeath", "Wexford", "Wicklow"
                         ])

fig_dir = os.path.join("C:"+os.sep,
                       r"Users\Alexandra\Documents\figures\aurora_eire")

def county_bar_chart():

    data, counties, n_photos = read_data.read_summary_admin_actions()

    missing_counties = np.array(list(set(county_names) - set(counties)))
    
    for c in missing_counties:
        counties = np.append(counties, c)
        n_photos = np.append(n_photos, 0)

    fig, ax = plt.subplots()

    ax.bar(counties, n_photos, color='#169B62')
    ax.tick_params("x", rotation=90)
    ax.set_ylabel("Number of photos", fontsize=fontsize)
    ax.set_xlabel("County", fontsize=fontsize)
    ax.set_title("Number of photos: " + str(data['total_photos']))

    ax.axhline(10, linestyle='dashed', color='grey')

    fig.tight_layout()

    figname = os.path.join(fig_dir,
                           "county_availability_bar_" + dt.datetime.now().strftime("%Y_%m_%d") + ".png")

    fig.savefig(figname)
    
def map_availability():
    
    # Read in County Borders
    gdf = read_data.read_county_borders()
    
    # Derry is missing "None" value
    gdf.NAME_EN[30] = "County Derry"
    
    # Read in Photo collection data
    data, counties, n_photos = read_data.read_summary_admin_actions()
    
    gdf_count_list = np.full(len(gdf), np.nan)
    for i in range(len(gdf)):
        gdf_string = gdf.NAME_EN[i]
        data_i, = np.where(counties == gdf_string[7:])
        gdf_count_list[i] = n_photos[data_i]
    # gdf.boundary.plot(figsize=(8, 10), color='black', linewidth=1.5)
    # plt.title("County Boundaries of Ireland")
    # plt.show()   

    gdf['color_index'] = gdf_count_list
    # create a numeric column for coloring
    #gdf["color_index"] = range(len(gdf))
    
    fig, ax = plt.subplots(figsize=(8, 10))
    
    gdf.plot(
        column="color_index",      # assign colors by index
        cmap="plasma",              # or try: Set3, tab10, Paired, Pastel1
        legend=True,              # turn on if you want a legend
        ax=ax,
        edgecolor="black",         # draw borders
        linewidth=0.3
    )
    
    ax.set_title("n photos per county")
    ax.set_axis_off()
    
    #fig.colorbar(s, ax=ax)
    
    plt.show()
    
    # NEED TO GO THROUGH AND EYEBALL THE COUNTY OUTLINES TO MAKE SURE THEY LOOK OK