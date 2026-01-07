# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:01:55 2026

@author: A R Fogg
"""

import os
import sys
import pathlib
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
    QVBoxLayout, QWidget)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


from auroral_image_class import Auroral_Image

# image_path = os.path.join(
#     "C:"+os.sep, r"Users\Alexandra\Documents\wind_waves_akr_code\aurora_eire",
#     "aurora_eire_logo.png")
# image_path = "aurora_eire_logo.png"
image_dir = os.path.join(
    "C:"+os.sep, r"\Users\Alexandra\Documents\data\aurora_eire\test_images")


class ImageWindow(QLabel):

    def __init__(self, image_path=None):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.pixmap_original = None

        if image_path is not None:
            self.set_image(image_path)

    def set_image(self, image_path):
        """Load a new image and display it."""
        self.pixmap_original = QPixmap(image_path)
        self._update_pixmap()

    def resizeEvent(self, event):
        self._update_pixmap()
        super().resizeEvent(event)

    def _update_pixmap(self):
        if self.pixmap_original and not self.pixmap_original.isNull():
            scaled = self.pixmap_original.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)


# class ImageWindow(QLabel):
#     # A generic window-like container

#     def __init__(self, image_path):
#         super().__init__()

#         # Align image within window
#         self.setAlignment(Qt.AlignCenter)
#         # Store the image once
#         self.pixmap_original = QPixmap(image_path)

#     # Called whenever the window size changes
#     def resizeEvent(self, event):
#         if not self.pixmap_original.isNull():
#             scaled = self.pixmap_original.scaled(
#                 self.size(),
#                 Qt.KeepAspectRatio,
#                 Qt.SmoothTransformation
#             )
#             self.setPixmap(scaled)

#         super().resizeEvent(event)


class ImageViewer(QWidget):
    # This is the main window
    # it contains other widgets
    # manages the "application state" i.e. which image we're on
    # responds to user actions (buttons)
    def __init__(self, image_paths):

        # Initialise the Qt machinery
        super().__init__()

        # Store the image paths into the class
        self.image_paths = image_paths

        # Initialise tracker for which image we are on
        self.index = 0

        # Start up the ImageWindow, pass it the path for image 0
        self.image_label = ImageWindow(self.image_paths[self.index])

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

        # Stack the widget vertically with image on top, button underneath
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.next_button)
        layout.addWidget(self.previous_button)

        # Apply the layout
        self.setLayout(layout)

        # Window title
        self.setWindowTitle("Resizable Image Viewer")
        # Initial window size
        self.resize(600, 600)

        self.update_buttons()

    # def next_image(self):
    #     # Function that steps through to next image
    #     # Add 1 to the image and wrap around at the end
    #     self.index = (self.index + 1) % len(self.image_paths)
    #     # Load the new image
    #     self.image_label.set_image(self.image_paths[self.index])
    #     # self.image_label.pixmap_original = QPixmap(
    #     #     self.image_paths[self.index]
    #     # )
    #     # # Bodge to force a redraw - needs cleaning up later
    #     # self.image_label.resizeEvent(None)
    def next_image(self):
        if self.index < len(self.image_paths) - 1:
            self.index += 1
            self.image_label.set_image(self.image_paths[self.index])
            self.update_buttons()


    # def previous_image(self):
    #     # Function that steps through to previous image
    #     # Add 1 to the image and wrap around at the end
    #     self.index = (self.index - 1) 
    #     # Load the new image
    #     self.image_label.set_image(self.image_paths[self.index])
    def previous_image(self):
        if self.index > 0:
            self.index -= 1
            self.image_label.set_image(self.image_paths[self.index])
            self.update_buttons()
        
    def update_buttons(self):
        self.previous_button.setEnabled(self.index > 0)
        self.next_button.setEnabled(self.index < len(self.image_paths) - 1)

def list_images():

    # NEEDS TO BE MORE GENERAL FOR ALL FILETYPES
    # Automatically list PNG and JPEG images in the directory
    image_paths = sorted([
        str(p) for p in pathlib.Path(image_dir).glob("*")
        if p.suffix.lower() in [".png", ".jpg", ".jpeg"]
    ])

    if not image_paths:
        raise ValueError(f"No images found in {image_dir}")

    return image_paths


def main():

    image_paths = list_images()

    app = QApplication(sys.argv)

    # label = ImageWindow(image_paths[0])

    # label.setWindowTitle("Resizable Image Viewer")
    # label.resize(600, 600)
    # label.show()

    # sys.exit(app.exec())


    viewer = ImageViewer(image_paths)
    viewer.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
