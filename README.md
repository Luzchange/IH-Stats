# IH-Stats
Bayesian Thinking in Exposure Assessment

# Monte Carlo Simulation for Well-Mixed Room Model

This code performs a Monte Carlo simulation to estimate the concentration of a chemical in a well-mixed room, considering the uncertainty in the emission rate. 

## Functionality

The code implements the following:

1. **Well-Mixed Room Model:** It uses a simple well-mixed room model to calculate the steady-state concentration of a chemical based on emission rate (G), ventilation rate (Q), and room volume (V).

2. **Monte Carlo Simulation:** It runs a Monte Carlo simulation to account for uncertainty in the emission rate. The emission rate is assumed to follow a normal distribution. The simulation generates multiple random samples of the emission rate and calculates the corresponding concentrations.

3. **Interactive Widget:** It provides an interactive slider to control the number of iterations in the Monte Carlo simulation. The calculated statistics (mean, standard deviation, 95th percentile) are dynamically updated based on the selected number of iterations.

## Usage

1. **Input Parameters:** You need to provide the following input parameters:
   - Emission Rate (G) (mg/min)
   - Ventilation Rate (Q) (m3/min)
   - Room Volume (V) (m3)

2. **Interactive Slider:** Use the slider to adjust the number of iterations for the Monte Carlo simulation. The output statistics will update automatically.

3. **Output:** The code displays the following results:
   - Mean Concentration (mg/m3)
   - Standard Deviation (mg/m3)
   - 95th Percentile (mg/m3)

## Requirements

- Python 3
- Libraries: `pymc3`, `pandas`, `scipy`, `numpy`, `matplotlib`, `ipywidgets`

To install the required libraries, run in `Bash` (Linux users) or `Git Bash` (Windows users):

```
pip install pymc3 pandas scipy numpy matplotlib ipywidgets
```

## Execution on Command Line

### Python Virtual Environments
If you are using a Python Virtual Environment. You will need to update the shebang statement to point to the path of your virtual environment installation. It will look as follows:

```
#!/home/XXXXX/.venv/imagesearch/bin/python3
```

Where the `XXXXX` will likely be your username. You can navigate (eg `cd ~/.venv/imagesearch/bin/`) to where your venv is installed and use `pwd` to get the full path

If you would like to install a Python Virtual environment:
```commandline
python3 -m venv ~/.venv/imagesearch
```


Load the venv:
```commandline
source ~/.venv/imagesearch/bin/activate`
```

### Execution

Ensure the scripts are executable:
```commandline
chmod +x mcs_wmr*.py
```

To execute the Python scripts:
```commandline
./mcs_wmr_slider.py
```

OR

```commandline
./mcs_wmr_slider.py
```

## Example

After providing the inputs, an interactive slider will appear. Adjust the slider to change the number of iterations, and the calculated statistics will update accordingly.


## Note

- The code assumes a normal distribution for the emission rate. You can modify the distribution if needed.
- The well-mixed room model is a simplified representation of real-world scenarios. More complex models might be necessary for accurate predictions in certain cases.
