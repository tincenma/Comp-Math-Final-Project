def bisection_method(f, a, b, tol):
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

# Definition of a function
def f(x):
    return x**3 - 4*x - 9

# Using bisection method
root = bisection_method(f, 2, 3, 1e-6)
print(f"Approximate root: {root}")