# 🚀 Rocket League 2D — *Pygame Edition*

A 2D top-down arcade soccer/hockey game inspired by Rocket League, built with **Python** and **Pygame**. Drive a car around the field, smash a ball (or puck) with momentum-based physics, and outscore your opponent — with an AI goalkeeper guarding each net.

---

## 🎮 Features

- **Two Game Modes**
  - **Classic Soccer** — grass field, balanced physics
  - **Ice Hockey** — icy rink, very low friction, faster puck (default mode)
- **Full Menu System** — animated logo/menu, mode select screen, controls screen, "How to Play" screen, and a match setup screen
- **Custom match setup** — set match duration and name both players before kickoff
- **2-Player Gameplay** — 1v1 human players, each backed by an **AI goalkeeper**
- **Boost mechanic** — hold your boost key for ~1.5x speed
- **Momentum-based physics** — collisions between cars and the ball transfer momentum realistically
- **Overtime** — matches can go into extra time if scores are tied
- **Pause / Resume / Restart / Quit-to-menu**
- Ships with a full set of textures, fonts, and music already in `assets/`

---

## 🕹️ How to Play

1. Launch the game (see [Setup](#-setup--installation) below) — you'll land on the **Main Menu**.
2. From the main menu you can:
   - **Play Match** — go straight to match setup
   - **Game Mode** — pick Classic Soccer or Ice Hockey
   - **Controls** — view the key bindings
   - **How to Play** — view the objective and rules
   - **Exit**
3. In **Play Match**, set the **match duration** (in seconds) and type in names for the **Blue** and **Red** players, then press **Enter** or click **PLAY**.
4. During the match, each player drives their car around the field, aiming to knock the ball/puck into the opponent's goal. Each side also has an **AI goalkeeper** that defends automatically — you don't control it.
5. If the score is tied when time runs out, the match goes to **Overtime** (sudden extra time).
6. Press **P** or **ESC** any time to pause. From the pause screen you can restart, return to the menu, or quit.

### Controls

**Player 1 — Blue**
| Action | Key |
|---|---|
| Move | `W` `A` `S` `D` |
| Boost | `Left Shift` |

**Player 2 — Red**
| Action | Key |
|---|---|
| Move | Arrow Keys (`↑` `↓` `←` `→`) |
| Boost | `M` |

**Universal**
| Action | Key |
|---|---|
| Pause / Resume | `P` or `ESC` |
| Restart match (while paused / game over) | `R` |
| Return to Menu (while paused / game over) | `M` |
| Quit (while paused / game over) | `Q` |

> Note: the in-game "Controls" screen displays Player 2's boost as "Right Shift," but as currently coded it's bound to the **`M`** key — use `M` to boost as Player 2.

### Gameplay Tips

- **Boost** gives roughly 1.5x speed — use it to close the gap on the ball or outrun your opponent, but don't overshoot.
- Angle your car into the ball/puck to control the direction of your hit instead of just ramming it head-on.
- **Ice Hockey mode** is much more slippery than Soccer mode — the puck (and your car) slide a lot further after every hit, so plan ahead.
- Watch the clock — a tied score at zero sends the match to overtime, so a late equalizer isn't the end of the world.

---

## 💻 Setup & Installation

### Requirements

- **Python 3.7+**
- **Pygame 2.0+**

### 1. Clone the repository

```bash
git clone https://github.com/muhammad-moiz-ansari/Rocket-League-2D.git
cd Rocket-League-2D
```

### 2. Install dependencies

```bash
pip install pygame
```

*(Optional but recommended)* Use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install pygame
```

### 3. Run the game

```bash
python main.py
```

The main menu should appear immediately — this folder already includes all textures, fonts, and music, so no extra setup is needed.

---

## 📁 Project Structure

```
Rocket-League-2D/
└── assets/              # Textures, fonts, and music (already included)
    ├── textures/
    ├── fonts/
    └── music/
    └── sfx/
├── main.py              # Entry point — run this file
├── settings.py          # Constants: dimensions, colors, physics, game mode configs
├── assets_loader.py     # Loads images/sounds/fonts, with safe fallbacks
├── physics.py           # Collision & movement math
├── objects.py           # Car, Ball, and Goalkeeper classes
├── menu.py              # Main menu, mode select, controls, how-to-play, match setup
├── game.py              # The match loop (scoring, overtime, pausing, timer, HUD)
├── favicon.ico
├── favicon.png
├── LICENSE
└── README.md
```

---

## 🔧 Customization

Gameplay tuning lives in `settings.py`:

- Screen resolution (`WIDTH`, `HEIGHT`)
- Friction/physics coefficients per game mode (`friction_car`, `friction_ball`)
- Ball/puck speed multiplier and default match duration per mode (`GAME_MODES`)
- Colors and visual constants

---

## 🐛 Troubleshooting

- **`ModuleNotFoundError: No module named 'pygame'`** — run `pip install pygame` in the same Python environment you're using to launch the game.
- **Textures/fonts/music appear missing** — The `assets/` folder already ships with everything needed; make sure you run python `main.py` directly from the root project folder.
- **Player 2's boost doesn't seem to work with Right Shift** — that's expected; boost is actually bound to the `M` key (see the note under [Controls](#controls)).

---

## 📝 License

This project is licensed under the **MIT License** — see [`LICENSE`](./LICENSE) for details.

## 👥 Credits

Created by **Muhammad Moiz Ansari**.