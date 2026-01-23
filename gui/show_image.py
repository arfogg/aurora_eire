# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:01:55 2026

@author: A R Fogg
"""

import os
import sys
import pathlib
from functools import partial

from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout,
                               QSizePolicy, QCheckBox, QRadioButton,
                               QButtonGroup)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from auroral_image_class import AuroralImage

sys.path.append(r'C:\Users\Alexandra\Documents\wind_waves_akr_code\aurora_eire')
from read_data import read_user_input_data


image_dir = os.path.join(
    "C:"+os.sep, r"\Users\Alexandra\Documents\data\aurora_eire\test_images")


class ImageWindow(QLabel):
    """
    Class for an Image Window. Based on a QLabel class which provides a text
    or image display.
    """
    def __init__(self, image_path=None):
        # Initialise the Qt machinery
        super().__init__()

        # Set the Alignment of the image
        self.setAlignment(Qt.AlignCenter)

        # Allow image to grow
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
            )

        # Create empty pixmap variable
        self.pixmap_original = None

        # Set image_path if on first image (otherwise it's set/changed later)
        if image_path is not None:
            self.set_image(image_path)

    def set_image(self, image_path):
        """
        Load a new image and display it.
        """
        # Fill in pixmap_original with a QPixmap made from the image in the
        # filepath. Docs says a QPixmap is an "off-screen image representation
        # that can be used as a paint device"
        # Load the image once, at full resolution
        self.pixmap_original = QPixmap(image_path)
        # Scale image to current widget size and display
        self._update_pixmap()

    def resizeEvent(self, event):
        """
        Rescales the image following window resize events.

        Parameters
        ----------
        event : TYPE
            DESCRIPTION.

        """
        # Resize image if window size is changed
        self._update_pixmap()
        super().resizeEvent(event)

    def _update_pixmap(self):
        """
        Scale the original pixmap to the current widget size and display it.
        """
        if self.pixmap_original and not self.pixmap_original.isNull():
            scaled = self.pixmap_original.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)


class ImageViewer(QWidget):
    # This is the main window
    # it contains other widgets
    # manages the "application state" i.e. which image we're on
    # responds to user actions (buttons)
    def __init__(self, images):

        # Initialise the Qt machinery
        super().__init__()

        # Store the image paths into the class
        self.images = images

        # Store number of images
        self.n_images = len(self.images)

        # Initialise tracker for which image we are on
        self.index = 0

        # Start up the ImageWindow, pass it the path for image 0
        self.image_label = ImageWindow(self.images[self.index].filepath)

        # Create gui label for image counter
        self.image_title = QLabel()
        self.image_title.setAlignment(Qt.AlignCenter)

        # Metadata panel container
        self.metadata_panel = QWidget()
        self.metadata_layout = QVBoxLayout(self.metadata_panel)
        
        # Metadata title
        self.metadata_title = QLabel("Image Metadata")
        self.metadata_title.setAlignment(Qt.AlignLeft)
        self.metadata_title.setStyleSheet("font-weight: bold;")
        
        # Metadata content
        self.metadata_label = QLabel()
        self.metadata_label.setAlignment(Qt.AlignTop)
        self.metadata_label.setWordWrap(True)
        
        self.metadata_layout.addWidget(self.metadata_title)
        self.metadata_layout.addWidget(self.metadata_label)
        self.metadata_layout.addStretch()

        

        # Create a Next button
        self.next_button = QPushButton("Next")
        # Clicked is the signal we get from next_button
        # next_image is a method that runs when we click
        self.next_button.clicked.connect(self.next_image)

        # Create a Previous button
        self.previous_button = QPushButton("Previous")
        # Clicked is the signal we get from next_button
        # next_image is a method that runs when we click
        self.previous_button.clicked.connect(self.previous_image)

        # # Main horizontal layout
        # main_layout = QHBoxLayout()
        
        # Left-hand side: image + title + buttons
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.image_title)
        left_layout.addWidget(self.previous_button)
        left_layout.addWidget(self.next_button)
        
        # # Right-hand side: metadata

        # Initialise Right Hand Panel
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        # Add title
        self.right_title = QLabel(
            "Aurora Éire Image review\nMay = 10th-14th May 2024\nOct = 10th-14th Oct 2024")
        self.right_title.setAlignment(Qt.AlignCenter)
        self.right_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.right_layout.addWidget(self.right_title)

        # Initialise metadata place
        self.metadata_row = QWidget()
        self.metadata_row_layout = QHBoxLayout(self.metadata_row)
        self.image_metadata_panel = QWidget()
        self.image_metadata_layout = QVBoxLayout(self.image_metadata_panel)
        
        self.image_metadata_title = QLabel("Image metadata")
        self.image_metadata_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.image_metadata_layout.addWidget(self.image_metadata_title)
        self.image_metadata_layout.addWidget(self.metadata_label)
        self.image_metadata_layout.addStretch()

        
        # User inputs place
        self.user_metadata_panel = QWidget()
        self.user_metadata_layout = QVBoxLayout(self.user_metadata_panel)
        
        self.user_metadata_title = QLabel("User metadata")
        self.user_metadata_title.setStyleSheet("font-weight: bold;")
        
        self.user_metadata_label = QLabel()
        self.user_metadata_label.setAlignment(Qt.AlignTop)
        self.user_metadata_label.setWordWrap(True)
        
        self.user_metadata_layout.addWidget(self.user_metadata_title)
        self.user_metadata_layout.addWidget(self.user_metadata_label)
        self.user_metadata_layout.addStretch()
        

        self.metadata_row_layout.addWidget(self.image_metadata_panel)
        self.metadata_row_layout.addWidget(self.user_metadata_panel)
        
        self.right_layout.addWidget(self.metadata_row)
        self.annotations_panel = QWidget()
        self.annotations_layout = QVBoxLayout(self.annotations_panel)
        
        
        # PRACTICAL QUESTIONS
        self.practical_title = QLabel("Practical questions")
        self.practical_title.setStyleSheet("font-weight: bold;")

        self.annotations_layout.addWidget(self.practical_title)

        # Is it the night sky
        self.is_night_sky_checkbox = QCheckBox("Is this an image of the night sky?")
        self.is_night_sky_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "is_night_sky")
        )
        self.annotations_layout.addWidget(self.is_night_sky_checkbox)    

        # Compare the metadata and user date/time. Do they match (to the minute)?


        # Based on the modified vs capture time, did the user edit the photo?
        self.is_modified_checkbox = QCheckBox("Based on the modified vs capture time, did the user edit the photo?")
        self.is_modified_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "is_modified")
        )
        self.annotations_layout.addWidget(self.is_modified_checkbox)    


        # Is the input datetime during either storm?
        self.is_during_storm_checkbox = QCheckBox("Is the datetime during either storm?")
        self.is_during_storm_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "is_during_storm")
        )
        self.annotations_layout.addWidget(self.is_during_storm_checkbox)    

        # Based on the dates, did the user select the correct storm?
        self.is_correct_storm_checkbox = QCheckBox("Based on the dates, did the user select the correct storm?")
        self.is_correct_storm_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "is_correct_storm")
        )
        self.annotations_layout.addWidget(self.is_correct_storm_checkbox)    

        # Will we need to crop this (i.e. to remove someone's face, or if it's a screenshot, crop around the image)
        self.needs_crop_checkbox = QCheckBox("Will we need to crop this image? (e.g. to remove someone's face, or if it's a screenshot, crop around the image)")
        self.needs_crop_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "needs_crop")
        )
        self.annotations_layout.addWidget(self.needs_crop_checkbox)    

        # Do we need a follow up discussion on this image        
        self.follow_up_checkbox = QCheckBox("Does this image require follow up discussion")
        self.follow_up_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "follow_up")
        )
        self.annotations_layout.addWidget(self.follow_up_checkbox)    
        
        # Do we need a follow up discussion on this image        
        self.setting_correct = QCheckBox("Does the user-selected setting look correct?")
        self.setting_correct.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "setting_correct")
        )
        self.annotations_layout.addWidget(self.setting_correct)    
        
                
        
        
                
        self.scientific_title = QLabel("Scientific notes")
        self.scientific_title.setStyleSheet("font-weight: bold;")
        self.annotations_layout.addSpacing(10)
        self.annotations_layout.addWidget(self.scientific_title)  
        
                
        # Can we see aurora?
        self.aurora_present_checkbox = QCheckBox("Can you see any aurorae in this image?")
        self.aurora_present_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "scientific", "aurora_present")
        )
        self.annotations_layout.addWidget(self.aurora_present_checkbox)    

        # Is it faint/bright?
        self.brightness_button = self.add_radio_group(
            layout=self.annotations_layout,
            title="How bright are the Aurorae in this image?",
            options=["Faint", "Moderate", "Bright"],
            on_change=lambda value: self.annotation_radio_changed(
                section="scientific",
                key="aurora_brightness",
                value=value.lower()
            )
        )

        # What colours can we see? (green/red/pink/purple/...?)

        # Sky state: clear/some cloud/lots of cloud
        self.cloud_button = self.add_radio_group(
            layout=self.annotations_layout,
            title="How much cloud cover is there?",
            options=["No clouds", "Some cloud cover", "Completely clouded"],
            on_change=lambda value: self.annotation_radio_changed(
                section="scientific",
                key="cloud_cover",
                value=value.lower()
            )
        )
        # What shapes of aurora can we see (according to the herlingshaw guide)
                
        
        
        
        
        
        self.annotations_layout.addStretch()

        self.right_layout.addWidget(self.annotations_panel, stretch=1)

        main_layout = QHBoxLayout()
        
        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addWidget(self.right_panel, stretch=2)
        
        self.setLayout(main_layout)

        # Window title
        self.setWindowTitle("Aurora Éire Image Viewer")
        # Initial window size
        self.resize(700, 700)

        # Update buttons, title, etc
        self.image_change_updates()

    def annotation_radio_changed(self, section, key, value):
        image = self.images[self.index]
        image.set_annotation(section=section, key=key, value=value)

    def set_radio_group_value(self, group, value):
        for button in group.buttons():
            button.blockSignals(True)
            button.setChecked(button.text().lower() == value)
            button.blockSignals(False)

    def add_radio_group(self, layout, title, options, on_change=None):
        """
        Create a titled radio-button group and add it to a layout.
    
        Parameters
        ----------
        layout : QLayout
            Layout to add widgets to.
        title : str
            Title shown above the radio buttons.
        options : list[str]
            List of option labels.
        on_change : callable, optional
            Function called with selected text when selection changes.
    
        Returns
        -------
        QButtonGroup
        """
        # Title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label)
    
        # Button group
        group = QButtonGroup(self)
    
        for opt in options:
            button = QRadioButton(opt)
            group.addButton(button)
            layout.addWidget(button)
    
        if on_change is not None:
            group.buttonClicked.connect(
                lambda btn: on_change(btn.text())
            )
    
        return group



    def annotation_checkbox_changed(self, section, key, state):
        image = self.images[self.index]
        value = (state == Qt.Checked)
    
        image.set_annotation(
            section=section,
            key=key,
            value=value
        )


    def set_checkbox(self, checkbox, value):
        checkbox.blockSignals(True)
        checkbox.setChecked(bool(value))
        checkbox.blockSignals(False)

    def update_annotations(self):
        image = self.images[self.index]
    
        # value = image.get_annotation(
        #     "practical",
        #     "is_night_sky",
        #     default=False
        # )
    
        # self.is_night_sky_checkbox.blockSignals(True)
        # self.is_night_sky_checkbox.setChecked(value)
        # self.is_night_sky_checkbox.blockSignals(False)

        # Practical annotations
        # Checkboxes
        for cb in ["is_night_sky", "is_modified", "is_during_storm",
                   "is_correct_storm", "needs_crop", "follow_up",
                   "setting_correct"]:
            self.set_checkbox(
                self.is_night_sky_checkbox,
                image.get_annotation("practical", cb, False)
            )


        # Scientific annotations
        # Checkboxes
        for cb in ["aurora_present"]:
            self.set_checkbox(
                self.is_night_sky_checkbox,
                image.get_annotation("scientific", cb, False)
            )


        brightness = image.get_annotation(
            "scientific",
            "aurora_brightness",
            default=None
        )
        
        self.set_radio_group_value(self.brightness_button, brightness)


        cloudy = image.get_annotation(
            "scientific",
            "cloud_cover",
            default=None
        )
        
        self.set_radio_group_value(self.cloud_button, cloudy)








    def update_metadata(self):
        image = self.images[self.index]

        fc = self.images[self.index].file_created
        fm = self.images[self.index].file_modified
        ex = self.images[self.index].exif_datetime

        text = (
            # f"Record ID: {image.record_id}\n"
            f"File created: {fc}\n"
            f"File modified: {fm}\n"
            f"EXIF time: {ex}\n"
            f"File size: {image.file_size_in_bytes} bytes\n"  
        )

        self.metadata_label.setText(text)

    def update_userinput(self):
        image = self.images[self.index]

        text = (
            f"Date: {image.capture_date}\n"
            f"Time: {image.capture_time}\n"
            f"Time provided?: {image.time_provided}\n"
            f"Storm: {image.storm_name}\n"
            f"User says setting: {image.setting}\n"
            f"User says edited: {image.edited}\n"
            "\n"
            f"User comment: {image.user_comment}\n"
        )
    
        self.user_metadata_label.setText(text)


    def update_image_title(self):
        """
        Update the image title.

        Returns
        -------
        None.

        """
        current = self.index + 1  # Going from 1 -> n_images
        total = self.n_images
        self.image_title.setText(
            f"Image {current} / {total}\n"
            + f"Filename: {self.images[self.index].filename}\n"
            + f"Record ID: {self.images[self.index].record_id}")

    def next_image(self):
        """
        Move to the next image.

        Returns
        -------
        None.

        """
        if self.index < (self.n_images - 1):
            self.index += 1
            self.image_label.set_image(self.images[self.index].filepath)
            self.image_change_updates()

    def previous_image(self):
        """
        Move to the previous image.

        Returns
        -------
        None.

        """
        if self.index > 0:
            self.index -= 1
            self.image_label.set_image(self.images[self.index].filepath)
            self.image_change_updates()

    def update_buttons(self):
        """
        Updates the next and previous buttons.

        Returns
        -------
        None.

        """
        self.previous_button.setEnabled(self.index > 0)
        self.next_button.setEnabled(self.index < (self.n_images - 1))

    def image_change_updates(self):
        """
        Updates buttons, text/labels, etc

        Returns
        -------
        None.

        """
        self.update_buttons()
        self.update_image_title()
        self.update_metadata()
        self.update_userinput()
        self.update_annotations()


def list_images():

    user_data_df = read_user_input_data()
    
    # NEEDS TO BE MORE GENERAL FOR ALL FILETYPES
    # Automatically list PNG and JPEG images in the directory
    image_files = sorted([
        str(p) for p in pathlib.Path(image_dir).glob("*")
        if p.suffix.lower() in [".png", ".jpg", ".jpeg"]
    ])

    if not image_files:
        raise ValueError(f"No images found in {image_dir}")

    images = []
    for i, path in enumerate(image_files):
        img = AuroralImage(filepath=str(path), image_n=i)
        img.attach_user_data(user_data_df)

        images.append(img)
        # images.append(
        #     AuroralImage(filepath=str(path), image_n=i)
        # )

    return images


def main():
    

    images = list_images()
    


    app = QApplication(sys.argv)

    viewer = ImageViewer(images)
    viewer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
