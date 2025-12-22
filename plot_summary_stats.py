# -*- coding: utf-8 -*-
"""
Created on Mon Dec 22 16:56:57 2025

@author: A R Fogg
"""

import read_data

import string

#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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

def raw_summary_stats():
    
    data, counties, n_photos = read_data.read_summary_admin_actions()
    
    fig = plt.figure(layout=None, figsize=(15, 15))
    gs = fig.add_gridspec(nrows=5, ncols=1, left=0.05, right=0.75,
                          hspace=0.1, wspace=0.05)
    ax0 = fig.add_subplot(gs[:-2, :])
    
    ax1 = fig.add_subplot(gs[-2, -1])
    ax = [ax0, ax1]

    # Pie chart / bar chart showing share of devices ?
    # same for settings
    # same for directions
    # number with geolocation provided
    # number for each storm
    # number of contributors
    
    
    
    
    
    # Timeseries of daily submissions
    # Reformat the data
    # TURN ALL OF THIS STUFF INTO A CLASS
    days = list(data['daily_submissions'].keys())
    date = []
    n_photos = []
    for i in range(len(days)):
        date.append(pd.Timestamp(days[i]) + pd.Timedelta(hours=12))
        n_photos.append(data['daily_submissions'][days[i]])

    # Plot the data
    ax[1].plot(date, n_photos, linewidth=0.,
               marker='o', color='slategrey', markersize=fontsize*0.7)

    ax[1].set_xlabel("Date")    
    ax[1].set_ylabel("Number of Photo\nSubmissions (counts)")

    