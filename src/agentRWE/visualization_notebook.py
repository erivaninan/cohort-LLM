#cohort_LLM/src/agentRWE/visualization_notebook.py
# Data analysis module that generates standardized visual
# representations of simulations.

import plotly.express as px

def plot_adherence_trends(df, shock_month=3, save_path=None):
    """Generates a dynamic line plot for average adherence trends."""
    # Data aggregation
    stats = df.groupby('month')['observance'].mean().reset_index()

    # Create the dynamic line plot
    fig = px.line(stats, x='month', y='observance',
                  title="Mean Cohort Adherence",
                  markers=True,
                  labels={'observance': 'Adherence (%)', 'month': 'Month'})

    # Add vertical line for the shock month
    if shock_month:
        fig.add_vline(x=shock_month, line_dash="dash", line_color="red",
                      annotation_text="Shock Event")

    # Update layout for a cleaner look
    fig.update_layout(yaxis_range=[0, 105], template="plotly_white")

    # Save as interactive HTML if path provided
    if save_path:
        fig.write_html(save_path.replace('.png', '.html'))

    fig.show()

def plot_symptom_progression(df, save_path=None):
    """Generates a dynamic boxplot for symptom distribution."""
    fig = px.box(df, x='month', y='symptomes',
                 color='month',
                 title="Symptom Distribution per Month",
                 labels={'symptomes': 'Symptom Level (1-10)'})

    fig.update_layout(template="plotly_white")

    if save_path:
        fig.write_html(save_path.replace('.png', '.html'))

    fig.show()

def plot_individual_paths(df, save_path=None):
    """Displays the trajectories of ALL patients on a single graph."""
    fig = px.line(df, x='month', y='adherence', color='patient_id',
                  title="Individual Patient Trajectories",
                  labels={'adherence': 'Adherence (%)', 'patient_id': 'Patient ID'},
                  render_mode="svg")  # Better rendering for small datasets
    fig.update_layout(yaxis_range=[0, 105], template="plotly_white")

    # saving
    if save_path:
        fig.write_html(save_path.replace('.png', '.html'))

    return fig