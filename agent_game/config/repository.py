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

    def load_cookies(self):
        cookies_filepath = self.config_dir + "/cookies.json"
        with open(cookies_filepath) as f:
                    return json.load(f)
    
    def load_from_profile(self, profile_name: str) -> AgentConfig:
        path = create_config_filepath(self.config_dir, profile_name)

        with open(path) as f:
            return config_from_dict(json.load(f))

    def save_profile(self, profile_name: str, config: AgentConfig):
        path = create_config_filepath(self.config_dir, profile_name)
        with open(path, "w") as f:
            json.dump(dict_from_config(config), f, indent=4)   

    def create_profile(self, profile_name: str, config: AgentConfig):
        path = create_config_filepath(self.config_dir, profile_name)
        if os.path.exists(path):
             raise FileExistsError(profile_name)
        self.save_profile(profile_name, config)
    

    
    def list_profiles(self) -> list[str]:
        prefix = "config_"
        suffix = ".json"

        profiles = [
            f.removeprefix(prefix).removesuffix(suffix) 
            for f in os.listdir(self.config_dir)
            if f.startswith(prefix) and f.endswith(suffix)
        ]

        profiles.remove("recovery")
        profiles = sorted(profiles)
        return profiles

