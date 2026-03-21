import random
import time
import json
import os

SCORE_FILE = "scores.json"


# LOAD & SAVE SCOREBOARD

def load_scores():
    if not os.path.exists(SCORE_FILE):
        return []
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def save_score(name, attempts, difficulty):
    scores = load_scores()
    scores.append({
        "name": name,
        "attempts": attempts,
        "difficulty": difficulty,
        "time": time.ctime()
    })
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=4)

def show_scores():
    scores = load_scores()
    if not scores:
        print("\n No scores yet!")
        return
    
    print("\n SCOREBOARD")
    print("-" * 40)
    for entry in scores:
        print(f"{entry['name']} | Attempts: {entry['attempts']} | Level: {entry['difficulty']} | {entry['time']}")
    print("-" * 40)



# CHOOSE DIFFICULTY

def choose_difficulty():
    print("\nChoose difficulty:")
    print("1. Easy (1–20, unlimited attempts)")
    print("2. Medium (1–50, 10 attempts)")
    print("3. Hard (1–100, 7 attempts)")
    print("4. Custom Range")
    
    while True:
        choice = input("Enter choice (1-4): ")
        if choice == "1":
            return (1, 20, None, "Easy")
        elif choice == "2":
            return (1, 50, 10, "Medium")
        elif choice == "3":
            return (1, 100, 7, "Hard")
        elif choice == "4":
            return custom_range()
        else:
            print(" Invalid choice, try again.")


def custom_range():
    print("\nEnter your own number range.")

    while True:
        try:
            start = int(input("Start number: "))
            end = int(input("End number: "))
            if start >= end:
                print(" Start must be LESS than end!")
                continue
            return (start, end, None, f"Custom {start}-{end}")
        except:
            print(" Enter valid numbers!")



# GET USER GUESS

def get_guess(start, end):
    while True:
        try:
            guess = int(input(f"Enter your guess ({start}–{end}): "))
            if start <= guess <= end:
                return guess
            else:
                print(" Out of range!")
        except:
            print(" Enter a valid number!")



# PLAY ONE ROUND

def play_game():
    name = input("\nEnter your name: ").strip() or "Player"

    start, end, max_attempts, difficulty = choose_difficulty()
    secret = random.randint(start, end)
    attempts = 0

    print(f"\nI picked a number between {start} and {end}. Can you guess it? ")

    while True:
        guess = get_guess(start, end)
        attempts += 1

        # Check guess
        if guess < secret:
            print(" Too low!")
        elif guess > secret:
            print(" Too high!")
        else:
            print(f"\n Correct! You guessed it in {attempts} attempts!")
            save_score(name, attempts, difficulty)
            break
        
        # Show attempts left for limited modes
        if max_attempts:
            remaining = max_attempts - attempts
            print(f" Attempts left: {remaining}")

            if remaining <= 0:
                print("\n You ran out of attempts!")
                print(f"The number was: {secret}")
                break
        
        # Give hints
        if attempts % 3 == 0:
            hint = "even" if secret % 2 == 0 else "odd"
            print(f" Hint: The number is {hint}!")



# MAIN MENU

def main():
    while True:
        print("\n=====================")
        print("1 GUESSING GAME MENU")
        print("=====================")
        print("1. Play Game")
        print("2. View Scoreboard")
        print("3. Exit")
        
        choice = input("Choose an option: ")

        if choice == "1":
            play_game()
        elif choice == "2":
            show_scores()
        elif choice == "3":
            print("\nGoodbye! Thanks for playing! ")
            break
        else:
            print(" Invalid choice, try again.")



# ENTRY POINT

if __name__ == "__main__":
    main()