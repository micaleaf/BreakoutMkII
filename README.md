# Breakout Game -Group 3
This is a Python-based Breakout game developed by Group 3 for the Capstone project. The game is built using the Pygame library and follows a modular, object-oriented structure.

## Group Members
(1) Micaela Leaf       (2) Julian Kushto
(3) Stefanie Merceron  (3) Tanner Goodenow

---

## Features Implemented in Phase I
- Paddle movement using arrow keys
- Ball launch with randomized direction
- Brick wall generation with color gradients
- Collision detection (paddle, ball, and bricks)
- Menu, Help, and End game screens
- Score and lives tracking
- Unit testing using pytest
---

## Features Implemented in Phase II
- Refactored game structure into modular, testable components
- Power-up system with random falling items from destroyed bricks that need to be catched by the paddle
- Sticky Ball that attaches to the paddle on contact
- Laser Mode allowing the paddle to shoot lasers
- Slow Paddle and Fast Ball mechanics to alter gameplay pace
- Reverse controls to challenge user reflexes
- Paddle size expansion and shrinks
- Timer effect with expiration and state resets
- Centralized configuration through `settings.json` and `config.py`
- Extended unit tests for gameplay logic and power-up mechanics

---

## Power-Ups

The following power-ups may randomly drop from destroyed bricks and will activate when collected by the paddle:

| Power-Up        | Effect Description                                  | Keys     |
|-----------------|-----------------------------------------------------|----------|
| Expand          | Increases the paddle width by 50 percent            | Click 1  |
| Shrink          | Decreases the paddle width by 40 percent            | Click 2  |
| Sticky          | Ball sticks to paddle on contact until re-launched  | Click 6  |
| Laser           | Paddle fires lasers to destroy bricks               | Click 5  |
| Slow Paddle     | Slows down paddle movement                          | Click 7  |
| Fast Ball       | Increases ball speed significantly                  | Click 4  |
| Reverse         | Inverts left and right paddle controls              | Click 8  |
| Extra Life      | Grants the player an additional life                | Click 3  |

Each power-up effect lasts for a limited time before reverting to default settings.

---

## How to Run the Game

Ensure Python 3.10 or later is installed. Install the Pygame library if not already installed:

```bash
pip install pygame
```

Then launch the game using:

```bash
python main.py
```
---

## Unit Testing
We used pytest to test logic-based components of the game (e.g., paddle movement, ball launch, score/lives updates). Test files are located in the `Code/tests` folder. Run the test suite with:
`python -m pytest tests/`
