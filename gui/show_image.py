# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:01:55 2026

@author: A R Fogg
"""

import os
import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# image_path = os.path.join(
#     "C:"+os.sep, r"Users\Alexandra\Documents\wind_waves_akr_code\aurora_eire",
#     "aurora_eire_logo.png")
image_path = "aurora_eire_logo.png"

def main():
    app = QApplication(sys.argv)

    label = QLabel()
    label.setWindowTitle("Minimal Image Viewer")
    label.setAlignment(Qt.AlignCenter)

    pixmap = QPixmap(image_path)
    label.setPixmap(
        pixmap.scaled(
            label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
    )


    label.resize(600, 600)
    label.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
