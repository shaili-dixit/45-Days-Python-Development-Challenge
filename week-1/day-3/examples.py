# Day 3 — Examples
# User Input in Python

# Taking basic user input
name = input("Enter your name: ")

print("Hello", name)

# Multiple inputs
city = input("Enter your city: ")
favorite_food = input("Enter your favorite food: ")

print("City:", city)
print("Favorite Food:", favorite_food)

# Taking numeric input
age = int(input("Enter your age: "))

print("Next year, you will be", age + 1)

# Adding two numbers
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

total = num1 + num2

print("Total:", total)

# Multiplication example
number = int(input("Enter a number: "))

print("Double:", number * 2)
print("Triple:", number * 3)

# Creating a mini profile
name = input("Enter your name: ")
hobby = input("Enter your hobby: ")
dream_job = input("Enter your dream job: ")

print("----- PROFILE -----")
print("Name:", name)
print("Hobby:", hobby)
print("Dream Job:", dream_job)

# Small calculator
a = int(input("Enter first value: "))
b = int(input("Enter second value: "))

print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)

# Slightly harder example
marks1 = int(input("Enter Math marks: "))
marks2 = int(input("Enter Science marks: "))
marks3 = int(input("Enter English marks: "))

total_marks = marks1 + marks2 + marks3
average = total_marks / 3

print("Total Marks:", total_marks)
print("Average Marks:", average)

# Final message
print("Day 3 completed successfully!")