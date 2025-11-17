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

  