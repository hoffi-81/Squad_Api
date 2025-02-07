import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QPixmap
from Battlemetrics_api import factions_short
from Squadutils_api import asset_names
import pyperclip
import os



def find_image_path(filename, base_folder="media"):
    '''
    Getting the top folder where the icon is located
    '''
    for root, dirs, files in os.walk(base_folder):  # Walk through all subfolders
        if filename in files:
            return os.path.join(root, filename)




class UnitAssetsViewer(QMainWindow):
     def __init__(self):
          super().__init__()
          self.setWindowIcon(QIcon("media/clipboard.png"))

          # Sample data from your variables
          data_1st_row = {
               "faction": factions_short[0],  
               "assets": asset_names[0]
          }
          data_2nd_row = {
               "faction": factions_short[1],
               "assets": asset_names[1]
          }
          
          self.setWindowTitle("Squad assets to Clipboard")
          self.setGeometry(100, 100, 600, 400)

          # Main widget
          main_widget = QWidget()
          self.setCentralWidget(main_widget)

          # Scroll area
          scroll_area = QScrollArea()
          scroll_area.setWidgetResizable(True)
          scroll_area.setStyleSheet("background-color: #2e3440; border: 10px;")

          # Table container
          table_container = QWidget()
          table_layout = QHBoxLayout(table_container)  # Use QHBoxLayout for columns
          table_layout.setContentsMargins(0, 0, 0, 0)
          table_layout.setSpacing(20)
          # Create a vertical layout for each faction's column
          column_1_layout = QVBoxLayout()
          column_2_layout = QVBoxLayout()

          # Add headers for each column
          # === Header 1 ===
          header_1 = QLabel(data_1st_row["faction"])
          header_1_icon_lb = QLabel()
          header_1_icon = QPixmap(find_image_path(data_1st_row["faction"]+ ".png"))
          header_1_icon = header_1_icon.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
          header_1_icon_lb.setPixmap(header_1_icon)
          header_1.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 14px; padding: 30;")
          column_1_layout.addWidget(header_1_icon_lb)
          column_1_layout.addWidget(header_1)

          # == Header 2 ===
          header_2 = QLabel(data_2nd_row["faction"])
          header_2_icon_lb = QLabel()
          header_2_icon = QPixmap(find_image_path(data_2nd_row["faction"]+ ".png"))
          header_2_icon = header_2_icon.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
          header_2_icon_lb.setPixmap(header_2_icon)
          header_2.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 14px; padding: 30;")
          column_2_layout.addWidget(header_2_icon_lb)
          column_2_layout.addWidget(header_2)

          # Populate the first column with assets from faction 1
          for vehicle, icon in zip(data_1st_row["assets"][0], data_1st_row["assets"][1]):
               asset_button_1 = QPushButton(vehicle)
               asset_button_1.setIcon(QIcon(find_image_path("{}.png".format(icon))))
               asset_button_1.setIconSize(QSize(25, 25))
               asset_button_1.setStyleSheet(
                    """
                    QPushButton {
                    background-color: #4c566a;
                    color: #d8dee9;
                    font-size: 12px;
                    border: 1px solid #434c5e;
                    padding: 2px 6px;  /* Adjust padding for smaller buttons */
                    border-radius: 3px;
                    min-height: 20px;  /* Reduce height */
                    }
                    QPushButton:hover {
                    background-color: #5e81ac;
                    }
                    """
               )
               asset_button_1.clicked.connect(lambda checked, name=vehicle: self.on_asset_clicked(name))
               column_1_layout.addWidget(asset_button_1)

          # Populate the second column with assets from faction 2
          for vehicle, icon in zip(data_2nd_row["assets"][0], data_2nd_row["assets"][1]):
               asset_button_2 = QPushButton(vehicle)
               asset_button_2.setIcon(QIcon(find_image_path("{}.png".format(icon))))
               asset_button_2.setIconSize(QSize(25, 25))
               asset_button_2.setStyleSheet(
                    """
                    QPushButton {
                    background-color: #4c566a;
                    color: #d8dee9;
                    font-size: 12px;
                    border: 1px solid #434c5e;
                    padding: 2px 6px;  /* Adjust padding for smaller buttons */
                    border-radius: 3px;
                    min-height: 20px;  /* Reduce height */
                    }
                    QPushButton:hover {
                    background-color: #5e81ac;
                    }
                    """
               )
               asset_button_2.clicked.connect(lambda checked, name=vehicle: self.on_asset_clicked(name))
               column_2_layout.addWidget(asset_button_2)

          # Add the columns to the table layout
          table_layout.addLayout(column_1_layout)
          table_layout.addLayout(column_2_layout)

          # Set the table container in the scroll area
          scroll_area.setWidget(table_container)

          # Set the layout for the main widget
          layout = QVBoxLayout(main_widget)
          layout.setContentsMargins(0, 0, 0, 0)
          layout.setSpacing(0)
          layout.addWidget(scroll_area)
          main_widget.setLayout(layout)





     def on_asset_clicked(self, name):
          '''
          Copies the button name that the user clicked and plays a sound
          '''
          # Copy to clipboard
          pyperclip.copy(name)
          sound_path = 'media/click.wav'
          if os.path.exists(sound_path):
               QSound.play(sound_path)



if __name__ == "__main__":
     app = QApplication(sys.argv)
     viewer = UnitAssetsViewer()
     viewer.show()
     sys.exit(app.exec_())
