"""
Simple test script for the numerical integration calculator
"""

import numpy as np
import sympy as sp
from sympy import symbols, sin, cos, exp, pi

def test_integration_methods():
    """Test the integration methods with a simple function"""
    
    # Test function: f(x) = x^2 from 0 to 1
    # Exact result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.333333
    
    x = symbols('x')
    f_expr = x**2
    f = sp.lambdify(x, f_expr, modules=['numpy'])
    
    a, b = 0, 1
    n = 10
    
    print("Testing integration methods for f(x) = x^2 from 0 to 1")
    print(f"Exact result: 1/3 ≈ 0.333333")
    print("-" * 50)
    
    # Test trapezoidal rule
    h = (b - a) / n
    x_points = np.linspace(a, b, n + 1)
    y_points = f(x_points)
    trapezoidal_result = h * (0.5 * y_points[0] + 0.5 * y_points[-1] + np.sum(y_points[1:-1]))
    print(f"Trapezoidal Rule: {trapezoidal_result:.6f}")
    
    # Test Simpson's 1/3 rule
    if n % 2 == 0:
        simpson_13_result = h/3 * (y_points[0] + 4*np.sum(y_points[1:-1:2]) + 2*np.sum(y_points[2:-1:2]) + y_points[-1])
        print(f"Simpson's 1/3 Rule: {simpson_13_result:.6f}")
    else:
        print("Simpson's 1/3 Rule: n must be even")
    
    # Test Simpson's 3/8 rule
    if n % 3 == 0:
        simpson_38_result = 3*h/8 * (y_points[0] + 3*np.sum(y_points[1:-1:3]) + 3*np.sum(y_points[2:-1:3]) + 2*np.sum(y_points[3:-1:3]) + y_points[-1])
        print(f"Simpson's 3/8 Rule: {simpson_38_result:.6f}")
    else:
        print("Simpson's 3/8 Rule: n must be divisible by 3")
    
    print("-" * 50)
    print("Test completed successfully!")

if __name__ == "__main__":
    test_integration_methods() 