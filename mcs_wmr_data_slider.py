#!/home/kkiragu/.venv/imagesearch/bin/python3

import pandas as pd
from scipy import stats
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import Slider, ColumnDataSource, DataTable, TableColumn

## Initial Values
G = float(1)
Q = float(1)
V = float(1)
iterations = 1

## Sliders
g_slider = Slider(title='Emission Rate (G) (mg/min)', value=G, start=1, end=1000, step=1)
q_slider = Slider(title='Ventilation Rate (Q) (m3/min)', value=Q, start=1, end=1000, step=1)
v_slider = Slider(title='Emission Room Volume (V) (m3)', value=V, start=1, end=1000, step=1)
i_slider = Slider(title='Iterations for Monte Carlo', value=iterations, start=1, end=1000, step=1)

data = dict(concentrations = list(range(0, 1)))
source = ColumnDataSource(data)

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
    for _ in range(iterations):
        # Generate random values for each parameter based on the specified distribution
        param_values = {
            param: dist.rvs() for param, dist in distributions.items()
        }
        # Evaluate the function (e.g., well_mixed_room) with the random parameters
        result = func(**{**params, **param_values})
        results.append(result)

    return np.array(results)

def update_data(attrname, old, new):

    # Get the current slider values
    G = g_slider.value
    Q = q_slider.value
    V = v_slider.value
    iterations = i_slider.value

    # Generate the new curve
    params = {'Q': Q, 'V': V}  # Use input values for Q and V
    distributions = {'G': stats.norm(loc=G, scale=2)}  # Example: G follows a normal distribution
    results  = monte_carlo_simulation(well_mixed_room, params, distributions, iterations)

    data = dict(concentrations = results)

    source.data = dict(data)

for w in [g_slider, q_slider, v_slider, i_slider]:
    w.on_change('value', update_data)

columns = [TableColumn(field="concentrations", title="Concentrations")]
data_table = DataTable(columns=columns, source=source, width=400, height=280) # bokeh table

#Setting up what to display
inputs = column(g_slider, q_slider, v_slider, i_slider)
curdoc().add_root(column(inputs, data_table))
curdoc().title = "Monte Carlo Simulation for Well-Mixed Room Model"
