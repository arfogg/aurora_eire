# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:28:30 2026

@author: A R Fogg
"""

import os

class submitted_image():
    """
    A class containing the information for an individual photo.
    """

    def __init__(self, filepath, record_id):

        # Store the filepath, name, extension
        self.filepath = filepath
        self.filename = os.path.split(self.filepath)[1]
        self.file_extension = os.path.splitext(self.filepath)[1]        

        # Store the unique number describing this image
        self.record_id = record_id

