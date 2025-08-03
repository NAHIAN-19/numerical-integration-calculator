import pytest
import math
from io_.parser import parse_input
from io_.validator import validate_params

def test_validate_params_valid():
    # Should not raise
    validate_params(0, 1, 4)

@pytest.mark.parametrize("a,b,n", [
    (1, 0, 5),     # a >= b
    (0, 1, 0),     # n < 1
    (0, 1, -3),    # n negative
    (0, 1, 2.5),   # n not integer
])
def test_validate_params_invalid(a, b, n):
    with pytest.raises(ValueError):
        validate_params(a, b, n)

def test_parse_input_from_dict_polynomial():
    spec = {"function": "x**2", "a": 0, "b": 2, "n": 4}
    f, a, b, n = parse_input(spec)
    assert a == 0.0
    assert b == 2.0
    assert n == 4
    assert math.isclose(f(1), 1.0, rel_tol=1e-9)

def test_parse_input_from_dict_transcendental():
    spec = {"function": "sin(x) + exp(x)", "a": 0, "b": 1, "n": 10}
    f, a, b, n = parse_input(spec)
    assert math.isclose(f(0), 1.0, rel_tol=1e-9)  # sin(0) + exp(0) = 1
    val = f(1)  # Check it runs without error
    assert isinstance(val, float)