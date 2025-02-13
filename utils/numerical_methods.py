import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import io, cmath

def evaluate_function(function_str, x):
    # Evaluates the given function string safely.
    try:
        return eval(function_str, {"x": x, "np": np, "cmath": cmath})
    except Exception as e:
        print(f"Error evaluating function: {e}")
        return None

def compute_derivative(function_str):
    # Computes the symbolic derivative of a function and returns a callable function.
    try:
        x = sp.Symbol('x')
        derivative = sp.diff(sp.sympify(function_str), x)
        return sp.lambdify(x, derivative, 'numpy')
    except Exception as e:
        print(f"Error computing derivative: {e}")
        return None

def generate_graph(function_str, x_min, x_max, root, method):
    # Generates a plot of the function with the found root.
    x = np.linspace(x_min, x_max, 500)
    y = np.array([evaluate_function(function_str, xi) for xi in x])

    plt.figure(figsize=(6, 5))
    plt.plot(x, y, label=f"f(x) = {function_str}")
    plt.axhline(0, color='red', linestyle='--', label="y = 0")
    
    if root is not None:
        plt.scatter(root, 0, color='blue', zorder=3, label="Root Found")

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(f"Numerical Method: {method.capitalize()}")
    plt.legend()
    plt.grid()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

# Root Finding Method

def find_root(function_str, x_range, method, df_str=None):
    # Selects and applies the appropriate numerical method.
    def f(x): return evaluate_function(function_str, x)
    df = compute_derivative(function_str)

    x_values = list(map(float, x_range.split()))

    if len(x_values) < 2:
        print("Invalid range. Please provide two values.")
        return None, None

    x_min, x_max = x_values[0], x_values[1]

    # Choose method dynamically
    if method == "bisection":
        root = bisection_method(f, x_min, x_max)
    elif method == "newton_raphson":
        if not df:
            print("Could not compute derivative for Newton-Raphson method.")
            return None, None
        root = newton_raphson_method(f, df, x_min)
    elif method == "secant":
        root = secant_method(f, x_min, x_max)
    elif method == "fixed_point_iteration":
        root = fixed_point_iteration(f, x_min)
    elif method == "false_position":
        root = false_position_method(f, x_min, x_max)
    elif method == "muller":
        root = muller_method(f, x_min, x_max, x_max + 1)
    else:
        print("Invalid method selected.")
        return None, None

    graph_img = generate_graph(function_str, x_min, x_max, root, method)
    return root, graph_img

# Numerical Methods Functions

def bisection_method(f, a, b, tol=1e-6):
    if f(a) * f(b) >= 0:
        print("Invalid initial values. f(a) and f(b) must be of different signs.")
        return None

    midpoint = (a + b) / 2 
    while abs(f(midpoint)) > tol:
        if f(a) * f(midpoint) < 0: 
            b = midpoint 
        else:
            a = midpoint 
        midpoint = (a + b) / 2 
    return midpoint

def newton_raphson_method(f, df, x0, tol=1e-6):
    x = x0
    while abs(f(x)) > tol:
        x = x - f(x) / df(x)
    return x

def secant_method(f, x0, x1, tol=1e-6):
    while abs(f(x1)) > tol:
        x_temp = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
        x0, x1 = x1, x_temp
    return x1

def fixed_point_iteration(g, x0, tol=1e-6, max_iter=100):
    x = x0
    for i in range(max_iter):
        x_next = g(x)
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    print("The method did not converge within the specified number of iterations.")
    return None

def false_position_method(f, a, b, tol):
    # We check that the root really lies in the interval [a, b]
    if f(a) * f(b) >= 0:
        print("Invalid initial values. f(a) and f(b) must be of different signs.")
        return None

    c = a 
    while abs(f(c)) > tol:
        c = b - f(b) * (b - a) / (f(b) - f(a))  # Formula
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return c

def muller_method(f, x0, x1, x2, tol, max_iter=100):
    # Iterative root approximation by Muller's method
    for _ in range(max_iter):
        h0 = x1 - x0
        h1 = x2 - x1
        delta0 = (f(x1) - f(x0)) / h0
        delta1 = (f(x2) - f(x1)) / h1
        a = (delta1 - delta0) / (h1 + h0)
        b = a * h1 + delta1
        c = f(x2)

        discriminant = cmath.sqrt(b**2 - 4*a*c)
        if abs(b + discriminant) > abs(b - discriminant):
            denominator = b + discriminant
        else:
            denominator = b - discriminant

        x3 = x2 - (2 * c) / denominator  # Formula

        if abs(x3 - x2) < tol:  # Stop condition
            return x3
        x0, x1, x2 = x1, x2, x3

    print("The method did not converge within the specified number of iterations.")
    return None