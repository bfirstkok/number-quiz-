# number-quiz 🔢

A terminal number-guessing game with four difficulty levels, a scoring system, and a top-10 leaderboard saved locally.

## Features

- 4 difficulty levels: Easy, Medium, Hard, Insane
- Score based on tries used + time bonus
- Top-10 leaderboard saved to `highscores.json`
- Multiple rounds in one session

## Usage

```bash
python quiz.py
```

You'll be prompted for your name, then choose a difficulty. Guess the secret number within the allowed tries!

## Scoring

```
Score = base_score × (remaining_tries / max_tries) + time_bonus
```

| Difficulty | Range  | Tries | Base Score |
|------------|--------|-------|-----------|
| Easy       | 1–50   | 10    | 100       |
| Medium     | 1–100  | 7     | 300       |
| Hard       | 1–200  | 6     | 600       |
| Insane     | 1–1000 | 5     | 1500      |

## Requirements

- Python 3.6+ (no external packages needed)

## License

MIT
