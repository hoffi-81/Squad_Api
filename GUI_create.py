import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QScrollArea, QGridLayout, QPushButton, QLabel, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QPixmap
from Battlemetrics_api import factions_short, server_info, current_map_short, gamemode
from Squadutils_api import asset_names
from Get_cfg_data import read_config
import pyperclip
import os
import psutil
import pygetwindow as gw
import keyboard
import time



# ========== Todo ==========
# 1. Display Server Name
# 2. Display Current Map




def find_image_path(filename, base_folder="media") -> None:
     """
     Find the path of an image file in the specified base folder.

     Getting the top folder where the icon is located.
     """
     for root, dirs, files in os.walk(base_folder):  # Walk through all subfolders
          if filename in files:
               return os.path.join(root, filename)


class UnitAssetsViewer(QMainWindow):
     def __init__(self):
          super().__init__()
          self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
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

          self.setWindowTitle("Dynamic Hotkey for Squad Assets")
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
          table_layout = QGridLayout(table_container)
          table_layout.setContentsMargins(0, 0, 0, 0)
          table_layout.setSpacing(20)

          # Add headers for each column
          self.add_header(table_layout, data_1st_row["faction"], 0, 0)
          # self.add_header(table_layout, server_info, -1, 1)

          label1 = QLabel(server_info, self)
          label2 = QLabel("{} - {}".format(current_map_short, gamemode), self)
          label1.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 8px; padding-top: 5; padding-bottom: 10;")
          label2.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 9px; padding-top: 35; padding-bottom: 10; Background-color: rgb(0,0,0,0);")
          table_layout.addWidget(label1, 0, 0, 1, 2, alignment=Qt.AlignCenter)
          table_layout.addWidget(label2, 0, 0, 1, 2, alignment=Qt.AlignCenter)





          self.add_header(table_layout, data_2nd_row["faction"], 0, 1)

          # Populate the first column with assets from faction 1
          self.populate_column(table_layout, data_1st_row["assets"], 1, 0)

          # Populate the second column with assets from faction 2
          self.populate_column(table_layout, data_2nd_row["assets"], 1, 1)

          # Set the table container in the scroll area
          scroll_area.setWidget(table_container)

          # table_layout.setColumnStretch(0, 10)
          # table_layout.setColumnStretch(1, 1)
          # table_layout.setColumnStretch(2, 10)  



          # Set the layout for the main widget
          layout = QVBoxLayout(main_widget)
          layout.setContentsMargins(0, 0, 0, 0)
          layout.setSpacing(0)
          layout.addWidget(scroll_area)
          main_widget.setLayout(layout)

     def add_header(self, layout, faction, row, col):
          header = QLabel(faction)
          header_icon_lb = QLabel()
          header_icon = QPixmap(find_image_path(f"{faction}.png"))
          if header_icon:
               header_icon = header_icon.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
               header_icon_lb.setPixmap(header_icon)
               header_icon_lb.setStyleSheet("padding-top: 20px;")
          header.setStyleSheet("color: #eceff4; font-weight: bold; font-size: 14px; padding-top: 5; padding-bottom: 10;")
          layout.addWidget(header_icon_lb, row, col, alignment=Qt.AlignCenter)
          layout.addWidget(header, row + 1, col, alignment=Qt.AlignCenter)
     def populate_column(self, layout, assets, start_row, col):
          for i, (vehicle, icon) in enumerate(zip(assets[0], assets[1])):
               i += 1
               asset_button = QPushButton(vehicle)
               icon_path = find_image_path(f"{icon}.png")
               if icon_path:
                    asset_button.setIcon(QIcon(icon_path))
                    asset_button.setIconSize(QSize(25, 25))
               asset_button.setStyleSheet(
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
                    QPushButton:hover:pressed
                    {
                    border: 3px solid #4c566a;
                    }
                    """
               )
               asset_button.clicked.connect(lambda checked, name=vehicle: self.on_asset_clicked(name))
               layout.addWidget(asset_button, start_row + i, col)

     def on_asset_clicked(self, name):
          '''
          Copies the button name that the user clicked, plays a sound, 
          and pastes it into Notepad if Notepad is open.
          '''
          # Copy to clipboard
          pyperclip.copy('CreateSquad "{}" 1'.format(name))

          # Check if Notepad is running
          notepad_running = False
          for process in psutil.process_iter(attrs=['pid', 'name']):
               if "notepad++.exe" in process.info['name'].lower(): #notepad++.exe
                    notepad_running = True
                    break

          if notepad_running:
               try:
                    # Find the Notepad window
                    notepad_window = None
                    for window in gw.getWindowsWithTitle("Notepad"):
                         if "Notepad" in window.title:
                              notepad_window = window
                              break

                    if notepad_window:
                         # Bring Notepad to the foreground
                         notepad_window.activate()
                         time.sleep(0)  # Wait a bit for the window to activate
                       #  if not read_config()["debug_mode"]:
                         # keyboard.press_and_release(read_config()["button_cmd_line"])
                         keyboard.send("l")
                         keyboard.press_and_release("ctrl+v")
                         keyboard.press_and_release("enter")


               except Exception as e:
                    print(f"Error switching to Notepad: {e}")


if __name__ == "__main__":
     app = QApplication(sys.argv)
     viewer = UnitAssetsViewer()
     viewer.show()
     sys.exit(app.exec_())
