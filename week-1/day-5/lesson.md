# Day 5 — Working with Strings

Welcome to Day 5.

Today, you'll learn:
- what strings are,
- how to combine strings,
- string formatting,
- and useful string methods.

---

# What is a String?

A string is a sequence of characters used to store text.

Strings are written inside quotes.

## Example

```python
name = "Alex"
```

---

# Printing Strings

## Example

```python
print("Hello World!")
```

## Output

```text
Hello World!
```

---

# Combining Strings

You can combine strings using the `+` operator.

This is called string concatenation.

## Example

```python
first_name = "Alex"
last_name = "Smith"

full_name = first_name + " " + last_name

print(full_name)
```

## Output

```text
Alex Smith
```

---

# Combining Strings with Variables

## Example

```python
name = "Alex"

print("Hello " + name)
```

---

# Using Commas in `print()`

Python automatically adds spaces when using commas.

## Example

```python
name = "Alex"

print("Hello", name)
```

---

# f-Strings

f-strings make it easier to insert variables into text.

## Example

```python
name = "Alex"
age = 18

print(f"My name is {name} and I am {age} years old.")
```

## Output

```text
My name is Alex and I am 18 years old.
```

---

# Useful String Methods

Python provides built-in methods for working with strings.

---

## Uppercase

```python
name = "alex"

print(name.upper())
```

## Output

```text
ALEX
```

---

## Lowercase

```python
name = "ALEX"

print(name.lower())
```

---

## Title Case

```python
movie = "harry potter"

print(movie.title())
```

## Output

```text
Harry Potter
```

---

# String Length

You can count characters using `len()`.

## Example

```python
game = "Minecraft"

print(len(game))
```

---

# Taking String Input

## Example

```python
favorite_food = input("Enter your favorite food: ")

print(f"You like {favorite_food}.")
```

---

# Practice Tasks

## Task 1
Create a variable called `city` and print it in uppercase.

---

## Task 2
Combine your first name and last name into one string.

---

## Task 3
Ask the user for their favorite movie and print it using an f-string.

---

## Task 4
Print the length of a word.

---

# Mini Challenge

Create a mini profile formatter.

Your program should:
- ask for the user's name,
- ask for their favorite game,
- ask for their city,
- and print everything neatly using f-strings.

Example:

```python
name = input("Enter your name: ")
game = input("Enter your favorite game: ")
city = input("Enter your city: ")

print(f"{name} lives in {city} and likes playing {game}.")
```

---

# Common Beginner Mistakes

## Forgetting Quotes

Wrong:
```python
name = Alex
```

Correct:
```python
name = "Alex"
```

---

## Forgetting the `f` in f-strings

Wrong:
```python
print("Hello {name}")
```

Correct:
```python
print(f"Hello {name}")
```

---

# Key Takeaways

Today you learned:
- what strings are,
- how to combine text,
- how to use f-strings,
- and useful string methods.

Your programs can now create cleaner and more dynamic text output.