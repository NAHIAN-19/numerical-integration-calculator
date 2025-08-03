import json
import sympy as sp
from io_.validator import validate_params
from typing import Callable, Tuple, Union, Dict, Any

_ALLOWED_FUNCS = {
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'exp': sp.exp,
    'log': sp.log,
    'sqrt': sp.sqrt,
}

def parse_input(spec: Union[str, Dict[str, Any]]) -> Tuple[Callable[[float], float], float, float, int]:
    """
    Parses either:
        - A JSON file path string, or
        - A dict with keys: "function", "a", "b", "n"

    Returns:
        f (callable): f(x), supporting transcendental funcs
        a (float): lower bound
        b (float): upper bound
        n (int): number of subintervals
    """
    # Load JSON if path given
    if isinstance(spec, str):
        with open(spec, 'r') as f:
            data = json.load(f)
    else:
        data = spec

    # Check required keys
    required_keys = {"function", "a", "b", "n"}
    if not required_keys.issubset(data.keys()):
        missing = required_keys - data.keys()
        raise ValueError(f"Missing required input fields: {', '.join(missing)}")

    # Extract and validate parameters
    func_str = str(data["function"]).strip()
    a = float(data["a"])
    b = float(data["b"])
    n = int(data["n"])
    validate_params(a, b, n)

    # Parse and compile the function
    x = sp.symbols('x')
    try:
        expr = sp.sympify(func_str, locals=_ALLOWED_FUNCS)
    except sp.SympifyError as e:
        raise ValueError(f"Invalid function expression: {func_str}") from e

    f_callable = sp.lambdify(x, expr, modules=["math"])
    return f_callable, a, b, n
