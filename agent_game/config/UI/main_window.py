import PyQt6.QtWidgets as QtW
import PyQt6.QtCore as QtC

from agent_game.config.repository import ProfileRepository
from agent_game.config.controller import ConfigController
from agent_game.config.UI.main_tab import MainTab
from agent_game.config.UI.advanced_tab import AdvancedTab

class MainWindow(QtW.QMainWindow):
    def __init__(self, config_dir):
        super().__init__()
        
        """
        self.load_initial_data()
        self.init_ui()
        self.init_connections()
        self.refresh_all()
        """

        self.pr = ProfileRepository(config_dir=config_dir)
        self.cc = ConfigController(pr=self.pr)

        #self.profiles = self.pm.get_profiles_from_dir()
        #self.active_profile = self.pm.active_profile
        #self.config_data = self.pm.config_data
        

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


        tabs.addTab(MainTab(config_controller=self.cc), "Main")
        tabs.addTab(AdvancedTab(config_controller=self.cc), "Advanced")

        self.setCentralWidget(tabs)

    def init_ui(self):
        pass 

    def init_connections(self):
        pass  



config_dir = "agent_game/config/config_files"


def run_main_window(config_dir: str):
    app = QtW.QApplication([])
    window = MainWindow(config_dir=config_dir)
    window.show()
    app.exec()

    return window.pm.active_profile, window.pm.config_data

if __name__ == "__main__":
    run_main_window(config_dir=config_dir)