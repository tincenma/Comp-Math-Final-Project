import cmath


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