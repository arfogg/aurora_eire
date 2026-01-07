# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:28:30 2026

@author: A R Fogg
"""

import os
import numpy as np
import pandas as pd

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


    def attach_user_data(self, user_input_df):
        
        img_user_data = user_input_df.loc[
            user_input_df.Filename == self.filename]

        # Store initial data
        self.storm_name = img_user_data.Storm
        self.County = img_user_data.County
        self.geo_lat = img_user_data.Latitude
        self.geo_lon = img_user_data.Longitude
        self.direction = img_user_data.Direction
        self.capture_date = img_user_data.Date
        self.capture_time = img_user_data.Time
        self.setting = img_user_data.Setting
        self.device = img_user_data.Device
        # breakpoint()
        self.edited = True if img_user_data.Edited.values[0] == 'yes' else False
        self.user_comment = img_user_data.Comments
        self.filesize = img_user_data.Filesize
        self.filetype = img_user_data.MimeType
        self.make_model_meta_data = img_user_data.Metadata
        self.SubmissionTimestamp = img_user_data.SubmissionTimestamp
        self.ProcessedTimestamp = img_user_data.ProcessedTimestamp

        # Format time
        if pd.isnull(img_user_data.Time) is True:
            print('bananas')
            # ?? here we should consider what time of day, could be better to assume end of day
            self.capture_Timestamp = pd.Timestamp(img_user_data.Date.values[0])
            # Record that time was not provided
            self.time_provided = False
        else:
            print('apples')
            #breakpoint()
            # Add together date and time
            self.capture_Timestamp = pd.Timestamp(img_user_data.Date.values[0] + 'T' + img_user_data.Time.values[0])
            # Record time was provided
            self.time_provided = True
