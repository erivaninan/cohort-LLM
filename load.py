#load.py

import tomllib
import google.generativeai as genai
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_api(config_path="config/api.toml"):
    """
    Loads the Gemini API key from a toml file and configures the GenerativeAI library.
    """
    config_path = os.path.join(ROOT_DIR, "config", "api.toml")
    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
        genai.configure(api_key=config_data["api"]["gemini_key"])
        return True
    except Exception as e:
        print(f"API Configuration failed: {e}")
        return False

def load_cohort(config_path="config/cohort.toml"):
    """
    Reads the patient cohort from a toml file.
    Returns: A list of dictionaries, where each dictionary is a patient profile.
    """
    config_path = os.path.join(ROOT_DIR, "config", "cohort.toml")
    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)

        # parsing list under [[patients]] key
        cohort = config_data.get("patients", [])
        return cohort

    except FileNotFoundError:
        print(f"Error: {config_path} not found.")
        return []
    except Exception as e:
        print(f"Error parsing cohort: {e}")
        return []

def load_simu_params(config_path="config/simulation.toml"):
    """
    Reads study simulation parameters (duration, shock event) from toml.
    """
    config_path = os.path.join(ROOT_DIR, "config", "simulation.toml")
    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
        return config_data.get("params", {})
    except Exception as e:
        print(f"Error loading simulation params: {e}")
        return {}

