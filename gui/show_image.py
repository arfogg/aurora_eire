# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:01:55 2026

@author: A R Fogg
"""

import os
import sys
import pathlib
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# image_path = os.path.join(
#     "C:"+os.sep, r"Users\Alexandra\Documents\wind_waves_akr_code\aurora_eire",
#     "aurora_eire_logo.png")
# image_path = "aurora_eire_logo.png"
image_dir = os.path.join(
    "C:"+os.sep, r"\Users\Alexandra\Documents\data\aurora_eire\test_images")

class ImageLabel(QLabel):
    def __init__(self, image_path):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        # Store the image once
        self.pixmap_original = QPixmap(image_path)

    # Called whenever the window size changes
    def resizeEvent(self, event):
        if not self.pixmap_original.isNull():
            scaled = self.pixmap_original.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)

        super().resizeEvent(event)

def list_images():

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

    label = ImageLabel(image_paths[0])
    label.setWindowTitle("Resizable Image Viewer")
    label.resize(600, 600)
    label.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()


# def main():
#     app = QApplication(sys.argv)

#     label = QLabel()
#     label.setWindowTitle("Minimal Image Viewer")
#     label.setAlignment(Qt.AlignCenter)

#     pixmap = QPixmap(image_path)
#     label.setPixmap(
#         pixmap.scaled(
#             label.size(),
#             Qt.KeepAspectRatio,
#             Qt.SmoothTransformation
#         )
#     )

#     label.resize(600, 600)
#     label.show()

#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()
