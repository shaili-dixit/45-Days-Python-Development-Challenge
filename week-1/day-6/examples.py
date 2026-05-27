# Day 6 — Examples
# Conditional Statements

# Basic if statement
age = 18

if age >= 18:
    print("You are an adult.")

# if and else
temperature = 30

if temperature > 25:
    print("It is hot outside.")
else:
    print("It is cool outside.")

# Equality check
password = "python123"

if password == "python123":
    print("Correct password.")

# Checking even or odd numbers
number = int(input("Enter a number: "))

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")

# Using user input
age = int(input("Enter your age: "))

if age >= 18:
    print("You can vote.")
else:
    print("You cannot vote yet.")

# Grading system
score = int(input("Enter your score: "))

if score >= 90:
    print("Grade A")
elif score >= 75:
    print("Grade B")
elif score >= 50:
    print("Grade C")
else:
    print("Grade F")

# Simple login system
username = input("Enter username: ")
password = input("Enter password: ")

if password == "admin123":
    print("Login successful")
else:
    print("Incorrect password")

# Number comparison
a = int(input("Enter first number: "))
b = int(input("Enter second number: "))

if a > b:
    print("First number is larger")
elif a < b:
    print("Second number is larger")
else:
    print("Both numbers are equal")

# Slightly harder example
coins = int(input("Enter your coins: "))

if coins >= 100:
    print("You can buy the sword.")
else:
    print("Not enough coins.")

# Final message
print("Day 6 completed successfully!")