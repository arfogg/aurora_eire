# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:01:55 2026

@author: A R Fogg
"""

import os
import sys
import pathlib
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy)
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

        # Initialise widget for displaying metadata
        self.metadata_label = QLabel()
        # Stop centering
        self.metadata_label.setAlignment(Qt.AlignTop)
        # Wraps long text around
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

        # Main horizontal layout
        main_layout = QHBoxLayout()
        
        # Left-hand side: image + title + buttons
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.image_label)
        left_layout.addWidget(self.image_title)
        left_layout.addWidget(self.previous_button)
        left_layout.addWidget(self.next_button)
        
        # Right-hand side: metadata
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Metadata"))  # header
        right_layout.addWidget(self.metadata_label)
        
        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)
        
        self.setLayout(main_layout)


        # # Stack the widget vertically with image on top, button underneath
        # layout = QVBoxLayout()
        # layout.addWidget(self.image_label)
        # layout.addWidget(self.image_title)
        # layout.addWidget(self.next_button)
        # layout.addWidget(self.previous_button)

        # # Apply the layout
        # self.setLayout(layout)

        # Window title
        self.setWindowTitle("Aurora Éire Image Viewer")
        # Initial window size
        self.resize(700, 700)

        # Update buttons, title, etc
        self.image_change_updates()

    def update_metadata(self):
        image = self.images[self.index]

        text = (
            f"Record ID: {image.record_id}\n"
            f"Filename: {image.filename}\n"
            f"Extension: {image.file_extension}\n"
            "\n(Metadata placeholder)"
        )
    
        self.metadata_label.setText(text)


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
        print(i)
        img = AuroralImage(filepath=str(path), image_n=i)
        img.attach_user_data(user_data_df)

        images.append(
            AuroralImage(filepath=str(path), image_n=i)
        )

    return images


def main():
    

    images = list_images()
    


    app = QApplication(sys.argv)

    viewer = ImageViewer(images)
    viewer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
