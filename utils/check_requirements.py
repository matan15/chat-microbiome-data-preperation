import requests as req
from .setup_config import setup_config

def is_internet_available():
    try:
        ressponse = req.get("https://www.google.com", timeout=5)
        ressponse.raise_for_status()
        return True
    except req.RequestException:
        pass
    return False
    

def check_requirements():
    if not setup_config():
        return "bad_credentials"
    if not is_internet_available():
        return "not_internet"