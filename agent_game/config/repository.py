import json
import os

from agent_game.config.model import AgentConfig, config_from_dict, dict_from_config

def create_config_filepath(config_dir, profile_name: str) -> str:
    filepath = config_dir + "/config_" + profile_name + ".json"
    return filepath


class ProfileRepository():
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.cookies = self.load_cookies()
        self.startup_profile = self.cookies["last_active"]
        self.agent_types = self.cookies["agent_type_options"]
        self.profiles = self.get_profiles_from_dir()

        ### No longer in ProfileRepository
        #self.config_data = self.load_from_profile(self.active_profile)
        

    def load_cookies(self):
        cookies_filepath = self.config_dir + "/cookies.json"
        with open(cookies_filepath) as f:
                    cookies = json.load(f)
        return cookies
    
    def load_from_profile(self, profile_name: str) -> AgentConfig:
        path = create_config_filepath(self.config_dir, profile_name)

        with open(path) as f:
            config_data = config_from_dict(json.load(f))
        return config_data
    
    def create_profile(self, profile_name):
        profile_name = profile_name
        
        # Check if any new profile name was entered
        if not profile_name:
            return False, "Empty profile name", "Profile name cannot be empty"
        
        # Avoid adding duplicate profiles
        if profile_name in self.profiles:
            return False, "Profile exists", f"A profile named '{profile_name}' already exists."
        
        self.save_profile(profile_name, self.config_data)

        self.profiles.append(profile_name)
        self.active_profile = profile_name
        self.save_profile(profile_name, self.config_data)


        return True, "Succesful creation", "Profile created succesfully"

    def save_profile(self, profile_name: str, config: AgentConfig):
        filepath = create_config_filepath(self.config_dir, profile_name)
        with open(filepath, "w") as f:
            json.dump(dict_from_config(config), f, indent=4)

    def set_active_profile(self, profile_name):
        self.active_profile = profile_name
        self.config_data = self.load_from_profile(profile_name)

    
    def get_profiles_from_dir(self) -> list[str]:
        prefix = "config_"
        suffix = ".json"

        profiles = [
            f.removeprefix(prefix).removesuffix(suffix) for f in os.listdir(self.config_dir)
            if f.startswith(prefix) and f.endswith(suffix)
        ]

        profiles.remove("recovery")
        profiles = sorted(profiles)
        profiles.append("Add new")

        return profiles

