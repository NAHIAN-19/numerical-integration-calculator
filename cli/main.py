import argparse
import sys
from io_layer.parser import parse_input

def main():
    parser = argparse.ArgumentParser(description="Numerical Integration Calculator - IO Test CLI")

    parser.add_argument(
        "--spec",
        type=str,
        help="Path to JSON spec file OR JSON string for function parameters"
    )
    parser.add_argument("--function", type=str, help="Function of x (e.g., 'sin(x) + exp(x)')")
    parser.add_argument("--a", type=float, help="Lower bound of integration")
    parser.add_argument("--b", type=float, help="Upper bound of integration")
    parser.add_argument("--n", type=int, help="Number of subintervals")

    args = parser.parse_args()

    # Decide input mode
    if args.spec:
        spec = args.spec
    else:
        # Build dict from flags
        if not all([args.function, args.a is not None, args.b is not None, args.n is not None]):
            print("Error: Must provide either --spec or all of --function, --a, --b, --n")
            sys.exit(1)
        spec = {
            "function": args.function,
            "a": args.a,
            "b": args.b,
            "n": args.n
        }

    try:
        f, a, b, n = parse_input(spec)
        print("\n✅ Input parsed successfully!")
        print(f"Function: {args.function or 'From spec file'}")
        print(f"Bounds: a = {a}, b = {b}, n = {n}")
        print(f"Test f(a) = f({a}) = {f(a)}")
        print(f"Test f(b) = f({b}) = {f(b)}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
