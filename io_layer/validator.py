def validate_params(a: float, b: float, n: int) -> None:
    """
    Ensure:
        - a < b
        - n >= 1 and integer
    Raises:
        ValueError on violation
    """
    if a >= b:
        raise ValueError(f"Lower bound 'a' must be less than upper bound 'b' (got a={a}, b={b})")

    if not isinstance(n, int):
        raise ValueError(f"'n' must be an integer (got type {type(n).__name__})")
    if n < 1:
        raise ValueError(f"'n' must be a positive integer (got n={n})")
