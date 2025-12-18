# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 12:00:45 2025

@author: A R Fogg
"""

import os
import string
import numpy as np
import datetime as dt

import matplotlib.pyplot as plt

import read_data


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

# Set up fontsizes
fontsize = 20
plt.rcParams['font.size'] = fontsize
plt.rcParams['axes.titlesize'] = fontsize
plt.rcParams['axes.labelsize'] = fontsize
plt.rcParams['xtick.labelsize'] = fontsize
plt.rcParams['ytick.labelsize'] = fontsize
plt.rcParams['legend.fontsize'] = fontsize

alphabet = list(string.ascii_lowercase)
axes_labels = []
for a in alphabet:
    axes_labels.append('(' + a + ')')


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

    # Read in Population data
    pop_df = read_data.combined_pop()

    # Initialise empty arrays for photo and population data
    gdf_count_list = np.full(len(gdf), np.nan)
    gdf_pop_list = np.full(len(gdf), np.nan)
    # Find the corresponding rows so the photo/pop data can go into the gdf
    for i in range(len(gdf)):
        gdf_string = gdf.NAME_EN[i]
        # Photo numbers
        data_i, = np.where(counties == gdf_string[7:])
        gdf_count_list[i] = n_photos[data_i]
        # Population stats
        pop_i, = np.where(pop_df['County'] == gdf_string[7:])
        gdf_pop_list[i] = pop_df['Population'].iloc[pop_i]

    # Add in photo and population columns to gdf object
    gdf['n_photos'] = gdf_count_list
    gdf['population'] = gdf_pop_list
    gdf['n_photos_normpop'] = (gdf_count_list / gdf_pop_list) * 100.

    # Initialise figure
    fig, ax = plt.subplots(ncols=3, figsize=(24, 10))

    # Pure photo counts
    gdf.plot(column="n_photos",
             legend=True,
             ax=ax[0],
             cmap="summer", edgecolor="black",             
             linewidth=0.4,
             legend_kwds={"label": "Number of Photos (counts)",
                          "orientation": "horizontal",
                          "pad": 0.01})

    # Population
    gdf.plot(column="population",
             legend=True,
             ax=ax[1],
             cmap="viridis", edgecolor="black",
             linewidth=0.4,
             legend_kwds={"label": "Population (counts)",
                          "orientation": "horizontal",
                          "pad": 0.01})

    # Normalised photo counts
    gdf.plot(column="n_photos_normpop",
             legend=True,
             ax=ax[2],
             cmap="Wistia_r", edgecolor="black",
             linewidth=0.4,
             legend_kwds={"label": "Number of Photos Normalised by Population (%)",
                          "orientation": "horizontal",
                          "pad": 0.01})

    # Formatting bits
    for (i, a) in enumerate(ax):
        t = a.text(0.07, 0.93, axes_labels[i], transform=a.transAxes,
                    fontsize=fontsize*1.5, va='top', ha='left')
        t.set_bbox(dict(facecolor='white', alpha=0.75, edgecolor='grey'))
        a.set_axis_off()

    fig.tight_layout()
    # plt.show()

    # do one with a dot for every geo location given
    # NEED TO GO THROUGH AND EYEBALL THE COUNTY OUTLINES TO MAKE SURE THEY LOOK OK