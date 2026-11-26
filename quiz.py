#!/usr/bin/env python3
"""
number-quiz: Guess the secret number. Tracks score, streaks, and high scores.
"""

import random
import json
import os
import time

SCORES_FILE = "highscores.json"


DIFFICULTIES = {
    "1": {"name": "Easy",   "range": (1, 50),   "max_tries": 10},
    "2": {"name": "Medium", "range": (1, 100),  "max_tries": 7},
    "3": {"name": "Hard",   "range": (1, 200),  "max_tries": 6},
    "4": {"name": "Insane", "range": (1, 1000), "max_tries": 5},
}


def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    with open(SCORES_FILE, "r") as f:
        return json.load(f)


def save_score(name, difficulty, score, tries):
    scores = load_scores()
    scores.append(
        {
            "name": name,
            "difficulty": difficulty,
            "score": score,
            "tries": tries,
            "date": time.strftime("%Y-%m-%d"),
        }
    )
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # keep top 10
    with open(SCORES_FILE, "w") as f:
        json.dump(scores, f, indent=2)


def show_leaderboard():
    scores = load_scores()
    if not scores:
        print("\n  No scores yet. Be the first!\n")
        return
    print("\n  🏆 Top 10 Leaderboard")
    print("  " + "-" * 46)
    print(f"  {'#':<3} {'Name':<12} {'Difficulty':<10} {'Score':<8} {'Tries':<6} Date")
    print("  " + "-" * 46)
    for i, s in enumerate(scores, 1):
        print(
            f"  {i:<3} {s['name']:<12} {s['difficulty']:<10} {s['score']:<8} {s['tries']:<6} {s['date']}"
        )
    print()


def calculate_score(difficulty_key, tries, max_tries, elapsed):
    base = {"1": 100, "2": 300, "3": 600, "4": 1500}[difficulty_key]
    efficiency = max(0, (max_tries - tries + 1) / max_tries)
    time_bonus = max(0, 30 - int(elapsed))
    return int(base * efficiency) + time_bonus


def play_game(player_name):
    print("\n  Choose difficulty:")
    for key, d in DIFFICULTIES.items():
        lo, hi = d["range"]
        print(f"    {key}. {d['name']:<8}  ({lo}–{hi}, {d['max_tries']} tries)")
    print()

    choice = input("  Enter 1-4: ").strip()
    if choice not in DIFFICULTIES:
        print("  Invalid choice. Defaulting to Medium.")
        choice = "2"

    diff = DIFFICULTIES[choice]
    lo, hi = diff["range"]
    max_tries = diff["max_tries"]
    secret = random.randint(lo, hi)

    print(f"\n  🎮 {diff['name']} mode — Guess a number between {lo} and {hi}.")
    print(f"  You have {max_tries} tries. Good luck!\n")

    start = time.time()

    for attempt in range(1, max_tries + 1):
        remaining = max_tries - attempt + 1
        try:
            guess_str = input(f"  Try {attempt}/{max_tries} ➤ ").strip()
            guess = int(guess_str)
        except ValueError:
            print("  ⚠️  Please enter a valid number.\n")
            continue

        if guess < lo or guess > hi:
            print(f"  ⚠️  Out of range! Enter a number between {lo} and {hi}.\n")
            continue

        if guess == secret:
            elapsed = time.time() - start
            score = calculate_score(choice, attempt, max_tries, elapsed)
            print(f"\n  🎉 Correct! You got it in {attempt} try/tries!")
            print(f"  ⏱  Time: {elapsed:.1f}s")
            print(f"  ⭐ Score: {score} points\n")
            save_score(player_name, diff["name"], score, attempt)
            return True

        hint = "📉 Too low!" if guess < secret else "📈 Too high!"
        print(f"  {hint}  ({remaining - 1} tries left)\n")

    print(f"\n  💀 Out of tries! The number was {secret}.\n")
    return False


def main():
    print("\n" + "=" * 50)
    print("       🔢  Number Quiz  🔢")
    print("=" * 50)

    player_name = input("\n  Enter your name: ").strip() or "Player"

    while True:
        print("\n  What would you like to do?")
        print("    1. Play")
        print("    2. Leaderboard")
        print("    3. Quit")

        action = input("\n  Choice: ").strip()

        if action == "1":
            win = play_game(player_name)
            again = input("  Play again? (y/n): ").strip().lower()
            if again != "y":
                print(f"\n  Thanks for playing, {player_name}! 👋\n")
                break
        elif action == "2":
            show_leaderboard()
        elif action == "3":
            print(f"\n  Goodbye, {player_name}! 👋\n")
            break
        else:
            print("  Invalid choice.")


if __name__ == "__main__":
    main()
