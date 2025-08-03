"""
Test script for enhanced features: error analysis and method comparison
"""

import numpy as np
import sympy as sp
from sympy import symbols, sin, cos, exp, pi

def test_error_analysis():
    """Test error analysis with a simple function"""
    
    # Test function: f(x) = x^2 from 0 to 1
    # Exact result: ∫x^2 dx from 0 to 1 = 1/3 ≈ 0.333333
    
    x = symbols('x')
    f_expr = x**2
    f = sp.lambdify(x, f_expr, modules=['numpy'])
    
    a, b = 0, 1
    n = 10
    
    print("Testing Error Analysis for f(x) = x^2 from 0 to 1")
    print(f"Exact result: 1/3 ≈ 0.333333")
    print("-" * 50)
    
    # Calculate exact value
    exact_integral = sp.integrate(f_expr, (x, a, b))
    exact_result = float(exact_integral)
    print(f"Exact Value: {exact_result:.8f}")
    
    # Test trapezoidal rule
    h = (b - a) / n
    x_points = np.linspace(a, b, n + 1)
    y_points = f(x_points)
    trapezoidal_result = h * (0.5 * y_points[0] + 0.5 * y_points[-1] + np.sum(y_points[1:-1]))
    
    # Calculate errors
    absolute_error = abs(trapezoidal_result - exact_result)
    relative_error = (absolute_error / abs(exact_result)) * 100
    
    print(f"Trapezoidal Rule: {trapezoidal_result:.8f}")
    print(f"Absolute Error: {absolute_error:.8f}")
    print(f"Relative Error: {relative_error:.4f}%")
    
    print("-" * 50)
    print("Error analysis test completed!")

def test_method_comparison():
    """Test method comparison"""
    
    # Test function: f(x) = sin(x) from 0 to pi
    # Exact result: ∫sin(x) dx from 0 to pi = 2
    
    x = symbols('x')
    f_expr = sp.sin(x)
    f = sp.lambdify(x, f_expr, modules=['numpy'])
    
    a, b = 0, float(sp.pi)
    n = 6
    
    print("\nTesting Method Comparison for f(x) = sin(x) from 0 to pi")
    print(f"Exact result: 2")
    print("-" * 50)
    
    # Calculate exact value
    exact_integral = sp.integrate(f_expr, (x, a, b))
    exact_result = float(exact_integral)
    print(f"Exact Value: {exact_result:.8f}")
    
    results = {}
    
    # Test Trapezoidal Rule
    h = (b - a) / n
    x_points = np.linspace(a, b, n + 1)
    y_points = f(x_points)
    trapezoidal_result = h * (0.5 * y_points[0] + 0.5 * y_points[-1] + np.sum(y_points[1:-1]))
    results["Trapezoidal"] = trapezoidal_result
    
    # Test Simpson's 1/3 Rule
    n_13 = n if n % 2 == 0 else n + 1
    h_13 = (b - a) / n_13
    x_13 = np.linspace(a, b, n_13 + 1)
    y_13 = f(x_13)
    simpson_13_result = h_13/3 * (y_13[0] + 4*np.sum(y_13[1:-1:2]) + 2*np.sum(y_13[2:-1:2]) + y_13[-1])
    results["Simpson's 1/3"] = simpson_13_result
    
    # Test Simpson's 3/8 Rule
    n_38 = n if n % 3 == 0 else ((n // 3) + 1) * 3
    h_38 = (b - a) / n_38
    x_38 = np.linspace(a, b, n_38 + 1)
    y_38 = f(x_38)
    simpson_38_result = 3*h_38/8 * (y_38[0] + 3*np.sum(y_38[1:-1:3]) + 3*np.sum(y_38[2:-1:3]) + 2*np.sum(y_38[3:-1:3]) + y_38[-1])
    results["Simpson's 3/8"] = simpson_38_result
    
    # Display results
    print(f"{'Method':<15} {'Result':<15} {'Absolute Error':<15}")
    print("-" * 45)
    for method, result in results.items():
        error = abs(result - exact_result)
        print(f"{method:<15} {result:<15.8f} {error:<15.8f}")
    
    # Find best method
    best_method = min(results.keys(), key=lambda x: abs(results[x] - exact_result))
    print(f"\nBest Method: {best_method}")
    print(f"Best Error: {abs(results[best_method] - exact_result):.8f}")
    
    print("-" * 50)
    print("Method comparison test completed!")

if __name__ == "__main__":
    test_error_analysis()
    test_method_comparison() 