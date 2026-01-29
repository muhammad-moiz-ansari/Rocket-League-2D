# AI Prompt: Add Professional Menu System to Rocket Soccer 2D Game

## OBJECTIVE
Transform the existing basic Rocket Soccer 2D game into a polished, professional game with a comprehensive interactive menu system, multiple game modes, and enhanced visual presentation.

---

## PROJECT STRUCTURE TO CREATE

Refactor the current single-file game into a modular structure:

```
RocketSoccer/
│
├── main.py              <-- Entry point (Run this file!)
├── settings.py          <-- Game constants (Colors, Dimensions, Physics)
├── assets_loader.py     <-- Handles loading images/sounds/fonts
├── physics.py           <-- Collision detection and resolution
├── objects.py           <-- Game object classes (Car, Ball, Goalkeeper)
├── menu.py              <-- Main Menu system with all screens
├── game.py              <-- Match gameplay loop
│
└── assets/              <-- Asset folder structure
    ├── textures/
    │   ├── menu_bg.png       (1000x600 px - Dark gradient or stadium background)
    │   ├── logo.png          (Transparent PNG, ~400px wide, "ROCKET SOCCER" text)
    │   ├── field_grass.png   (1000x600 px - Green soccer field texture)
    │   ├── field_ice.png     (1000x600 px - Blue/white ice hockey rink texture)
    │   ├── car_red.png       (Top-down view, red sports car, ~50x50px)
    │   ├── car_blue.png      (Top-down view, blue sports car, ~50x50px)
    │   ├── gk_red.png        (Red goalkeeper sprite, ~50x50px)
    │   ├── gk_blue.png       (Blue goalkeeper sprite, ~50x50px)
    │   ├── ball_soccer.png   (Soccer ball, 32x32px)
    │   ├── ball_puck.png     (Ice hockey puck, 32x32px)
    │   ├── button_normal.png (Optional: 300x60px button background)
    │   └── button_hover.png  (Optional: 300x60px button hover state)
    │
    ├── fonts/
    │   ├── main_font.ttf     (Primary: "Orbitron" or "Russo One" - futuristic/sporty)
    │   ├── title_font.ttf    (Title: "Bungee" or "Black Ops One" - bold headers)
    │   └── body_font.ttf     (Readable: "Rajdhani" or "Saira" - instructions/rules)
    │
    ├── music/
    │   ├── menu_music.mp3    (Upbeat electronic music for menus, 2-3 min loop)
    │   └── game_music.mp3    (Energetic gameplay music, 2-3 min loop)
    │
    └── sfx/
        ├── click.wav         (UI button click sound)
        ├── hover.wav         (Button hover sound - subtle)
        ├── goal.wav          (Crowd cheering/whistle)
        ├── bounce.wav        (Ball collision sound)
        └── boost.wav         (Car boost activation sound)
```

---

## MENU SYSTEM SPECIFICATIONS

### **1. MAIN MENU SCREEN**

**Visual Design:**
- Display game logo at top-center (if available, else render "ROCKET SOCCER" in title_font, size 80)
- Background: Use `menu_bg.png` if available, else dark gradient (RGB 20,20,40 to 60,60,80)
- Animated elements: Gently pulsing logo (scale 1.0 to 1.05), floating particles/stars in background
- Footer: Small text "v1.0 | Press ESC to Exit" in bottom-right

**Menu Buttons (Vertical Layout):**
Use main_font, size 40 for all menu buttons. Buttons should be centered with 60px spacing.

1. **PLAY GAME** - Launches game with current settings
2. **GAME MODE** - Opens Game Mode selection submenu
3. **CONTROLS** - Shows controls screen
4. **HOW TO PLAY** - Shows rules and instructions
5. **SETTINGS** - Opens settings submenu (theme selection, music volume, SFX volume)
6. **EXIT** - Quit to desktop

**Button Interaction:**
- Default state: White text with subtle drop shadow
- Hover state: Color changes to orange/yellow (RGB 255,165,0), scale increases 1.1x, play hover.wav
- Click state: Scale down to 0.95x briefly, play click.wav
- Support both mouse click and keyboard navigation (W/S or UP/DOWN to navigate, ENTER to select)

---

### **2. GAME MODE SELECTION SCREEN**

**Layout:**
- Title at top: "SELECT GAME MODE" (title_font, size 60)
- Two large option cards side-by-side (each 400x500px)

