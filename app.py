from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.graph_generator import generate_graphical_plot
from utils.numerical_methods import (
    bisection_method, secant_method, jacobi_method, iterative_matrix_inverse
)
from utils.approximations_and_errors import calculate_absolute_error, calculate_relative_error
from utils.interpolation import newton_forward_interpolation
from utils.numerical_integrations import trapezoidal_rule
import sympy as sp
import numpy as np

app = Flask(__name__)
CORS(app)

def evaluate_function(function_str):
    x = sp.Symbol('x')
    expr = sp.sympify(function_str)
    return sp.lambdify(x, expr, "numpy")

# --------------------- Task 1 ---------------------
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
        a = float(data.get("initial_guess_1"))
        b_val = float(data.get("initial_guess_2"))
        tol = float(data.get("tolerance"))
        
        root = bisection_method(f, a, b_val, tol)
        if root is None:
            return jsonify({"error": "Bisection method failed. Check initial guesses."}), 400
        
        return jsonify({"true_root": root})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/calculate-bisection", methods=["POST"])
def calculate_newton_raphson():
    data = request.json
    try:
        f = evaluate_function(data.get("function"))
        a = float(data.get("initial_guess_1"))
        b_val = float(data.get("initial_guess_2"))
        tol = float(data.get("tolerance"))
        
        root = bisection_method(f, a, b_val, tol)
        if root is None:
            return jsonify({"error": "Bisection method failed. Check initial guesses."}), 400
        return jsonify({"true_root": root})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calculate-absolute-error', methods=['POST'])
def calculate_abs_error():
    data = request.json

    try:
        true_root = float(data.get("true_root"))
        approx_root = float(data.get("approximate_root"))
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid data: {str(e)}"}), 400
    abs_error = calculate_absolute_error(true_root, approx_root)
    return jsonify({"absolute_error": abs_error})

# --------------------- Task 2: Comparison of Root-Finding Methods ---------------------
@app.route("/calculate-secant", methods=["POST"])
def calculate_secant():
    data = request.json
    try:
        f = evaluate_function(data.get("function"))
        x0 = float(data.get("initial_guess_1"))
        x1 = float(data.get("initial_guess_2"))
        tol = float(data.get("tolerance"))
        # Secant method from numerical_methods.py
        root_secant = secant_method(f, x0, x1, tol)
        return jsonify({"secant_root": root_secant})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/compare-root-finding", methods=["POST"])
def compare_root_finding():
    data = request.json
    try:
        f = evaluate_function(data.get("function"))
        a = float(data.get("initial_guess_1"))
        b_val = float(data.get("initial_guess_2"))
        x0_secant = a  # for secant method, you may choose appropriate values
        x1_secant = b_val
        tol = float(data.get("tolerance"))
        # Calculate roots and assume that your functions return iteration count if needed
        root_bisect, iter_bisect = bisection_method(f, a, b_val, tol, return_iterations=True)
        root_secant, iter_secant = secant_method(f, x0_secant, x1_secant, tol, return_iterations=True)
        rel_error_bisect = calculate_relative_error(root_bisect, float(data.get("approximate_root", root_bisect)))
        rel_error_secant = calculate_relative_error(root_secant, float(data.get("approximate_root", root_secant)))
        return jsonify({
            "bisection": {"root": root_bisect, "iterations": iter_bisect, "relative_error": rel_error_bisect},
            "secant": {"root": root_secant, "iterations": iter_secant, "relative_error": rel_error_secant}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Task 3: Jacobi Method ---------------------
@app.route("/solve-jacobi",methods=["POST"])
def solve_jacobi():
    data = request.json
    try:
        # Expecting matrix A and vector b in JSON (as lists)
        A = np.array(data.get("A"))
        b = np.array(data.get("b"))
        x0 = np.array(data.get("x0"))
        tol = float(data.get("tol", 1e-6))
        max_iter = int(data.get("max_iter", 100))
        solution = jacobi_method(A, b, x0, tol, max_iter)
        return jsonify({"solution": solution.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Task 4: Iterative Matrix Inversion ---------------------
@app.route("/iterative-matrix-inverse", methods=["POST"])
def inverse_matrix():
    data = request.json
    try:
        A = np.array(data.get("A"))
        tol = float(data.get("tol", 1e-6))
        max_iter = int(data.get("max_iter", 100))
        # Use your iterative_matrix_inverse function from numerical_methods.py
        A_inv = iterative_matrix_inverse(A, tol, max_iter)
        return jsonify({"inverse": A_inv.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Task 5: Linear Curve Fitting ---------------------
@app.route("/linear-curve-fit", methods=["POST"])
def curve_fit():
    data = request.json
    try:
        # Expecting data points x and y as lists
        x = np.array(data.get("x"))
        y = np.array(data.get("y"))
        # Use least squares (np.polyfit) for linear fit (degree=1)
        coefficients = np.polyfit(x, y, 1)
        m, c = coefficients
        # Optionally, generate fitted line points for plotting
        fitted_y = m * x + c
        return jsonify({"slope": m, "intercept": c, "fitted_y": fitted_y.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Task 6: Newton’s Forward Interpolation ---------------------
@app.route("/newton-forward-interpolation", methods=["POST"])
def newton_forward():
    data = request.json
    try:
        # Expecting x, y data points and a value to interpolate
        x = np.array(data.get("x"))
        y = np.array(data.get("y"))
        x_value = float(data.get("x_value"))
        interpolated_value = newton_forward_interpolation(x, y, x_value)
        return jsonify({"interpolated_value": interpolated_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Task 7: First Derivative Using Forward Difference ---------------------
@app.route("/first-derivative", methods=["POST"])
def first_derivative():
    data = request.json
    try:
        x = np.array(data.get("x"))
        y = np.array(data.get("y"))
        x_value = float(data.get("x_value"))
        derivative = newton_forward_interpolation(x, y, x_value)
        return jsonify({"derivative": derivative})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --------------------- Task 8: Trapezoidal Rule for Integration ---------------------
@app.route("/trapezoidal-rule", methods=["POST"])
def integrate_trapezoidal():
    data = request.json
    try:
        func_str = data.get("function")
        f = evaluate_function(func_str)
        a, b = map(float, data.get("interval").split())
        n = int(data.get("subintervals"))
        integral_value = trapezoidal_rule(f, a, b, n)
        return jsonify({"integral": integral_value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)