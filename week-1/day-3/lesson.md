# Day 3 — User Input

Welcome to Day 3.

Today, you'll learn:
- how to take input from users,
- how to store user input in variables,
- and how to create interactive programs.

---

# What is User Input?

User input allows people to enter information while the program is running.

This makes programs interactive.

In Python, we use the `input()` function to get user input.

---

# Your First Input Program

## Example

```python
name = input("Enter your name: ")

print("Hello", name)
```

---

# Understanding the Code

```python
name = input("Enter your name: ")
```

### Breakdown

- `input()` waits for the user to type something.
- The text inside the parentheses is called a prompt.
- The entered value gets stored in the variable `name`.

---

# Example Output

```text
Enter your name: Alex
Hello Alex
```

---

# Taking Multiple Inputs

Programs can take multiple inputs from users.

## Example

```python
name = input("Enter your name: ")
city = input("Enter your city: ")

print("Hello", name)
print("You live in", city)
```

---

# Input is Stored as Text

By default, `input()` stores data as a string.

## Example

```python
age = input("Enter your age: ")

print(age)
```

Even if the user enters a number, Python treats it as text.

---

# Converting Input to Numbers

To perform calculations, we convert input into integers using `int()`.

## Example

```python
age = int(input("Enter your age: "))

print(age + 1)
```

---

# Example Output

```text
Enter your age: 18
19
```

---

# Using Input in Calculations

## Example

```python
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

total = num1 + num2

print("Total:", total)
```

---

# Creating Interactive Programs

User input makes programs feel more dynamic and fun.

## Example

```python
favorite_game = input("What is your favorite game? ")

print("Your favorite game is", favorite_game)
```

---

# Practice Tasks

## Task 1
Ask the user for their name and print a greeting.

---

## Task 2
Ask the user for their favorite food.

---

## Task 3
Ask the user for two numbers and print their sum.

---

## Task 4
Ask the user for their age and print how old they will be next year.

---

# Mini Challenge

Create a mini introduction program.

Your program should:
- ask for the user's name,
- ask for their age,
- ask for their hobby,
- and print all the information neatly.

Example:

```python
name = input("Enter your name: ")
age = input("Enter your age: ")
hobby = input("Enter your hobby: ")

print("Name:", name)
print("Age:", age)
print("Hobby:", hobby)
```

---

# Common Beginner Mistakes

## Forgetting `int()` for Calculations

Wrong:
```python
num1 = input("Enter number: ")
num2 = input("Enter number: ")

print(num1 + num2)
```

Output:
```text
23
```

Correct:
```python
num1 = int(input("Enter number: "))
num2 = int(input("Enter number: "))

print(num1 + num2)
```

Output:
```text
5
```

---

## Forgetting Parentheses

Wrong:
```python
name = input "Enter your name: "
```

Correct:
```python
name = input("Enter your name: ")
```

---

# Key Takeaways

Today you learned:
- how to use `input()`,
- how to store user input,
- how to convert text into numbers,
- and how to build interactive programs.

Your programs can now interact with real users.