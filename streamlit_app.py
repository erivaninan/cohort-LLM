#cohort_LLM/app.py

import streamlit as st
import pandas as pd
import os
import sys

# Ensure the 'src' directory is in the python path
sys.path.append(os.getcwd())

from src.agentRWE.load import load_simu_results
from src.agentRWE.visualization import (
    plot_adherence_trends,
    plot_symptom_progression,
    plot_individual_paths
)

# Page configuration
st.set_page_config(
    page_title="AgentRWE Dashboard",
    layout="wide",
    page_icon="🧪"
)

st.title("🧪 AgentRWE: Real-World Evidence Simulation")
st.markdown("---")

# 1. Load Simulation Results
df = load_simu_results()

if df is not None:
    # --- SIDEBAR SETTINGS ---
    st.sidebar.header("Dashboard Settings")
    shock_m = st.sidebar.slider("Visualize Shock at Month", 1, 6, 3)

    # --- KPI SECTION ---
    # Calculating key metrics
    avg_obs = df['observance'].mean()
    avg_symp = df['symptomes'].mean()
    nb_pat = df['patient_id'].nunique()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cohort", f"{nb_pat} Patients")
    col2.metric("Mean Adherence", f"{avg_obs:.1f} %")
    col3.metric("Mean Symptoms", f"{avg_symp:.1f} / 10")

    st.markdown("---")

    # --- MAIN TABS ---
    tab1, tab2, tab3 = st.tabs(["📊 Global Trends", "👥 Individual Analysis", "📋 Raw Data & Journals"])

    with tab1:
        # Side-by-side global charts
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(plot_adherence_trends(df, shock_month=shock_m), use_container_width=True)
        with c2:
            st.plotly_chart(plot_symptom_progression(df), use_container_width=True)

    with tab2:
        # Full width individual trajectory chart
        st.plotly_chart(plot_individual_paths(df), use_container_width=True)

        st.markdown("### 🔍 Patient-Specific Insights")
        selected_id = st.selectbox("Select a Patient ID to inspect", df['patient_id'].unique())

        patient_records = df[df['patient_id'] == selected_id]

        # Displaying the LLM-generated journals as a timeline
        for _, row in patient_records.iterrows():
            with st.chat_message("user" if row['observance'] > 50 else "assistant"):
                st.write(
                    f"**Month {row['month']}** (Adherence: {row['observance']}% | Symptoms: {row['symptomes']}/10)")
                st.write(f"_{row['journal']}_")

    with tab3:
        st.subheader("Simulation Dataset")
        st.dataframe(df, use_container_width=True)

        # Download button for recruiters/researchers
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="agent_rwe_results.csv",
            mime="text/csv"
        )

else:
    st.warning("No simulation results found. Please run the simulation pipeline first.")
    if st.button("Run Simulation Now"):
        st.info("Simulation engine started... Check your terminal for progress.")
        # Optional: Add call to run_full_pipeline() here