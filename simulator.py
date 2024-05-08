import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, RadioButtons

# Constants
cp = 4.186  # Specific heat capacity of water in kJ/kgK

def double_pipe_heat_exchanger(mh, mc, Thi, Tci, L, flow_type):
    """
    Simulate a double pipe heat exchanger.

    Parameters:
    mh : float - Mass flow rate of hot fluid in kg/s
    mc : float - Mass flow rate of cold fluid in kg/s
    Thi : float - Inlet temperature of hot fluid in °C
    Tci : float - Inlet temperature of cold fluid in °C
    L : float - Length of the heat exchanger in meters
    flow_type : str - 'counter' or 'parallel' flow

    Returns:
    x : numpy array - Position along the heat exchanger
    Th : numpy array - Temperature profile of hot fluid along the heat exchanger
    Tc : numpy array - Temperature profile of cold fluid along the heat exchanger
    """
    # Discretize the length of the heat exchanger
    x = np.linspace(0, L, 100)
    Th = np.zeros_like(x)
    Tc = np.zeros_like(x)
    
    # Calculate effectiveness of the heat exchanger
    U = 2000  # Overall heat transfer coefficient in W/m²K
    A = np.pi * 0.034  # Cross-sectional area of the outer tube in m²
    NTU = U * A * L / (mc * cp * 1000)
    C_min = min(mh, mc) * cp * 1000
    C_max = max(mh, mc) * cp * 1000
    effectiveness = (1 - np.exp(-NTU * (1 - C_min / C_max))) / (1 - C_min / C_max * np.exp(-NTU * (1 - C_min / C_max)))

    # Heat exchanged
    Q = effectiveness * C_min * (Thi - Tci)
    
    # Temperature profiles along the heat exchanger
    for i in range(len(x)):
        if flow_type == 'counter':
            Th[i] = Thi - Q / (mh * cp * 1000) * (x[i] / L)
            Tc[i] = Tci + Q / (mc * cp * 1000) * (x[i] / L)
        else:  # parallel flow
            Th[i] = Thi - Q / (mh * cp * 1000) * (x[i] / L)
            Tc[i] = Tci + Q / (mc * cp * 1000) * (x[i] / L)

    return x, Th, Tc

# Interactive plotting
def plot_heat_exchanger(mh, mc, Thi, Tci, flow_type):
    L = 1.2  # Length of the heat exchanger in meters
    x, Th, Tc = double_pipe_heat_exchanger(mh, mc, Thi, Tci, L, flow_type)
    
    plt.figure(figsize=(10, 5))
    plt.plot(x, Th, label='Hot Fluid Temp (°C)', color='red')
    plt.plot(x, Tc, label='Cold Fluid Temp (°C)', color='blue')
    plt.title(f"{flow_type.capitalize()} Flow Heat Exchanger Temperature Profile")
    plt.xlabel("Length of the Exchanger (m)")
    plt.ylabel("Temperature (°C)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Create interactive widgets
interact(plot_heat_exchanger,
         mh=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='Hot Flow Rate (kg/s)'),
         mc=FloatSlider(min=0.1, max=2.0, step=0.1, value=1.0, description='Cold Flow Rate (kg/s)'),
         Thi=FloatSlider(min=50, max=100, step=1, value=70, description='Hot Inlet Temp (°C)'),
         Tci=FloatSlider(min=10, max=50, step=1, value=20, description='Cold Inlet Temp (°C)'),
         flow_type=RadioButtons(options=['counter', 'parallel'], value='counter', description='Flow Type'))
