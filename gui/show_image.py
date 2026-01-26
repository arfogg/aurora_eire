# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:01:55 2026

@author: A R Fogg
"""

import os
import sys
import csv
import pathlib
from functools import partial

from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout,
                               QSizePolicy, QCheckBox, QRadioButton,
                               QButtonGroup, QGridLayout, QMessageBox,
                               QDialog, QLineEdit)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from auroral_image_class import AuroralImage

sys.path.append(r'C:\Users\Alexandra\Documents\wind_waves_akr_code\aurora_eire')
from read_data import read_user_input_data

# This is the path where you put the images
image_dir = os.path.join(
    "C:"+os.sep, r"\Users\Alexandra\Documents\data\aurora_eire\test_images")

output_data_dir = os.path.join(
    "C:"+os.sep,
    r"\Users\Alexandra\Documents\data\aurora_eire\pass1_annotations")
# OUTPUT_CSV = "aurora_annotations.csv"

ALLOWED_USERS = {
    "ARF": "Alexandra",
    "SAM": "Sophie",
    "SJW": "Simon",
    "DMH": "Daragh"
}


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
    def __init__(self, images, user_initials, user_name):

        # Initialise the Qt machinery
        super().__init__()

        # Store the image paths into the class
        self.images = images
        
        # Store the current user
        self.user_initials = user_initials
        self.user_name = user_name

        # Store number of images
        self.n_images = len(self.images)

        # Initialise tracker for which image we are on
        self.index = 0

        # Start up the ImageWindow, pass it the path for image 0
        self.image_label = ImageWindow(self.images[self.index].filepath)

        # Create gui label for image counter
        self.image_title = QLabel()
        self.image_title.setAlignment(Qt.AlignCenter)
 
        # Metadata content
        self.metadata_label = QLabel()
        self.metadata_label.setAlignment(Qt.AlignTop)
        self.metadata_label.setWordWrap(True)

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
        
        self.user_label = QLabel(f"Hello {self.user_name}, thank you for reviewing images today!")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        self.right_layout.insertWidget(0, self.user_label)

        self.user_metadata_title = QLabel("User metadata")
        self.user_metadata_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        
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
        self.practical_title.setStyleSheet("font-weight: bold; font-size: 14px;")

        self.annotations_layout.addWidget(self.practical_title)

        # Is it the night sky
        self.is_night_sky_checkbox = QCheckBox("Is this an image of the night sky?")
        self.is_night_sky_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "is_night_sky")
        )
        self.annotations_layout.addWidget(self.is_night_sky_checkbox)    

        # Based on the modified vs capture time, did the user edit the photo?
        self.is_modified_checkbox = QCheckBox("Based on the modified vs capture time, did the user edit the photo?")
        self.is_modified_checkbox.stateChanged.connect(
            partial(self.annotation_checkbox_changed, "practical", "is_modified")
        )
        self.annotations_layout.addWidget(self.is_modified_checkbox)    

        # Is the input datetime during either storm?
        self.is_during_storm_checkbox = QCheckBox("Are any of the datetimes during either storm?")
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
        
        # Scientific Annotations
        self.scientific_title = QLabel("Scientific notes")
        self.scientific_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.annotations_layout.addSpacing(10)
        self.annotations_layout.addWidget(self.scientific_title)  
        
        # # Can we see aurora?
        # self.aurora_present_checkbox = QCheckBox("Can you see any aurorae in this image?")
        # self.aurora_present_checkbox.stateChanged.connect(
        #     partial(self.annotation_checkbox_changed, "scientific", "aurora_present")
        # )
        # self.annotations_layout.addWidget(self.aurora_present_checkbox)    

        # Is it faint/bright?
        self.brightness_button = self.add_radio_group(
            layout=self.annotations_layout,
            title="How bright are the Aurorae in this image?* [select one]",
            options=["No aurora", "Faint", "Moderate", "Bright"],
            on_change=lambda value: self.annotation_radio_changed(
                section="scientific",
                key="aurora_brightness",
                value=value.lower()
                )
        )

        # What colours can we see? (green/red/pink/purple/...?)
        self.aurora_colours = self.add_multiselect_checkboxes(
            layout=self.annotations_layout,
            title="Which aurorae colours can you identify? [select none-multiple]",
            options=["No aurora", "Green", "Red", "Blue", "Purple",
                     "Pink", "Black", "Sunlit top"],
            section="scientific",
            key="aurora_colours",
            columns=7
        )

        # Sky state: clear/some cloud/lots of cloud
        self.cloud_button = self.add_radio_group(
            layout=self.annotations_layout,
            title="How much cloud cover is there?* [select one]",
            options=["No clouds", "Some cloud cover", "Completely clouded"],
            on_change=lambda value: self.annotation_radio_changed(
                section="scientific",
                key="cloud_cover",
                value=value.lower()
            )
        )

        # What shapes of aurora can we see (according to the herlingshaw guide)
        self.aurora_shapes = self.add_multiselect_checkboxes(
            layout=self.annotations_layout,
            title="Which auroral forms can you identify? [select none-multiple]",
            options=["No aurora", "Quiet Arc", "Active Arc", "Rays/Pillars",
                     "Rayed Arc/Curtain", "Bands", "Beads", "Curls", "Folds",
                     "Spiral/Cinnamon Roll", "Corona",
                     "Westward Travelling Surge", "Enhanced Aurora"],
            section="scientific",
            key="aurora_shapes",
            columns=5
        )   
             
        # Any other artifacts present? stars / moon / light pollution / ground level object (tree/car/animal)
        self.artifacts = self.add_multiselect_checkboxes(
            layout=self.annotations_layout,
            title="Are there any other artifacts partially blocking the aurora? [select none-multiple]",
            options=["None", "Stars", "Moon", "Light Pollution",
                     "Ground object (tree/car/animal)",
                     "Sky object (e.g. plane/helicopter/UAF)"],
            section="scientific",
            key="artifacts",
            columns=4
        )   

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


    # -------------------------------------------------------
    # Helper Functions for different annotations
    #
    # MULTISELECT -------------------------------------------
    def set_multiselect(self, checkbox_dict, values):
        """
        Set/reset values for a multiselect widget.

        Parameters
        ----------
        checkbox_dict : TYPE
            DESCRIPTION.
        values : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        if values is None:
            values = set()
    
        for value, checkbox in checkbox_dict.items():
            checkbox.blockSignals(True)
            checkbox.setChecked(value in values)
            checkbox.blockSignals(False)

    def multiselect_changed(self, section, key, option, state):
        """
        Changer function for multiselect widget.

        Parameters
        ----------
        section : TYPE
            DESCRIPTION.
        key : TYPE
            DESCRIPTION.
        option : TYPE
            DESCRIPTION.
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        image = self.images[self.index]
        current = image.get_annotation(section, key, default=set())

        # Ensure we are working with a set
        if not isinstance(current, set):
            current = set(current)
    
        if state == Qt.Checked:
            current.add(option.lower())
        else:
            current.discard(option.lower())
    
        image.set_annotation(section, key, current)
        self.update_buttons()

    def add_multiselect_checkboxes(self, layout, title, options, section,
                                   key, columns=4):
        """
        Create a titled group of checkboxes arranged in a grid (wrapping).
        """
        title_label = QLabel(title)
        layout.addWidget(title_label)
    
        grid = QGridLayout()
        grid.setHorizontalSpacing(15)
        grid.setVerticalSpacing(5)
    
        checkboxes = {}
    
        for i, opt in enumerate(options):
            row = i // columns
            col = i % columns
    
            cb = QCheckBox(opt)
            cb.stateChanged.connect(
                lambda state, o=opt: self.multiselect_changed(
                    section, key, o, state
                )
            )
    
            grid.addWidget(cb, row, col)
            checkboxes[opt.lower()] = cb

        layout.addLayout(grid)

        return checkboxes

    # RADIO GROUPS -------------------------------------------
    def annotation_radio_changed(self, section, key, value):
        """
        Changer function for radio group widgets.

        Parameters
        ----------
        section : TYPE
            DESCRIPTION.
        key : TYPE
            DESCRIPTION.
        value : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        image = self.images[self.index]
        image.set_annotation(section=section, key=key, value=value)
        self.update_buttons()

    def set_radio_group_value(self, group, value):
        """
        Set/reset the value of a radio group widget.

        Parameters
        ----------
        group : TYPE
            DESCRIPTION.
        value : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # Temporarily allow unchecking all buttons
        group.setExclusive(False)
    
        for button in group.buttons():
            button.blockSignals(True)
            button.setChecked(False)
            button.blockSignals(False)
    
        group.setExclusive(True)
    
        # Now set the desired value (if any)
        if value is not None:
            for button in group.buttons():
                if button.text().lower() == value:
                    button.blockSignals(True)
                    button.setChecked(True)
                    button.blockSignals(False)
                    break


    def add_radio_group(self, layout, title, options, on_change=None):
        """
        Create a titled radio-button group widget and add it to a layout.
    
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
        #title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label)
    
        # Button group
        group = QButtonGroup(self)
        
        button_layout = QHBoxLayout()
        
        for opt in options:
            button = QRadioButton(opt)
            group.addButton(button)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        if on_change is not None:
            group.buttonClicked.connect(
                lambda btn: on_change(btn.text())
            )
    
        return group

    # CHECKBOXES -------------------------------------------
    def annotation_checkbox_changed(self, section, key, state):
        """
        Changer function for checkbox widget.

        Parameters
        ----------
        section : TYPE
            DESCRIPTION.
        key : TYPE
            DESCRIPTION.
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        image = self.images[self.index]
        value = (state == Qt.Checked)
    
        image.set_annotation(
            section=section,
            key=key,
            value=value
        )
        self.update_buttons()

    def set_checkbox(self, checkbox, value):
        """
        Set/reset checkbox widget.

        Parameters
        ----------
        checkbox : TYPE
            DESCRIPTION.
        value : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        checkbox.blockSignals(True)
        # checkbox.setChecked(bool(value))
        checkbox.setChecked(bool(value))
        checkbox.blockSignals(False)
    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    # UPDATE FUNCTIONS
    #
    # UPDATE ANNOTATIONS ------------------------------------
    def update_annotations(self):
        """
        Function to update all annotations when needed.

        Returns
        -------
        None.

        """
        image = self.images[self.index]

        # Practical annotations
        cbs = [self.is_night_sky_checkbox, self.is_modified_checkbox,
              self.is_during_storm_checkbox, self.is_correct_storm_checkbox,
              self.needs_crop_checkbox, self.follow_up_checkbox,
              self.setting_correct]
        cb_values = ["is_night_sky", "is_modified", "is_during_storm",
                   "is_correct_storm", "needs_crop", "follow_up",
                   "setting_correct"]
        # Checkboxes
        # for k, (cb, cb_value) in enumerate(zip(cbs, cb_values)):
        #     self.set_checkbox(
        #         cb,
        #         image.get_annotation("practical", cb_value, False)
        #     )
        for cb, cb_value in zip(cbs, cb_values):
            val = image.get_annotation("practical", cb_value, None)
            self.set_checkbox(cb, val is True)
            
        # Scientific annotations
        # # Checkboxes
        # self.set_checkbox(self.aurora_present_checkbox,
        #         image.get_annotation("scientific", "aurora_present", False)
        #     )

        # Radio buttons
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

        # Multiselect
        # Auroral Colours
        colours = image.get_annotation(
            "scientific",
            "aurora_colours",
            default=set()
        )
        self.set_multiselect(self.aurora_colours, colours)
        
        # Auroral shapes
        shapes = image.get_annotation(
            "scientific",
            "aurora_shapes",
            default=set()
        )
        self.set_multiselect(self.aurora_shapes, shapes)        
        
        # Artifacts
        arfs = image.get_annotation(
            "scientific",
            "artifacts",
            default=set()
        )
        self.set_multiselect(self.artifacts, arfs)        

    # UPDATE IMAGE METADATA IF IMAGE CHANGED ----------------------------
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

    # UPDATE USER INPUT DATA IF IMAGE CHANGED ---------------------------
    def update_userinput(self):
        image = self.images[self.index]

        text = (
            f"Date: {image.capture_date} | Time: {image.capture_time}\n"
            f"Storm: {image.storm_name} | Time provided?: {image.time_provided}\n"
            f"Setting: {image.setting} | Edited: {image.edited}\n"
            f"User comment: {image.user_comment}\n"
        )
    
        self.user_metadata_label.setText(text)

    # UPDATE IMAGE TITLE IF IMAGE CHANGED -------------------------------
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

    # -------------------------------------------------------
    #
    # -------------------------------------------------------
    # MOVE BETWEEN IMAGES
    #    
    def next_image(self):
        """
        Move to next image

        Returns
        -------
        None.

        """
        if not self.can_leave_image():
            self.show_incomplete_warning()
            return
    
        self.write_current_image_to_csv(self.images[self.index])
    
        if self.index < (self.n_images - 1):
            self.index += 1
            self.image_label.set_image(self.images[self.index].filepath)
            self.image_change_updates()

    def previous_image(self):
        """
        Move to previous image

        Returns
        -------
        None.

        """
        if not self.can_leave_image():
            self.show_incomplete_warning()
            return
    
        self.write_current_image_to_csv(self.images[self.index])
    
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
        can_move = self.can_leave_image()
    
        self.previous_button.setEnabled(self.index > 0 and can_move)
        self.next_button.setEnabled(self.index < (self.n_images - 1) and can_move)


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
        self.images[self.index].set_reviewer(self.user_initials)

    def can_leave_image(self, REQUIRED_ANNOTATIONS = {"scientific": [
            "aurora_brightness", "cloud_cover", ]}):
        image = self.images[self.index]
    
        for section, keys in REQUIRED_ANNOTATIONS.items():
            for key in keys:
                value = image.get_annotation(section, key, default=None)
    
                # Checkboxes → must not be None
                if value is None:
                    return False
    
                # Radio groups → must not be None
                if isinstance(value, str) and value.strip() == "":
                    return False
    
        return True

    def show_incomplete_warning(self):
        QMessageBox.warning(
            self,
            "Incomplete annotations",
            "Please answer all questions* before leaving this image."
        )
    # -------------------------------------------------------


    
    def write_current_image_to_csv(self, image):
        # image = self.images[self.index]
        row = image.to_flat_dict()
    
        output_csv = os.path.join(output_data_dir,
                                  "annotations_" + self.user_initials + ".csv")
    
        file_exists = os.path.exists(output_csv)
    
        with open(output_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
    
            if not file_exists:
                writer.writeheader()
    
            writer.writerow(row)



class LoginDialog(QDialog):

    def __init__(self, allowed_users):
        super().__init__()
        self.allowed_users = allowed_users
        self.user_initials = None
        self.user_name = None

        self.setWindowTitle("User login")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Enter your initials (all caps, inc. middle):"))

        self.input = QLineEdit()
        self.input.setMaxLength(5)
        layout.addWidget(self.input)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        btn = QPushButton("Login")
        btn.clicked.connect(self.try_login)
        layout.addWidget(btn)

    def try_login(self):
        initials = self.input.text().strip().upper()

        if initials not in self.allowed_users:
            self.error_label.setText("Unknown initials")
            return

        self.user_initials = initials
        self.user_name = self.allowed_users[initials]
        self.accept()


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

    login = LoginDialog(ALLOWED_USERS)
    if login.exec() != QDialog.Accepted:
        sys.exit()

    viewer = ImageViewer(images, user_initials=login.user_initials,
        user_name=login.user_name)
    viewer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
