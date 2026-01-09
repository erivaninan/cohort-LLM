#cohort_LLM/src/agentRWE/patient_agent.py

import google.generativeai as genai
from google.generativeai.types import generation_types
import json
from src.agentRWE.utils import ensure_dict, validate_scores, safe_generate_content

class PatientAgent:
    def __init__(self, config):
        self.id = config["id"]
        self.profile = config["profile"]
        self.history = []
        self.model = genai.GenerativeModel('models/gemini-2.0-flash')

    def react_to_month(self, month, event):
        # 1. Context Construction
        context = ""
        if self.history:
            last = self.history[-1]
            context = f"Last month, your treatment adherence was {last['observance']}%."

        # 2. Prompt Definition
        prompt = f"""
        You are simulating a real patient: {self.profile}
        History: {context}
        Current time: Month {month}
        Event: {event}

        Return ONLY a JSON object:
        {{
            "observance": (0-100),
            "symptomes": (1-10),
            "journal": (one short sentence in English)
        }}
        """

        # 3. Safe API Call
        config = generation_types.GenerationConfig(response_mime_type="application/json")
        response = safe_generate_content(self.model, prompt, config)

        # 4. Data Processing & Fallback
        if response:
            data = ensure_dict(json.loads(response.text))
        else:
            data = {"observance": 0, "symptomes": 5, "journal": "API disconnected."}

        # 5. Validation & History
        data = validate_scores(data, "observance", 0, 100)
        data = validate_scores(data, "symptomes", 1, 10)
        data.update({"month": month, "patient_id": self.id})
        self.history.append(data)

        print(f"Agent {self.id} | Month {month} | Adherence: {data['observance']}%")
        return data