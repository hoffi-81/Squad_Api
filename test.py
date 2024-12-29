from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("My Custom Window")

        # Set the window icon
        self.setWindowIcon(QIcon("media/clipboard.png"))

        # Set window size
        self.resize(400, 300)

# Create the application
app = QApplication([])

# Create and show the window
window = MyWindow()
window.show()

# Run the application
app.exec_()
