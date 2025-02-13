import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 4*x + 1

# Plotting a graph
x = np.linspace(0, 3, 500)  # Range of x values
y = f(x)
