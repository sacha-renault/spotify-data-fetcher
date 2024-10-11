from dataclasses import dataclass
import os
from dotenv import load_dotenv

@dataclass
class EnvVariables:
    spotify_client_id: str
    spotify_client_secret: str

def get_env_var() -> EnvVariables:
    load_dotenv()
    env_variables = EnvVariables(
        os.environ.get("SPOTIFY_ID"),
        os.environ.get("SPOTIFY_SECRET")
    )
    return env_variables