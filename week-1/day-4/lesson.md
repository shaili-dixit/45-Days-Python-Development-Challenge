# Day 4 — Basic Math Operations

Welcome to Day 4.

Today, you'll learn:
- how to perform calculations in Python,
- different math operators,
- and how to use variables in calculations.

---

# Math in Python

Python can perform mathematical calculations just like a calculator.

## Example

```python
print(5 + 3)
```

## Output

```text
8
```

---

# Addition Operator (`+`)

The `+` operator adds numbers together.

## Example

```python
print(10 + 5)
```

## Output

```text
15
```

---

# Subtraction Operator (`-`)

The `-` operator subtracts numbers.

## Example

```python
print(20 - 7)
```

## Output

```text
13
```

---

# Multiplication Operator (`*`)

The `*` operator multiplies numbers.

## Example

```python
print(6 * 4)
```

## Output

```text
24
```

---

# Division Operator (`/`)

The `/` operator divides numbers.

## Example

```python
print(12 / 3)
```

## Output

```text
4.0
```

Notice that division returns a decimal value.

---

# Modulus Operator (`%`)

The `%` operator returns the remainder after division.

## Example

```python
print(10 % 3)
```

## Output

```text
1
```

---

# Using Variables in Calculations

Variables make calculations more flexible.

## Example

```python
a = 10
b = 5

total = a + b

print(total)
```

---

# Combining Input and Math

You can take numbers from users and perform calculations.

## Example

```python
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

print("Sum:", num1 + num2)
```

---

# Order of Operations

Python follows standard math rules.

## Example

```python
print(2 + 3 * 4)
```

## Output

```text
14
```

Multiplication happens before addition.

---

# Using Parentheses

Parentheses change the order of calculations.

## Example

```python
print((2 + 3) * 4)
```

## Output

```text
20
```

---

# Practice Tasks

## Task 1
Create two number variables and print their sum.

---

## Task 2
Print the result of:
- multiplication,
- subtraction,
- and division.

---

## Task 3
Ask the user for two numbers and print their product.

---

## Task 4
Ask the user for a number and print:
- double the number,
- triple the number.

---

# Mini Challenge

Create a simple calculator program.

Your program should:
- ask the user for two numbers,
- print:
  - addition,
  - subtraction,
  - multiplication,
  - division.

Example:

```python
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)
```

---

# Common Beginner Mistakes

## Forgetting `int()`

Wrong:
```python
a = input("Enter number: ")
b = input("Enter number: ")

print(a + b)
```

Output:
```text
23
```

Correct:
```python
a = int(input("Enter number: "))
b = int(input("Enter number: "))

print(a + b)
```

---

## Dividing by Zero

Wrong:
```python
print(10 / 0)
```

This causes an error because division by zero is not allowed.

---

# Key Takeaways

Today you learned:
- how to perform math operations,
- different arithmetic operators,
- how calculations work with variables,
- and how to build simple calculator programs.

Your programs can now process numbers and calculations.