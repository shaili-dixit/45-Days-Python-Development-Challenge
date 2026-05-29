"""Simple Python basics examples.

This file contains a few short, self-contained examples useful for
beginners: greeting, arithmetic, factorial, FizzBuzz, list comprehension,
and a small demonstration runner.
"""

from typing import List


def greet(name: str = "World") -> str:
	"""Return a friendly greeting for `name`."""
	return f"Hello, {name}!"


def add(a: float, b: float) -> float:
	"""Return the sum of two numbers."""
	return a + b


def factorial(n: int) -> int:
	"""Return n! (factorial) for n >= 0. Raises ValueError for negative n."""
	if n < 0:
		raise ValueError("n must be non-negative")
	result = 1
	for i in range(2, n + 1):
		result *= i
	return result


def fizzbuzz(n: int = 20) -> List[str]:
	"""Return FizzBuzz sequence from 1..n as a list of strings."""
	out: List[str] = []
	for i in range(1, n + 1):
		if i % 15 == 0:
			out.append("FizzBuzz")
		elif i % 3 == 0:
			out.append("Fizz")
		elif i % 5 == 0:
			out.append("Buzz")
		else:
			out.append(str(i))
	return out


def demonstrate() -> None:
	"""Run a short demonstration printing example outputs."""
	print(greet("Developer"))
	print("2 + 3 =", add(2, 3))
	print("5! =", factorial(5))
	print("FizzBuzz (1..15):", ", ".join(fizzbuzz(15)))

	# Lists and comprehensions
	squares = [x * x for x in range(6)]
	print("Squares:", squares)

	# Simple dictionary usage
	info = {"name": "Alice", "age": 30}
	print("Info keys:", list(info.keys()))


if __name__ == "__main__":
	# Keep the demo non-interactive so it runs in CI and learners can execute it
	demonstrate()