**Card 1: SOCCER (Classic)**
- Large soccer ball icon at top
- Title: "CLASSIC SOCCER" (main_font, size 36)
- Description: "Traditional soccer on grass field. Score goals with realistic ball physics!"
- Details:
  - Field: Green grass texture
  - Ball: Standard soccer ball
  - Friction: Normal (0.985)
  - Gameplay: 5 minute default

**Card 2: ICE HOCKEY**
- Large hockey puck icon at top
- Title: "ICE HOCKEY" (main_font, size 36)
- Description: "Fast-paced hockey action on ice! Low friction, high-speed chaos!"
- Details:
  - Field: Blue/white ice rink texture
  - Ball: Hockey puck (smaller, faster)
  - Friction: Very low (0.995) - slippery!
  - Ball speed: 1.2x normal
  - Gameplay: 3 minute default (faster pace)

**Interaction:**
- Hover over card: Brighter border (RGB 100,255,100 for soccer, 100,200,255 for hockey)
- Click to select mode and proceed to duration input
- ESC key returns to main menu

---

### **3. CONTROLS SCREEN**

**Title:** "GAME CONTROLS" (title_font, size 60, centered)

**Layout:** Two-column design for Player 1 (Blue) and Player 2 (Red)

**Content (body_font, size 28):**

```
┌──────────────────────────────────────────────────┐
│                    GAME CONTROLS                 │
├──────────────────────┬───────────────────────────┤
│   PLAYER 1 (BLUE)    │      PLAYER 2 (RED)       │
├──────────────────────┼───────────────────────────┤
│  W - Accelerate      │   ↑ Arrow - Accelerate    │
│  S - Reverse         │   ↓ Arrow - Reverse       │
│  A - Steer Left      │   ← Arrow - Steer Left    │
│  D - Steer Right     │   → Arrow - Steer Right   │
│  Left SHIFT - Boost  │   Right SHIFT - Boost     │
├──────────────────────┴───────────────────────────┤
│                UNIVERSAL CONTROLS                │
├──────────────────────────────────────────────────┤
│  P or ESC - Pause Game                           │
│  During Pause:                                   │
│    • R - Restart Match                           │
│    • M - Return to Main Menu                     │
│    • Q - Quit to Desktop                         │
└──────────────────────────────────────────────────┘
```

**Note at bottom:** "Each team has 1 player + 1 AI Goalkeeper"

**Footer:** "Press ESC or BACKSPACE to Return" (small text, centered)

---

### **4. HOW TO PLAY SCREEN**

**Title:** "HOW TO PLAY" (title_font, size 60)

**Scrollable Text Area** (body_font, size 24, left-aligned with padding):

```
OBJECTIVE:
Score more goals than your opponent before time runs out!

GAME RULES:

1. TEAM COMPOSITION
   • Each team has 2 players:
     - 1 Human-controlled Car
     - 1 AI Goalkeeper (stays near goal)

2. SCORING
   • Push the ball into the opponent's goal to score
   • Goal counts when ball fully crosses the goal line
   • After each goal, all players reset to starting positions
   • Ball is placed at center with random initial direction

3. MATCH DURATION
   • You set the match duration before starting (default: 300 seconds)
   • Game ends when timer reaches zero
   • Team with most goals wins
   • If tied, match ends in a DRAW

4. BOOST MECHANIC
   • Hold SHIFT to activate boost for extra speed
   • Boost gives 1.4x speed and 1.5x acceleration
   • Use strategically to chase the ball or defend

5. PHYSICS
   • Cars have realistic momentum and friction
   • Ball bounces off walls and cars
   • Collisions transfer momentum between objects
   • In ICE HOCKEY mode, friction is reduced for slippery gameplay

6. GOALKEEPER AI
   • Goalkeepers automatically track the ball
   • They defend their goal zone but won't chase far from goal
   • Use teamwork - you handle offense, GK handles defense!

TIPS FOR SUCCESS:
• Use boost wisely - momentum can carry you past the ball!
• Angle your hits to control ball direction
• Defend when needed - preventing goals is as important as scoring
• In Ice Hockey mode, plan ahead - the ball slides much further!

WINNING THE GAME:
• Most goals when time expires = WINNER
• Equal goals = DRAW
• Good sportsmanship always wins! 🏆
```

**Footer:** "Press ESC or BACKSPACE to Return" (centered, small)

