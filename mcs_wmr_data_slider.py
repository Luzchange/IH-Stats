#!/home/kkiragu/.venv/imagesearch/bin/python3

import pandas as pd
from scipy import stats
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Slider, ColumnDataSource, DataTable, TableColumn

## Initial Values
G = float(1)
Q = float(1)
V = float(1)
iterations = 1

## Sliders
g_slider = Slider(title='Emission Rate (G) (mg/min)',value=G,start=1,end=1000)
q_slider = Slider(title='Ventilation Rate (Q) (m3/min)',value=Q,start=1,end=1000)
v_slider = Slider(title='Emission Room Volume (V) (m3)',value=V,start=1,end=1000)
i_slider = Slider(title='Iterations for Monte Carlo',value=iterations,start=1,end=1000)

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
    # g_slider.value = G
    # q_slider.value = Q
    # v_slider.value = V
    # i_slider.value = iterations
    curdoc().add_root(column(g_slider, q_slider, v_slider, i_slider, data_table))


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
