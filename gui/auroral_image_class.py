# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:28:30 2026

@author: A R Fogg
"""

import os


class AuroralImage():
    """
    A class containing the information for an individual photo.
    """

    def __init__(self, filepath, image_n):

        # Store the filepath, name, extension
        self.filepath = filepath
        self.filename = os.path.split(self.filepath)[1]
        self.file_extension = os.path.splitext(self.filepath)[1]

        # Store the number in the list i.e. 1-10 images
        self.image_n = image_n
        # Store the unique catalogue / metadata ID number describing this image
        self.record_id = self.filename[0:len(self.file_extension)-2]
