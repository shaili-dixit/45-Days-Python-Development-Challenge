# Day 7 — Examples
# Quiz Game Project

# Basic welcome message
print("Welcome to the Python Quiz Game!")

# Starting score
score = 0

# Question 1
answer = input("What is 5 + 5? ")

if answer == "10":
    print("Correct!")
    score = score + 1
else:
    print("Wrong answer.")

# Question 2
answer = input("What color is the sky? ")

if answer.lower() == "blue":
    print("Correct!")
    score = score + 1
else:
    print("Wrong answer.")

# Question 3
answer = input("Which programming language are you learning? ")

if answer.lower() == "python":
    print("Correct!")
    score = score + 1
else:
    print("Wrong answer.")

# Display final score
print("Final Score:", score)

# Score message
if score == 3:
    print("Excellent work!")
elif score == 2:
    print("Good job!")
else:
    print("Keep practicing!")

# Slightly harder example
print("\n----- Gaming Quiz -----")

gaming_score = 0

answer = input("Which company created Minecraft? ")

if answer.lower() == "mojang":
    print("Correct!")
    gaming_score = gaming_score + 1
else:
    print("Incorrect.")

answer = input("What color is Luigi's shirt? ")

if answer.lower() == "green":
    print("Correct!")
    gaming_score = gaming_score + 1
else:
    print("Incorrect.")

print("Gaming Quiz Score:", gaming_score)

# Final message
print("Day 7 completed successfully!")