---

### **5. SETTINGS SCREEN**

**Title:** "SETTINGS" (title_font, size 60)

**Options Layout (centered, vertical):**

```
SELECT THEME
┌──────────────┬──────────────┬──────────────┐
│  🌿 CLASSIC  │  ❄️ ICE     │  🌙 NIGHT    │
│   (Green)    │   (Blue)     │  (Dark Blue) │
└──────────────┴──────────────┴──────────────┘
```

**Theme Options:**
1. **CLASSIC** - Original green field, white lines
2. **ICE** - Blue/cyan color scheme, ice-like appearance  
3. **NIGHT** - Dark blue/purple field, neon-style lines

**Volume Controls:**
```
MUSIC VOLUME:   [========>---] 80%
SFX VOLUME:     [=========>--] 90%
```
- Use LEFT/RIGHT arrows or click-drag sliders
- Range: 0-100%
- Real-time volume adjustment with preview sounds

**Additional Settings:**
- [ ] Fullscreen Mode (toggle with F key)
- [ ] Show FPS Counter (toggle with C key)

**Footer:** 
- "Press SPACE to Reset to Defaults"
- "Press ESC to Save and Return"

---

## FONTS TO USE

### **Font Priority System:**

1. **Title/Headers** (for "ROCKET SOCCER", screen titles):
   - **Primary:** "Black Ops One" (bold, military/sports style) - Size: 80-100px
   - **Alternative:** "Bungee" (geometric, modern) - Size: 70-90px
   - **Fallback:** Bold system font - Size: 70px

2. **Menu Buttons & UI** (for interactive elements):
   - **Primary:** "Orbitron" (futuristic, clean) - Size: 36-44px
   - **Alternative:** "Russo One" (strong, sporty) - Size: 36-44px
   - **Fallback:** Arial Bold - Size: 36px

3. **Body Text** (instructions, descriptions, rules):
   - **Primary:** "Rajdhani" (modern, readable) - Size: 22-28px
   - **Alternative:** "Saira" (geometric, clear) - Size: 22-28px
   - **Fallback:** Arial - Size: 24px

4. **In-Game HUD** (score, timer during gameplay):
   - **Primary:** "Orbitron" (matches menu consistency) - Size: 32-48px
   - **Fallback:** Bold system font - Size: 36px

### **Font Loading Strategy:**
```python
# In assets_loader.py
def load_font(name, size):
    """Try custom font, fall back to system font if unavailable"""
    path = os.path.join("assets", "fonts", name)
    try:
        return pygame.font.Font(path, size)
    except (FileNotFoundError, pygame.error):
        print(f"Font '{name}' not found. Using system default.")
        return pygame.font.SysFont('Arial', size, bold=True)
```

---

## IMAGES NEEDED

### **Menu Graphics:**
1. **menu_bg.png** (1000x600px)
   - Dark gradient background (stadium atmosphere or abstract tech)
   - Can be dark blue/purple gradient
   - Optional: Subtle stadium lights or particle effects

2. **logo.png** (400px wide, transparent background)
   - "ROCKET SOCCER" text in stylized font
   - Optional: Soccer ball icon integrated
   - Use bright colors (white, orange, yellow)

### **Gameplay Textures:**

3. **field_grass.png** (1000x600px)
   - Green soccer field with white lines
   - Center circle, penalty boxes
   - Grass texture detail

4. **field_ice.png** (1000x600px)
   - Blue/white ice hockey rink
   - Red/blue lines
   - Ice texture with skating marks

5. **car_red.png & car_blue.png** (50x50px each)
   - Top-down view of sports car
   - Car should point to the RIGHT (0°) in base image
   - Transparent background
   - Bold team colors

6. **gk_red.png & gk_blue.png** (50x50px each)
   - Goalkeeper variant (maybe different shape/markings)
   - Or use same car images with different tint

7. **ball_soccer.png** (32x32px)
   - Classic black/white soccer ball pattern
   - Transparent background

8. **ball_puck.png** (32x32px)
   - Black hockey puck
   - Transparent background

### **Optional UI Elements:**
9. **button_normal.png & button_hover.png** (300x60px)
   - Rounded rectangle button backgrounds
   - Normal: Dark semi-transparent
   - Hover: Brighter/glowing version

---

## SOUND REQUIREMENTS

