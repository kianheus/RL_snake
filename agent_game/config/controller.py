import PyQt6.QtCore as QtC

from agent_game.config.repository import ProfileRepository
from agent_game.config.agent_config import AgentConfig, AgentType


class ConfigController(QtC.QObject):
    config_changed = QtC.pyqtSignal(AgentConfig)
    profile_changed = QtC.pyqtSignal(str)
    error_occurred = QtC.pyqtSignal(str, str)

    def __init__(self, pr: ProfileRepository):
        super().__init__()
        self.pr = pr

        self.active_profile = self.pr.startup_profile
        self.config = self.pr.load_from_profile(self.active_profile)
        
        self.run_sim = False


    def set_agent_type(self, agent_type: str):
        self.config.agent_type = agent_type
        if agent_type != "Ego":
            self.config.occupance_size = 0
        self.emit_config_change()

    def switch_profile(self, profile_name: str):
        self.active_profile = profile_name
        self.config = self.pr.load_from_profile(profile_name)
        self.emit_profile_change()

    def reset_profile(self):
        self.config = self.pr.load_from_profile("recovery")
        self.emit_profile_change()
    
    def create_profile(self, profile_name: str):
        # Check if any new profile name was entered
        if not profile_name:
            self.error_occurred.emit(
                "Profile creation error", 
                "Profile name cannot be empty."
                )
            return
        
        # Avoid adding duplicate profiles
        if profile_name in self.pr.list_profiles():
            self.error_occurred.emit(
                "Profile creation error", 
                f"A profile named '{profile_name}' already exists."
                )
            return
        
        # Save new profile to .json, switch and emit
        self.pr.save_profile(profile_name, self.config)
        self.switch_profile(profile_name)
    
    def delete_profile(self):
        if self.active_profile in self.pr.core_profiles:
            self.error_occurred.emit(
                "Invalid remove", 
                "Cannot remove core profiles"
                )
            return
        
        self.pr.delete_profile(self.active_profile)
        profiles = self.pr.list_profiles()
        self.active_profile = profiles[0]
        self.config = self.pr.load_from_profile(self.active_profile)
        self.emit_profile_change()
        

    def save_settings(self, nn_layers: list[str]):

        if self.config.agent_type == AgentType.EGO:
            if self.config.occupance_size % 2 == 0:
                self.error_occurred.emit(
                    "Save cancelled",
                    "Occupance size must be an odd number."
                )
                return
        else:
            self.config.occupance_size = 0
        
        self.config.nn_layers = []
        for i, layer in enumerate(nn_layers):
            if not layer:
                self.error_occurred.emit(
                    "Save cancelled",
                    "Empty network layer."
                )
                return
            value = int(layer)
            if value > 1024:
                self.error_occurred.emit(
                    "Save cancelled",
                    f"nn layer {i+1} too large."
                )
                return
            self.config.nn_layers.append(value)
        
        self.pr.save_profile(self.active_profile, self.config)

    def available_profiles(self) -> list[str]:
        return self.pr.list_profiles()

    def available_agent_types(self) -> list[str]:
        return [a.value for a in AgentType]
    
    def set_occupance(self, size_string: int):
        self.config.occupance_size = size_string if size_string.isdigit() else 0
        self.emit_config_change()

    def set_config_variable(self, config_key, value):
        if hasattr(self.config, config_key):
            setattr(self.config, config_key, value)
            self.config_changed.emit(self.config)
            print(f"updated config {config_key} to {value}")
        else: 
            raise KeyError(f"Unrecognized config key {config_key}.")

    def emit_inital_state(self):
        self.emit_profile_change()

    def emit_profile_change(self):
        self.profile_changed.emit(self.active_profile)
        self.config_changed.emit(self.config)
    
    def emit_config_change(self):
        self.config_changed.emit(self.config)