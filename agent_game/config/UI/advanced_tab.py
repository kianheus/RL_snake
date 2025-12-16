import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC

from agent_game.config.controller import ConfigController

class AdvancedTab(QtW.QWidget):
    def __init__(self, config_controller: ConfigController):
        super().__init__()
        self.cc = config_controller
        self.init_ui()
        self.init_connections()

    def init_ui(self):

        ### LR input
        
        # Text description
        self.lbl_lr = QtW.QLabel("Learning rate:")

        # Input box
        self.inp_lr = QtW.QLineEdit()
        self.inp_lr.setPlaceholderText("0.001")
        self.inp_lr.setFixedWidth(100)

        # Add items to layout
        self.lyt_lr = QtW.QHBoxLayout()
        self.lyt_lr.addStretch()
        self.lyt_lr.addWidget(self.lbl_lr)
        self.lyt_lr.addWidget(self.inp_lr)

        ### Gamma input
        
        # Text description
        self.lbl_gamma = QtW.QLabel("Gamma:")

        # Input box
        self.inp_gamma = QtW.QLineEdit()
        self.inp_gamma.setPlaceholderText("0.9")
        self.inp_gamma.setFixedWidth(100)

        # Add items to layout
        self.lyt_gamma = QtW.QHBoxLayout()
        self.lyt_gamma.addStretch()
        self.lyt_gamma.addWidget(self.lbl_gamma)
        self.lyt_gamma.addWidget(self.inp_gamma)

        ### Batch_size input
        
        # Text description
        self.lbl_batch_size = QtW.QLabel("Batch size:")

        # Input box
        self.inp_batch_size = QtW.QLineEdit()
        self.inp_batch_size.setPlaceholderText("1000")
        self.inp_batch_size.setFixedWidth(100)

        # Add items to layout
        self.lyt_batch_size = QtW.QHBoxLayout()
        self.lyt_batch_size.addStretch()
        self.lyt_batch_size.addWidget(self.lbl_batch_size)
        self.lyt_batch_size.addWidget(self.inp_batch_size)

        
        ### Max memory input
        
        # Text description
        self.lbl_max_memory = QtW.QLabel("Max memory:")

        # Input box
        self.inp_max_memory = QtW.QLineEdit()
        self.inp_max_memory.setPlaceholderText("10000")
        self.inp_max_memory.setFixedWidth(100)

        # Add items to layout
        self.lyt_max_memory = QtW.QHBoxLayout()
        self.lyt_max_memory.addStretch()
        self.lyt_max_memory.addWidget(self.lbl_max_memory)
        self.lyt_max_memory.addWidget(self.inp_max_memory)


        ### Add all items to main tab

        self.lyt_main = QtW.QVBoxLayout()
        self.lyt_main.addLayout(self.lyt_lr)
        self.lyt_main.addLayout(self.lyt_gamma)
        self.lyt_main.addLayout(self.lyt_batch_size)
        self.lyt_main.addLayout(self.lyt_max_memory)
        self.lyt_main.addStretch()
        self.setLayout(self.lyt_main)


        ### Tab advanced formatting and spacing
        self.lyt_main.setContentsMargins(20, 20, 20, 20)
        self.lyt_main.setSpacing(0)

    def init_connections(self):
        pass
