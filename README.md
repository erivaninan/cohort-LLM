##  [AgentRWE] LLM-Powered Real-World Evidence Simulation

<p>
  <img src="https://img.shields.io/badge/Status-Work_In_Progress-orange?style=flat-square&logo=git" alt="Status">
</p>

| **Live Dashboard** |
| :--- |
| *Access the live dashboard: [🧪 AgentRWE Live](https://cohort-llm.streamlit.app/)* <br><br> <img width="390" alt="dashboard" src="https://github.com/user-attachments/assets/68e71712-9eb1-436a-824b-a1e011e077bb" /> |

### Project Overview

<hr>

**AgentRWE** is a behavioral simulation platform designed to model patient journeys in chronic disease management. 

Using **Large Language Models (LLMs)** as autonomous agents, the system simulates how a cohort of patients reacts to real-world events, such as drug supply chain disruptions or side-effect appearances.

Unlike traditional static simulations, `AgentRWE` leverages the reasoning capabilities of **Gemini 2.0 Flash** to generate qualitative "patient journals" and quantitative metrics (adherence and symptom levels), providing a bridge between clinical data and behavioral psychology.

<div align="center">
  <a href="https://github.com/user-attachments/assets/375d93ab-5b4d-4387-9f44-8f0b536dd57a">
    <img src="https://github.com/user-attachments/assets/375d93ab-5b4d-4387-9f44-8f0b536dd57a" alt="AgentRWE Architecture" width="600">
  </a>
  <br>
  <p><em>AgentRWE system architecture.</em></p>
</div>


### The Core Engine: LLM as a Patient Agent

At the heart of this project is the `PatientAgent` class. Each patient is not just a row in a database, but an **autonomous agent** with:

* **Unique Profiles:** Defined by age, medical history, and personality traits.
* **Cognitive Continuity:** The agent processes monthly events and decides its adherence level based on its "mental state."
* **Qualitative Output:** The LLM generates short journal entries explaining *why* the patient behaved in a certain way, providing context that numbers alone cannot capture.

### The Power of Causal Reasoning

One of the main objectives of `AgentRWE` is to move beyond mere correlation to explore **Causal Inference** in healthcare:

* **Simulating "What-If" Scenarios (Counterfactuals)**: By introducing a "Shock Event" (e.g., a treatment shortage in Month 3), we can observe the direct **causal impact** on patient adherence and symptom progression.
* **Understanding the "Why" (Mechanisms)**: Traditional RWD (Real-World Data) often shows a drop in adherence without explanation. By using LLM agents, we can identify the **causal pathway**: *Shortage -> Anxiety -> Intentional Non-Adherence -> Symptom Relapse*.
* **Heterogeneous Treatment Effects**: We can observe how the same cause (the shock) produces different effects across the cohort, helping researchers understand which patient profiles are most "causally vulnerable" to specific risks.

<br>

<hr>
Why do Agents behave this way ?
<details>
  <summary><h3> Click to learn more about the application of Causal Inference in this project.</h3></summary>
<br>
  
  ### Deep Dive: From Correlation to Causal Simulation
  
  Traditional Real-World Data (RWD) is often purely observational, leading to the "correlation is not causation" trap. `AgentRWE` addresses this by implementing a structural approach to patient behavior.

  **The Causal Directed Acyclic Graph (DAG)**

**Simple case: Considering there are no unobserved covariates** (also known as the "No Unmeasured Confounders" assumption).

  Our simulation models the following causal structure for each patient:

<div align="center">
  <a href="https://github.com/user-attachments/assets/b20c4161-f369-48ef-9229-ae4b0f15c574">
    <img src="https://github.com/user-attachments/assets/b20c4161-f369-48ef-9229-ae4b0f15c574" alt="Directed Acyclic Graph (DAG) of our Simulation." width="250">
  </a>
  <br>
  <p><em>Directed Acyclic Graph (DAG) of our Simulation.</em></p>
</div>

<br>

  where:
  - $X$ **(Baseline/Profile)**: Socio-demographic factors and personality traits defined in `cohort.toml`.
  - $M$ **(Mediator)**: The LLM-generated cognitive state (Anxiety, Confusion, Trust).
  - $E$ **(Exposure/Shock)**: The exogenous intervention (e.g., Drug Shortage) defined in `simulation.toml`.
  - $Y$ **(Outcome)**: Quantitative health metrics (Adherence score and Symptom levels).

By manipulating the Shock $E$, we perform a $do$-intervention ( $do(E=1)$ ), allowing us to observe the downstream effects on $Y$ through the mediator $M$.


**Estimating the Average Treatment Effect (ATE)**

By comparing a baseline simulation (no shock) with our experimental run, the platform serves as a tool to estimate the **Average Treatment Effect (ATE)** of logistical or clinical disruptions on a specific cohort:

<p align="center">
$$ATE = E[Y | do(E=1)] - E[Y | do(E=0)]$$
<p>
  
The LLM agents provides a high-dimensional simulation of how $M$ (patient psychology) reacts to $E$, which is typically the "missing data" in standard clinical databases.

**Heterogeneous Treatment Effects**

A key scientific feature of AgentRWE is the inclusion of a Control Group within the `cohort.toml`.

- Resilient Profiles: Patients with high literacy or strong support systems.
- Vulnerable Profiles: Patients with geographic or financial barriers.

This setup allows the visualization of Heterogeneous Treatment Effects, understanding **not just** if a shock impacts a population, but which specific subgroups are most at risk.

</details>

<hr>

## Tech Stack

<details>
  <summary><b> Click to expand. </b></summary>
<br>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Gemini_2.0-8E75B2?style=for-the-badge&logo=google-gemini&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/uv-installed-purple?style=for-the-badge" alt="uv">
</p>

* **Engine:** Python 3.x
* **LLM API:** Google Gemini 2.0 Flash (via `google-genai`)
* **Interface:** Streamlit (Interactive Web Dashboard)
* **Data Visualization:** Plotly (Dynamic charts & individual trajectories)
* **Data Handling:** Pandas

</details>

## How to Run

### 1. Locally

<details>
  <summary><b>Click to expand installation guide.</b></summary>
<br>
  
**1. Clone the repository**
```bash
git clone https://github.com/erivaninan/cohort-LLM.git
cd cohort-LLM
```

**2. Install dependencies**

```bash
uv sync # using uv (recommended)
pip install -r requirements.txt # using pip
```

**3. Configure your API Key**
Create the `config/api.toml` configuration file, paste your Gemini API Key inside:

```toml
GEMINI_KEY = "your_actual_key_here"
```

**4. (Optional) Customize & Generate your Cohort**
Before running the simulation, you can modify the experimental conditions:

* **Parameters:** Edit `config/simulation.toml` to change `duration_months` or the `shock_event`.
* **Profiles:** Edit `config/cohort.toml` to modify patient biographies (including the **Control Group**).

Once ready, launch the simulation engine:

```bash
uv run python main.py # Using uv
python main.py # Using standard python
```

**Step 5: Launch the Dashboard**
Visualize the results and the causal pathways on the interactive web interface:

```bash
uv run streamlit run app.py # Using uv
streamlit run app.py # Using standard streamlit
```
  
</details>


### 2. On the Web

Access the live dashboard here: [🧪 AgentRWE Live](https://cohort-llm.streamlit.app/)

--------


### Future Roadmap

* **RAG Integration:** Allow agents to "read" medical brochures to see how information impacts their behavior.
* **Advanced Causal Graphs:** Integrating `Do-Calculus` libraries to formally map the causal relationships generated by the agents.


-------

### References 

#### **Core Scientific Framework**

* **Causal Inference & Do-Calculus:** Pearl, J. (2009). *Causality: Models, Reasoning, and Inference*. Cambridge University Press. The fundamental theory behind the  operator and Structural Causal Models (SCM).
* **The Book of Why:** Pearl, J., & Mackenzie, D. (2018). *The Book of Why: The New Science of Cause and Effect*. Basic Books. (Accessible introduction to the "Ladder of Causation" used in this project).
* **Generative Agents:** Park, J. S., et al. (2023). *Generative Agents: Interactive Simulacra of Human Behavior*. arXiv preprint. This work inspired the use of LLMs to maintain "cognitive continuity" in autonomous agents.

#### **Technical Stack & Tools**

* **LLM Engine (Gemini 2.0 Flash)**: Google DeepMind (2024). *Gemini: A Family of Highly Capable Multimodal Models*. Used here for high-speed, long-context behavioral reasoning.
* **Causal Python Ecosystem** (still in progress): Inspired by libraries like **Py-Why/DoWhy**, which formalizes the four steps of causal inference (Model, Identify, Estimate, Refute).
* **Modern Python Tooling**: Managed with **uv**, an extremely fast Python package and project manager that ensures reproducible environments.

#### **Inspiration**

* **AI Village**: This project acknowledges the creative and safety-oriented approach to agent simulation pioneered by the [AI Village](https://theaidigest.org/village) community at DEF CON.
