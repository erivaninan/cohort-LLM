#cohort_LLM/src/agentRWE/visualization.py

import plotly.express as px

def plot_adherence_trends(df, shock_month=3):
    """Generates a line plot for average cohort adherence."""
    # Ensure data is clean
    stats = df.groupby('month')['observance'].mean().reset_index()

    fig = px.line(stats, x='month', y='observance',
                  title="📈 Mean Cohort Adherence",
                  markers=True,
                  labels={'observance': 'Adherence (%)', 'month': 'Month'})

    if shock_month:
        fig.add_vline(x=shock_month, line_dash="dash", line_color="red",
                      annotation_text="Shock Event")

    fig.update_layout(yaxis_range=[0, 105], template="plotly_white")
    return fig


def plot_symptom_progression(df):
    """Generates a boxplot for symptom distribution over time."""
    fig = px.box(df, x='month', y='symptomes', color='month',
                 title="🌡️ Symptom Distribution",
                 labels={'symptomes': 'Level (1-10)', 'month': 'Month'})
    fig.update_layout(template="plotly_white")
    return fig


def plot_individual_paths(df):
    """Displays the adherence trajectories of all patients individually."""
    fig = px.line(df, x='month', y='observance', color='patient_id',
                  title="👥 Individual Adherence Trajectories",
                  labels={'observance': 'Adherence (%)', 'patient_id': 'Patient ID'})
    fig.update_layout(yaxis_range=[0, 105], template="plotly_white")
    return fig