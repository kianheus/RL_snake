import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC

class SaveWindow(QtW.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.save_info = True
        self.save_weights = True
        self.save_anim = True

        """     General window settings     """

        window_x = 250
        window_y = 250

        window_width = 400
        window_height = 300

        self.setWindowTitle("Simulation save settings")
        self.setFixedSize(QtC.QSize(window_width, window_height))
        self.center_window()

        self.init_ui()
        self.init_connections()


    def init_ui(self):
        self.spacer1 = QtW.QWidget()
        self.spacer1.setFixedWidth(10)

        ### Training info save row
        # Text description
        self.lbl_info = QtW.QLabel("Save training info:")

        # Checkbox
        self.chb_info = QtW.QCheckBox(self)
        self.chb_info.setChecked(True)

        # Combine into layout
        self.lyt_info = QtW.QHBoxLayout()
        self.lyt_info.addStretch()
        self.lyt_info.addWidget(self.lbl_info)
        self.lyt_info.addWidget(self.spacer1)
        self.lyt_info.addWidget(self.chb_info)


        ### Weights and biases save row
        # Text description
        self.lbl_weights = QtW.QLabel("Save model weights:")

        # Checkbox
        self.chb_weights = QtW.QCheckBox(self)
        self.chb_weights.setChecked(True)

        # Combine into layout
        self.lyt_weights = QtW.QHBoxLayout()
        self.lyt_weights.addStretch()
        self.lyt_weights.addWidget(self.lbl_weights)
        self.lyt_weights.addWidget(self.spacer1)
        self.lyt_weights.addWidget(self.chb_weights)


        ### Animation save row
        # Text description
        self.lbl_anim = QtW.QLabel("Save best run animation:")

        # Checkbox
        self.chb_anim = QtW.QCheckBox(self)
        self.chb_anim.setChecked(True)

        # Combine into layout
        self.lyt_anim = QtW.QHBoxLayout()
        self.lyt_anim.addStretch()
        self.lyt_anim.addWidget(self.lbl_anim)
        self.lyt_anim.addWidget(self.spacer1)
        self.lyt_anim.addWidget(self.chb_anim)


        ### Buttons row

        # Define select all button
        self.btn_select = QtW.QPushButton("Select all")
        self.btn_select.setFixedWidth(110)

        # Define deselect button
        self.btn_deselect = QtW.QPushButton("Deselect all")
        self.btn_deselect.setFixedWidth(110)

        # Define save button
        self.btn_save = QtW.QPushButton("Save and close")
        self.btn_save.setFixedWidth(110)

        # Add items to save/recover layout
        self.lyt_save = QtW.QHBoxLayout()
        self.lyt_save.addWidget(self.btn_select)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_deselect)
        self.lyt_save.addStretch()
        self.lyt_save.addWidget(self.btn_save)

        self.lyt_main = QtW.QVBoxLayout()
        self.lyt_main.addStretch()
        self.lyt_main.addLayout(self.lyt_info)
        self.lyt_main.addLayout(self.lyt_weights)
        self.lyt_main.addLayout(self.lyt_anim)
        self.lyt_main.addStretch()
        self.lyt_main.addLayout(self.lyt_save)

        central_widget = QtW.QWidget()
        central_widget.setLayout(self.lyt_main)

        self.setCentralWidget(central_widget)


    def init_connections(self):
        self.chb_info.stateChanged.connect(self.chb_info_changed)
        self.chb_weights.stateChanged.connect(self.chb_weights_changed)
        self.chb_anim.stateChanged.connect(self.chb_anim_changed)

        self.btn_select.clicked.connect(self.select_all_clicked)
        self.btn_deselect.clicked.connect(self.deselect_all_clicked)
        self.btn_save.clicked.connect(self.save_clicked)

    def center_window(self):
        screen = QtW.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def chb_info_changed(self):
        self.save_info = self.chb_info.isChecked()

    def chb_weights_changed(self):
        self.save_weights = self.chb_weights.isChecked()

    def chb_anim_changed(self):
        self.save_anim = self.chb_anim.isChecked()

    def select_all_clicked(self):
        self.chb_info.setChecked(True)
        self.chb_weights.setChecked(True)
        self.chb_anim.setChecked(True)

    def deselect_all_clicked(self):
        self.chb_info.setChecked(False)
        self.chb_weights.setChecked(False)
        self.chb_anim.setChecked(False)

    def save_clicked(self):
        self.window().close()



def run_save_window():
    app = QtW.QApplication([])
    window = SaveWindow()
    window.show()
    app.exec()

    return window.save_info, window.save_weights, window.save_anim

if __name__ == "__main__":
    save_info, save_weights, save_anim = run_save_window()
    print("I", "should" if save_info else "should not", "save simulation info")
    print("I", "should" if save_weights else "should not", "save model weights")
    print("I", "should" if save_anim else "should not", "save animation")