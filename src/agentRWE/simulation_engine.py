#cohort_LLM/src/agentRWE/simulation_engine.py

import pandas as pd
import time
from src.agentRWE.patient_agent import PatientAgent

class SimulationEngine:
    def __init__(self, patients_data):
        """
        Initializes the engine with a list of patient profiles.
        """
        # transform raw data (dictionaries) into Agent objects
        self.agents = [PatientAgent(p) for p in patients_data]
        self.all_results = []

    def run_simulation(self, months, shock_month, event):
        """
        Main loop orchestrating the simulation over time.
        """
        print(f"Starting simulation for {len(self.agents)} agents over {months} months.")

        for m in range(1, months + 1):
            # Determine the context for the current month
            current_event = event if m == shock_month else "Normal conditions"
            print(f"--- Month {m} ({current_event}) ---")

            for agent in self.agents:
                # Trigger agent reaction
                result = agent.react_to_month(m, current_event)
                self.all_results.append(result)

                time.sleep(4)

        return pd.DataFrame(self.all_results)