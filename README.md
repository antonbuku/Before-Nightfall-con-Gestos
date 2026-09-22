## Ejecución con reconocimiento de gestos

Para instalar las dependencias y ejecutar el juego, abre una terminal en la carpeta raíz del repositorio y ejecuta los siguientes comandos:

```bash
python3.12 -m pip install -r requirements.txt
python3.12 .\main.py
```

El archivo que contiene la implementación del reconocimiento de gestos se encuentra en la ruta:

`core/gestures.py`

### Funcionamiento de los gestos

| Tecla original | Gesto implementado | Acción |
|---|---|---|
| W | Pulgar recogido | Saltar |
| A | Inclinar izquierda | Mover izquierda |
| S | Puño | Bajar |
| D | Inclinar derecha | Mover derecha |

A continuación, aparece el README del repositorio original

<div align="center">

# Before Nightfall
### A co-op platformer about two friends, a town full of portals, and a setting sun

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/downloads/)
[![pygame-ce](https://img.shields.io/badge/pygame--ce-2.5.7-green?logo=python)](https://pyga.me/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyWeek 41](https://img.shields.io/badge/PyWeek-41-6e5494.svg)](https://pyweek.org/41/)
[![GitHub release](https://img.shields.io/github/release/Walkercito/Python-Game-Jam-2026-.svg)](https://github.com/Walkercito/Python-Game-Jam-2026-/releases)

</div>

---

> *"Fig and Moss lost track of time. Again. Every night, when the last light fades, the portals close. Every single one of them. No warning. No exceptions."*

---

## Overview

**Before Nightfall** is a local and online co-op platformer made for [PyWeek 41](https://pyweek.org/41/). Two friends, **Fig** and **Moss**, need to make it through the town's portals before nightfall closes them all. Work together, press plates, open doors, and platform your way home.

- **Local split-screen co-op** with dynamic LEGO-style camera
- **Online multiplayer** via party codes (LAN or internet with ngrok)
- **Narrated intro** with cinematic typewriter text
- **Multiple levels** with progressive mechanics

Notice: The game is unfinished. It was supposed to have a level 3 and a final level, but it doesn’t even have level 2 complete. I had time, I just didn’t have the creativity to continue and felt too stressed with work. I hope you enjoy what was done.

---

## How to Play

### Controls

| Action | Player 1 (WASD) | Player 2 (Numpad) | Player 2 (Arrows) |
|--------|:---:|:---:|:---:|
| Move | `A` / `D` | `1` / `3` | `←` / `→` |
| Jump | `W` | `5` | `↑` |
| Fast Fall | `S` | `2` | `↓` |

Controls are customizable in Settings. Players can swap between WASD, Numpad, and Arrows.

### Mechanics

- **Pressure plates** - Stand on them to open doors (some close when you step off)
- **Co-op plates** - Color-coded plates that need the right player standing on them
- **Breakable platforms** - They crumble on contact
- **One-way platforms** - Jump through from below, land on top
- **Moving platforms** - Ride them between waypoints
- **Stairs** - Climb up and down
- **Water** - Slower movement, floaty physics
- **Lava** - Get out fast or you're toast
- **Portals** - Reach them to advance to the next level

---

## Installation

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended)

### Setup

```bash
git clone https://github.com/Walkercito/Python-Game-Jam-2026.git
cd Python-Game-Jam-2026
```

**With uv:**
```bash
uv sync
uv run main.py
```

**With pip:**
```bash
pip install -e .
python main.py
```

### Start a specific level
```bash
uv run main.py --level level_001
```

### Pre-built binaries
Check [Releases](https://github.com/Walkercito/Python-Game-Jam-2026-/releases) for Windows, Linux, and macOS builds.

---

## Online Multiplayer

Before Nightfall supports online co-op through party codes:

1. **Host** clicks "Host Party" and gets a 6-digit code
2. **Join** clicks "Join Party" and enters the code

On the same LAN, it works automatically. For internet play, the host can start an ngrok tunnel from the lobby (requires [ngrok](https://ngrok.com/) installed).

---

## Built With

- [pygame-ce](https://pyga.me/) - Game engine
- [pytmx](https://github.com/bitcraft/PyTMX) - TMX map loading
- [repodnet](https://github.com/Walkercito/repodnet) - Networking
- [Tiled](https://www.mapeditor.org/) - Level editor
- [PyInstaller](https://pyinstaller.org/) - Cross-platform builds

---

## Project Structure

```
Before Nightfall/
├── assets/
│   ├── audio/          # Music, SFX, voice lines
│   ├── characters/     # Player spritesheets (green & orange)
│   ├── gui/            # Panels, icons, key prompts
│   ├── tiled/          # TMX maps and tilesets
│   └── vfx/            # Landing dust particles
├── core/
│   ├── config/         # Constants, levels, settings
│   ├── scenes/         # Menu, gameplay, intro, settings, lobby
│   ├── player.py       # Player physics and animation
│   ├── doors.py        # Pressure plate door systems
│   ├── moving_platform.py
│   ├── audio.py        # Centralized audio manager
│   ├── camera.py       # Dynamic split-screen
│   └── ...
└── main.py             # Entry point
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">

Made with <3 by [Walkercito](https://github.com/Walkercito) for [PyWeek 41](https://pyweek.org/41/)

</div>
