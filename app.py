from flask import Flask, request, jsonify, render_template, send_file
from utils.graph_generator import generate_graphical_plot
from utils.numerical_methods import find_root
from utils.errors_calculations import calculate_absolute_error
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graphical-method', methods=['POST'])
def graphical_method():
    data = request.json
    function_str = data.get("function")
    x_range = data.get("x_range")

    # Generate graph and return it
    img = generate_graphical_plot(function_str, x_range)
    return send_file(img, mimetype='image/png')

@app.route('/numerical-method', methods=['POST'])
def numerical_method():
    data = request.json
    function_str = data.get("function")
    x_range = data.get("x_range")
    method = data.get("method")

    root, img = find_root(function_str, x_range, method)
    return jsonify({"root": root, "image": img})

@app.route('/calculate-absolute-error', methods=['POST'])
def calculate_absolute_error():
    data = request.json
    user_root = float(data.get("user_root"))
    true_root = float(data.get("true_root"))

    abs_error = calculate_absolute_error(true_root, user_root)
    return jsonify({"absolute_error": abs_error})

if __name__ == '__main__':
    app.run(debug=True)