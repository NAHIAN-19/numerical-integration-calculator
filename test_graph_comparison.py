"""
Test script for graph comparison and JSON file functionality
"""

import json
import numpy as np
import sympy as sp
from sympy import symbols, sin, cos, exp, pi

def test_json_functionality():
    """Test JSON save/load functionality"""
    
    print("Testing JSON functionality...")
    print("-" * 50)
    
    # Sample data
    sample_data = {
        "function": "sin(x)",
        "lower_limit": "0",
        "upper_limit": "pi",
        "intervals": "6",
        "method": "Trapezoidal"
    }
    
    # Test saving
    try:
        with open("test_config.json", 'w') as f:
            json.dump(sample_data, f, indent=2)
        print("✓ JSON save successful")
    except Exception as e:
        print(f"✗ JSON save failed: {e}")
    
    # Test loading
    try:
        with open("test_config.json", 'r') as f:
            loaded_data = json.load(f)
        print("✓ JSON load successful")
        print(f"  Loaded function: {loaded_data['function']}")
        print(f"  Loaded limits: {loaded_data['lower_limit']} to {loaded_data['upper_limit']}")
        print(f"  Loaded intervals: {loaded_data['intervals']}")
        print(f"  Loaded method: {loaded_data['method']}")
    except Exception as e:
        print(f"✗ JSON load failed: {e}")
    
    print("-" * 50)

def test_graph_comparison():
    """Test graph comparison functionality"""
    
    print("\nTesting Graph Comparison...")
    print("-" * 50)
    
    # Test function: f(x) = x^2 from 0 to 1
    x = symbols('x')
    f_expr = x**2
    f = sp.lambdify(x, f_expr, modules=['numpy'])
    
    a, b = 0, 1
    n = 10
    
    print(f"Function: f(x) = {f_expr}")
    print(f"Limits: {a} to {b}")
    print(f"Intervals: {n}")
    
    # Generate points for different methods
    methods_data = {}
    
    # Trapezoidal points
    h = (b - a) / n
    x_trap = np.linspace(a, b, n + 1)
    y_trap = f(x_trap)
    methods_data["Trapezoidal"] = {"x": x_trap, "y": y_trap}
    
    # Simpson's 1/3 points
    n_13 = n if n % 2 == 0 else n + 1
    h_13 = (b - a) / n_13
    x_13 = np.linspace(a, b, n_13 + 1)
    y_13 = f(x_13)
    methods_data["Simpson's 1/3"] = {"x": x_13, "y": y_13}
    
    # Simpson's 3/8 points
    n_38 = n if n % 3 == 0 else ((n // 3) + 1) * 3
    h_38 = (b - a) / n_38
    x_38 = np.linspace(a, b, n_38 + 1)
    y_38 = f(x_38)
    methods_data["Simpson's 3/8"] = {"x": x_38, "y": y_38}
    
    print("\nIntegration points for each method:")
    for method, data in methods_data.items():
        print(f"{method}: {len(data['x'])} points")
        print(f"  x range: {data['x'][0]:.3f} to {data['x'][-1]:.3f}")
        print(f"  y range: {min(data['y']):.3f} to {max(data['y']):.3f}")
    
    print("-" * 50)
    print("Graph comparison test completed!")

def test_sample_configs():
    """Test the sample configuration files"""
    
    print("\nTesting Sample Configurations...")
    print("-" * 50)
    
    sample_files = ["sample_config.json", "sample_config2.json"]
    
    for filename in sample_files:
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            print(f"✓ Loaded {filename}:")
            print(f"  Function: {data['function']}")
            print(f"  Limits: {data['lower_limit']} to {data['upper_limit']}")
            print(f"  Intervals: {data['intervals']}")
            print(f"  Method: {data['method']}")
            
        except Exception as e:
            print(f"✗ Failed to load {filename}: {e}")
    
    print("-" * 50)

if __name__ == "__main__":
    test_json_functionality()
    test_graph_comparison()
    test_sample_configs() 