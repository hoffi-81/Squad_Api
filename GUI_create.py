import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from Battlemetrics_api import factions_short
from Squadutils_api import asset_names
import pyperclip


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
          table_layout = QVBoxLayout(table_container)
          table_layout.setContentsMargins(0, 0, 0, 0)
          table_layout.setSpacing(20)

          # Add the table headers (two headers for the two columns)
          header_layout = QHBoxLayout()
          header_layout.setContentsMargins(0, 0, 0, 0)
          header_layout.setSpacing(1)

          header_name_1 = QLabel(data_1st_row["faction"])
          header_name_2 = QLabel(data_2nd_row["faction"])
          header_name_1.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 14px; padding: 30;")
          header_name_2.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 14px; padding: 30;")
          header_layout.addWidget(header_name_1)
          header_layout.addWidget(header_name_2)
          table_layout.addLayout(header_layout)

          # Determine the number of rows based on the maximum number of assets
          max_rows = max(len(data_1st_row["assets"]), len(data_2nd_row["assets"]))

          # Populate table rows with data for both factions
          for i in range(max_rows):
               row_layout = QHBoxLayout()
               row_layout.setContentsMargins(10, 10, 10, 0)  # Remove margins for rows
               row_layout.setSpacing(30)  # Adjust spacing between columns

               # First column: Asset from faction 1
               if i < len(data_1st_row["assets"]):
                    asset_button_1 = QPushButton(data_1st_row["assets"][i])
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
                    asset_button_1.clicked.connect(lambda checked, name=data_1st_row["assets"][i]: self.on_asset_clicked(name))
                    row_layout.addWidget(asset_button_1)
               else:
                    row_layout.addWidget(QWidget())  # Empty space for missing data

               # Second column: Asset from faction 2
               if i < len(data_2nd_row["assets"]):
                    asset_button_2 = QPushButton(data_2nd_row["assets"][i])
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
                    asset_button_2.clicked.connect(lambda checked, name=data_2nd_row["assets"][i]: self.on_asset_clicked(name))
                    row_layout.addWidget(asset_button_2)
               else:
                    row_layout.addWidget(QWidget())  # Empty space for missing data

               # Add the row layout to the table
               table_layout.addLayout(row_layout)

          # Set the table container in the scroll area
          scroll_area.setWidget(table_container)

          # Set the layout for the main widget
          layout = QVBoxLayout(main_widget)
          layout.setContentsMargins(0, 0, 0, 0)  # Remove outer margins for the main layout
          layout.setSpacing(0)  # Remove extra spacing between the scroll area and window edges
          layout.addWidget(scroll_area)
          main_widget.setLayout(layout)

     def on_asset_clicked(self, name):
          '''
          Copies the button name that the user clicked and plays a sound
          '''
          # Copy to clipboard
          QSound.play('media/click.wav')
          pyperclip.copy(name)

          # Play sound when clicked (you can replace with your own sound file)
          
if __name__ == "__main__":
     app = QApplication(sys.argv)
     viewer = UnitAssetsViewer()
     viewer.show()
     sys.exit(app.exec_())
