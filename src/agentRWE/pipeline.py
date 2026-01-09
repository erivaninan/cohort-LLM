#cohort_LLM/src/agentRWE/pipeline.py

from src.agentRWE.load import *
from src.agentRWE.simulation_engine import SimulationEngine
import os

def run_full_pipeline():
    """
    Orchestrates the entire simulation:
    1. Auth 2. Data Loading 3. Simulation 4. Export
    """
    print("--- Starting AgentRWE Pipeline ---")

    # api config
    if not load_api():
        print("Pipeline aborted: API configuration failed.")
        return

    # load experimental protocol and subject data
    cohort = load_cohort()
    sim_params = load_simu_params()

    if not cohort or not sim_params:
        print("Pipeline aborted: Missing cohort or simulation parameters.")
        return

    # initialize and run simulation
    print(f"Initializing Simulation Engine for {len(cohort)} patients...")
    engine = SimulationEngine(cohort)

    # We pass the TOML parameters to the run method
    df_results = engine.run_simulation(
        months=sim_params['duration_months'],
        shock_month=sim_params['shock_month'],
        event=sim_params['shock_event']
    )

    # 4. Save and Export Data
    if not df_results.empty:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

        output_path = "output/final_simulation_results.csv"
        df_results.to_csv(output_path, index=False)
        print(f"--- Pipeline Completed Successfully ---")
        print(f"Results saved to: {output_path}")
        return df_results
    else:
        print("Pipeline finished but no data was generated.")