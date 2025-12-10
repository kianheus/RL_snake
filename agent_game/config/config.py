import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import json


class MainWindow(QtW.QMainWindow):
    def __init__(self, config_data):
        super().__init__()

        self.config_data = config_data

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
        self.lyt_main = QtW.QVBoxLayout()


        ### Agent selection row

        # Text description
        self.lbl_agent = QtW.QLabel("Agent type:")

        # Combobox
        self.cmb_agent_type = QtW.QComboBox(tabs)
        self.cmb_agent_type.addItems(["Basic", "Ego", "Convolutional"])
        self.cmb_agent_type.setCurrentText(self.config_data["agent_type"])
        self.cmb_agent_type.currentTextChanged.connect(self.agent_type_changed)

        # Add items to agent layout
        self.lyt_agent = QtW.QHBoxLayout()
        self.lyt_agent.addWidget(self.lbl_agent)
        self.lyt_agent.addWidget(self.cmb_agent_type)




        ### Add all items to main tab
        self.lyt_main.addLayout(self.lyt_agent)
        self.lyt_main.addStretch()


        ### Get QWidget from lyt_main
        self.tab_main = QtW.QWidget()
        self.tab_main.setLayout(self.lyt_main)


        """     Tab Advanced     """
        placeholder2 = QtW.QWidget()



        tabs.addTab(self.tab_main, "Main")
        tabs.addTab(placeholder2, "Advanced")

        self.setCentralWidget(tabs)


    def agent_type_changed(self, type_string):
        self.config_data["agent_type"] = type_string
        print(self.config_data["agent_type"])


with open("agent_game/config/config_base.json") as json_file:
    config_data = json.load(json_file)


app = QtW.QApplication([])

window = MainWindow(config_data)
window.show()


app.exec()
