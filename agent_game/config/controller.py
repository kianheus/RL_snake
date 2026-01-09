import PyQt6.QtCore as QtC

from agent_game.config.repository import ProfileRepository
from agent_game.config.model import AgentConfig, AgentType


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
        if profile_name in self.pr.list_profiles():
            raise ValueError(f"A profile named '{profile_name}' already exists.")
        
        self.pr.save_profile(profile_name, self.config)
        self.switch_profile(profile_name)

    def save(self):
        self.pr.save_profile(self.active_profile, self.config)

    def available_profiles(self) -> list[str]:
        return self.pr.list_profiles()

    def available_agent_types(self) -> list[str]:
        return [a.value for a in AgentType]
    
    def set_occupance(self, size_string: int):
        self.config.occupance_size = int(size_string) if size_string.isdigit() else 0
        self.config_changed.emit(self.config)

    def select_profile(self, profile_name):
        self.active_profile = profile_name