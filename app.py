from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.graph_generator import generate_graphical_plot
from utils.numerical_methods import bisection_method, iterative_matrix_inverse
from utils.errors_calculations import calculate_absolute_error
import sympy as sp

app = Flask(__name__)
CORS(app)

def evaluate_function(function_str):
    x = sp.Symbol('x')
    expr = sp.sympify(function_str)
    return sp.lambdify(x, expr, "numpy")

@app.route('/')
def index():
    return "Server is working..."

@app.route("/plot_graph", methods=["POST"])
def plot_graph():
    data = request.json
    func_str = data.get("function")
    f = evaluate_function(func_str)
    range_x = data.get("range_x").split()
    return generate_graphical_plot(f, func_str, range_x)

@app.route("/calculate-bisection", methods=["POST"])
def calculate_bisection():
    data = request.json

    try:
        f = evaluate_function(data.get("function"))
        init_guess1 = float(data.get("initial_guess_1"))
        init_guess2 = float(data.get("initial_guess_2"))
        tol = float(data.get("tolerance"))

        root = bisection_method(f, init_guess1, init_guess2, tol)

        if root is None:
            return jsonify({"error": "Bisection method failed. Check initial guesses."}), 400
        
        return jsonify({"true_root": root})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calculate-absolute-error', methods=['POST'])
def calculate_abs_error():
    data = request.json

    if not data or "true_root" not in data:
        return jsonify({"error": "Missing true_root in request"}), 400
    
    try:
        true_root = float(data.get("true_root"))
        approximate_root = float(data.get("approximate_root"))
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid data: {str(e)}"}), 400

    abs_error = calculate_absolute_error(true_root, approximate_root)
    return jsonify({"absolute_error": abs_error})

@app.route('/invert-matrix', methods=['POST'])
def invert_matrix():
    data = request.get_json()
    if "matrix" not in data or not isinstance(data["matrix"], list):
        return jsonify({"error": "Invalid input"}), 400

    inverse, error = iterative_matrix_inverse(data["matrix"])
    if error:
        return jsonify({"error": error}), 400

    return jsonify({"inverse_matrix": inverse})

if __name__ == '__main__':
    app.run(debug=True)