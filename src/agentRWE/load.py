#cohort_LLM/src/agentRWE/load.py
# Utility module dedicated to securely loading API credentials
# and external configuration files.

import tomllib
from google import genai
import pandas as pd
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def load_api(config_name="api.toml"):
    """
    Loads the Gemini API key from a toml file and initializes the GenAI Client.
    """
    config_path = os.path.join(BASE_DIR, "config", config_name)
    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)

        api_key = config_data.get("api", {}).get("gemini_key")

        client = genai.Client(api_key=api_key)
        return client

    except Exception as e:
        print(f"API configuration failed: {e}")
        return None

def load_cohort(config_path="config/cohort.toml"):
    """
    Reads the patient cohort from a toml file.
    Returns: A list of dictionaries, where each dictionary is a patient profile.
    """
    config_path = os.path.join(ROOT_DIR, "../../config", "cohort.toml")
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
    config_path = os.path.join(ROOT_DIR, "../../config", "simulation.toml")
    try:
        with open(config_path, "rb") as f:
            config_data = tomllib.load(f)
        return config_data.get("params", {})
    except Exception as e:
        print(f"Error loading simulation params: {e}")
        return {}

def load_simu_results(filename="final_simulation_results.csv"):
    """Loads simulation results from the output folder into a DataFrame."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base_dir, "output", filename)
    return pd.read_csv(path)

