import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 4*x + 1

# Plotting a graph
x = np.linspace(0, 3, 500)  # Range of x values
y = f(x)

plt.figure(figsize=(6, 7))
plt.plot(x, y, label="f(x) = x^3 - 4x + 1")
plt.axhline(0, color='red', linestyle='--', label="y = 0")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Graphical method")
plt.legend()
plt.grid()
plt.show()