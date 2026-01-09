#cohort_LLM/src/agentRWE/patient_agent.py
# Defines autonomous agent behavior using LLM memory
# and specific patient profiles to simulate longitudinal health journeys.

import json
from google import genai
from src.agentRWE.utils import ensure_dict, validate_scores, safe_generate_content


class PatientAgent:
    def __init__(self, client, config):
        self.client = client
        self.id = config.get('id', 0)
        self.profile = config.get('profile', "Unknown")
        self.model = "gemini-2.0-flash"

    def react_to_month(self, month, event):
        prompt = (
            f"Patient profile: {self.profile}\n"
            f"Month: {month}\n"
            f"Event: {event}\n\n"
            "Return only a json object: : 'observance' (0-100), 'symptomes' (1-10), 'journal' (short sentence)."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )

            # initial parsing
            data = json.loads(response.text)

            # if model has returned a list, extract the first dict
            if isinstance(data, list) and len(data) > 0:
                data = data[0]

            # if it is still not a dict, create an empty dict
            if not isinstance(data, dict):
                data = {}

            return {
                "observance": int(data.get("observance", 0)),
                "symptomes": int(data.get("symptomes", 0)),
                "journal": str(data.get("journal", "No comment."))
            }

        except Exception as e:
            print(f"Erreur Patient {self.id}: {e}")
            return {"observance": 0, "symptomes": 0, "journal": f"Erreur: {str(e)[:30]}"}