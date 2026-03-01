# 🧪 The Fitzroy Cabinet

**A Victorian Apothecary Experience**

An interactive 3D apothecary cabinet built with Streamlit and Three.js. Explore Dr. Alistair Fitzroy's private collection of medicines, surgical instruments, and anatomical specimens — every bottle tells a story.

Part of the **Crimson Rose** interactive fiction series.

---

## ✨ Features

### 3D Interactive Cabinet
- Full Three.js r160 scene with PBR materials, dynamic lighting, and particle effects
- Mahogany cabinet with glass doors, brass hardware, and a flickering candle
- **12 unique bottles** — each with distinct geometry (tall apothecary, cobalt sphere, crystal stopper, decorative tin, and more)
- **8 surgical instruments** — scarificator, leech jar with animated leeches, trephination drill, hypodermic syringe, bone saw, scalpel set (one missing...)
- **6 anatomical specimens** — heart floating in formaldehyde, brain cross-section, blood sample rack
- **7 personal artifacts** — Fitzroy's notebook, a locket, choir sheet music, the Red Rose wax seal
- Click any item for lore tooltips
- Orbit, zoom, and drag controls

### 🔦 UV Blacklight Mode
Toggle ultraviolet light to reveal hidden labels, secret markings, and invisible ink. Every item has a UV layer with clues tied to the story.

### 🧪 Mixing Table
- Select two bottles and combine them
- **10 discoverable recipes** — from the contaminated infant tonic to Thomas's poison ring formula
- Each bottle rendered as a unique hand-crafted SVG with mode-adaptive styling
- Danger rating system (1–5) for each combination
- Results include lore connections and character ties

### Three Visual Modes
| Mode | Atmosphere |
|------|-----------|
| 🕯️ **Gaslight** | Warm amber lighting. The respectable scholar's view. |
| 🌹 **Gothic** | Deep crimson shadows. The cabinet feels alive. |
| 🔬 **Clinical** | Stark white light. Cold. Efficient. Forensic. |

### Progressive Intensity (1–5)
- **Level 1–2**: Descriptions and basic medical information
- **Level 3**: Secrets revealed — hidden histories, tampered labels, unexplained evidence
- **Level 4**: Full lore — character connections, faction ties, narrative implications
- **Level 5**: Everything. The cabinet holds nothing back.

### 🔐 Secret Discovery System
Five hidden secrets unlock based on your interactions:
- Examine enough items
- Trace Sebastian's captivity through objects
- Recreate the contaminated tonic
- Find evidence of the brothers' shared past
- Unlock the hidden drawer

### Five Tabs
| Tab | Content |
|-----|---------|
| 🗄️ **Cabinet** | Interactive 3D scene |
| 📋 **Catalogue** | Shelf-by-shelf inventory with expandable item cards |
| 🧪 **Mixing Table** | Combine bottles, discover recipes, SVG bottle gallery |
| 🔬 **Examination** | Detailed single-item view with full lore |
| 📖 **Formulary** | Searchable reference compendium |

---

## 🚀 Run Locally

```bash
pip install -r requirements.txt
streamlit run fitzroy_cabinet_app.py
```

## ☁️ Deploy to Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set:
   - **Main file path**: `fitzroy_cabinet_app.py`
   - **Python version**: 3.12 (recommended, Cloud default)
4. Deploy

No API keys, secrets, environment variables, or `packages.txt` required. The only dependency is Streamlit itself (≥1.54.0).

---

## 📁 Project Structure

```
fitzroy_cabinet/
├── fitzroy_cabinet_app.py    # Main Streamlit app (UI, tabs, controls)
├── cabinet_content.py        # All item data, recipes, secrets, lore
├── cabinet_3d.py             # Three.js 3D cabinet renderer
├── cabinet_2d_bottles.py     # Hand-crafted SVG bottles & mixing results
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## 🌹 The Crimson Rose Series

The Fitzroy Cabinet is a companion piece to *Whisper of the Crimson Rose*, a historical fiction thriller set in Victorian England exploring medical ethics, institutional corruption, and psychological manipulation.

The cabinet belongs to **Dr. Alistair Fitzroy** — pharmacologist, Red Rose Society operative, and a man who believes knowledge justifies anything. Every bottle, instrument, and specimen connects to the larger narrative of the Crimson Rose world.

---

## 🛠️ Technical Notes

- **Streamlit ≥1.54.0** — same version as the Anatomy Theatre companion app
- **Three.js r160** via cdnjs (classic script tag, no ES modules — compatible with Streamlit's `components.html()`)
- **No external dependencies** beyond Streamlit — all rendering is pure HTML/JS/SVG
- **Session state** tracks examination progress, discovered secrets, and mixed recipes
- SVG bottles are generated server-side with mode-adaptive palettes
- The 3D scene uses PBR materials with physically correct lighting (r155+ intensity calibration)
- **Community Cloud compatible** — tested with Python 3.12, no `packages.txt` needed

---

*"Every item in this cabinet tells the same story: a brilliant man who believed knowledge justified anything."*
