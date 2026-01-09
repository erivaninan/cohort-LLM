# cohorte-LLM/main.py
# Primary entry point that orchestrates the execution of the full RWE simulation pipeline.

from src.agentRWE.pipeline import run_full_pipeline

if __name__ == '__main__':
    # Run simulation from command line
    run_full_pipeline()