#!/home/kkiragu/.venv/imagesearch/bin/python3

import pandas as pd
from scipy import stats
import numpy as np
import pymc as pm  # Import PyMC3 for Bayesian analysis
import matplotlib.pyplot as plt  # Import Matplotlib for plotting
from bokeh.io import show
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Slider, ColumnDataSource, DataTable, TableColumn


# --- Input Parameters ---

# Well-Mixed Room Model
# G = float(input("Enter Emission Rate (G) (mg/min): "))
# Q = float(input("Enter Ventilation Rate (Q) (m3/min): "))
# V = float(input("Enter Room Volume (V) (m3): "))

# Two-Zone Model (uncomment and modify if needed)
# G = float(input("Enter Emission Rate (G) (mg/min): "))
# Q = float(input("Enter Ventilation Rate (Q) (m3/min): "))
# V_n = float(input("Enter Near Field Volume (V_n) (m3): "))
# V_f = float(input("Enter Far Field Volume (V_f) (m3): "))
# k_nf = float(input("Enter Mass Transfer Coefficient (k_nf) (1/min): "))
# k_fn = float(input("Enter Mass Transfer Coefficient (k_fn) (1/min): "))

# Monte Carlo Simulation
# iterations = int(input("Enter Number of Iterations for Monte Carlo: "))

## Sliders
g_slider = Slider(title='Emission Rate (G) (mg/min)',value=1,start=1,end=1000)
q_slider = Slider(title='Ventilation Rate (Q) (m3/min)',value=1,start=1,end=1000)
v_slider = Slider(title='Emission Room Volume (V) (m3)',value=1,start=1,end=1000)
i_slider = Slider(title='Iterations for Monte Carlo',value=1,start=1,end=1000)

# --- Calculations ---

# Well-Mixed Room Model
def well_mixed_room(G, Q, V):
    """
    Calculates the steady-state concentration in a well-mixed room.

    Args:
      G: Emission rate (mg/min)
      Q: Ventilation rate (m3/min)
      V: Room volume (m3)

    Returns:
      C: Concentration (mg/m3)
    """
    C = G / Q
    return C

# Calculate and print the deterministic result
# C = well_mixed_room(G, Q, V)
# print("\nDeterministic Result:")
# print(f"Concentration (C): {C:.2f} mg/m3")

# --- Monte Carlo Simulation ---

def monte_carlo_simulation(func, params, distributions, iterations=10000):
    """
    Performs a Monte Carlo simulation.

    Args:
      func: The function to evaluate (e.g., well_mixed_room)
      params: A dictionary of parameter names and their base values
      distributions: A dictionary of parameter names and their distributions
                     (e.g., {'G': stats.norm(loc=10, scale=2)})
      iterations: The number of iterations

    Returns:
      results: An array of simulation results
    """
    results = []
    results_dict = {}
    iteration = 1
    for _ in range(iterations):
        # Generate random values for each parameter based on the specified distribution
        param_values = {
            param: dist.rvs() for param, dist in distributions.items()
        }
        # Evaluate the function (e.g., well_mixed_room) with the random parameters
        result = func(**{**params, **param_values})
        results.append(result)
        results_dict['iteration'] = iteration
        results_dict['concentration']  = result
        iteration += 1

    return np.array(results), results_dict

# Example usage (modify distributions as needed)
# params = {'Q': Q, 'V': V}  # Use input values for Q and V
# distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
# results, results_dict = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)

# --- Analyze and Output Monte Carlo Results ---

# print("\nMonte Carlo Simulation Results:")
# print(f"Mean Concentration: {np.mean(results):.2f} mg/m3")
# print(f"Standard Deviation: {np.std(results):.2f} mg/m3")
# print(f"95th Percentile: {np.percentile(results, 95):.2f} mg/m3")
#
# # Tabular output of the simulated concentrations using pandas
# df = pd.DataFrame({'Concentration': results})
# print("\nSimulated Concentrations:")
# print(df.head())  # Print the first few rows
# ... (You can print the entire DataFrame or save it to a file)

# --- Bayesian Statistics ---

# Example using PyMC3 (modify the model and priors as needed)
# with pm.Model() as model:
#     # Priors for the parameters (example: normal priors)
#     G_prior = pm.Normal("G", mu=G, sigma=2)  # Prior for G
#     Q_prior = pm.Normal("Q", mu=Q, sigma=1)  # Prior for Q
#
#     # Likelihood (assuming normal distribution of the concentration)
#     C_obs = pm.Normal("C_obs", mu=G_prior / Q_prior, sigma=1, observed=C)
#
#     # Inference (using MCMC sampling)
#     trace = pm.sample(2000, tune=1000)
#
# # Analyze the posterior distributions
# print("\nBayesian Analysis Results:")
# pm.summary(trace)

def update_g(attr, old, new):
    G = float(new)
    params = {'Q': Q, 'V': V}  # Use input values for Q and V
    distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
    results, results_dict = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)
    update_table(results)

def update_q(attr, old, new):
    Q = float(new)
    params = {'Q': Q, 'V': V}  # Use input values for Q and V
    distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
    results, results_dict = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)
    update_table(results)

def update_v(attr, old, new):
    V = float(new)
    params = {'Q': Q, 'V': V}  # Use input values for Q and V
    distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
    results, results_dict = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)
    update_table(results)

def update_i(attr, old, new):
    iterations = int(new)
    params = {'Q': Q, 'V': V}  # Use input values for Q and V
    distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
    results, results_dict = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)
    #print(f'results: {results}; \n results_dict: {results_dict}')
    update_table(results)


def update_table(new_results):
    df = pd.DataFrame({'Concentration': new_results})
    columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns]
    #print(f'df.head():\n {df.head()}')
    #print(f'ColumnDataSource(df): \n{ColumnDataSource(df)}')
    data_table = DataTable(columns=columns, source=ColumnDataSource(df), width=400, height=280)
    create_curdoc(data_table)


def create_curdoc(data_table):
    curdoc().clear()
    g_slider.value = G
    q_slider.value = Q
    v_slider.value = V
    i_slider.value = iterations
    curdoc().add_root(column(g_slider, q_slider, v_slider, i_slider, data_table))


# Define Data Table
# columns = [TableColumn(field="iteration", title="Iteration"),
#            TableColumn(field="concentration", title="Concentration")]

G = float(1)
Q = float(1)
V = float(1)
iterations = 1
params = {'Q': Q, 'V': V}  # Use input values for Q and V
distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
results, results_dict = monte_carlo_simulation(well_mixed_room, params, distributions, 1)
df = pd.DataFrame({'Concentration': results})
columns = [TableColumn(field=Ci, title=Ci) for Ci in df.columns] # bokeh columns
data_table = DataTable(columns=columns, source=ColumnDataSource(df), width=400, height=280) # bokeh table

# Change events
g_slider.on_change('value', update_g)
q_slider.on_change('value', update_q)
v_slider.on_change('value', update_v)
i_slider.on_change('value', update_i)

#Setting up what to display
curdoc().add_root(column(g_slider, q_slider, v_slider, i_slider, data_table))


# --- Further analysis of the posterior distributions ---


# Calculate credible intervals
# G_ci = pm.stats.hdi(trace['G'])
# Q_ci = pm.stats.hdi(trace['Q'])
# print(f"95% Credible Interval for G: {G_ci}")
# print(f"95% Credible Interval for Q: {Q_ci}")
