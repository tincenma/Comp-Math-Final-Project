from flask import jsonify
import matplotlib.pyplot as plt
import numpy as np
import io, base64

def generate_graphical_plot(f, func_str, x_range):
    
    try:
        x_min, x_max = map(float, x_range)

        # Generating x values
        x = np.linspace(x_min, x_max, 500)
        y = f(x)

        # Plot
        plt.figure(figsize=(4, 5))
        plt.plot(x, y, label=f"f(x) = {func_str}")
        plt.axhline(0, color='red', linestyle='--', label="y = 0")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Graphical Method")
        plt.legend()
        plt.grid()

        # Save image as base64
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        
        return jsonify({"image": base64.b64encode(img.getvalue()).decode()})

    except Exception as e:
        return jsonify({"error": str(e)})
