import matplotlib.pyplot as plt
import numpy as np
import io

def generate_graphical_plot(function_str, x_range):
    def f(x):
        return eval(function_str)

    x_min, x_max = map(float, x_range.split())
    x = np.linspace(x_min, x_max, 500)
    y = f(x)

    plt.figure(figsize=(5, 6))
    plt.plot(x, y, label=f"f(x) = {function_str}")
    plt.axhline(0, color='red', linestyle='--', label="y = 0")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Graphical Method")
    plt.legend()
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return img
