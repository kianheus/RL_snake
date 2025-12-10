import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import PyQt6.QtGui as QtG
import json

import os


def create_config_filepath(config_dir, profile_name: str) -> str:
    filepath = config_dir + "/config_" + profile_name + ".json"
    return filepath
    

class MainWindow(QtW.QMainWindow):
    def __init__(self, config_dir):
        super().__init__()

        self.config_dir = config_dir
        cookies_filepath = config_dir + "/cookies.json"

        with open(cookies_filepath) as json_file:
                    cookies = json.load(json_file)

        self.active_profile = cookies["last_active"]
        self.agent_types = cookies["agent_type_options"]

        profile_filepath = create_config_filepath(config_dir, self.active_profile)

        with open(profile_filepath) as json_file:
            self.config_data = json.load(json_file)

        self.update_profiles_from_dir()
        

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
        self.cmb_profile.addItems(self.profiles)
        self.cmb_profile.setCurrentText(self.active_profile)
        self.cmb_profile.currentTextChanged.connect(self.profile_type_changed)

        # Add items to profile selection layout
        self.lyt_profile_select = QtW.QHBoxLayout()
        self.lyt_profile_select.addWidget(self.lbl_profile)
        self.lyt_profile_select.addWidget(self.cmb_profile)


        ### Profile creation row

        # Input row
        self.inp_new_profile = QtW.QLineEdit()
        self.inp_new_profile.setPlaceholderText("New profile name")

        # Ensure that only valid expressions can be profile names
        validator = QtG.QRegularExpressionValidator(
            QtC.QRegularExpression("[A-Za-z0-9_-]+")
        )
        self.inp_new_profile.setValidator(validator)

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
        self.cmb_agent_type.addItems(self.agent_types)
        self.cmb_agent_type.setCurrentText(self.config_data["agent_type"])
        self.cmb_agent_type.currentTextChanged.connect(self.agent_type_changed)

        # Add items to agent layout
        self.lyt_agent = QtW.QHBoxLayout()
        self.lyt_agent.addWidget(self.lbl_agent)
        self.lyt_agent.addWidget(self.cmb_agent_type)


        ### NN layers selection box

        # Text description
        self.lbl_nn_layers = QtW.QLabel("NN hidden layers:")

        # New layer button
        self.btn_add_nn_layer = QtW.QPushButton("Add layer")
        self.btn_add_nn_layer.setFixedWidth(100)
        self.btn_add_nn_layer.clicked.connect(self.create_nn_layer)  

        # Small spacer
        self.nn_w_spacer = QtW.QWidget()
        self.nn_w_spacer.setFixedWidth(10)

        # Remove layer button
        self.btn_remove_nn_layer = QtW.QPushButton("Remove layer")
        self.btn_remove_nn_layer.setFixedWidth(100)
        self.btn_remove_nn_layer.clicked.connect(self.remove_nn_layer)  
        self.btn_remove_nn_layer.setEnabled(False)


        self.lyt_nn_description = QtW.QHBoxLayout()
        self.lyt_nn_description.addWidget(self.lbl_nn_layers)
        self.lyt_nn_description.addWidget(self.btn_add_nn_layer)
        self.lyt_nn_description.addWidget(self.nn_w_spacer)
        self.lyt_nn_description.addWidget(self.btn_remove_nn_layer)


        # List of nn layers
        self.inp_nn_layers = []

        # Create small whitespace
        self.nn_h_spacer = QtW.QWidget()
        self.nn_h_spacer.setFixedHeight(10)


        # Prepare nn layers QHBox
        self.lyt_nn_layers = QtW.QHBoxLayout()
        self.create_nn_layer()

        # Add items to NN layers layout
        self.lyt_nn_box = QtW.QVBoxLayout()
        self.lyt_nn_box.addLayout(self.lyt_nn_description)
        self.lyt_nn_box.addWidget(self.nn_h_spacer)
        self.lyt_nn_box.addLayout(self.lyt_nn_layers)


        ### Save/delete/recover buttons row

        # Define recover button
        self.btn_recover = QtW.QPushButton("Reset profile")
        self.btn_recover.setFixedWidth(130)
        self.btn_recover.clicked.connect(self.reset_profile)

        # Define delete button
        self.btn_delete_profile = QtW.QPushButton("Delete profile")
        self.btn_delete_profile.setFixedWidth(130)
        self.btn_delete_profile.clicked.connect(self.delete_profile)

        # Define save button
        self.btn_save = QtW.QPushButton("Save")
        self.btn_save.setFixedWidth(80)
        self.btn_save.clicked.connect(self.save_settings)

        # Add items to save/recover layout
        self.lyt_save = QtW.QHBoxLayout()
        self.lyt_save.addWidget(self.btn_recover)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_delete_profile)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_save)



        ### Add all items to main tab


        line_height = self.fontMetrics().height()

        self.lyt_main.addLayout(self.lyt_profile)
        self.spacer1 = QtW.QWidget()
        self.spacer1.setFixedHeight(self.profile_row_height)
        self.lyt_main.addWidget(self.spacer1)
        self.lyt_main.addLayout(self.lyt_agent)
        self.spacer2 = QtW.QWidget()
        self.spacer2.setFixedHeight(self.profile_row_height)
        self.lyt_main.addWidget(self.spacer2)
        self.lyt_main.addLayout(self.lyt_nn_box)
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
            self.active_profile = type_string
            profile_filepath = create_config_filepath(self.config_dir, self.active_profile)
            with open(profile_filepath) as json_file:
                self.config_data = json.load(json_file)      
            self.refresh_all()      
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

    def reset_profile(self):
        with open("agent_game/config/config_recovery.json") as json_file:
            self.config_data = json.load(json_file)
            self.refresh_all()

    def delete_profile(self):
        if self.active_profile == "basic_01" or self.active_profile == "ego_01":
            QtW.QMessageBox.warning(self, "Invalid remove", "Cannot remove core profiles.")
            return
        

        self.profiles.remove(self.active_profile)
        file_path = create_config_filepath(self.config_dir, self.active_profile)
        os.remove(file_path)
        self.active_profile = self.profiles[0]
        self.refresh_all()

        

    def refresh_all(self):
        self.update_profiles_from_dir()
        self.alphabetize_profile_options()

        self.cmb_agent_type.blockSignals(True)
        self.cmb_agent_type.setCurrentText(self.config_data["agent_type"])
        self.cmb_agent_type.blockSignals(False)

        self.cmb_profile.blockSignals(True)
        self.cmb_profile.clear()
        self.cmb_profile.addItems(self.profiles)
        self.cmb_profile.setCurrentText(self.active_profile)
        self.cmb_profile.blockSignals(False)

    def save_settings(self):
        file_string = "agent_game/config/config_" + self.active_profile + ".json"
        if not os.path.exists(file_string):
            print("Profile does not exist, creating new profile:", self.active_profile)
        else:
            print("Saving onto existing profile:", self.active_profile)

        with open(file_string, "w") as json_file:
            json.dump(self.config_data, json_file, indent=4)

    def create_profile(self):
        name = self.inp_new_profile.text().strip()
        
        # Check if any new profile name was entered
        if not name:
            return
        
        # Avoid adding duplicate profiles
        if name in self.profiles:
            QtW.QMessageBox.warning(self, "Profile exists",
                                    f"A profile named '{name}' already exists.")
            return
        
        # Add to data model
        # TODO: Add the new profile above the "Add new" option
        self.profiles.append(name)

        self.active_profile = name
        self.save_settings()

        self.alphabetize_profile_options()

        self.cmb_profile.blockSignals(True)
        self.cmb_profile.clear()
        self.cmb_profile.addItems(self.profiles)
        self.cmb_profile.setCurrentText(name) # TODO: Consider whether this should be in the refresh_all() function
        self.cmb_profile.blockSignals(False)

        #self.refresh_all()

        # Add to UI
        #self.refresh_all()


        # Clear input box
        self.inp_new_profile.clear()

    def update_profiles_from_dir(self):
        prefix = "config_"
        suffix = ".json"

        self.profiles = [
            f.removeprefix(prefix).removesuffix(suffix) for f in os.listdir(self.config_dir)
            if f.startswith(prefix) and f.endswith(suffix)
        ]

        self.profiles.remove("recovery")
        self.profiles.append("Add new")
        
    
    def alphabetize_profile_options(self): 
        self.profiles.remove("Add new")
        self.profiles = sorted(self.profiles)
        self.profiles.append("Add new")



config_dir = "agent_game/config"


app = QtW.QApplication([])

window = MainWindow(config_dir=config_dir)
window.show()

app.exec()
