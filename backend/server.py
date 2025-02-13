from flask import Flask, send_file
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

def f(x):
    return x**3 - 4*x + 1

@app.route('/task1')
def plot():
    # Генерация графика
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

    # Сохранение графика в буфер
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
