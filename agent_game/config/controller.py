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
        self.config.agent_type = agent_type
        if agent_type != "Ego":
            self.config.occupance_size = 0
        self.config_changed.emit(self.config)

    def switch_profile(self, profile_name: str):
        self.active_profile = profile_name
        self.config = self.pr.load_from_profile(profile_name)
        self.profile_changed.emit(profile_name)
        self.config_changed.emit(self.config)
    
    def create_profile(self, profile_name: str):
        # Check if any new profile name was entered
        if not profile_name:
            raise ValueError("Profile name cannot be empty.")
        
        # Avoid adding duplicate profiles
        if profile_name in self.profiles:
            raise ValueError(f"A profile named '{profile_name}' already exists.")
        
        self.pr.save_profile(profile_name, self.config)
        self.switch_profile(profile_name)

    def save(self):
        self.pr.save_profile(self.active_profile, self.config)