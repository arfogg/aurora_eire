# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:28:30 2026

@author: A R Fogg
"""

import os
import numpy as np
import pandas as pd

from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


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

        # Store the image metadata into the class
        self.store_file_metadata()
        self.read_exif_datetime()
        
        # Initialise variables to contain user annotations
        self.annotations = {
            "practical": {},
            "scientific": {}
        }
        self.reviewer = None
        
    def set_reviewer(self, initials):
        self.reviewer = initials


    def attach_user_data(self, user_input_df):
        
        img_user_data = user_input_df.loc[
            user_input_df.Filename == self.filename]

        # Store initial data
        self.storm_name = img_user_data.Storm.values[0]
        self.County = img_user_data.County.values[0]
        self.geo_lat = img_user_data.Latitude.values[0]
        self.geo_lon = img_user_data.Longitude.values[0]
        self.direction = img_user_data.Direction.values[0]
        self.capture_date = img_user_data.Date.values[0]
        self.capture_time = img_user_data.Time.values[0]
        self.setting = img_user_data.Setting.values[0]
        self.device = img_user_data.Device.values[0]
        # breakpoint()
        self.edited = True if img_user_data.Edited.values[0] == 'yes' else False
        self.user_comment = img_user_data.Comments.values[0]
        self.filesize = img_user_data.Filesize.values[0]
        self.filetype = img_user_data.MimeType.values[0]
        # self.make_model_meta_data = img_user_data.Metadata.values[0]
        # breakpoint()
        if img_user_data.Metadata.values[0] == '[]':
            self.camera_make = None
            self.camera_model= None
        else:
            self.camera_make = img_user_data.Metadata.values[0]["camera_make"]
            self.camera_model =img_user_data.Metadata.values[0]["camera_model"]
        self.SubmissionTimestamp = img_user_data.SubmissionTimestamp.values[0]
        self.ProcessedTimestamp = img_user_data.ProcessedTimestamp.values[0]

        # Format time
        if pd.isnull(img_user_data.Time) is True:
            # print('bananas')
            # ?? here we should consider what time of day, could be better to assume end of day
            self.capture_Timestamp = pd.Timestamp(img_user_data.Date.values[0])
            # Record that time was not provided
            self.time_provided = False
        else:
            # print('apples')
            #breakpoint()
            # Add together date and time
            self.capture_Timestamp = pd.Timestamp(img_user_data.Date.values[0] + 'T' + img_user_data.Time.values[0])
            # Record time was provided
            self.time_provided = True

    def store_file_metadata(self):
        """
        Read filesystem creation and modification times.
        """
        stat = os.stat(self.filepath)
    
        self.file_created = datetime.fromtimestamp(stat.st_ctime)
        self.file_modified = datetime.fromtimestamp(stat.st_mtime)
        self.file_size_in_bytes = stat.st_size
    
    def read_exif_datetime(self):
        """
        Read EXIF DateTimeOriginal if present: something available
        from some cameras/software.
        """
        self.exif_datetime = None
    
        try:
            with Image.open(self.filepath) as img:
                exif = img._getexif()
                if exif is None:
                    return
    
                for tag, value in exif.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTimeOriginal":
                        self.exif_datetime = pd.to_datetime(
                            value.replace(":", "-", 2)
                        )
                        return
        except Exception:
            pass

    # def set_annotation(self, section, key, value):
    #     self.annotations[section][key] = value
    
    # def get_annotation(self, section, key, default=None):
    #     return self.annotations[section].get(key, default)
    def set_annotation(self, section, key, value):
        if section not in self.annotations:
            self.annotations[section] = {}
    
        self.annotations[section][key] = value
    
    
    def get_annotation(self, section, key, default=None):
        return self.annotations.get(section, {}).get(key, default)
        
    
    
    def to_flat_dict(self):
        row = {
            "filename": self.filename,
            "file_extension": self.file_extension,
            "image_n": self.image_n,
            "record_id": self.record_id,
            "reviewed_by": getattr(self, "reviewer", None),
            
            "file_created_time": self.file_created,
            "file_modified_time": self.file_modified,
            "exif_datetime": self.exif_datetime,
            "file_size_in_bytes": self.file_size_in_bytes,
            
            
            
            "user_capture_date": self.capture_date,
            "user_capture_time": self.capture_time,
            "capture_Timestamp": self.capture_Timestamp,
            "user_time_provided": self.time_provided,
            "storm_name": self.storm_name,
            "County": self.County,
            "geo_lat": self.geo_lat,
            "geo_lon": self.geo_lon,
            "direction": self.direction,

            "setting": self.setting,
            "device": self.device,
            "edited": self.edited,
            "user_comment": self.user_comment,
            "filesize": self.filesize,
            "filetype": self.filetype,
            "camera_make": self.camera_make,
            "camera_model": self.camera_model,
            "SubmissionTimestamp": self.SubmissionTimestamp,
            "ProcessedTimestamp": self.ProcessedTimestamp,
            
            # "is_night_sky": self.is_night_sky,
            # "is_modified": self.is_modified,
            # "is_during_storm": self.is_during_storm,
            # "is_correct_storm": self.is_correct_storm,
            # "needs_crop": self.needs_crop,
            # "follow_up": self.follow_up,
            # "setting_correct": self.setting_correct,
            # "aurora_brightness": self.aurora_brightness,
            # "aurora_colours": self.aurora_colours,
            # "cloud_cover": self.cloud_cover,
            # "aurora_shapes": self.aurora_shapes,
            # "artifacts": self.artifacts
        }
    
        for section, values in self.annotations.items():
            for key, val in values.items():
                if isinstance(val, set):
                    row[f"{key}"] = ",".join(sorted(val))
                else:
                    row[f"{key}"] = val
    
        return row


    # def determine_capture_time(self):
    #     """
    #     Choose the best available capture timestamp.
    #     """
    #     if self.exif_datetime is not None:
    #         self.capture_timestamp_file = self.exif_datetime
    #         self.capture_source = "EXIF"
    #     else:
    #         self.capture_timestamp_file = self.fs_created
    #         self.capture_source = "filesystem"

