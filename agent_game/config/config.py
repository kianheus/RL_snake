import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import json


class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()

        window_x = 150
        window_y = 150

        window_width = 500
        window_height = 500

        self.setWindowTitle("RL Snake settings")
        self.setFixedSize(QtC.QSize(window_width, window_height))



app = QtW.QApplication([])

window = MainWindow()
window.show()


app.exec()
