import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        layout = QHBoxLayout(self)
        self.label3 = QLabel(self)
        self.title = QLabel("Wild Lion's Browser")
        self.pixmap = QPixmap('media/icons/flags/ADF.png')
        self.label3.setPixmap(self.pixmap)
        self.label3.setAlignment(Qt.AlignCenter)
        self.title.setMinimumHeight(self.pixmap.height())
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label3)
        layout.addWidget(self.title)
        # self.label3.setStyleSheet("""
        #     background-color: black;
        # """)
        self.title.setStyleSheet("""
            color: black;
            padding: 0px 10px 0px 10px;
        """)
        layout.setSpacing(0)
        layout.addStretch()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.setGeometry(600, 100, 200, 30)
    window.show()
    sys.exit(app.exec_())