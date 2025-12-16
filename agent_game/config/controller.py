import PyQt6.QtCore as QtC

from config.repository import ProfileRepository
from config.model import AgentConfig


class ConfigController(QtC.QObject):
    config_changed = QtC.pyqtSignal(AgentConfig)

    def __init__(self, profile_repository: ProfileRepository):
        super().__init__()
        self.pr = profile_repository
        self.profile = self.pr.startup_profile
        self.config = self.pr.load_from_profile(self.profile)


    def set_agent_type(self, agent_type: str):
        self.config
