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

class ProfileManager():
    def __init__(self, config_dir):
        self.config_dir = config_dir
        cookies_filepath = config_dir + "/cookies.json"

        with open(cookies_filepath) as json_file:
                    cookies = json.load(json_file)

        self.active_profile = cookies["last_active"]
        self.agent_types = cookies["agent_type_options"]
        self.cookies = self.load_cookies()
        self.active_profile = self.cookies["last_active"]
        self.agent_types = self.cookies["agent_type_options"]
        self.config_data = self.load_from_profile(self.active_profile)
        self.profiles = self.get_profiles_from_dir()

        profile_filepath = create_config_filepath(config_dir, self.active_profile)
    def load_cookies(self):
        cookies_filepath = config_dir + "/cookies.json"
        with open(cookies_filepath) as f:
                    cookies = json.load(f)
        return cookies
    
    def load_from_profile(self, profile_name):
        profile_filepath = create_config_filepath(config_dir, profile_name)

        with open(profile_filepath) as json_file:
            self.config_data = json.load(json_file)
        with open(profile_filepath) as f:
            config_data = json.load(f)
        return config_data
    
    def save_profile(self, profile_name, data):
        filepath = create_config_filepath(self.config_dir, profile_name)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

        self.update_profiles_from_dir()
        
    def set_active_profile(self, profile_name):
        self.active_profile = profile_name
        self.config_data = self.load_from_profile(profile_name)

        """     General window settings     """
    
    def get_profiles_from_dir(self) -> list[str]:
        prefix = "config_"
        suffix = ".json"

        window_x = 150
        window_y = 150
        profiles = [
            f.removeprefix(prefix).removesuffix(suffix) for f in os.listdir(self.config_dir)
            if f.startswith(prefix) and f.endswith(suffix)
        ]

        window_width = 500
        window_height = 500
        profiles.remove("recovery")
        profiles = sorted(profiles)
        profiles.append("Add new")

        self.setWindowTitle("RL Snake settings")
        self.setFixedSize(QtC.QSize(window_width, window_height))
        return profiles

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
        self.awaiting_delete_confirmation = False

        # Define save button
        self.btn_save = QtW.QPushButton("Save")
        self.btn_save.setFixedWidth(130)
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
        self.load_nn_inputs()

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
            self.load_nn_inputs()

    def show_add_profile(self):
        self.inp_new_profile.show()
        self.btn_create_profile.show()
        self.spacer1.hide()
        self.disable_below_profile()

    def hide_add_profile(self):
        self.inp_new_profile.hide()
        self.btn_create_profile.hide()
        self.spacer1.show()
        self.enable_below_profile()    

    def agent_type_changed(self, type_string):
        self.config_data["agent_type"] = type_string

    def reset_profile(self):
        with open("agent_game/config/config_recovery.json") as json_file:
            self.config_data = json.load(json_file)

        self.inp_nn_layers = []
        self.load_nn_inputs()
        self.refresh_all()

    def delete_profile(self):

        if self.active_profile == "basic_01" or self.active_profile == "ego_01":
            self.show_warning_message(title="Invalid remove", message="Cannot remove core profiles.")
            return
        
        if self.awaiting_delete_confirmation:
            self.btn_delete_profile.setText("Delete profile")
            self.awaiting_delete_confirmation = False
            self.profiles.remove(self.active_profile)
            file_path = create_config_filepath(self.config_dir, self.active_profile)
            os.remove(file_path)
            self.active_profile = self.profiles[0]
            self.refresh_all()  
        else:
            self.btn_delete_profile.setText("Confirm delete")
            self.awaiting_delete_confirmation = True

    def refresh_all(self):
        self.update_profiles_from_dir()
        self.alphabetize_profile_options()
        self.update_nn_inputs()

        self.cmb_agent_type.blockSignals(True)
        self.cmb_agent_type.setCurrentText(self.config_data["agent_type"])
        self.cmb_agent_type.blockSignals(False)

        self.cmb_profile.blockSignals(True)
        self.cmb_profile.clear()
        self.cmb_profile.addItems(self.profiles)
        self.cmb_profile.setCurrentText(self.active_profile)
        self.cmb_profile.blockSignals(False)

        

    def save_settings(self):


        # Check if all nn layer inputs are valid
        for i, inp_nn_layer in enumerate(self.inp_nn_layers):
            if not inp_nn_layer.text():
                if len(self.inp_nn_layers) == 1:
                    self.show_warning_message(title="Invalid nn layer", message="Network needs at least one layer, save cancelled")    
                else:
                    self.show_warning_message(title="Invalid nn layer", message="Empty nn layer, save cancelled")
                return
            value = int(inp_nn_layer.text())
            if value > 1024:
                self.show_warning_message(title="Invalid nn layer", message="nn layer " + str(i+1) + " too large, save cancelled")
                return
            self.config_data["nn_layers"][i] = value

        self.create_file()

    def create_profile(self):
        name = self.inp_new_profile.text().strip()
        
        # Check if any new profile name was entered
        if not name:
            return
        
        # Avoid adding duplicate profiles
        if name in self.profiles:
            self.show_warning_message(title="Profile exists", message=f"A profile named '{name}' already exists.")
            return
        
        # Add to data model
        # TODO: Add the new profile above the "Add new" option
        self.profiles.append(name)

        self.active_profile = name
        self.create_file()

        self.alphabetize_profile_options()

        self.cmb_profile.blockSignals(True)
        self.cmb_profile.clear()
        self.cmb_profile.addItems(self.profiles)
        self.cmb_profile.setCurrentText(name) # TODO: Consider whether this should be in the refresh_all() function
        self.hide_add_profile()
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

    def create_nn_layer(self):
        n_layers = len(self.inp_nn_layers)

        inp_nn_layer = QtW.QLineEdit()
        inp_nn_layer.setPlaceholderText("Layer " + str(n_layers+1))
        inp_nn_layer.setFixedWidth(60)

        # Ensure that only valid expressions can be profile names
        nn_validator = QtG.QRegularExpressionValidator(
            QtC.QRegularExpression("[0-9]+")
        )
        inp_nn_layer.setValidator(nn_validator)  

        self.inp_nn_layers.append(inp_nn_layer)
        self.update_nn_inputs()

    def remove_nn_layer(self):
        removed_widget = self.inp_nn_layers.pop()
        removed_widget.deleteLater()
        self.update_nn_inputs()

    def update_nn_inputs(self):

        n_layers = len(self.inp_nn_layers)
        if n_layers >= 5:
            self.btn_add_nn_layer.setEnabled(False)
        else:
            self.btn_add_nn_layer.setEnabled(True)
        if n_layers <= 1:
            self.btn_remove_nn_layer.setEnabled(False)
        else:
            self.btn_remove_nn_layer.setEnabled(True)

        self.clear_layout(self.lyt_nn_layers)

        for inp_nn_layer in self.inp_nn_layers:
            self.lyt_nn_layers.addWidget(inp_nn_layer)
            self.lyt_nn_layers.addSpacing(10)
        self.lyt_nn_layers.addStretch()
        

    def load_nn_inputs(self):
        while self.inp_nn_layers:
            self.remove_nn_layer()
        for layer in self.config_data["nn_layers"]:
            if layer != 0:
                self.create_nn_layer()
        for i, inp_nn_layer in enumerate(self.inp_nn_layers):
            inp_nn_layer.setText(str(self.config_data["nn_layers"][i]))

    def clear_layout(self, layout: QtW.QBoxLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                layout.removeWidget(widget)

    def show_warning_message(self, title, message):
        QtW.QMessageBox.warning(self, title, message)

    def create_file(self):
        # Generate file string to save config data to
        file_string = "agent_game/config/config_" + self.active_profile + ".json"

        # Save config data
        with open(file_string, "w") as json_file:
            json.dump(self.config_data, json_file, indent=4)

    def disable_below_profile(self):
        self.cmb_agent_type.setEnabled(False)
        self.btn_add_nn_layer.setEnabled(False)
        self.btn_remove_nn_layer.setEnabled(False)
        self.btn_delete_profile.setEnabled(False)
        self.btn_recover.setEnabled(False)
        self.btn_save.setEnabled(False)  
        for inp_nn_layer in self.inp_nn_layers:
            inp_nn_layer.setEnabled(False)

    def enable_below_profile(self):
        self.cmb_agent_type.setEnabled(True)
        #self.btn_add_nn_layer.setEnabled(True)
        #self.btn_remove_nn_layer.setEnabled(True)
        self.btn_delete_profile.setEnabled(True)
        self.btn_recover.setEnabled(True)
        self.btn_save.setEnabled(True)  
        for inp_nn_layer in self.inp_nn_layers:
            inp_nn_layer.setEnabled(True)

config_dir = "agent_game/config"


app = QtW.QApplication([])

window = MainWindow(config_dir=config_dir)
window.show()

app.exec()
