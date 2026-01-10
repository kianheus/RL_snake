import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC
import PyQt6.QtGui as QtG

# We shouldn't be needing these
#import json
#import os

from agent_game.config.controller import ConfigController
#from agent_game.config.repository import ProfileRepository, create_config_filepath 
# TODO: That create_config_filepath import probably shouldn't have to exist




class MainTab(QtW.QWidget):
    def __init__(self, config_controller: ConfigController):
        super().__init__()
        self.cc = config_controller
        self.init_ui()
        self.init_connections()

    def init_ui(self):

        self.lyt_main = QtW.QVBoxLayout()

        ### Profile selection row

        # Text description
        self.lbl_profile = QtW.QLabel("Profile:")

        # Combobox
        self.cmb_profile = QtW.QComboBox()
        self.cmb_profile.addItems(self.cc.available_profiles())
        self.cmb_profile.setCurrentText(self.cc.active_profile)

        # Fill layout
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

        # Fill layout
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
        self.cmb_agent_type = QtW.QComboBox()
        self.cmb_agent_type.addItems(self.cc.available_agent_types())
        self.cmb_agent_type.setCurrentText(self.cc.config.agent_type)

        # Add items to layout
        self.lyt_agent = QtW.QHBoxLayout()
        self.lyt_agent.addWidget(self.lbl_agent)
        self.lyt_agent.addWidget(self.cmb_agent_type)

        ### Ego agent occupance row

        # Text description
        self.lbl_ego_occupance = QtW.QLabel("Occupance size:")

        # Input field

        self.inp_ego_occupance = QtW.QLineEdit()
        ego_occupance_validator = QtG.QIntValidator(1, 21)
        self.inp_ego_occupance.setValidator(ego_occupance_validator) 
        self.inp_ego_occupance.setFixedWidth(50)
        self.inp_ego_occupance.setPlaceholderText("7")

        # Fill layout
        self.lyt_ego_occupance = QtW.QHBoxLayout()
        self.lyt_ego_occupance.addStretch()
        self.lyt_ego_occupance.addWidget(self.lbl_ego_occupance)
        self.lyt_ego_occupance.addSpacing(10)
        self.lyt_ego_occupance.addWidget(self.inp_ego_occupance)


        ### NN layers selection box

        # Text description
        self.lbl_nn_layers = QtW.QLabel("NN hidden layers:")

        # New layer button
        self.btn_add_nn_layer = QtW.QPushButton("Add layer")
        self.btn_add_nn_layer.setFixedWidth(100)

        # Small spacer
        self.nn_w_spacer = QtW.QWidget()
        self.nn_w_spacer.setFixedWidth(10)

        # Remove layer button
        self.btn_remove_nn_layer = QtW.QPushButton("Remove layer")
        self.btn_remove_nn_layer.setFixedWidth(100)
        self.btn_remove_nn_layer.setEnabled(False)

        # Add items to layout
        self.lyt_nn_description = QtW.QHBoxLayout()
        self.lyt_nn_description.addWidget(self.lbl_nn_layers)
        self.lyt_nn_description.addWidget(self.btn_add_nn_layer)
        self.lyt_nn_description.addWidget(self.nn_w_spacer)
        self.lyt_nn_description.addWidget(self.btn_remove_nn_layer)

        # Prepare list of nn layers
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
        self.btn_recover.setFixedWidth(110)

        # Define delete button
        self.btn_delete_profile = QtW.QPushButton("Delete profile")
        self.btn_delete_profile.setFixedWidth(110)
        self.awaiting_delete_confirmation = False

        # Define save button
        self.btn_save = QtW.QPushButton("Save")
        self.btn_save.setFixedWidth(110)
        
        # Define save and run button
        self.btn_save_and_run = QtW.QPushButton("Save and run")
        self.btn_save_and_run.setFixedWidth(110)

        # Add items to save/recover layout
        self.lyt_save = QtW.QHBoxLayout()
        self.lyt_save.addWidget(self.btn_recover)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_delete_profile)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_save)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_save_and_run)

        ### Add all items to main tab
        line_height = self.fontMetrics().height()

        self.lyt_main.addLayout(self.lyt_profile)
        self.spacer1 = QtW.QWidget()
        self.spacer1.setFixedHeight(self.profile_row_height)
        self.lyt_main.addWidget(self.spacer1)
        self.lyt_main.addLayout(self.lyt_agent)
        self.lyt_main.addLayout(self.lyt_ego_occupance)
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
        self.setLayout(self.lyt_main)

        ### Call any methods required at startup
        self.refresh_all()
        self.hide_add_profile()
        self.hide_occupance_input()
        self.load_nn_inputs()

    def init_connections(self):

        self.cmb_profile.currentTextChanged.connect(self.profile_type_changed)
        self.btn_create_profile.clicked.connect(self.handle_profile_creation)  

        self.cmb_agent_type.currentTextChanged.connect(self.agent_type_changed)

        self.inp_ego_occupance.textChanged.connect(self.occupance_input_changed)

        self.btn_add_nn_layer.clicked.connect(self.create_nn_layer)  
        self.btn_remove_nn_layer.clicked.connect(self.remove_nn_layer)  

        self.btn_recover.clicked.connect(self.reset_profile)
        self.btn_delete_profile.clicked.connect(self.delete_profile)
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_save_and_run.clicked.connect(self.save_and_run)

        self.cc.profile_changed.connect(self.render_profile)
        self.cc.config_changed.connect(self.render_config)

        self.cc.profile_created.connect(self.on_profile_created)
        self.cc.error_occurred.connect(self.show_warning_message)

    def occupance_input_changed(self, size_string):
        self.cc.set_occupance(size_string)

    def profile_type_changed(self, text: str):

        if text == "Add new":
            self.show_add_profile()
            return

        self.hide_add_profile()
        self.cc.switch_profile(profile_name=text)

    """
    def profile_type_changed(self, type_string):
        if type_string == "Add new":
            self.show_add_profile()
        else:
            self.pm.active_profile = type_string
            profile_filepath = create_config_filepath(self.pm.config_dir, self.pm.active_profile)   
            self.pm.config_data = self.pm.load_from_profile(type_string)
            self.refresh_all()      
            self.hide_add_profile()
            self.load_nn_inputs()
    """

    def handle_profile_creation(self):
        profile_name = self.inp_new_profile.text().strip()
        ok, title, msg = self.pm.create_profile(profile_name)

        if not ok:
            self.show_warning_message("Profile error", title, msg)
            return

        self.update_config_from_ui()

        self.cmb_profile.blockSignals(True)
        self.cmb_profile.clear()
        self.cmb_profile.addItems(self.pm.profiles)
        self.cmb_profile.setCurrentText(profile_name) # TODO: Consider whether this should be in the refresh_all() function
        self.cmb_profile.blockSignals(False)
        
        # Clear input box
        self.hide_add_profile()
        self.inp_new_profile.clear()

    def agent_type_changed(self, type_string):
        self.cc.config.agent_type = type_string
        if type_string == "Ego":
            self.show_occupance_input()
        else:
            self.hide_occupance_input()

    def create_nn_layer(self):
        n_layers = len(self.inp_nn_layers)

        inp_nn_layer = QtW.QLineEdit()
        inp_nn_layer.setPlaceholderText("Layer " + str(n_layers+1))
        inp_nn_layer.setFixedWidth(60)

        # Ensure that only valid expressions can be profile names
        nn_validator = QtG.QIntValidator(1, 1024)
        inp_nn_layer.setValidator(nn_validator)  

        self.inp_nn_layers.append(inp_nn_layer)
        self.update_nn_inputs()

    def remove_nn_layer(self):
        removed_widget = self.inp_nn_layers.pop()
        removed_widget.deleteLater()
        self.update_nn_inputs()

    def reset_profile(self):
        with open("agent_game/config/config_recovery.json") as f:
            self.pm.config_data = json.load(f)

        self.inp_nn_layers = []
        self.load_nn_inputs()
        self.refresh_all()

    def delete_profile(self):

        if self.pm.active_profile == "basic_01" or self.pm.active_profile == "ego_01":
            self.show_warning_message(title="Invalid remove", message="Cannot remove core profiles.")
            return
        
        if self.awaiting_delete_confirmation:
            self.btn_delete_profile.setText("Delete profile")
            self.awaiting_delete_confirmation = False
            self.pm.profiles.remove(self.pm.active_profile)
            file_path = create_config_filepath(self.pm.config_dir, self.pm.active_profile)
            os.remove(file_path)
            self.pm.active_profile = self.pm.profiles[0]
            self.refresh_all()  
        else:
            self.btn_delete_profile.setText("Confirm delete")
            self.awaiting_delete_confirmation = True

    def save_settings(self):

        if self.pm.config_data.agent_type == "Ego":
            if self.pm.config_data.occupance_size % 2 == 0:
                self.show_warning_message(title="Even occupance size", message="Occupance size must be an odd number")
                return
        else:
            self.pm.config_data.occupance_size = 0

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
            self.pm.config_data.nn_layers[i] = value

        self.pm.save_profile(self.pm.active_profile, self.pm.config_data)

    def save_and_run(self):
        self.save_settings()
        self.window().close()

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

    def show_occupance_input(self):
        self.lbl_ego_occupance.show()
        self.inp_ego_occupance.show()
        self.spacer2.hide()
    
    def hide_occupance_input(self):
        self.lbl_ego_occupance.hide()
        self.inp_ego_occupance.hide()
        self.spacer2.show()


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
        self.btn_delete_profile.setEnabled(True)
        self.btn_recover.setEnabled(True)
        self.btn_save.setEnabled(True)  
        for inp_nn_layer in self.inp_nn_layers:
            inp_nn_layer.setEnabled(True)

    def load_nn_inputs(self):
        while self.inp_nn_layers:
            self.remove_nn_layer()
        for layer in self.cc.config.nn_layers:
            if layer != 0:
                self.create_nn_layer()
        for i, inp_nn_layer in enumerate(self.inp_nn_layers):
            inp_nn_layer.setText(str(self.cc.config.nn_layers[i]))

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

    def clear_layout(self, layout: QtW.QBoxLayout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                layout.removeWidget(widget)
        

    def refresh_all(self):
        profiles = self.cc.available_profiles()
        self.update_nn_inputs()

        #self.cmb_agent_type.blockSignals(True)
        self.cmb_agent_type.setCurrentText(self.cc.config.agent_type)
        #self.cmb_agent_type.blockSignals(False)

        self.cmb_profile.blockSignals(True)
        self.cmb_profile.clear()
        self.cmb_profile.addItem("Add new")
        self.cmb_profile.addItems(self.cc.available_profiles())
        self.cmb_profile.setCurrentText(self.cc.active_profile)
        self.cmb_profile.blockSignals(False)

    def update_config_from_ui(self):
        # Copy agent type
        self.pm.config_data.agent_type = self.cmb_agent_type.currentText()

        # Copy NN layers from the QLineEdits
        nn_layers = []
        for inp_nn_layer in self.inp_nn_layers:
            text = inp_nn_layer.text()
            if text:
                nn_layers.append(int(text))
            else:
                nn_layers.append(0)
        self.pm.config_data.nn_layers = nn_layers

    def show_warning_message(self, title, message):
        QtW.QMessageBox.warning(self, title, message)

    def render_profile(self, profile):
        print("rendering the profile, biip baap")
        print("Does this exist?", profile)

    def render_config(self, config):
        print("rendering the config, beep boop")
        print("Does this variable exist?", config)
        self.refresh_all()