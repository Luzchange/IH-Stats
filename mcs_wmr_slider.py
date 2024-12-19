#!/home/kkiragu/.venv/imagesearch/bin/python3

import pymc as pm
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import display, clear_output

# --- Input Parameters ---
# Well-Mixed Room Model
G = float(input("Enter Emission Rate (G) (mg/min): "))
Q = float(input("Enter Ventilation Rate (Q) (m3/min): "))
V = float(input("Enter Room Volume (V) (m3): "))

# --- Calculations ---
# Well-Mixed Room Model
def well_mixed_room(G, Q, V):
    C = G / Q
    return C

# --- Monte Carlo Simulation ---
def monte_carlo_simulation(func, params, distributions, iterations=10000):
    results = []
    for _ in range(iterations):
        param_values = {param: dist.rvs() for param, dist in distributions.items()}
        result = func(**{**params, **param_values})
        results.append(result)
    return np.array(results)

# --- Interactive Widget ---
def update_output(iterations):
    clear_output(wait=True)

    params = {'Q': Q, 'V': V}
    distributions = {'G': stats.norm(loc=G, scale=2)}
    results = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)

    # --- Analyze and Output Monte Carlo Results ---
    print("\nMonte Carlo Simulation Results:")
    print(f"Mean Concentration: {np.mean(results):.2f} mg/m3")
    print(f"Standard Deviation: {np.std(results):.2f} mg/m3")
    print(f"95th Percentile: {np.percentile(results, 95):.2f} mg/m3")

# Create slider widget
iterations_slider = widgets.IntSlider(
    value=1000,
    min=100,
    max=10000,
    step=100,
    description='Iterations:',
    continuous_update=False,
)

# Link slider to update_output function
widgets.interactive(update_output, iterations=iterations_slider)

# Display the interactive plot
display(iterations_slider)
