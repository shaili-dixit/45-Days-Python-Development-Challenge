# Day 5 — Examples
# Working with Strings

# Basic strings
name = "Alex"
city = "Chennai"

print(name)
print(city)

# Combining strings
first_name = "Alex"
last_name = "Smith"

full_name = first_name + " " + last_name

print(full_name)

# Using commas in print
print("Hello", name)

# Using f-strings
age = 18

print(f"My name is {name} and I am {age} years old.")

# Uppercase
game = "minecraft"

print(game.upper())

# Lowercase
movie = "INTERSTELLAR"

print(movie.lower())

# Title case
book = "harry potter and the goblet of fire"

print(book.title())

# String length
favorite_food = "Pizza"

print(len(favorite_food))

# Taking user input
country = input("Enter your country: ")

print(f"You live in {country}.")

# Combining user input
hobby = input("Enter your hobby: ")
dream_job = input("Enter your dream job: ")

print(f"Your hobby is {hobby} and you want to become a {dream_job}.")

# Slightly harder example
username = input("Create a username: ")

print("Original:", username)
print("Uppercase:", username.upper())
print("Lowercase:", username.lower())
print("Length:", len(username))

# Fun formatting example
hero_name = input("Enter a hero name: ")
power = input("Enter a superpower: ")

print("----- HERO PROFILE -----")
print(f"Hero Name: {hero_name.title()}")
print(f"Superpower: {power.title()}")

# String repetition
print("Python! " * 3)

# Final message
print("Day 5 completed successfully!")