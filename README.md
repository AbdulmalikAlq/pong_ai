# 🏓 Ping Pong AI (Python + Pygame)

A classic Pong game built with **Python** and **Pygame**, where you play against an AI opponent. Features adjustable difficulty levels, customizable ball size, and a simple start menu with settings. Smooth gameplay and responsive controls make it a fun project to learn game development.

## 🎮 Features

- **AI Opponent with Difficulty Levels**
  - Easy: slower reaction, larger error margin
  - Medium: balanced AI
  - Hard: fast and precise AI
- **Settings Menu**
  # 🏓 Ping Pong AI (Python + Pygame)

  A simple Pong clone written in Python using Pygame. Play against a prediction-based AI with configurable difficulty, ball size, and an adjustable win score.

  ## Features

  - Main menu with Play / Settings / Quit
  - Adjustable difficulty (Easy / Medium / Hard) — affects AI speed, reaction and aiming error
  - Adjustable ball size
  - Adjustable win score (changeable from Settings)
  - Pause (P), reset scores (R), and win screen when a player reaches the win score
  - AI prediction that simulates the ball trajectory (including wall bounces) for smarter play
  - Ball speed increases slightly on paddle hits (capped)

  ## Controls

  - Move up: ↑ (Up arrow)
  - Move down: ↓ (Down arrow)
  - Pause / Resume: P
  - Reset scores & ball: R
  - Back / Exit to menu: Esc

  Settings menu keys (open from Main Menu → Settings):
  - Change difficulty: ← / →
  - Change ball size: ↑ / ↓
  - Change win score: + / - (supports main keyboard and keypad)

  ## Requirements

  - Python 3.8+
  - pygame

  Install pygame with pip if you don't have it:

  ```bash
  python3 -m pip install pygame
  ```

  If you use the included virtualenv (`.venv`), activate it first:

  ```bash
  source .venv/bin/activate
  ```

  ## Run

  From the project root (where `pong_ai.py` is located):

  ```bash
  python3 pong_ai.py
  ```

  ## Notes & Tips

  - The win score default can be changed in Settings; it's bounded between 1 and 50.
  - If the AI feels too easy or too hard, try the other difficulty levels — they adjust AI speed, reaction delay and aiming error.
  - This project is intended as a learning/demo project; feel free to fork and add features like sound, keyboard remapping, or two-player mode.

  ## License

  MIT-style; see repository for details.

