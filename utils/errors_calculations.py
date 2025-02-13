def calculate_absolute_error(true_value, approx_value):
    absolute_error = abs(true_value - approx_value)
    return absolute_error

def calculate_relative_error(true_value, approx_value):
    absolute_error = calculate_absolute_error(true_value, approx_value)
    relative_error = absolute_error / true_value if true_value != 0 else float('inf')
    return relative_error

def calculate_percentage_error(true_value, approx_value):
    absolute_error = calculate_absolute_error(true_value, approx_value)
    percentage_error = (absolute_error / true_value) * 100 if true_value != 0 else float('inf')
    return percentage_error