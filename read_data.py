# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 11:56:18 2025

@author: A R Fogg
"""

import os
import numpy as np

data_dir = os.path.join("C:"+os.sep,
                        r"Users\Alexandra\Documents\irish_citizen_science_auroral_project\data")



def read_summary_admin_actions():
    
    json_f = os.path.join(data_dir, "admin_actions.json")
    

    import json

    with open(json_f) as f:
        data = json.load(f)

    # Sort per county data
    d_sorted = dict(sorted(data['counties'].items(), key=lambda x: x[1], reverse=True))

    counties = np.array(list(d_sorted.keys()))
    n_photos = np.array(list(d_sorted.values()))

    return data, counties, n_photos