# Day 7 — Final Mini Project: Quiz Game

Welcome to Day 7.

Today, you'll build your first mini project by combining everything you've learned so far.

You will use:
- variables,
- user input,
- strings,
- math,
- and conditional statements.

By the end of this lesson, you'll create a simple interactive quiz game.

---

# What is a Quiz Game?

A quiz game asks questions and checks whether the user's answers are correct.

This is a great beginner project because it combines multiple programming concepts into one program.

---

# Step 1 — Welcome Message

Start by greeting the player.

## Example

```python
print("Welcome to the Python Quiz Game!")
```

---

# Step 2 — Create a Score Variable

We need a variable to keep track of points.

## Example

```python
score = 0
```

---

# Step 3 — Ask a Question

Use `input()` to get an answer from the player.

## Example

```python
answer = input("What is 5 + 5? ")
```

---

# Step 4 — Check the Answer

Use an `if` statement to check whether the answer is correct.

## Example

```python
if answer == "10":
    print("Correct!")
    score = score + 1
else:
    print("Wrong answer.")
```

---

# Step 5 — Add More Questions

You can repeat the same structure for multiple questions.

## Example

```python
answer = input("What color is the sky? ")

if answer == "blue":
    print("Correct!")
    score = score + 1
else:
    print("Wrong answer.")
```

---

# Step 6 — Show Final Score

At the end of the game, print the player's score.

## Example

```python
print("Final Score:", score)
```

---

# Full Example

```python
print("Welcome to the Python Quiz Game!")

score = 0

answer = input("What is 2 + 2? ")

if answer == "4":
    print("Correct!")
    score = score + 1
else:
    print("Wrong!")

answer = input("What color is grass? ")

if answer == "green":
    print("Correct!")
    score = score + 1
else:
    print("Wrong!")

print("Final Score:", score)
```

---

# Improving the Quiz

You can make your quiz more fun by:
- adding more questions,
- using different topics,
- adding emojis,
- using uppercase formatting,
- creating custom messages.

---

# Practice Tasks

## Task 1
Create a quiz with two questions.

---

## Task 2
Add a score system.

---

## Task 3
Print a special message if the player gets all answers correct.

---

## Task 4
Add questions about movies, games, or sports.

---

# Mini Challenge

Create your own custom quiz game.

Requirements:
- at least 3 questions,
- score tracking,
- use `if` statements,
- print the final score,
- and display a final message based on the score.

Example:

```text
Score 3/3 → Excellent!
Score 2/3 → Good job!
Score 1/3 → Keep practicing!
```

---

# Common Beginner Mistakes

## Forgetting Quotes in Conditions

Wrong:
```python
if answer == blue:
```

Correct:
```python
if answer == "blue":
```

---

## Forgetting to Update Score

Wrong:
```python
print("Correct!")
```

Correct:
```python
print("Correct!")
score = score + 1
```

---

# Key Takeaways

Today you learned:
- how to combine multiple concepts,
- how to build an interactive project,
- how quiz logic works,
- and how to track scores.

You officially completed your first week of Python.