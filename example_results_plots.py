# -*- coding: utf-8 -*-
"""
Created on Wed Sep 10 15:31:21 2025

@author: A R Fogg
"""

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def aurora_over_ireland():
    
    fig, ax = plt.subplots()
    
    ax = create_map_of_ireland(ax)

def create_map_of_ireland(ax, plot_MagIE=True,
                          markersize=1650):
    """
    Draw a map of Ireland onto the parsed axis.

    Parameters
    ----------
    ax : matplotlib axis object
        Axis to draw map onto.
    plot_MagIE : bool, optional
        If True, crosses are drawn over approximate locations of MagIE
        magnetometers. The default is True.
    markersize : int, optional
        Size of markers for MagIE. The default is 1650.

    Returns
    -------
    None.

    """

    # Setup Lambert Conformal basemap
    m = Basemap(width=400000, height=500000, projection='lcc', resolution='i',
                lat_0=53.336585, lon_0=-7.806423, ax=ax)

    # Draw coastlines
    m.drawcoastlines()
    # Draw a boundary around the map, fill the background.
    m.drawmapboundary(fill_color='lightskyblue')
    # Fill continents, set lake color same as ocean color.
    m.fillcontinents(color='lightgreen', lake_color='lightskyblue')


    if plot_MagIE:
        # Approximate location of Dunsink Observatory (from Google Maps)
        lat_dun, lon_dun = 53.387371, -6.338553
        # Approximate location of Valentia Magnetometer (from SuperMAG)
        lat_val, lon_val = 51.93, 349.75-360.
        # Concat arrays
        lat = [lat_dun, lat_val]
        lon = [lon_dun, lon_val]
        # Convert to map projection coords.
        xpt, ypt = m(lon, lat)
        # Convert back to lat/lon
        lonpt, latpt = m(xpt, ypt, inverse=True)
        m.scatter(xpt, ypt, marker='X', color='gold', edgecolor='black',
                  s=markersize, zorder=5)

