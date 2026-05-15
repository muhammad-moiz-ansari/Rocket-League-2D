# Rocket Soccer - Professional Menu Edition

A 2-player arcade soccer/hockey game with professional menu system and multiple game modes!

## 🎮 Features

- **Two Game Modes:**
  - **Classic Soccer**: Traditional soccer on grass with normal physics
  - **Ice Hockey**: Fast-paced hockey on ice with slippery physics!

- **Professional Menu System:**
  - Main menu with animated logo
  - Game mode selection
  - Controls screen
  - How to Play guide
  - Settings (music/SFX volume control)

- **Gameplay:**
  - 2v2 matches (2 human players + 2 AI goalkeepers)
  - Boost mechanic for extra speed
  - Realistic ball physics with rotation
  - Customizable match duration
  - Pause/resume functionality

## 📋 Requirements

- Python 3.7+
- Pygame 2.0+

```bash
pip install pygame
```

## 🚀 Quick Start

1. **Install dependencies:**
```bash
pip install pygame
```

2. **Run the game:**
```bash
python main.py
```

3. **Controls:**

**Player 1 (Blue):**
- W/A/S/D - Move
- Left SHIFT - Boost

**Player 2 (Red):**
- Arrow Keys - Move
- Right SHIFT - Boost

**Universal:**
- P or ESC - Pause
- During pause: R (Restart) | M (Menu) | Q (Quit)

## 📁 Project Structure

```
RocketSoccer/
├── main.py              # Entry point
├── settings.py          # Game constants & mode configs
├── assets_loader.py     # Asset loading system
├── physics.py           # Collision physics
├── objects.py           # Game objects (Car, Ball, Goalkeeper)
├── menu.py              # Complete menu system
├── game.py              # Match gameplay loop
├── config.json          # User settings (auto-generated)
└── assets/              # Asset folder (see below)
```

## 🎨 Assets Required

The game will run without assets (using fallback graphics), but for the full experience, add these files:

### Textures (`assets/textures/`)

**Menu Graphics:**
- `menu_bg.png` - 1000x600px dark gradient background
- `logo.png` - Transparent PNG, ~400px wide "ROCKET SOCCER" logo

**Fields:**
- `field_grass.png` - 1000x600px green soccer field
- `field_ice.png` - 1000x600px blue ice hockey rink
- `field.png` - 1000x600px fallback field (optional)

**Balls:**
- `ball_soccer.png` - 32x32px soccer ball
- `ball_puck.png` - 32x32px hockey puck
- `ball.png` - 32x32px fallback ball (optional)

**Cars:**
- `car_blue.png` - 50x50px blue car (top-down view)
- `car_red.png` - 50x50px red car (top-down view)
- `gk_blue.png` - 50x50px blue goalkeeper
- `gk_red.png` - 50x50px red goalkeeper

### Fonts (`assets/fonts/`)

- `main_font.ttf` - Main UI font (e.g., "Orbitron")
- `title_font.ttf` - Title font (e.g., "Black Ops One")
- `body_font.ttf` - Body text font (e.g., "Rajdhani")

**Recommended free fonts:**
- Orbitron: https://fonts.google.com/specimen/Orbitron
- Black Ops One: https://fonts.google.com/specimen/Black+Ops+One
- Rajdhani: https://fonts.google.com/specimen/Rajdhani

### Music (`assets/music/`)

- `menu_music.mp3` - Upbeat electronic music (2-3 min loop)
- `game_music.mp3` - Energetic sports music (2-3 min loop)

### Sound Effects (`assets/sfx/`)

- `click.wav` - UI button click
- `hover.wav` - Button hover sound (optional)
- `goal.wav` - Goal celebration sound
- `bounce.wav` - Ball collision (optional)
- `boost.wav` - Boost activation (optional)

## 🎨 Creating Assets

### Quick Asset Creation Tips:

**For Images:**
- Use tools like GIMP, Photoshop, or online tools
- Keep backgrounds transparent (PNG format)
- Simple solid colors work great for prototypes

**For Sounds:**
- Free sources: freesound.org, zapsplat.com
- Or use online generators for simple beeps/clicks

**For Music:**
- Free sources: incompetech.com, freemusicarchive.org
- Use royalty-free electronic/sports music

## ⚙️ Settings

Settings are saved automatically to `config.json`:

- **Game Mode**: Last selected mode (Soccer/Hockey)
- **Music Volume**: 0-100%
- **SFX Volume**: 0-100%

**Adjust volumes in-game:**
- Settings menu → Use arrow keys
- LEFT/RIGHT: Adjust SFX volume
- CTRL + LEFT/RIGHT: Adjust music volume

## 🎯 Game Modes

### Classic Soccer
- Normal friction (0.985)
- Standard ball physics
- Default: 5 minute matches
- Green grass field

### Ice Hockey
- Low friction (0.995) - Very slippery!
- 1.2x ball speed multiplier
- Default: 3 minute matches
- Blue ice rink

## 🐛 Troubleshooting

**Game runs but no graphics/sounds:**
- Assets are optional - the game uses fallback graphics
- Check the assets folder structure matches the requirements
- Verify file names are exact (case-sensitive on Linux/Mac)

**Font errors:**
- Game will use system fonts if custom fonts are missing
- No impact on gameplay

**Music not playing:**
- Check MP3 files are in `assets/music/`
- Verify pygame.mixer initialized correctly
- Some systems may need different audio formats (try OGG)

## 📝 License

This is a learning/demonstration project. Feel free to modify and extend!

## 🎮 Gameplay Tips

1. **Use boost strategically** - Momentum can carry you past the ball!
2. **Angle your hits** to control ball direction
3. **Defense matters** - preventing goals is as important as scoring
4. **In Ice Hockey mode** - Plan ahead, the ball slides much further!
5. **Teamwork** - Your goalkeeper AI has your back, focus on offense!

## 🔧 Customization

Edit `settings.py` to customize:
- Screen resolution (WIDTH, HEIGHT)
- Physics values (friction coefficients)
- Game mode configurations
- Colors and visual settings

## 👥 Credits

Original game mechanics by the Rocket Soccer team.
Menu system and enhancements by Claude AI.

Enjoy the game! ⚽🏒
