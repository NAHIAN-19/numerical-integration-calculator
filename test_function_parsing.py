"""
Test script to verify function parsing works with trigonometric functions
"""

import sympy as sp
from sympy import symbols, sin, cos, log, exp, pi

def test_function_parsing():
    """Test the function parsing with various functions"""
    
    x = symbols('x')
    
    # Test cases
    test_cases = [
        ("sin(x)", "sine function"),
        ("cos(x)", "cosine function"),
        ("exp(x)", "exponential function"),
        ("log(x)", "logarithm function"),
        ("x**2", "quadratic function"),
        ("pi*x", "pi times x"),
        ("sin(x) + cos(x)", "sum of sine and cosine")
    ]
    
    print("Testing function parsing...")
    print("-" * 50)
    
    for func_str, description in test_cases:
        try:
            # Create a local namespace with mathematical functions
            local_dict = {
                'sin': sp.sin,
                'cos': sp.cos,
                'log': sp.log,
                'exp': sp.exp,
                'pi': sp.pi,
                'x': x
            }
            
            # Create the expression using the local dictionary
            expr = sp.sympify(func_str, locals=local_dict)
            f = sp.lambdify(x, expr, modules=['numpy'])
            
            # Test the function
            test_x = 1.0
            result = f(test_x)
            
            print(f"✓ {func_str} ({description}): f({test_x}) = {result:.6f}")
            
        except Exception as e:
            print(f"✗ {func_str} ({description}): ERROR - {e}")
    
    print("-" * 50)
    print("Test completed!")

def test_limit_parsing():
    """Test the limit parsing with constants"""
    
    print("\nTesting limit parsing...")
    print("-" * 50)
    
    test_limits = [
        ("0", "1", "simple numbers"),
        ("pi", "2*pi", "with pi constant"),
        ("0", "pi", "0 to pi"),
        ("-pi/2", "pi/2", "negative to positive")
    ]
    
    for a_str, b_str, description in test_limits:
        try:
            # Create a local namespace with mathematical constants
            local_dict = {
                'pi': sp.pi,
                'e': sp.E
            }
            
            a = float(sp.sympify(a_str, locals=local_dict))
            b = float(sp.sympify(b_str, locals=local_dict))
            
            print(f"✓ {a_str} to {b_str} ({description}): a={a:.6f}, b={b:.6f}")
            
        except Exception as e:
            print(f"✗ {a_str} to {b_str} ({description}): ERROR - {e}")
    
    print("-" * 50)
    print("Limit parsing test completed!")

if __name__ == "__main__":
    test_function_parsing()
    test_limit_parsing() 