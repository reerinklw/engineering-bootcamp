"""Simple CLI calculator for git/CI practice."""

import argparse
import sys


def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b


OPERATIONS = {
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Simple calculator")
    parser.add_argument(
        "operation",
        choices=OPERATIONS.keys(),
        help="Operation to perform",
    )
    parser.add_argument("a", type=float, help="First number")
    parser.add_argument("b", type=float, help="Second number")
    args = parser.parse_args(argv)

    try:
        result = OPERATIONS[args.operation](args.a, args.b)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
