#cohort_LLM/src/agentRWE/simulation_engine.py
# Core simulation logic that handles the temporal loop and synchronizes
# autonomous agent reactions to environmental events.

import pandas as pd
import time
from src.agentRWE.patient_agent import PatientAgent

class SimulationEngine:
    def __init__(self, client, patients_data):
        """
        Initializes the engine with the GenAI client and patient profiles.
        """
        self.client = client
        # transform raw data (dictionaries) into Agent objects
        self.agents = [PatientAgent(self.client, p) for p in patients_data]
        self.all_results = []

    def run_simulation(self, months, shock_month, event):
        """
        Main loop orchestrating the simulation over time.
        """
        print(f"Starting simulation for {len(self.agents)} agents over {months} months.")

        for m in range(1, months + 1):
            # determine the context for the current month
            current_event = event if m == shock_month else "Normal conditions"
            print(f"--- Month {m} ({current_event})")

            for agent in self.agents:
                # trigger agent reaction
                result = agent.react_to_month(m, current_event)

                # add useful cols
                result['month'] = m
                result['patient_id'] = agent.id

                self.all_results.append(result)

                # API rate limit
                time.sleep(5)

        df = pd.DataFrame(self.all_results)

        # csv column order
        cols = ['patient_id', 'month', 'observance', 'symptomes', 'journal']
        return df[cols]