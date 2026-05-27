# Day 6 — Conditional Statements

Welcome to Day 6.

Today, you'll learn:
- how programs make decisions,
- how to use `if` statements,
- how to use `else`,
- and how to compare values.

---

# What are Conditional Statements?

Conditional statements allow programs to make decisions.

They check whether a condition is `True` or `False`.

---

# The `if` Statement

The `if` statement runs code only if a condition is true.

## Example

```python
age = 18

if age >= 18:
    print("You are an adult.")
```

---

# Understanding the Code

```python
if age >= 18:
```

### Breakdown

- `if` starts the condition.
- `age >= 18` is the condition being checked.
- `:` is required after the condition.
- The indented code runs only if the condition is true.

---

# Indentation Matters

Python uses indentation to organize blocks of code.

## Correct

```python
if age >= 18:
    print("Access granted")
```

---

## Wrong

```python
if age >= 18:
print("Access granted")
```

This causes an error.

---

# The `else` Statement

`else` runs when the condition is false.

## Example

```python
age = 15

if age >= 18:
    print("Adult")
else:
    print("Minor")
```

---

# Comparison Operators

| Operator | Meaning |
|---|---|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal to |
| `<=` | Less than or equal to |

---

# Checking Equality

## Example

```python
password = "python123"

if password == "python123":
    print("Correct password")
```

---

# Using User Input with Conditions

## Example

```python
age = int(input("Enter your age: "))

if age >= 18:
    print("You can vote.")
else:
    print("You cannot vote yet.")
```

---

# Multiple Conditions with `elif`

`elif` allows checking additional conditions.

## Example

```python
score = 85

if score >= 90:
    print("Grade A")
elif score >= 75:
    print("Grade B")
else:
    print("Grade C")
```

---

# Nested Example

```python
number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")
```

---

# Practice Tasks

## Task 1
Ask the user for their age and check if they are an adult.

---

## Task 2
Ask the user for a number and check if it is even or odd.

---

## Task 3
Ask the user for a password and compare it with a correct password.

---

## Task 4
Create a simple grading system using `if`, `elif`, and `else`.

---

# Mini Challenge

Create a login system.

Your program should:
- ask the user for a username,
- ask for a password,
- check if the password is correct,
- and print an appropriate message.

Example:

```python
password = input("Enter password: ")

if password == "python123":
    print("Access granted")
else:
    print("Access denied")
```

---

# Common Beginner Mistakes

## Using `=` Instead of `==`

Wrong:
```python
if age = 18:
```

Correct:
```python
if age == 18:
```

`=` assigns values.  
`==` compares values.

---

## Forgetting the Colon

Wrong:
```python
if age >= 18
```

Correct:
```python
if age >= 18:
```

---

# Key Takeaways

Today you learned:
- how conditions work,
- how to use `if`, `else`, and `elif`,
- how comparison operators work,
- and how programs make decisions.

Your programs can now react differently based on user input.