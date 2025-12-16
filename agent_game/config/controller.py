import PyQt6.QtCore as QtC

from config.repository import ProfileRepository
from config.model import AgentConfig


class ConfigController(QtC.QObject):
    config_changed = QtC.pyqtSignal(AgentConfig)
    profile_changed = QtC.pyqtSignal(str)

    def __init__(self, pr: ProfileRepository):
        super().__init__()
        self.pr = pr
        self.active_profile = self.pr.startup_profile
        self.config = self.pr.load_from_profile(self.active_profile)


    def set_agent_type(self, agent_type: str):
        self.config