### **Music:**
1. **menu_music.mp3** - Upbeat electronic/synthwave (120-140 BPM), 2-3 min loop
2. **game_music.mp3** - High-energy sports/action music (140-160 BPM), 2-3 min loop

### **Sound Effects:**
3. **click.wav** - Sharp UI click (50-100ms)
4. **hover.wav** - Subtle whoosh/beep (30-50ms)
5. **goal.wav** - Crowd cheer + whistle (1-2 seconds)
6. **bounce.wav** - Ball collision thud (100-200ms)
7. **boost.wav** - Jet engine whoosh (500ms loop)

---

## CODE IMPLEMENTATION REQUIREMENTS

### **Key Features to Implement:**

1. **Smooth Transitions:**
   - Fade in/out effects between screens (200ms duration)
   - Slide animations for menu buttons appearing (stagger 50ms each)

2. **Game Mode System:**
   - Create a `GameMode` class or dictionary storing:
     - Field texture path
     - Ball texture path
     - Friction coefficient
     - Ball speed multiplier
     - Default match duration
   - Pass selected mode to `run_match()` function

3. **Menu State Machine:**
   - Use a state variable to track current screen
   - States: MAIN_MENU, GAME_MODE_SELECT, CONTROLS, HOW_TO_PLAY, SETTINGS, PLAYING
   - Clean navigation with ESC always returning to previous screen

4. **Persistent Settings:**
   - Save settings to `config.json` file:
     - Selected theme
     - Music volume
     - SFX volume
     - Last used game mode
   - Load settings on game startup

5. **Error Handling:**
   - Game must run even if assets are missing
   - Fallback to colored shapes/text for missing images
   - Print warnings but continue execution

6. **Performance:**
   - Maintain 60 FPS in gameplay
   - Menu can run at 30 FPS to save resources
   - Efficient asset caching (load once, reuse)


---

## ADDITIONAL POLISH SUGGESTIONS

1. **Particle Effects:**
   - Goal celebration: Confetti particles
   - Boost trail: Fire particles behind car
   - Ball impact: Small spark effect

2. **Stat Tracking:**
   - Track total goals scored across all games
   - Display in Stats, an option main menu: "Career Goals: X"

3. **Easter Eggs:**
   - Secret "TURBO MODE" unlocked by typing "SPEED" in main menu
   - Doubles all speeds for chaotic gameplay

---

## IMPLEMENTATION CHECKLIST

**Phase 1: Code Refactoring**
- [ ] Split single file into modular structure
- [ ] Create all 7 Python files
- [ ] Ensure game still runs with refactored code

**Phase 2: Asset Loading**
- [ ] Implement robust asset loading with fallbacks
- [ ] Test game with missing assets (should use shapes/defaults)
- [ ] Create assets folder structure

**Phase 3: Menu System**
- [ ] Build main menu with button navigation
- [ ] Implement all menu screens
- [ ] Add keyboard and mouse controls
- [ ] Screen transitions and animations

**Phase 4: Game Modes**
- [ ] Create game mode data structure
- [ ] Implement mode selection
- [ ] Modify gameplay to respect mode settings
- [ ] Add ice hockey physics adjustments

**Phase 5: Settings & Polish**
- [ ] Settings screen with sliders
- [ ] Save/load configuration
- [ ] Add sound effects to all interactions
- [ ] Test all navigation paths

**Phase 6: Final Testing**
- [ ] Test all menu flows
- [ ] Verify both game modes work correctly
- [ ] Confirm all controls work
- [ ] Check performance (60 FPS gameplay)

---

## EXPECTED OUTPUT

When complete, the game should:

1. **Launch** to an attractive main menu with animated logo
2. **Allow** easy navigation with mouse or keyboard
3. **Provide** two distinct game modes with different physics
4. **Display** comprehensive controls and rules
5. **Offer** customization through settings
6. **Maintain** smooth 60 FPS during gameplay
7. **Gracefully handle** missing assets with clear fallbacks
8. **Save** user preferences between sessions

The result should feel like a commercial indie game with professional presentation while maintaining the fun, arcade-style gameplay of the original Rocket Soccer concept.

---

## DELIVERABLES

1. **Complete refactored codebase** (7 Python files)
2. **Asset folder structure** with placeholder text files listing needed assets
3. **README.md** with:
   - Setup instructions
   - Asset requirements
   - Controls guide
   - Troubleshooting tips