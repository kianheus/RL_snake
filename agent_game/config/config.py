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


        ### Profile creation row

        # Input row
        self.inp_new_profile = QtW.QLineEdit()
        self.inp_new_profile.setPlaceholderText("New profile name")

        # Record row height for future formatting
        self.profile_row_height = self.inp_new_profile.sizeHint().height()

        # Button
        self.btn_create_profile = QtW.QPushButton("Create")
        self.btn_create_profile.setFixedWidth(90)
        self.btn_create_profile.clicked.connect(self.create_profile)  

        # Add items to profile creation layout
        self.lyt_profile_create = QtW.QHBoxLayout()
        self.lyt_profile_create.addWidget(self.inp_new_profile)
        self.lyt_profile_create.addWidget(self.btn_create_profile)

        # Combine profile layouts
        self.lyt_profile = QtW.QVBoxLayout()
        self.lyt_profile.addLayout(self.lyt_profile_select)
        self.lyt_profile.addLayout(self.lyt_profile_create)




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


        line_height = self.fontMetrics().height()

        self.lyt_main.addLayout(self.lyt_profile)
        self.spacer1 = QtW.QWidget()
        self.spacer1.setFixedHeight(self.profile_row_height)
        self.lyt_main.addWidget(self.spacer1)
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


        ### Call any methods required at startup
        self.hide_add_profile()

        self.setCentralWidget(tabs)

    def profile_type_changed(self, type_string):
        if type_string == "Add new":
            self.show_add_profile()
        else:
            self.config_data["active_profile"] = type_string
            self.hide_add_profile()

    def show_add_profile(self):
        self.inp_new_profile.show()
        self.btn_create_profile.show()
        self.spacer1.hide()

    def hide_add_profile(self):
        self.inp_new_profile.hide()
        self.btn_create_profile.hide()
        self.spacer1.show()        

    def agent_type_changed(self, type_string):
        self.config_data["agent_type"] = type_string
        print(self.config_data["agent_type"])

    def reset_settings(self):
        with open("agent_game/config/config_recovery.json") as json_file:
            self.config_data = json.load(json_file)
            self.refresh_all()

    def refresh_all(self):
        self.cmb_agent_type.setCurrentText(self.config_data["agent_type"])
        self.cmb_profile.clear()
        self.cmb_profile.addItems(self.config_data["profiles"])
        self.cmb_profile.setCurrentText(self.config_data["active_profile"])

    def save_settings(self):
        with open("agent_game/config/config_base.json", "w") as json_file:
            json.dump(self.config_data, json_file, indent=4)

    def create_profile(self):
        name = self.inp_new_profile.text().strip()
        
        # Check if any new profile name was entered
        if not name:
            return
        
        # Avoid adding duplicate profiles
        if name in self.config_data["profiles"]:
            QtW.QMessageBox.warning(self, "Profile exists",
                                    f"A profile named '{name}' already exists.")
            return
        
        # Add to data model
        # TODO: Add the new profile above the "Add new" option
        self.config_data["profiles"].append(name)
        self.config_data["active_profile"] = name

        # Add to UI
        self.cmb_profile.addItem(name)
        self.cmb_profile.setCurrentText(name) # TODO: Consider whether this should be in the refresh_all() function

        # Clear input box
        self.inp_new_profile.clear()

with open("agent_game/config/config_base.json") as json_file:
    config_data = json.load(json_file)


app = QtW.QApplication([])

window = MainWindow(config_data)
window.show()


app.exec()
