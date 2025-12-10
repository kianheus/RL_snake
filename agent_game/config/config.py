import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import json


class MainWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()

        """     General window settings     """

        window_x = 150
        window_y = 150

        window_width = 500
        window_height = 500

        self.setWindowTitle("RL Snake settings")
        self.setFixedSize(QtC.QSize(window_width, window_height))

        """     Tabs     """
        tabs = QtW.QTabWidget()
        tabs.setTabPosition(QtW.QTabWidget.TabPosition.North)
        tabs.setMovable(True)



        """     Tab Main     """
        placeholder1 = QtW.QWidget()


        """     Tab Advanced     """
        placeholder2 = QtW.QWidget()



        tabs.addTab(placeholder1, "Main")
        tabs.addTab(placeholder2, "Advanced")

        self.setCentralWidget(tabs)


app = QtW.QApplication([])

window = MainWindow()
window.show()


app.exec()
