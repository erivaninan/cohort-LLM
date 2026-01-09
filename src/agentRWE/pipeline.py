#cohort_LLM/src/agentRWE/pipeline.py
# Manages data loading, engine initialization and final result exportation.

from src.agentRWE.load import *
from src.agentRWE.simulation_engine import SimulationEngine
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_full_pipeline():
    """
    Orchestrates the entire simulation from API client initialization to results export.
    """
    print("--- Starting AgentRWE Pipeline ---")

    # API client init
    client = load_api()
    if client is None:
        print("API configuration failed.")
        return None

    cohort = load_cohort()
    sim_params = load_simu_params()

    if not cohort or not sim_params:
        print("Missing cohort or simulation parameters.")
        return None

    # run simu
    print(f"Initializing Simulation Engine for {len(cohort)} patients...")

    engine = SimulationEngine(client, cohort)

    # execution
    df_results = engine.run_simulation(
        months=sim_params['duration_months'],
        shock_month=sim_params['shock_month'],
        event=sim_params['shock_event']
    )

    # saving
    if df_results is not None and not df_results.empty:
        output_dir = os.path.join(BASE_DIR, "output")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "final_simulation_results.csv")
        df_results.to_csv(output_path, index=False)

        print(f"--- Pipeline Completed Successfully ---")
        print(f"Results saved to: {output_path}")
        return df_results
    else:
        print("Pipeline finished but no data was generated.")
        return None