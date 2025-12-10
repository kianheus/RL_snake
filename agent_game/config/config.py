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

        ### Profile selection row

        # Text description
        self.lbl_profile = QtW.QLabel("Profile:")

        # Combobox
        self.cmb_profile = QtW.QComboBox()
        self.cmb_profile.addItems(self.config_data["profiles"])
        self.cmb_profile.setCurrentText(self.config_data["active_profile"])
        self.cmb_profile.currentTextChanged.connect(self.profile_type_changed)

        # Add items to profile selection layout
        self.lyt_profile_select = QtW.QHBoxLayout()
        self.lyt_profile_select.addWidget(self.lbl_profile)
        self.lyt_profile_select.addWidget(self.cmb_profile)


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


        ### Save/recover buttons row

        # Define recover button
        self.btn_recover = QtW.QPushButton("Reset profile")
        self.btn_recover.setFixedWidth(130)
        self.btn_recover.clicked.connect(self.reset_settings)

        # Define save button
        self.btn_save = QtW.QPushButton("Save")
        self.btn_save.setFixedWidth(80)
        self.btn_save.clicked.connect(self.save_settings)

        # Add items to save/recover layout
        self.lyt_save = QtW.QHBoxLayout()
        self.lyt_save.addWidget(self.btn_recover)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_save)



        ### Add all items to main tab
        self.lyt_main.addLayout(self.lyt_profile_select)
        self.lyt_main.addLayout(self.lyt_agent)
        self.lyt_main.addStretch()
        self.lyt_main.addLayout(self.lyt_save)

        ### Tab main formatting and spacing
        self.lyt_main.setContentsMargins(20, 20, 20, 20)
        self.lyt_main.setSpacing(0)

        ### Get QWidget from lyt_main
        self.tab_main = QtW.QWidget()
        self.tab_main.setLayout(self.lyt_main)


        """     Tab Advanced     """
        placeholder2 = QtW.QWidget()



        tabs.addTab(self.tab_main, "Main")
        tabs.addTab(placeholder2, "Advanced")

        self.setCentralWidget(tabs)

    def profile_type_changed(self, type_string):
        self.config_data["active_profile"] = type_string
        

    def agent_type_changed(self, type_string):
        self.config_data["agent_type"] = type_string
        print(self.config_data["agent_type"])

    def reset_settings(self):
        with open("agent_game/config/config_recovery.json") as json_file:
            self.config_data = json.load(json_file)
            self.refresh_all()

    def refresh_all(self):
        self.cmb_agent_type.setCurrentText(self.config_data["agent_type"])
        self.cmb_profile.setCurrentText(self.config_data["active_profile"])

    def save_settings(self):
        with open("agent_game/config/config_base.json", "w") as json_file:
            json.dump(self.config_data, json_file, indent=4)

with open("agent_game/config/config_base.json") as json_file:
    config_data = json.load(json_file)


app = QtW.QApplication([])

window = MainWindow(config_data)
window.show()


app.exec()
