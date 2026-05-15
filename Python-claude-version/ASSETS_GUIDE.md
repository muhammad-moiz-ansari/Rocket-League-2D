# Assets Folder Structure

Create this exact folder structure in your project directory:

```
RocketSoccer/
│
├── main.py
├── settings.py
├── assets_loader.py
├── physics.py
├── objects.py
├── menu.py
├── game.py
│
└── assets/                     <-- Create this folder
    │
    ├── textures/               <-- Create this subfolder
    │   ├── menu_bg.png         (1000x600 px - Menu background)
    │   ├── logo.png            (Transparent PNG, ~400px wide)
    │   │
    │   ├── field_grass.png     (1000x600 px - Green soccer field)
    │   ├── field_ice.png       (1000x600 px - Blue ice rink)
    │   ├── field.png           (1000x600 px - Fallback field - OPTIONAL)
    │   │
    │   ├── ball_soccer.png     (32x32 px - Soccer ball)
    │   ├── ball_puck.png       (32x32 px - Hockey puck)
    │   ├── ball.png            (32x32 px - Fallback ball - OPTIONAL)
    │   │
    │   ├── car_blue.png        (50x50 px - Blue player car)
    │   ├── car_red.png         (50x50 px - Red player car)
    │   ├── gk_blue.png         (50x50 px - Blue goalkeeper)
    │   └── gk_red.png          (50x50 px - Red goalkeeper)
    │
    ├── fonts/                  <-- Create this subfolder
    │   ├── main_font.ttf       (UI font - e.g., "Orbitron")
    │   ├── title_font.ttf      (Title font - e.g., "Black Ops One")
    │   └── body_font.ttf       (Body font - e.g., "Rajdhani")
    │
    ├── music/                  <-- Create this subfolder
    │   ├── menu_music.mp3      (2-3 min loop for menus)
    │   └── game_music.mp3      (2-3 min loop for gameplay)
    │
    └── sfx/                    <-- Create this subfolder
        ├── click.wav           (UI click sound)
        ├── hover.wav           (Button hover - OPTIONAL)
        ├── goal.wav            (Goal celebration)
        ├── bounce.wav          (Ball collision - OPTIONAL)
        └── boost.wav           (Boost activation - OPTIONAL)
```

## 📝 Notes

### REQUIRED Assets (Game will look better with these):
- field_grass.png
- field_ice.png
- ball_soccer.png
- ball_puck.png
- All car textures (car_blue, car_red, gk_blue, gk_red)

### OPTIONAL Assets (Game uses fallbacks):
- menu_bg.png (uses gradient)
- logo.png (uses text)
- All fonts (uses system fonts)
- All sounds (game works silently)
- field.png, ball.png (old fallbacks)

### Asset Creation Quick Guide:

**Menu Background (menu_bg.png):**
- Size: 1000x600 pixels
- Style: Dark gradient, stadium atmosphere, or abstract tech
- Colors: Dark blue/purple gradient
- Tool: Any image editor or gradient generator

**Logo (logo.png):**
- Size: ~400px wide (height can vary)
- Text: "ROCKET SOCCER"
- Style: Bold, sporty, gaming font
- Format: PNG with transparent background
- Colors: Bright (white, orange, yellow)

**Field Textures:**
- Grass: Green field with white lines, center circle
- Ice: Blue/white with red/blue hockey lines
- Add grass/ice texture for realism

**Ball Textures:**
- Soccer: Classic black/white pentagon pattern
- Puck: Simple black or dark gray circle

**Car Sprites:**
- Top-down view of car
- Car should face RIGHT (0°) in base image
- Use bold team colors
- Transparent background

**Fonts:**
Download free fonts from Google Fonts:
- Main UI: Orbitron, Russo One
- Titles: Black Ops One, Bungee
- Body: Rajdhani, Saira

**Music:**
Free sources:
- incompetech.com (Kevin MacLeod)
- freemusicarchive.org
- Search for "royalty free electronic sports music"

**Sound Effects:**
Free sources:
- freesound.org
- zapsplat.com
- Quick Sounds (browser-based generator)

## 🎨 Quick Start Without Assets

The game works without ANY assets! It will use:
- Colored shapes for cars and balls
- System fonts for text
- Solid colors for backgrounds
- Silent operation (no sounds)

Simply create the folder structure and run the game to test. Add assets gradually to enhance the experience!

## 🔧 Testing Individual Assets

To test if assets load correctly:
1. Run the game
2. Check console for "Warning: Could not load..." messages
3. Fix file paths/names as needed
4. File names are case-sensitive on Linux/Mac!
