# Day 2 — Variables and Data Types

Welcome to Day 2.

Today, you'll learn:
- what variables are,
- how to store data,
- basic data types,
- and how variable reassignment works.

---

# What is a Variable?

A variable is used to store information in a program.

Think of it like a container that holds data.

## Example

```python
name = "Alex"
```

In this example:
- `name` is the variable name
- `"Alex"` is the value stored inside it

---

# Printing Variables

You can print variables using `print()`.

## Example

```python
name = "Alex"

print(name)
```

## Output

```text
Alex
```

---

# Multiple Variables

Programs often use multiple variables.

## Example

```python
name = "Alex"
age = 18
country = "India"

print(name)
print(age)
print(country)
```

---

# Basic Data Types

Python supports different types of data.

## Strings

Strings are text values written inside quotes.

```python
city = "Chennai"
```

---

## Integers

Integers are whole numbers.

```python
age = 18
```

---

## Floats

Floats are decimal numbers.

```python
height = 5.8
```

---

## Booleans

Booleans represent `True` or `False`.

```python
is_student = True
```

---

# Variable Reassignment

Variables in Python can be updated by assigning them a new value.

## Example

```python
score = 10

score = 20

print(score)
```

## Output

```text
20
```

The old value gets replaced by the new value.

---

# Using Variables in Calculations

Variables can also store numbers used in calculations.

## Example

```python
a = 5
b = 7

total = a + b

print(total)
```

## Output

```text
12
```

---

# Naming Variables

Good variable names make code easier to read.

## Good Examples

```python
first_name = "Alex"
age = 18
favorite_game = "Minecraft"
```

---

## Avoid This

```python
x = "Alex"
y = 18
z = "Minecraft"
```

Meaningful names are better for readability.

---

# Practice Tasks

## Task 1
Create a variable called `name` and store your name in it.

---

## Task 2
Create a variable called `age` and store your age.

---

## Task 3
Print both variables.

---

## Task 4
Create two number variables and print their sum.

---

# Mini Challenge

Create a small profile program using variables.

Your program should:
- store your name,
- store your age,
- store your favorite hobby,
- and print all the information.

Example:

```python
name = "Alex"
age = 18
hobby = "Gaming"

print(name)
print(age)
print(hobby)
```

---

# Common Beginner Mistakes

## Forgetting Quotes for Strings

Wrong:
```python
name = Alex
```

Correct:
```python
name = "Alex"
```

---

## Using Spaces in Variable Names

Wrong:
```python
favorite game = "Minecraft"
```

Correct:
```python
favorite_game = "Minecraft"
```

---

# Key Takeaways

Today you learned:
- how variables work,
- how to store data,
- different data types,
- and how to update variable values.

You are now writing programs that can store and manage information.