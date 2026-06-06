"""
Rule-Based Chatbot with Pattern Matching and Conversation Logger
Handles greetings, farewells, jokes, Q&A; logs all conversations to file.
"""

import re
import random
import os
from datetime import datetime

LOG_FILE = "chatbot_log.txt"

PATTERNS = [
    (r'\b(hi|hello|hey|howdy|sup)\b',        'greeting'),
    (r'\b(bye|goodbye|see you|cya|exit|quit)\b', 'farewell'),
    (r'\btell me a joke\b|joke please',        'joke'),
    (r'\bwhat is your name\b|\bwho are you\b', 'identity'),
    (r'\bhow are you\b|\bhow do you do\b',     'status'),
    (r'\bwhat time is it\b|\btime\b',          'time'),
    (r'\bwhat.*date\b|\btoday.*date\b',        'date'),
    (r'\bthank(s| you)\b',                     'thanks'),
    (r'\bhelp\b|\bwhat can you do\b',          'help'),
    (r'\bweather\b',                           'weather'),
    (r'\bfavorite (color|colour)\b',           'fav_color'),
    (r'\bfavorite (food|eat)\b',               'fav_food'),
    (r'\bwhat is (\d+[\+\-\*\/]\d+)\b',        'math'),
    (r'\bmy name is (\w+)\b',                  'learn_name'),
    (r'\bwhat is my name\b',                   'recall_name'),
    (r'\b(sad|unhappy|depressed|upset)\b',     'empathy'),
    (r'\b(happy|excited|great|awesome)\b',     'positive'),
    (r'\bfact\b|\bgive me a fact\b',           'fact'),
    (r'\brepeat (.+)',                         'repeat'),
]

RESPONSES = {
    'greeting':   ["Hello! How can I help you today?", "Hey there! Nice to meet you!", "Hi! What's on your mind?"],
    'farewell':   ["Goodbye! Have a wonderful day!", "See you later! Take care!", "Bye! Come back anytime."],
    'identity':   ["I'm ChatBot v1.0, your friendly rule-based assistant!", "I'm a simple Python chatbot here to help."],
    'status':     ["I'm just a program, but I'm doing great! How about you?", "Running perfectly well, thanks for asking!"],
    'time':       [f"The current time is {datetime.now().strftime('%H:%M:%S')}."],
    'date':       [f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."],
    'thanks':     ["You're welcome!", "Happy to help!", "Anytime! That's what I'm here for."],
    'help':       ["I can chat, tell jokes, answer time/date, do simple math, and more! Try: 'tell me a joke', 'what time is it', 'give me a fact'."],
    'weather':    ["I don't have real-time weather data, but I hope it's sunny wherever you are!"],
    'fav_color':  ["My favorite color is Python blue — #3776AB!"],
    'fav_food':   ["I'd eat bytes of data all day if I could! Delicious."],
    'empathy':    ["I'm sorry to hear that. Remember, things will get better. 💙", "I understand. It's okay to feel that way. I'm here to chat!"],
    'positive':   ["That's wonderful! Your energy is contagious! 😊", "Awesome! Keep that positive vibe going!"],
    'fact':       [
        "A group of flamingos is called a flamboyance.",
        "Honey never spoils — archaeologists found 3000-year-old edible honey in Egypt.",
        "Octopuses have three hearts and blue blood.",
        "Python was named after Monty Python, not the snake.",
        "The word 'robot' comes from the Czech word 'robota', meaning forced labor.",
        "A day on Venus is longer than a year on Venus.",
    ],
    'joke': [
        "Why do Python programmers prefer dark mode? Because light attracts bugs! 🐛",
        "Why did the programmer quit? Because they didn't get arrays! 😄",
        "I told my computer I needed a break... now it won't stop sending me Kit-Kat ads.",
        "What's a computer's favorite snack? Microchips!",
        "Why is the computer cold? It left its Windows open!",
        "How many programmers does it take to change a light bulb? None — that's a hardware problem.",
    ],
    'fallback': [
        "I'm not sure I understand. Could you rephrase that?",
        "Hmm, that's beyond my current knowledge. Try asking something else!",
        "Interesting! But I don't have a good answer for that yet.",
        "I'm still learning. Could you try asking differently?",
    ],
}

user_name = None


def match_pattern(user_input):
    global user_name
    text = user_input.lower().strip()

    for pattern, intent in PATTERNS:
        match = re.search(pattern, text)
        if match:
            if intent == 'time':
                return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
            if intent == 'date':
                return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
            if intent == 'math':
                expr = match.group(1)
                try:
                    result = eval(expr)
                    return f"The answer is {result}."
                except:
                    return "I couldn't compute that safely."
            if intent == 'learn_name':
                user_name = match.group(1).capitalize()
                return f"Nice to meet you, {user_name}! I'll remember your name."
            if intent == 'recall_name':
                return f"Your name is {user_name}!" if user_name else "I don't know your name yet. Tell me: 'My name is ...'"
            if intent == 'repeat':
                phrase = match.group(1)
                return f"You said: '{phrase}'"
            if intent == 'farewell':
                return random.choice(RESPONSES['farewell']) + (" " + user_name + "!" if user_name else ""), True
            responses = RESPONSES.get(intent, RESPONSES['fallback'])
            return random.choice(responses), False

    return random.choice(RESPONSES['fallback']), False


def log_conversation(user_msg, bot_msg):
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"[{ts}] USER: {user_msg}\n")
        f.write(f"[{ts}] BOT : {bot_msg}\n")
        f.write("─" * 50 + "\n")


def show_log(lines=20):
    if not os.path.exists(LOG_FILE):
        print("  No conversation log found.")
        return
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    print(f"\n  Last {lines} log lines:")
    for line in all_lines[-lines:]:
        print(f"  {line}", end='')


def chat():
    print("╔══════════════════════════════════════════╗")
    print("║   Rule-Based Chatbot v1.0                ║")
    print("╚══════════════════════════════════════════╝")
    print("  Type 'help' to see what I can do.")
    print("  Type 'log' to view conversation history.")
    print("  Type 'bye' to exit.\n")

    while True:
        try:
            user_input = input("  You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Bot: Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == 'log':
            show_log()
            continue

        result = match_pattern(user_input)
        if isinstance(result, tuple):
            response, should_exit = result
        else:
            response, should_exit = result, False

        print(f"  Bot: {response}\n")
        log_conversation(user_input, response)

        if should_exit:
            break


if __name__ == "__main__":
    chat()
