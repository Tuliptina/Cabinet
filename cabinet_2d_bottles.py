"""
🧪 The Fitzroy Cabinet — 2D SVG Bottle Renderer
Each bottle has a unique hand-crafted SVG design.
Supports gaslight/gothic/clinical modes and UV overlay.

BUG FIXES IMPLEMENTED:
- Fixed coordinate clipping by enforcing a static native viewBox (200x300) and scaling via img attributes.
- Encapsulated final SVGs into Base64 Data URIs to prevent Streamlit's `bleach` sanitizer from stripping `<filter>` and `<linearGradient>` tags.
"""

import base64

def get_mode_palette(mode: str) -> dict:
    palettes = {
        "gaslight": {
            "bg": "#0a0705", "card_bg": "#1a1208", "border": "#3d2817",
            "text": "#d4a574", "text_dim": "#8a6a4a", "label_bg": "#fffff0",
            "label_text": "#2a1a0a", "glow": "#ffa04033", "shelf": "#2c1810",
            "shadow": "rgba(0,0,0,0.6)", "highlight": "#ffa040",
        },
        "gothic": {
            "bg": "#050505", "card_bg": "#0a0303", "border": "#330808",
            "text": "#cc0000", "text_dim": "#661111", "label_bg": "#fff0f0",
            "label_text": "#3a0000", "glow": "#ff221133", "shelf": "#1a0505",
            "shadow": "rgba(80,0,0,0.5)", "highlight": "#ff3311",
        },
        "clinical": {
            "bg": "#e8e8e0", "card_bg": "#f5f5f0", "border": "#bbbbaa",
            "text": "#2f4f4f", "text_dim": "#667766", "label_bg": "#ffffff",
            "label_text": "#1a1a1a", "glow": "rgba(0,0,0,0.05)", "shelf": "#ddddcc",
            "shadow": "rgba(0,0,0,0.12)", "highlight": "#4a7a8a",
        },
    }
    return palettes.get(mode, palettes["gaslight"])


def bottle_svg(bottle_id: str, mode: str = "gaslight", selected: bool = False,
               uv: bool = False, size: int = 200, w: int = None, h: int = None, **kwargs) -> str:
    """Return a base64 encoded SVG image tag for a specific bottle."""
    p = get_mode_palette(mode)
    
    # Static native coordinate system to prevent path clipping
    native_w = 200
    native_h = 300
    
    # HTML display size (how large it appears on screen)
    disp_w = w if w is not None else size
    disp_h = h if h is not None else int(size * 1.5)
        
    sel_stroke = p["highlight"] if selected else "none"
    sel_width = 2 if selected else 0

    # UV overlay filter
    uv_filter = ""
    if uv:
        uv_filter = """<filter id="uvglow"><feGaussianBlur stdDeviation="3" result="blur"/>
        <feFlood flood-color="#9944ff" flood-opacity="0.4" result="color"/>
        <feComposite in="color" in2="blur" operator="in" result="glow"/>
        <feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""

    # Common defs
    defs = f"""<defs>
    {uv_filter}
    <filter id="shadow"><feDropShadow dx="1" dy="2" stdDeviation="2" flood-color="{p['shadow']}" flood-opacity="0.5"/></filter>
    <filter id="innershadow"><feOffset dx="0" dy="1"/><feGaussianBlur stdDeviation="1.5"/><feComposite operator="out" in="SourceGraphic"/><feFlood flood-color="#000" flood-opacity="0.15"/><feComposite operator="in" in2=""/><feComposite operator="over" in2="SourceGraphic"/></filter>
    <linearGradient id="glassShine" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="white" stop-opacity="0.25"/><stop offset="50%" stop-color="white" stop-opacity="0.05"/><stop offset="100%" stop-color="white" stop-opacity="0.15"/></linearGradient>
    <linearGradient id="liquidGrad_{bottle_id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="white" stop-opacity="0.15"/><stop offset="100%" stop-color="black" stop-opacity="0.2"/></linearGradient>
    </defs>"""

    # Route to specific bottle renderer
    renderers = {
        "laudanum": _laudanum, "chloroform": _chloroform, "mercury": _mercury,
        "ether": _ether, "strychnine": _strychnine, "arsenic_wafers": _arsenic_wafers,
        "dovers_powder": _dovers_powder, "paregoric": _paregoric,
        "fitzroy_tonic": _fitzroy_tonic, "distilled_blood": _distilled_blood,
        "smelling_salts": _smelling_salts, "belladonna": _belladonna,
    }

    renderer = renderers.get(bottle_id, _default_bottle)
    inner_svg = renderer(bottle_id, p, native_w, native_h, uv)

    uv_attr = 'filter="url(#uvglow)"' if uv else ""

    # Generate raw SVG string
    svg_str = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {native_w} {native_h}" width="{native_w}" height="{native_h}">
    {defs}
    <rect width="{native_w}" height="{native_h}" fill="none" stroke="{sel_stroke}" stroke-width="{sel_width}" rx="8"/>
    <g {uv_attr} filter="url(#shadow)">
    {inner_svg}
    </g>
    </svg>'''
    
    # Base64 encode to completely bypass Streamlit's HTML sanitizer
    b64 = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{disp_w}" height="{disp_h}" style="border-radius:8px; display:inline-block;" />'


# =============================================================================
# INDIVIDUAL BOTTLE RENDERERS
# =============================================================================

def _laudanum(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <path d="M{cx-22},{h-30} Q{cx-25},{h-35} {cx-25},{h-80}
             L{cx-20},{h-85} L{cx-18},{h-130}
             Q{cx-18},{h-140} {cx-12},{h-145}
             L{cx-12},{h-155} Q{cx},{h-162} {cx+12},{h-155}
             L{cx+12},{h-145} Q{cx+18},{h-140} {cx+18},{h-130}
             L{cx+20},{h-85} L{cx+25},{h-80}
             Q{cx+25},{h-35} {cx+22},{h-30} Z"
          fill="#b8860b" fill-opacity="0.7" stroke="#8a6a0b" stroke-width="0.8"/>
    <path d="M{cx-22},{h-30} Q{cx-25},{h-35} {cx-25},{h-80}
             L{cx-20},{h-85} L{cx-18},{h-130}
             Q{cx-18},{h-140} {cx-12},{h-145}
             L{cx-12},{h-155} Q{cx},{h-162} {cx+12},{h-155}
             L{cx+12},{h-145} Q{cx+18},{h-140} {cx+18},{h-130}
             L{cx+20},{h-85} L{cx+25},{h-80}
             Q{cx+25},{h-35} {cx+22},{h-30} Z"
          fill="url(#glassShine)"/>
    <path d="M{cx-23},{h-32} Q{cx-24},{h-35} {cx-24},{h-75}
             L{cx-19},{h-80} L{cx-17},{h-115}
             Q{cx},{h-118} {cx+17},{h-115}
             L{cx+19},{h-80} L{cx+24},{h-75}
             Q{cx+24},{h-35} {cx+23},{h-32} Z"
          fill="#8b4513" fill-opacity="0.75"/>
    <path d="M{cx-23},{h-32} Q{cx-24},{h-35} {cx-24},{h-75}
             L{cx-19},{h-80} L{cx-17},{h-115}
             Q{cx},{h-118} {cx+17},{h-115}
             L{cx+19},{h-80} L{cx+24},{h-75}
             Q{cx+24},{h-35} {cx+23},{h-32} Z"
          fill="url(#liquidGrad_{bid})"/>
    <rect x="{cx-8}" y="{h-170}" width="16" height="14" rx="2" fill="#8b7355" stroke="#6a5a3a" stroke-width="0.5"/>
    <line x1="{cx-6}" y1="{h-166}" x2="{cx+6}" y2="{h-166}" stroke="#6a5a3a" stroke-width="0.3"/>
    <line x1="{cx-6}" y1="{h-162}" x2="{cx+6}" y2="{h-162}" stroke="#6a5a3a" stroke-width="0.3"/>
    <rect x="{cx-28}" y="{h-115}" width="56" height="52" rx="2" fill="{p['label_bg']}" stroke="#8a7a5a" stroke-width="0.6"/>
    <rect x="{cx-26}" y="{h-113}" width="52" height="48" rx="1" fill="none" stroke="#c4a060" stroke-width="0.3"/>
    <text x="{cx}" y="{h-100}" text-anchor="middle" font-family="Georgia,serif" font-size="7" fill="{p['label_text']}" font-weight="bold">LAUDANUM</text>
    <text x="{cx}" y="{h-92}" text-anchor="middle" font-family="Georgia,serif" font-size="5" fill="{p['label_text']}" opacity="0.7">Tinctura Opii</text>
    <line x1="{cx-18}" y1="{h-88}" x2="{cx+18}" y2="{h-88}" stroke="{p['label_text']}" stroke-width="0.3" opacity="0.4"/>
    <circle cx="{cx}" cy="{h-78}" r="5" fill="none" stroke="{p['label_text']}" stroke-width="0.5" opacity="0.6"/>
    <circle cx="{cx-2}" cy="{h-80}" r="1" fill="{p['label_text']}" opacity="0.5"/>
    <circle cx="{cx+2}" cy="{h-80}" r="1" fill="{p['label_text']}" opacity="0.5"/>
    <line x1="{cx-2}" y1="{h-75}" x2="{cx+2}" y2="{h-75}" stroke="{p['label_text']}" stroke-width="0.4" opacity="0.5"/>
    <line x1="{cx+20}" y1="{h-50}" x2="{cx+23}" y2="{h-50}" stroke="#fffff0" stroke-width="0.4" opacity="0.3"/>
    <line x1="{cx+20}" y1="{h-70}" x2="{cx+23}" y2="{h-70}" stroke="#fffff0" stroke-width="0.4" opacity="0.3"/>
    {"" if not uv else f'<text x="{cx}" y="{h-40}" text-anchor="middle" font-family="monospace" font-size="5" fill="#bb88ff" opacity="0.9">3x STANDARD</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Laudanum</text>
    '''


def _chloroform(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <ellipse cx="{cx}" cy="{h-65}" rx="35" ry="40" fill="#2d5a27" fill-opacity="0.65" stroke="#1a3a15" stroke-width="0.8"/>
    <ellipse cx="{cx}" cy="{h-65}" rx="35" ry="40" fill="url(#glassShine)"/>
    <ellipse cx="{cx}" cy="{h-55}" rx="32" ry="30" fill="#1a3a15" fill-opacity="0.7"/>
    <ellipse cx="{cx}" cy="{h-55}" rx="32" ry="30" fill="url(#liquidGrad_{bid})"/>
    <rect x="{cx-10}" y="{h-120}" width="20" height="25" rx="3" fill="#2d5a27" fill-opacity="0.6" stroke="#1a3a15" stroke-width="0.6"/>
    <path d="M{cx-10},{h-120} Q{cx-15},{h-108} {cx-30},{h-95}" fill="none" stroke="#1a3a15" stroke-width="0.6"/>
    <path d="M{cx+10},{h-120} Q{cx+15},{h-108} {cx+30},{h-95}" fill="none" stroke="#1a3a15" stroke-width="0.6"/>
    <rect x="{cx-7}" y="{h-135}" width="14" height="14" rx="2" fill="#8b7355" stroke="#6a5a3a" stroke-width="0.5"/>
    <path d="M{cx-20},{h-128} Q{cx-8},{h-140} {cx},{h-133} Q{cx+8},{h-140} {cx+20},{h-128}"
          fill="none" stroke="#ddddcc" stroke-width="1.5" opacity="0.6"/>
    <path d="M{cx-20},{h-128} L{cx-22},{h-115}" stroke="#ddddcc" stroke-width="1" opacity="0.4"/>
    <path d="M{cx+20},{h-128} L{cx+22},{h-115}" stroke="#ddddcc" stroke-width="1" opacity="0.4"/>
    <rect x="{cx-24}" y="{h-85}" width="48" height="32" rx="1" fill="{p['label_bg']}" stroke="#aaa" stroke-width="0.4" transform="rotate(-3,{cx},{h-69})"/>
    <text x="{cx}" y="{h-72}" text-anchor="middle" font-family="'Segoe Script',cursive,Georgia" font-size="6.5" fill="{p['label_text']}" transform="rotate(-3,{cx},{h-72})">Chloroform</text>
    <text x="{cx}" y="{h-63}" text-anchor="middle" font-family="'Segoe Script',cursive,Georgia" font-size="4.5" fill="{p['label_text']}" opacity="0.6" transform="rotate(-3,{cx},{h-63})">Caution — Volatile</text>
    <path d="M{cx-5},{h-138} Q{cx-3},{h-148} {cx-6},{h-158}" fill="none" stroke="#aaddaa" stroke-width="0.4" opacity="0.3"/>
    <path d="M{cx+3},{h-140} Q{cx+5},{h-150} {cx+2},{h-160}" fill="none" stroke="#aaddaa" stroke-width="0.4" opacity="0.25"/>
    {"" if not uv else f'<text x="{cx}" y="{h-42}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">INCIDENT LOG — NOV 12</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Chloroform</text>
    '''


def _mercury(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <circle cx="{cx}" cy="{h-75}" r="32" fill="#1a3a6a" fill-opacity="0.75" stroke="#0d2040" stroke-width="1"/>
    <circle cx="{cx}" cy="{h-75}" r="32" fill="url(#glassShine)"/>
    <circle cx="{cx}" cy="{h-65}" r="26" fill="#c0c0c0" fill-opacity="0.45"/>
    <ellipse cx="{cx}" cy="{h-58}" rx="20" ry="6" fill="white" fill-opacity="0.1"/>
    <rect x="{cx-8}" y="{h-122}" width="16" height="18" rx="3" fill="#1a3a6a" fill-opacity="0.7" stroke="#0d2040" stroke-width="0.6"/>
    <ellipse cx="{cx}" cy="{h-130}" rx="12" ry="6" fill="#1a1a1a" stroke="#333" stroke-width="0.4"/>
    <circle cx="{cx}" cy="{h-130}" r="4" fill="#2a2a2a" stroke="#444" stroke-width="0.3"/>
    <path d="M{cx-6},{h-126} Q{cx-8},{h-120} {cx-7},{h-116}" fill="#1a1a1a" stroke="none"/>
    <path d="M{cx+5},{h-127} Q{cx+7},{h-121} {cx+6},{h-117}" fill="#1a1a1a" stroke="none"/>
    <rect x="{cx-22}" y="{h-95}" width="44" height="30" rx="3" fill="none" stroke="#4a6a9a" stroke-width="0.8"/>
    <text x="{cx}" y="{h-82}" text-anchor="middle" font-family="Georgia,serif" font-size="5.5" fill="#8aaacc" font-weight="bold" letter-spacing="1">Hg Cl₂</text>
    <text x="{cx}" y="{h-74}" text-anchor="middle" font-family="Georgia,serif" font-size="4" fill="#6a8aaa" opacity="0.8">MERCURIC CHLORIDE</text>
    <text x="{cx+28}" y="{h-50}" font-family="Georgia,serif" font-size="4" fill="#4a6a8a" opacity="0.4" transform="rotate(90,{cx+28},{h-50})">8 oz.</text>
    {"" if not uv else f'<text x="{cx}" y="{h-40}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">BLACKWOOD — PERSONAL</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Mercury</text>
    '''


def _ether(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <rect x="{cx-32}" y="{h-105}" width="64" height="70" rx="6" fill="#d4d4c8" fill-opacity="0.35" stroke="#aaa" stroke-width="0.7"/>
    <rect x="{cx-32}" y="{h-105}" width="64" height="70" rx="6" fill="url(#glassShine)"/>
    <rect x="{cx-29}" y="{h-65}" width="58" height="28" rx="3" fill="#eeeedd" fill-opacity="0.35"/>
    <ellipse cx="{cx}" cy="{h-65}" rx="28" ry="3" fill="white" fill-opacity="0.15"/>
    <rect x="{cx-34}" y="{h-110}" width="68" height="8" rx="3" fill="#d4d4c8" fill-opacity="0.5" stroke="#aaa" stroke-width="0.5"/>
    <path d="M{cx-38},{h-108} Q{cx-20},{h-125} {cx},{h-115} Q{cx+20},{h-125} {cx+38},{h-108}"
          fill="#ddddcc" fill-opacity="0.5" stroke="#bbbbaa" stroke-width="0.5"/>
    <path d="M{cx-38},{h-108} L{cx-42},{h-90}" stroke="#ccccbb" stroke-width="0.8" opacity="0.4"/>
    <path d="M{cx+38},{h-108} L{cx+42},{h-90}" stroke="#ccccbb" stroke-width="0.8" opacity="0.4"/>
    <path d="M{cx-8},{h-120} Q{cx-5},{h-135} {cx-10},{h-148}" fill="none" stroke="#ddddcc" stroke-width="0.5" opacity="0.2"/>
    <path d="M{cx+5},{h-122} Q{cx+8},{h-138} {cx+3},{h-150}" fill="none" stroke="#ddddcc" stroke-width="0.5" opacity="0.18"/>
    <path d="M{cx},{h-118} Q{cx+2},{h-132} {cx-2},{h-145}" fill="none" stroke="#ddddcc" stroke-width="0.5" opacity="0.15"/>
    <text x="{cx-30}" y="{h-50}" font-family="Georgia,serif" font-size="4" fill="#999" opacity="0.4" transform="rotate(-90,{cx-30},{h-50})">AETHER</text>
    <polygon points="{cx-6},{h-85} {cx},{h-93} {cx+6},{h-85}" fill="none" stroke="#aa6600" stroke-width="0.5" opacity="0.5"/>
    <text x="{cx}" y="{h-86}" text-anchor="middle" font-family="sans-serif" font-size="5" fill="#aa6600" opacity="0.5">!</text>
    {"" if not uv else f'<text x="{cx}" y="{h-40}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">FLAMMABLE</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Ether</text>
    '''


def _strychnine(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <path d="M{cx-10},{h-45} L{cx-12},{h-100} Q{cx-12},{h-110} {cx-8},{h-115}
             L{cx-8},{h-130} Q{cx},{h-135} {cx+8},{h-130}
             L{cx+8},{h-115} Q{cx+12},{h-110} {cx+12},{h-100}
             L{cx+10},{h-45} Z"
          fill="#8b0000" fill-opacity="0.8" stroke="#5a0000" stroke-width="0.8"/>
    <path d="M{cx-10},{h-45} L{cx-12},{h-100} Q{cx-12},{h-110} {cx-8},{h-115}
             L{cx-8},{h-130} Q{cx},{h-135} {cx+8},{h-130}
             L{cx+8},{h-115} Q{cx+12},{h-110} {cx+12},{h-100}
             L{cx+10},{h-45} Z"
          fill="url(#glassShine)"/>
    <path d="M{cx-9},{h-47} L{cx-11},{h-95} Q{cx},{h-98} {cx+11},{h-95} L{cx+9},{h-47} Z"
          fill="#4a0000" fill-opacity="0.75"/>
    <rect x="{cx-10}" y="{h-148}" width="20" height="16" rx="2" fill="#b8860b" stroke="#8a6a0b" stroke-width="0.6"/>
    <circle cx="{cx}" cy="{h-140}" r="2" fill="#1a1008"/>
    <rect x="{cx-1}" y="{h-140}" width="2" height="4" fill="#1a1008"/>
    <line x1="{cx-5}" y1="{h-143}" x2="{cx-3}" y2="{h-141}" stroke="#ddc070" stroke-width="0.3" opacity="0.5"/>
    <line x1="{cx+4}" y1="{h-144}" x2="{cx+2}" y2="{h-141}" stroke="#ddc070" stroke-width="0.3" opacity="0.5"/>
    <circle cx="{cx}" cy="{h-82}" r="7" fill="none" stroke="#ff6666" stroke-width="0.6" opacity="0.7"/>
    <circle cx="{cx-2.5}" cy="{h-84}" r="1.2" fill="#ff6666" opacity="0.6"/>
    <circle cx="{cx+2.5}" cy="{h-84}" r="1.2" fill="#ff6666" opacity="0.6"/>
    <path d="M{cx-2},{h-79} Q{cx},{h-78} {cx+2},{h-79}" fill="none" stroke="#ff6666" stroke-width="0.4" opacity="0.6"/>
    <line x1="{cx-8}" y="{h-73}" x2="{cx+8}" y2="{h-68}" stroke="#ff6666" stroke-width="0.6" opacity="0.5"/>
    <line x1="{cx+8}" y="{h-73}" x2="{cx-8}" y2="{h-68}" stroke="#ff6666" stroke-width="0.6" opacity="0.5"/>
    <text x="{cx}" y="{h-58}" text-anchor="middle" font-family="Georgia,serif" font-size="5" fill="#ff4444" letter-spacing="2" opacity="0.7">POISON</text>
    {"" if not uv else f'<text x="{cx}" y="{h-38}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">SCHEDULE I</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Strychnine</text>
    '''


def _arsenic_wafers(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <rect x="{cx-30}" y="{h-80}" width="60" height="35" rx="5" fill="#e8e0c8" stroke="#c4a060" stroke-width="0.8"/>
    <rect x="{cx-27}" y="{h-77}" width="54" height="29" rx="3" fill="none" stroke="#c4a060" stroke-width="0.4"/>
    <rect x="{cx-24}" y="{h-74}" width="48" height="23" rx="2" fill="none" stroke="#c4a060" stroke-width="0.3"/>
    <rect x="{cx-31}" y="{h-90}" width="62" height="12" rx="5" fill="#f0e8d0" stroke="#c4a060" stroke-width="0.6"/>
    <circle cx="{cx-12}" cy="{h-84}" r="3" fill="none" stroke="#c4a060" stroke-width="0.4"/>
    <circle cx="{cx}" cy="{h-84}" r="3" fill="none" stroke="#c4a060" stroke-width="0.4"/>
    <circle cx="{cx+12}" cy="{h-84}" r="3" fill="none" stroke="#c4a060" stroke-width="0.4"/>
    <text x="{cx}" y="{h-63}" text-anchor="middle" font-family="Georgia,serif" font-size="5" fill="#6a5a3a" font-style="italic">Dr. Mackenzie's</text>
    <text x="{cx}" y="{h-56}" text-anchor="middle" font-family="Georgia,serif" font-size="6" fill="#5a4a2a" font-weight="bold">COMPLEXION</text>
    <text x="{cx}" y="{h-49}" text-anchor="middle" font-family="Georgia,serif" font-size="6" fill="#5a4a2a" font-weight="bold">WAFERS</text>
    <path d="M{cx-15},{h-52} Q{cx},{h-55} {cx+15},{h-52}" fill="none" stroke="#c4a060" stroke-width="0.3"/>
    <ellipse cx="{cx}" cy="{h-42}" rx="32" ry="4" fill="black" fill-opacity="0.1"/>
    {"" if not uv else f'<text x="{cx}" y="{h-35}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">PWS CASE FILE #7</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="8" fill="{p['text']}">Arsenic Wafers</text>
    '''


def _dovers_powder(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <path d="M{cx-18},{h-35} L{cx-20},{h-100} Q{cx-20},{h-108} {cx-14},{h-112}
             L{cx-14},{h-135} Q{cx},{h-140} {cx+14},{h-135}
             L{cx+14},{h-112} Q{cx+20},{h-108} {cx+20},{h-100}
             L{cx+18},{h-35} Z"
          fill="#654321" fill-opacity="0.8" stroke="#4a3018" stroke-width="0.7"/>
    <path d="M{cx-18},{h-35} L{cx-20},{h-100} Q{cx-20},{h-108} {cx-14},{h-112}
             L{cx-14},{h-135} Q{cx},{h-140} {cx+14},{h-135}
             L{cx+14},{h-112} Q{cx+20},{h-108} {cx+20},{h-100}
             L{cx+18},{h-35} Z"
          fill="url(#glassShine)"/>
    <path d="M{cx-17},{h-37} L{cx-19},{h-95} Q{cx},{h-98} {cx+19},{h-95} L{cx+17},{h-37} Z"
          fill="#8b7355" fill-opacity="0.7"/>
    <rect x="{cx-8}" y="{h-150}" width="16" height="14" rx="2" fill="#8b7355" stroke="#6a5a3a" stroke-width="0.5"/>
    <rect x="{cx-22}" y="{h-100}" width="44" height="40" rx="1" fill="{p['label_bg']}" stroke="#8a7a5a" stroke-width="0.5"/>
    <text x="{cx}" y="{h-88}" text-anchor="middle" font-family="Georgia,serif" font-size="5.5" fill="{p['label_text']}" font-weight="bold">DOVER'S</text>
    <text x="{cx}" y="{h-81}" text-anchor="middle" font-family="Georgia,serif" font-size="5.5" fill="{p['label_text']}" font-weight="bold">POWDER</text>
    <line x1="{cx-16}" y1="{h-77}" x2="{cx+16}" y2="{h-77}" stroke="{p['label_text']}" stroke-width="0.3" opacity="0.3"/>
    <text x="{cx}" y="{h-71}" text-anchor="middle" font-family="Georgia,serif" font-size="4.5" fill="{p['label_text']}" opacity="0.5" text-decoration="line-through">Dose: 10 grains</text>
    <text x="{cx+4}" y="{h-65}" text-anchor="middle" font-family="'Segoe Script',cursive" font-size="5" fill="#8b0000">25 grains</text>
    {"" if not uv else f'<text x="{cx}" y="{h-40}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">DOSAGE MODIFIED</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Dover's Powder</text>
    '''


def _paregoric(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <path d="M{cx-14},{h-40} L{cx-16},{h-90}
             Q{cx-16},{h-100} {cx-10},{h-105}
             L{cx-10},{h-120} Q{cx},{h-125} {cx+10},{h-120}
             L{cx+10},{h-105} Q{cx+16},{h-100} {cx+16},{h-90}
             L{cx+14},{h-40} Z"
          fill="#c49a6c" fill-opacity="0.75" stroke="#a07850" stroke-width="0.7"/>
    <path d="M{cx-14},{h-40} L{cx-16},{h-90}
             Q{cx-16},{h-100} {cx-10},{h-105}
             L{cx-10},{h-120} Q{cx},{h-125} {cx+10},{h-120}
             L{cx+10},{h-105} Q{cx+16},{h-100} {cx+16},{h-90}
             L{cx+14},{h-40} Z"
          fill="url(#glassShine)"/>
    <path d="M{cx-13},{h-42} L{cx-15},{h-85} Q{cx},{h-88} {cx+15},{h-85} L{cx+13},{h-42} Z"
          fill="#a0724a" fill-opacity="0.7"/>
    <rect x="{cx-6}" y="{h-132}" width="12" height="10" rx="2" fill="#8b7355"/>
    <rect x="{cx-20}" y="{h-100}" width="40" height="42" rx="2" fill="{p['label_bg']}" stroke="#a08860" stroke-width="0.5"/>
    <ellipse cx="{cx}" cy="{h-88}" rx="6" ry="5" fill="none" stroke="{p['label_text']}" stroke-width="0.4" opacity="0.5"/>
    <path d="M{cx-3},{h-86} Q{cx},{h-84} {cx+3},{h-86}" fill="none" stroke="{p['label_text']}" stroke-width="0.3" opacity="0.4"/>
    <text x="{cx-10}" y="{h-90}" font-size="4" fill="{p['label_text']}" opacity="0.3">✦</text>
    <text x="{cx+8}" y="{h-92}" font-size="3" fill="{p['label_text']}" opacity="0.3">✦</text>
    <text x="{cx}" y="{h-76}" text-anchor="middle" font-family="Georgia,serif" font-size="5" fill="{p['label_text']}" font-style="italic">Paregoric</text>
    <text x="{cx}" y="{h-68}" text-anchor="middle" font-family="Georgia,serif" font-size="3.5" fill="{p['label_text']}" opacity="0.6">For the Quieting</text>
    <text x="{cx}" y="{h-63}" text-anchor="middle" font-family="Georgia,serif" font-size="3.5" fill="{p['label_text']}" opacity="0.6">of Infants</text>
    {"" if not uv else f'<text x="{cx}" y="{h-38}" text-anchor="middle" font-family="monospace" font-size="4" fill="#bb88ff">RED ROSE — LOT 34B</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Paregoric</text>
    '''


def _fitzroy_tonic(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <path d="M{cx-18},{h-30} L{cx-20},{h-110}
             Q{cx-20},{h-120} {cx-14},{h-125}
             L{cx-14},{h-148} Q{cx},{h-155} {cx+14},{h-148}
             L{cx+14},{h-125} Q{cx+20},{h-120} {cx+20},{h-110}
             L{cx+18},{h-30} Z"
          fill="#2a4a2a" fill-opacity="0.7" stroke="#1a3a1a" stroke-width="0.8"/>
    <path d="M{cx-18},{h-30} L{cx-20},{h-110}
             Q{cx-20},{h-120} {cx-14},{h-125}
             L{cx-14},{h-148} Q{cx},{h-155} {cx+14},{h-148}
             L{cx+14},{h-125} Q{cx+20},{h-120} {cx+20},{h-110}
             L{cx+18},{h-30} Z"
          fill="url(#glassShine)"/>
    <path d="M{cx-17},{h-32} L{cx-19},{h-105} Q{cx},{h-108} {cx+19},{h-105} L{cx+17},{h-32} Z"
          fill="#3a6a3a" fill-opacity="0.65"/>
    <rect x="{cx-10}" y="{h-165}" width="20" height="15" rx="2" fill="#888" stroke="#666" stroke-width="0.5"/>
    <line x1="{cx-8}" y1="{h-162}" x2="{cx+8}" y2="{h-162}" stroke="#999" stroke-width="0.3"/>
    <line x1="{cx-8}" y1="{h-158}" x2="{cx+8}" y2="{h-158}" stroke="#999" stroke-width="0.3"/>
    <line x1="{cx-8}" y1="{h-154}" x2="{cx+8}" y2="{h-154}" stroke="#999" stroke-width="0.3"/>
    <rect x="{cx-25}" y="{h-108}" width="50" height="55" rx="2" fill="{p['label_bg']}" stroke="#2a4a2a" stroke-width="0.8"/>
    <rect x="{cx-23}" y="{h-106}" width="46" height="51" rx="1" fill="none" stroke="#2a4a2a" stroke-width="0.3"/>
    <text x="{cx}" y="{h-96}" text-anchor="middle" font-family="Georgia,serif" font-size="4.5" fill="#2a4a2a" letter-spacing="2">FITZROY</text>
    <line x1="{cx-18}" y1="{h-93}" x2="{cx+18}" y2="{h-93}" stroke="#2a4a2a" stroke-width="0.3"/>
    <text x="{cx}" y="{h-86}" text-anchor="middle" font-family="Georgia,serif" font-size="6" fill="#1a3a1a" font-weight="bold">PEDIATRIC</text>
    <text x="{cx}" y="{h-78}" text-anchor="middle" font-family="Georgia,serif" font-size="6" fill="#1a3a1a" font-weight="bold">COMPOUND</text>
    <line x1="{cx-18}" y1="{h-74}" x2="{cx+18}" y2="{h-74}" stroke="#2a4a2a" stroke-width="0.3"/>
    <text x="{cx}" y="{h-68}" text-anchor="middle" font-family="Georgia,serif" font-size="3.5" fill="#4a6a4a">Safe for All Ages</text>
    <text x="{cx}" y="{h-58}" text-anchor="middle" font-family="monospace" font-size="3.5" fill="#6a8a6a">Batch 12-A</text>
    {"" if not uv else f'<text x="{cx}" y="{h-38}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">VERIFY DISTRIBUTION</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="8" fill="{p['text']}">Fitzroy's Tonic</text>
    '''


def _distilled_blood(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <rect x="{cx-24}" y="{h-75}" width="48" height="40" rx="4" fill="#3a2010" stroke="#2a1508" stroke-width="0.8"/>
    <rect x="{cx-22}" y="{h-73}" width="44" height="36" rx="3" fill="#4a3020" stroke="#3a2010" stroke-width="0.4"/>
    <line x1="{cx-20}" y1="{h-72}" x2="{cx-20}" y2="{h-38}" stroke="#6a5030" stroke-width="0.3" stroke-dasharray="2,2"/>
    <line x1="{cx+20}" y1="{h-72}" x2="{cx+20}" y2="{h-38}" stroke="#6a5030" stroke-width="0.3" stroke-dasharray="2,2"/>
    <rect x="{cx-8}" y="{h-110}" width="16" height="50" rx="4" fill="#4a0000" fill-opacity="0.85" stroke="#2a0000" stroke-width="0.6"/>
    <rect x="{cx-8}" y="{h-110}" width="16" height="50" rx="4" fill="url(#glassShine)"/>
    <rect x="{cx-6}" y="{h-85}" width="12" height="23" rx="3" fill="#8b0000" fill-opacity="0.8"/>
    <ellipse cx="{cx}" cy="{h-85}" rx="6" ry="2" fill="#aa0000" fill-opacity="0.4"/>
    <rect x="{cx-7}" y="{h-115}" width="14" height="6" rx="1" fill="#222" stroke="#111" stroke-width="0.4"/>
    <ellipse cx="{cx}" cy="{h-118}" rx="8" ry="4" fill="#8b0000" stroke="#5a0000" stroke-width="0.3"/>
    <rect x="{cx-4}" y="{h-38}" width="8" height="4" rx="1" fill="#b8860b" stroke="#8a6a0b" stroke-width="0.3"/>
    {"" if not uv else f'<text x="{cx}" y="{h-25}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">WARREN PROTOCOL</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="8" fill="{p['text']}">Blood Serum</text>
    '''


def _smelling_salts(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <polygon points="{cx},{h-110} {cx+18},{h-100} {cx+22},{h-70} {cx+18},{h-40} {cx-18},{h-40} {cx-22},{h-70} {cx-18},{h-100}"
             fill="#e8e4dc" fill-opacity="0.4" stroke="#ccc" stroke-width="0.5"/>
    <line x1="{cx}" y1="{h-110}" x2="{cx}" y2="{h-40}" stroke="white" stroke-width="0.3" opacity="0.2"/>
    <line x1="{cx-10}" y1="{h-106}" x2="{cx-10}" y2="{h-40}" stroke="white" stroke-width="0.2" opacity="0.15"/>
    <line x1="{cx+10}" y1="{h-106}" x2="{cx+10}" y2="{h-40}" stroke="white" stroke-width="0.2" opacity="0.15"/>
    <circle cx="{cx-8}" cy="{h-85}" r="1.5" fill="white" opacity="0.3"/>
    <circle cx="{cx+12}" cy="{h-65}" r="1" fill="white" opacity="0.25"/>
    <circle cx="{cx+5}" cy="{h-95}" r="1.2" fill="white" opacity="0.2"/>
    <ellipse cx="{cx}" cy="{h-55}" rx="15" ry="12" fill="white" fill-opacity="0.2"/>
    <circle cx="{cx-5}" cy="{h-55}" r="3" fill="white" fill-opacity="0.15"/>
    <circle cx="{cx+4}" cy="{h-50}" r="2.5" fill="white" fill-opacity="0.15"/>
    <circle cx="{cx}" cy="{h-60}" r="2" fill="white" fill-opacity="0.12"/>
    <rect x="{cx-10}" y="{h-125}" width="20" height="16" rx="3" fill="#c0c0c0" stroke="#999" stroke-width="0.5"/>
    <circle cx="{cx}" cy="{h-117}" r="5" fill="none" stroke="#ddd" stroke-width="0.3"/>
    <circle cx="{cx}" cy="{h-117}" r="3" fill="none" stroke="#ddd" stroke-width="0.3"/>
    <rect x="{cx+8}" y="{h-120}" width="4" height="3" rx="1" fill="#aaa"/>
    {"" if not uv else ""}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="8" fill="{p['text']}">Smelling Salts</text>
    '''


def _belladonna(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <path d="M{cx-16},{h-35} Q{cx-20},{h-45} {cx-22},{h-75}
             Q{cx-22},{h-95} {cx-16},{h-105}
             L{cx-12},{h-130} Q{cx-12},{h-140} {cx-8},{h-142}
             L{cx-8},{h-155} Q{cx},{h-160} {cx+8},{h-155}
             L{cx+8},{h-142} Q{cx+12},{h-140} {cx+12},{h-130}
             L{cx+16},{h-105} Q{cx+22},{h-95} {cx+22},{h-75}
             Q{cx+20},{h-45} {cx+16},{h-35} Z"
          fill="#3d1f5a" fill-opacity="0.7" stroke="#2a0a3a" stroke-width="0.8"/>
    <path d="M{cx-16},{h-35} Q{cx-20},{h-45} {cx-22},{h-75}
             Q{cx-22},{h-95} {cx-16},{h-105}
             L{cx-12},{h-130} Q{cx-12},{h-140} {cx-8},{h-142}
             L{cx-8},{h-155} Q{cx},{h-160} {cx+8},{h-155}
             L{cx+8},{h-142} Q{cx+12},{h-140} {cx+12},{h-130}
             L{cx+16},{h-105} Q{cx+22},{h-95} {cx+22},{h-75}
             Q{cx+20},{h-45} {cx+16},{h-35} Z"
          fill="url(#glassShine)"/>
    <path d="M{cx-15},{h-37} Q{cx-19},{h-45} {cx-21},{h-72}
             Q{cx-21},{h-90} {cx-15},{h-100}
             Q{cx},{h-103} {cx+15},{h-100}
             Q{cx+21},{h-90} {cx+21},{h-72}
             Q{cx+19},{h-45} {cx+15},{h-37} Z"
          fill="#2a0a3a" fill-opacity="0.7"/>
    <path d="M{cx-5},{h-158} L{cx-8},{h-168} Q{cx},{h-175} {cx+8},{h-168} L{cx+5},{h-158}"
          fill="#5a3a7a" fill-opacity="0.5" stroke="#4a2a6a" stroke-width="0.4"/>
    <ellipse cx="{cx}" cy="{h-80}" rx="12" ry="7" fill="none" stroke="#9966cc" stroke-width="0.6" opacity="0.7"/>
    <circle cx="{cx}" cy="{h-80}" r="4" fill="none" stroke="#9966cc" stroke-width="0.5" opacity="0.6"/>
    <circle cx="{cx}" cy="{h-80}" r="1.5" fill="#9966cc" opacity="0.5"/>
    <line x1="{cx-10}" y1="{h-85}" x2="{cx-12}" y2="{h-88}" stroke="#9966cc" stroke-width="0.3" opacity="0.5"/>
    <line x1="{cx-6}" y1="{h-87}" x2="{cx-7}" y2="{h-91}" stroke="#9966cc" stroke-width="0.3" opacity="0.5"/>
    <line x1="{cx+6}" y1="{h-87}" x2="{cx+7}" y2="{h-91}" stroke="#9966cc" stroke-width="0.3" opacity="0.5"/>
    <line x1="{cx+10}" y1="{h-85}" x2="{cx+12}" y2="{h-88}" stroke="#9966cc" stroke-width="0.3" opacity="0.5"/>
    <text x="{cx}" y="{h-65}" text-anchor="middle" font-family="Georgia,serif" font-size="5" fill="#bb88dd" font-style="italic" opacity="0.8">Belladonna</text>
    <text x="{cx}" y="{h-58}" text-anchor="middle" font-family="Georgia,serif" font-size="3.5" fill="#9966aa" opacity="0.6">Beautiful Lady</text>
    {"" if not uv else f'<text x="{cx}" y="{h-40}" text-anchor="middle" font-family="monospace" font-size="4" fill="#bb88ff">ORDER OF THE CRIMSON VEIL</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Belladonna</text>
    '''


def _default_bottle(bid, p, w, h, uv):
    cx = w // 2
    return f'''
    <rect x="{cx-15}" y="{h-120}" width="30" height="80" rx="4" fill="#888" fill-opacity="0.5" stroke="#666" stroke-width="0.7"/>
    <rect x="{cx-8}" y="{h-140}" width="16" height="22" rx="3" fill="#888" fill-opacity="0.4" stroke="#666" stroke-width="0.5"/>
    <rect x="{cx-6}" y="{h-150}" width="12" height="12" rx="2" fill="#8b7355"/>
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">{bid}</text>
    '''


# =============================================================================
# MIXING TABLE RESULT SVG
# =============================================================================

def mixing_result_svg(recipe: dict, mode: str = "gaslight", w: int = 400, h: int = 200) -> str:
    """Render a mixing result as a base64 encoded SVG image."""
    p = get_mode_palette(mode)
    danger_color = ["#4a8a4a", "#6a8a3a", "#aa8a2a", "#cc4a2a", "#cc0000"][min(recipe.get("danger", 1) - 1, 4)]
    danger_pips = "● " * recipe.get("danger", 1) + "○ " * (5 - recipe.get("danger", 1))
    rc = recipe.get("result_color", "#888888")

    svg_str = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <radialGradient id="rxglow"><stop offset="0%" stop-color="{rc}" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="{rc}" stop-opacity="0"/></radialGradient>
        <filter id="rxshadow"><feDropShadow dx="0" dy="2" stdDeviation="4" flood-color="black" flood-opacity="0.3"/></filter>
    </defs>
    <rect width="{w}" height="{h}" rx="8" fill="{p['card_bg']}" stroke="{p['border']}" stroke-width="1" filter="url(#rxshadow)"/>
    <ellipse cx="50" cy="{h//2}" rx="35" ry="35" fill="url(#rxglow)"/>
    <path d="M38,{h//2-20} L35,{h//2+15} Q50,{h//2+25} 65,{h//2+15} L62,{h//2-20} Z"
          fill="{rc}" fill-opacity="0.7" stroke="{p['border']}" stroke-width="0.6"/>
    <rect x="42" y="{h//2-30}" width="16" height="12" rx="2" fill="{rc}" fill-opacity="0.5" stroke="{p['border']}" stroke-width="0.4"/>
    <circle cx="47" cy="{h//2}" r="2" fill="white" fill-opacity="0.2"/>
    <circle cx="55" cy="{h//2-8}" r="1.5" fill="white" fill-opacity="0.15"/>
    <circle cx="50" cy="{h//2+5}" r="1" fill="white" fill-opacity="0.1"/>
    <text x="95" y="32" font-family="Georgia,serif" font-size="14" fill="{p['text']}" font-weight="bold">{recipe['name']}</text>
    <text x="95" y="52" font-family="Georgia,serif" font-size="10" fill="{p['text_dim']}">{recipe['description'][:80]}...</text>
    <text x="95" y="{h-45}" font-family="Georgia,serif" font-size="9" fill="{p['text_dim']}">Danger:</text>
    <text x="145" y="{h-45}" font-family="Georgia,serif" font-size="10" fill="{danger_color}">{danger_pips}</text>
    <text x="95" y="{h-20}" font-family="Georgia,serif" font-size="8" fill="{p['text_dim']}" font-style="italic">{recipe.get('lore','')[:90]}...</text>
    </svg>'''
    
    # Base64 encode to completely bypass Streamlit's HTML sanitizer
    b64 = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{w}" height="{h}" style="border-radius: 8px; max-width: 100%; display:inline-block;" />'


# =============================================================================
# INSTRUMENT SVG RENDERERS
# =============================================================================

def _b64_wrap(svg_str: str, disp_w: int, disp_h: int) -> str:
    """Base64 encode an SVG string into an img tag (same pattern as bottles)."""
    b64 = base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')
    return f'<img src="data:image/svg+xml;base64,{b64}" width="{disp_w}" height="{disp_h}" style="border-radius:8px; display:inline-block;" />'


def instrument_svg(instrument_id: str, mode: str = "gaslight", w: int = 160, h: int = 260) -> str:
    """Return a base64 encoded SVG image tag for a surgical instrument."""
    p = get_mode_palette(mode)
    native_w, native_h = 200, 300
    renderers = {
        "scarificator": _inst_scarificator,
        "leech_jar": _inst_leech_jar,
        "trephine": _inst_trephine,
        "amputation_saw": _inst_amputation_saw,
        "syringe": _inst_syringe,
        "scalpel_set": _inst_scalpel_set,
        "cupping_set": _inst_cupping_set,
        "obstetric_forceps": _inst_obstetric_forceps,
    }
    renderer = renderers.get(instrument_id, _inst_default)
    svg_str = renderer(p, native_w, native_h)
    return _b64_wrap(svg_str, w, h)


def _inst_leech_jar(p, w, h):
    """A tall glass jar with murky water and animated leeches."""
    cx = w // 2
    jar_top = 35
    jar_bot = h - 40
    water_top = jar_top + 25
    jar_w = 52
    lid_h = 12

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="lj_glass" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#88bbaa" stop-opacity="0.25"/>
            <stop offset="30%" stop-color="#aaddcc" stop-opacity="0.12"/>
            <stop offset="70%" stop-color="#aaddcc" stop-opacity="0.12"/>
            <stop offset="100%" stop-color="#88bbaa" stop-opacity="0.25"/>
        </linearGradient>
        <linearGradient id="lj_water" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#556644" stop-opacity="0.4"/>
            <stop offset="40%" stop-color="#445533" stop-opacity="0.55"/>
            <stop offset="100%" stop-color="#334422" stop-opacity="0.7"/>
        </linearGradient>
        <linearGradient id="lj_lid" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#ccbb99"/><stop offset="100%" stop-color="#aa9977"/>
        </linearGradient>
        <filter id="lj_murk"><feGaussianBlur stdDeviation="1.5"/></filter>
    </defs>

    <!-- Shadow beneath jar -->
    <ellipse cx="{cx}" cy="{jar_bot + 8}" rx="{jar_w - 5}" ry="6" fill="{p['shadow']}" opacity="0.4"/>

    <!-- Jar body -->
    <rect x="{cx - jar_w}" y="{jar_top}" width="{jar_w * 2}" height="{jar_bot - jar_top}"
          rx="6" fill="url(#lj_glass)" stroke="{p['border']}" stroke-width="0.8"/>

    <!-- Murky water -->
    <rect x="{cx - jar_w + 3}" y="{water_top}" width="{jar_w * 2 - 6}" height="{jar_bot - water_top - 3}"
          rx="4" fill="url(#lj_water)"/>

    <!-- Murky particles -->
    <g filter="url(#lj_murk)" opacity="0.4">
        <circle cx="{cx - 15}" cy="{water_top + 40}" r="8" fill="#445533"/>
        <circle cx="{cx + 20}" cy="{water_top + 70}" r="6" fill="#3a4a2a"/>
        <circle cx="{cx - 5}" cy="{water_top + 90}" r="10" fill="#3d4d2d"/>
        <circle cx="{cx + 10}" cy="{water_top + 30}" r="5" fill="#4a5a3a"/>
    </g>

    <!-- Water surface -->
    <path d="M{cx - jar_w + 8},{water_top} Q{cx},{water_top - 3} {cx + jar_w - 8},{water_top}"
          fill="none" stroke="#aaccaa" stroke-width="0.4" opacity="0.6"/>

    <!-- Leech 1 — curled on glass wall -->
    <path d="M{cx - 30},{water_top + 50} Q{cx - 38},{water_top + 60} {cx - 32},{water_top + 72}
             Q{cx - 26},{water_top + 80} {cx - 30},{water_top + 85}"
          fill="none" stroke="#1a1a0a" stroke-width="4.5" stroke-linecap="round" opacity="0.85"/>
    <ellipse cx="{cx - 30}" cy="{water_top + 48}" rx="3" ry="2.5" fill="#2a2a10" opacity="0.8"/>

    <!-- Leech 2 — swimming S-curve -->
    <path d="M{cx - 8},{water_top + 35} Q{cx + 8},{water_top + 45} {cx - 2},{water_top + 58}
             Q{cx - 12},{water_top + 68} {cx + 2},{water_top + 78}"
          fill="none" stroke="#222210" stroke-width="4" stroke-linecap="round" opacity="0.8"/>
    <ellipse cx="{cx - 8}" cy="{water_top + 33}" rx="2.8" ry="2" fill="#2a2a0a" opacity="0.75"/>

    <!-- Leech 3 — coiled at bottom -->
    <path d="M{cx + 18},{water_top + 95} Q{cx + 28},{water_top + 88} {cx + 22},{water_top + 78}
             Q{cx + 15},{water_top + 72} {cx + 25},{water_top + 68}"
          fill="none" stroke="#1f1f0a" stroke-width="3.8" stroke-linecap="round" opacity="0.75"/>
    <ellipse cx="{cx + 18}" cy="{water_top + 97}" rx="2.5" ry="2" fill="#252510" opacity="0.7"/>

    <!-- Leech segment textures -->
    <g opacity="0.15">
        <line x1="{cx - 4}" y1="{water_top + 42}" x2="{cx + 2}" y2="{water_top + 42}" stroke="#666600" stroke-width="0.5"/>
        <line x1="{cx + 2}" y1="{water_top + 50}" x2="{cx - 4}" y2="{water_top + 50}" stroke="#666600" stroke-width="0.5"/>
        <line x1="{cx - 6}" y1="{water_top + 62}" x2="{cx}" y2="{water_top + 62}" stroke="#666600" stroke-width="0.5"/>
    </g>

    <!-- Glass reflections -->
    <rect x="{cx - jar_w + 4}" y="{jar_top + 10}" width="4" height="{jar_bot - jar_top - 20}"
          rx="2" fill="white" opacity="0.08"/>
    <rect x="{cx + jar_w - 10}" y="{jar_top + 15}" width="2" height="{jar_bot - jar_top - 30}"
          rx="1" fill="white" opacity="0.05"/>

    <!-- Rim -->
    <rect x="{cx - jar_w - 2}" y="{jar_top - 3}" width="{jar_w * 2 + 4}" height="6"
          rx="3" fill="url(#lj_glass)" stroke="{p['border']}" stroke-width="0.6"/>

    <!-- Ceramic lid with perforations -->
    <rect x="{cx - jar_w - 4}" y="{jar_top - lid_h - 3}" width="{jar_w * 2 + 8}" height="{lid_h}"
          rx="4" fill="url(#lj_lid)" stroke="{p['border']}" stroke-width="0.7"/>
    <g fill="{p['border']}" opacity="0.5">
        <circle cx="{cx - 25}" cy="{jar_top - lid_h + 3}" r="1.5"/>
        <circle cx="{cx - 15}" cy="{jar_top - lid_h + 3}" r="1.5"/>
        <circle cx="{cx - 5}" cy="{jar_top - lid_h + 3}" r="1.5"/>
        <circle cx="{cx + 5}" cy="{jar_top - lid_h + 3}" r="1.5"/>
        <circle cx="{cx + 15}" cy="{jar_top - lid_h + 3}" r="1.5"/>
        <circle cx="{cx + 25}" cy="{jar_top - lid_h + 3}" r="1.5"/>
        <circle cx="{cx - 20}" cy="{jar_top - 3}" r="1.5"/>
        <circle cx="{cx - 10}" cy="{jar_top - 3}" r="1.5"/>
        <circle cx="{cx}" cy="{jar_top - 3}" r="1.5"/>
        <circle cx="{cx + 10}" cy="{jar_top - 3}" r="1.5"/>
        <circle cx="{cx + 20}" cy="{jar_top - 3}" r="1.5"/>
    </g>
    <!-- Lid knob -->
    <rect x="{cx - 8}" y="{jar_top - lid_h - 8}" width="16" height="6" rx="3"
          fill="#bbaa88" stroke="{p['border']}" stroke-width="0.5"/>

    <!-- Label -->
    <rect x="{cx - 28}" y="{jar_bot - 30}" width="56" height="22" rx="2"
          fill="{p['label_bg']}" opacity="0.85" stroke="{p['border']}" stroke-width="0.4"/>
    <text x="{cx}" y="{jar_bot - 16}" font-family="Georgia,serif" font-size="7"
          fill="{p['label_text']}" text-anchor="middle" font-style="italic">Hirudo medicinalis</text>
    <text x="{cx}" y="{jar_bot - 9}" font-family="Georgia,serif" font-size="5.5"
          fill="{p['label_text']}" text-anchor="middle" opacity="0.6">LIVE SPECIMENS</text>

    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Leech Jar</text>
    </svg>'''


def _inst_scarificator(p, w, h):
    """Brass spring-loaded bleeding device."""
    cx = w // 2
    bx, by, bw, bh = cx - 35, 60, 70, 45

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="sc_brass" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#c9a83e"/><stop offset="50%" stop-color="#b8860b"/><stop offset="100%" stop-color="#8a6508"/>
        </linearGradient>
        <linearGradient id="sc_steel" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#cccccc"/><stop offset="100%" stop-color="#888888"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 35}" rx="40" ry="5" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Main box -->
    <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4"
          fill="url(#sc_brass)" stroke="{p['border']}" stroke-width="1"/>
    <!-- Lid (slightly open) -->
    <rect x="{bx - 1}" y="{by - 18}" width="{bw + 2}" height="20" rx="4"
          fill="url(#sc_brass)" stroke="{p['border']}" stroke-width="0.8"
          transform="rotate(-8, {bx}, {by})"/>
    <!-- Hinge -->
    <circle cx="{bx + bw - 5}" cy="{by}" r="3" fill="#8a6508" stroke="{p['border']}" stroke-width="0.5"/>
    <!-- Blades visible inside -->
    <g transform="translate({cx - 22}, {by + 8})">
        <rect x="0" y="0" width="44" height="28" rx="2" fill="#1a1208" opacity="0.4"/>
        <!-- Spring coil -->
        <path d="M8,14 Q12,6 16,14 Q20,22 24,14 Q28,6 32,14 Q36,22 40,14"
              fill="none" stroke="url(#sc_steel)" stroke-width="1.2" opacity="0.7"/>
        <!-- Blade slots -->
        <g stroke="#aaaaaa" stroke-width="0.8" opacity="0.5">
            <line x1="6" y1="5" x2="6" y2="24"/><line x1="11" y1="5" x2="11" y2="24"/>
            <line x1="16" y1="5" x2="16" y2="24"/><line x1="21" y1="5" x2="21" y2="24"/>
            <line x1="26" y1="5" x2="26" y2="24"/><line x1="31" y1="5" x2="31" y2="24"/>
            <line x1="36" y1="5" x2="36" y2="24"/>
        </g>
    </g>
    <!-- Release knob -->
    <circle cx="{cx}" cy="{by - 12}" r="6" fill="url(#sc_brass)" stroke="{p['border']}" stroke-width="0.6"/>
    <circle cx="{cx}" cy="{by - 12}" r="2.5" fill="#8a6508"/>
    <!-- Engraving -->
    <text x="{cx}" y="{by + bh + 18}" font-family="Georgia,serif" font-size="8"
          fill="{p['text_dim']}" text-anchor="middle" font-style="italic" opacity="0.7">E.F.</text>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Scarificator</text>
    </svg>'''


def _inst_trephine(p, w, h):
    """Hand-cranked skull drill."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="tr_brass" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#c9a83e"/><stop offset="100%" stop-color="#8a6508"/>
        </linearGradient>
        <linearGradient id="tr_steel" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#cccccc"/><stop offset="100%" stop-color="#777777"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 35}" rx="30" ry="4" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Handle -->
    <rect x="{cx - 10}" y="40" width="20" height="55" rx="10" fill="url(#tr_brass)"
          stroke="{p['border']}" stroke-width="0.8"/>
    <ellipse cx="{cx}" cy="50" rx="12" ry="5" fill="#c9a83e" opacity="0.5"/>
    <ellipse cx="{cx}" cy="80" rx="11" ry="4" fill="#8a6508" opacity="0.3"/>
    <!-- Shaft -->
    <rect x="{cx - 4}" y="95" width="8" height="80" rx="2" fill="url(#tr_steel)"
          stroke="{p['border']}" stroke-width="0.5"/>
    <!-- Circular cutting blade -->
    <circle cx="{cx}" cy="185" r="16" fill="none" stroke="url(#tr_steel)" stroke-width="3"/>
    <circle cx="{cx}" cy="185" r="13" fill="none" stroke="#aaaaaa" stroke-width="0.5" stroke-dasharray="2,2"/>
    <!-- Teeth -->
    <g fill="#999999">
        <rect x="{cx - 1}" y="168" width="2" height="3"/>
        <rect x="{cx + 14}" y="183" width="3" height="2"/>
        <rect x="{cx - 17}" y="183" width="3" height="2"/>
    </g>
    <!-- Crank handle -->
    <line x1="{cx + 10}" y1="55" x2="{cx + 38}" y2="55" stroke="url(#tr_steel)" stroke-width="3" stroke-linecap="round"/>
    <circle cx="{cx + 38}" cy="55" r="5" fill="url(#tr_brass)" stroke="{p['border']}" stroke-width="0.5"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Trephination Drill</text>
    </svg>'''


def _inst_amputation_saw(p, w, h):
    """Bone saw with ivory handle."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="as_ivory" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#fffff0"/><stop offset="100%" stop-color="#d4c8a8"/>
        </linearGradient>
        <linearGradient id="as_steel" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#cccccc"/><stop offset="100%" stop-color="#888888"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 32}" rx="50" ry="4" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Ivory handle with stains -->
    <rect x="{cx - 12}" y="55" width="24" height="65" rx="6" fill="url(#as_ivory)"
          stroke="{p['border']}" stroke-width="0.8"/>
    <ellipse cx="{cx + 3}" cy="85" rx="6" ry="15" fill="#b8a888" opacity="0.3"/>
    <ellipse cx="{cx - 5}" cy="75" rx="4" ry="8" fill="#a09070" opacity="0.2"/>
    <!-- Bolts -->
    <circle cx="{cx}" cy="62" r="2.5" fill="#aaaaaa" stroke="{p['border']}" stroke-width="0.4"/>
    <circle cx="{cx}" cy="112" r="2.5" fill="#aaaaaa" stroke="{p['border']}" stroke-width="0.4"/>
    <!-- Blade spine -->
    <rect x="{cx - 50}" y="125" width="100" height="6" rx="1" fill="url(#as_steel)"
          stroke="{p['border']}" stroke-width="0.5"/>
    <!-- Curved blade -->
    <path d="M{cx - 50},131 Q{cx - 25},180 {cx},185 Q{cx + 25},180 {cx + 50},131"
          fill="url(#as_steel)" stroke="{p['border']}" stroke-width="0.6"/>
    <!-- Teeth -->
    <path d="M{cx - 45},140 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4
             l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4 l2,4 l2,-4"
          fill="none" stroke="#999999" stroke-width="0.5" opacity="0.6"/>
    <text x="{cx}" y="50" font-family="Georgia,serif" font-size="5.5"
          fill="{p['text_dim']}" text-anchor="middle" opacity="0.6">Weiss &amp; Son, London</text>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Amputation Saw</text>
    </svg>'''


def _inst_syringe(p, w, h):
    """Early hypodermic syringe — Pravaz model."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="sy_glass" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#ddddc8" stop-opacity="0.5"/>
            <stop offset="50%" stop-color="#eeeedd" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#ddddc8" stop-opacity="0.5"/>
        </linearGradient>
        <linearGradient id="sy_silver" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#cccccc"/><stop offset="100%" stop-color="#999999"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 32}" rx="15" ry="3" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Finger rings -->
    <ellipse cx="{cx - 15}" cy="50" rx="10" ry="14" fill="none"
             stroke="url(#sy_silver)" stroke-width="2.5"/>
    <ellipse cx="{cx + 15}" cy="50" rx="10" ry="14" fill="none"
             stroke="url(#sy_silver)" stroke-width="2.5"/>
    <!-- Plunger rod -->
    <rect x="{cx - 2}" y="60" width="4" height="30" fill="url(#sy_silver)"
          stroke="{p['border']}" stroke-width="0.3"/>
    <!-- Plunger disc -->
    <rect x="{cx - 9}" y="88" width="18" height="5" rx="2" fill="#aaaaaa"
          stroke="{p['border']}" stroke-width="0.4"/>
    <!-- Glass barrel -->
    <rect x="{cx - 9}" y="93" width="18" height="80" rx="4"
          fill="url(#sy_glass)" stroke="{p['border']}" stroke-width="0.8"/>
    <!-- Measurement marks -->
    <g stroke="{p['text_dim']}" stroke-width="0.4" opacity="0.5">
        <line x1="{cx + 9}" y1="105" x2="{cx + 14}" y2="105"/>
        <line x1="{cx + 9}" y1="115" x2="{cx + 14}" y2="115"/>
        <line x1="{cx + 9}" y1="125" x2="{cx + 14}" y2="125"/>
        <line x1="{cx + 9}" y1="135" x2="{cx + 14}" y2="135"/>
        <line x1="{cx + 9}" y1="145" x2="{cx + 14}" y2="145"/>
        <line x1="{cx + 9}" y1="155" x2="{cx + 14}" y2="155"/>
        <line x1="{cx + 9}" y1="165" x2="{cx + 14}" y2="165"/>
    </g>
    <!-- Residue inside -->
    <rect x="{cx - 6}" y="155" width="12" height="15" rx="2" fill="#88664433" opacity="0.6"/>
    <!-- Silver collar -->
    <rect x="{cx - 10}" y="173" width="20" height="6" rx="2" fill="url(#sy_silver)"
          stroke="{p['border']}" stroke-width="0.4"/>
    <!-- Needle hub -->
    <rect x="{cx - 4}" y="179" width="8" height="10" rx="1" fill="url(#sy_silver)"
          stroke="{p['border']}" stroke-width="0.3"/>
    <!-- Needle -->
    <line x1="{cx}" y1="189" x2="{cx}" y2="215" stroke="#cccccc" stroke-width="1.5"/>
    <line x1="{cx}" y1="215" x2="{cx}" y2="222" stroke="#cccccc" stroke-width="0.8"/>
    <circle cx="{cx}" cy="223" r="0.8" fill="#dddddd"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Hypodermic Syringe</text>
    </svg>'''


def _inst_scalpel_set(p, w, h):
    """Leather roll with graduated scalpels — one missing."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="sk_leather" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#5a3a1a"/><stop offset="100%" stop-color="#3a2008"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 32}" rx="55" ry="5" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Leather roll -->
    <rect x="{cx - 60}" y="50" width="120" height="140" rx="3"
          fill="url(#sk_leather)" stroke="{p['border']}" stroke-width="0.8"/>
    <!-- Stitching -->
    <rect x="{cx - 57}" y="53" width="114" height="134" rx="2" fill="none"
          stroke="#8a6a4a" stroke-width="0.4" stroke-dasharray="3,3" opacity="0.5"/>
    <!-- Slot dividers -->
    <g stroke="#2a1508" stroke-width="0.5" opacity="0.4">
        <line x1="{cx - 45}" y1="65" x2="{cx - 45}" y2="178"/>
        <line x1="{cx - 27}" y1="65" x2="{cx - 27}" y2="178"/>
        <line x1="{cx - 9}" y1="65" x2="{cx - 9}" y2="178"/>
        <line x1="{cx + 9}" y1="65" x2="{cx + 9}" y2="178"/>
        <line x1="{cx + 27}" y1="65" x2="{cx + 27}" y2="178"/>
        <line x1="{cx + 45}" y1="65" x2="{cx + 45}" y2="178"/>
    </g>
    <!-- Scalpels (graduated sizes, #3 EMPTY) -->
    <!-- #1 -->
    <rect x="{cx - 50}" y="105" width="6" height="30" rx="2" fill="#fffff0" stroke="{p['border']}" stroke-width="0.3"/>
    <rect x="{cx - 49}" y="75" width="4" height="32" rx="0.5" fill="#bbbbbb"/>
    <!-- #2 -->
    <rect x="{cx - 32}" y="100" width="7" height="33" rx="2" fill="#fff8e8" stroke="{p['border']}" stroke-width="0.3"/>
    <rect x="{cx - 31}" y="68" width="5" height="35" rx="0.5" fill="#bbbbbb"/>
    <!-- #3 — EMPTY SLOT -->
    <text x="{cx - 10}" y="130" font-family="Georgia,serif" font-size="6"
          fill="#cc4422" text-anchor="middle" opacity="0.7">?</text>
    <!-- #4 -->
    <rect x="{cx + 2}" y="93" width="8" height="38" rx="2" fill="#f8f0e0" stroke="{p['border']}" stroke-width="0.3"/>
    <rect x="{cx + 3}" y="58" width="6" height="38" rx="0.5" fill="#bbbbbb"/>
    <!-- #5 -->
    <rect x="{cx + 20}" y="90" width="8" height="40" rx="2" fill="#fffff0" stroke="{p['border']}" stroke-width="0.3"/>
    <rect x="{cx + 21}" y="55" width="6" height="38" rx="0.5" fill="#aaaaaa"/>
    <!-- #6 -->
    <rect x="{cx + 36}" y="88" width="9" height="42" rx="2" fill="#f0e8d8" stroke="{p['border']}" stroke-width="0.3"/>
    <rect x="{cx + 37}" y="52" width="7" height="39" rx="0.5" fill="#aaaaaa"/>
    <!-- Tie strap -->
    <rect x="{cx - 2}" y="185" width="4" height="20" rx="1" fill="#4a2a10"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Scalpel Set</text>
    </svg>'''


def _inst_cupping_set(p, w, h):
    """Brass cupping set in velvet case."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="cu_brass" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#c9a83e"/><stop offset="100%" stop-color="#8a6508"/>
        </linearGradient>
        <radialGradient id="cu_cup">
            <stop offset="0%" stop-color="#c9a83e"/><stop offset="100%" stop-color="#6a4508"/>
        </radialGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 32}" rx="55" ry="5" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Velvet-lined case -->
    <rect x="{cx - 58}" y="45" width="116" height="150" rx="5"
          fill="#2a0a0a" stroke="{p['border']}" stroke-width="1"/>
    <rect x="{cx - 54}" y="49" width="108" height="142" rx="3" fill="#3a0a0a" opacity="0.6"/>
    <!-- Three graduated brass cups -->
    <ellipse cx="{cx - 28}" cy="90" rx="20" ry="12" fill="url(#cu_cup)" stroke="{p['border']}" stroke-width="0.6"/>
    <ellipse cx="{cx - 28}" cy="87" rx="16" ry="8" fill="#1a0808" opacity="0.4"/>
    <ellipse cx="{cx + 28}" cy="90" rx="18" ry="11" fill="url(#cu_cup)" stroke="{p['border']}" stroke-width="0.6"/>
    <ellipse cx="{cx + 28}" cy="87" rx="14" ry="7" fill="#1a0808" opacity="0.4"/>
    <ellipse cx="{cx}" cy="130" rx="15" ry="9" fill="url(#cu_cup)" stroke="{p['border']}" stroke-width="0.6"/>
    <ellipse cx="{cx}" cy="128" rx="12" ry="6" fill="#1a0808" opacity="0.4"/>
    <!-- Spirit lamp -->
    <rect x="{cx - 8}" y="155" width="16" height="12" rx="3" fill="url(#cu_brass)" stroke="{p['border']}" stroke-width="0.4"/>
    <rect x="{cx - 2}" y="150" width="4" height="6" rx="1" fill="#666666"/>
    <!-- Small blade -->
    <rect x="{cx + 28}" y="150" width="3" height="18" rx="0.5" fill="#bbbbbb"/>
    <rect x="{cx + 26}" y="165" width="7" height="12" rx="2" fill="#5a3a1a"/>
    <!-- Case clasp -->
    <rect x="{cx - 5}" y="42" width="10" height="6" rx="2" fill="url(#cu_brass)" stroke="{p['border']}" stroke-width="0.3"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Cupping Set</text>
    </svg>'''


def _inst_obstetric_forceps(p, w, h):
    """Curved steel obstetric forceps."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="of_steel" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stop-color="#bbbbbb"/><stop offset="100%" stop-color="#888888"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 32}" rx="35" ry="4" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Oilcloth wrapping -->
    <rect x="{cx - 45}" y="140" width="90" height="50" rx="3"
          fill="#8a8a6a" stroke="{p['border']}" stroke-width="0.6" opacity="0.5"/>
    <path d="M{cx - 40},140 Q{cx - 30},130 {cx - 20},138" fill="#8a8a6a" stroke="{p['border']}"
          stroke-width="0.4" opacity="0.4"/>
    <!-- Left arm + blade -->
    <path d="M{cx - 8},55 L{cx - 12},100 Q{cx - 25},145 {cx - 30},170 Q{cx - 28},185 {cx - 15},195"
          fill="none" stroke="url(#of_steel)" stroke-width="5" stroke-linecap="round"/>
    <ellipse cx="{cx - 15}" cy="195" rx="14" ry="20" fill="none" stroke="url(#of_steel)" stroke-width="3"/>
    <!-- Right arm + blade -->
    <path d="M{cx + 8},55 L{cx + 12},100 Q{cx + 25},145 {cx + 30},170 Q{cx + 28},185 {cx + 15},195"
          fill="none" stroke="url(#of_steel)" stroke-width="5" stroke-linecap="round"/>
    <ellipse cx="{cx + 15}" cy="195" rx="14" ry="20" fill="none" stroke="url(#of_steel)" stroke-width="3"/>
    <!-- Ebony handles -->
    <rect x="{cx - 12}" y="45" width="8" height="25" rx="4" fill="#1a1a1a" stroke="{p['border']}" stroke-width="0.5"/>
    <rect x="{cx + 4}" y="45" width="8" height="25" rx="4" fill="#1a1a1a" stroke="{p['border']}" stroke-width="0.5"/>
    <!-- Pivot screw -->
    <circle cx="{cx}" cy="100" r="4" fill="#aaaaaa" stroke="{p['border']}" stroke-width="0.5"/>
    <circle cx="{cx}" cy="100" r="1.5" fill="#666666"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Obstetric Forceps</text>
    </svg>'''


def _inst_default(p, w, h):
    """Fallback instrument."""
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <rect x="{cx - 30}" y="60" width="60" height="120" rx="6"
          fill="{p['card_bg']}" stroke="{p['border']}" stroke-width="1"/>
    <text x="{cx}" y="130" font-family="Georgia,serif" font-size="28"
          fill="{p['text']}" text-anchor="middle">&#x1F52C;</text>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">Instrument</text>
    </svg>'''


# =============================================================================
# SPECIMEN SVG RENDERERS
# =============================================================================

def specimen_svg(specimen_id: str, mode: str = "gaslight", w: int = 160, h: int = 260) -> str:
    """Return a base64 encoded SVG image tag for a specimen."""
    p = get_mode_palette(mode)
    native_w, native_h = 200, 300
    renderers = {
        "heart_jar": _spec_heart,
        "brain_section": _spec_brain,
        "eye_collection": _spec_eyes,
        "hand_bones": _spec_hand,
        "blood_rack": _spec_blood_rack,
        "wax_moulage": _spec_wax,
    }
    renderer = renderers.get(specimen_id, _spec_default)
    svg_str = renderer(p, native_w, native_h)
    return _b64_wrap(svg_str, w, h)


def _spec_heart(p, w, h):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <defs>
        <linearGradient id="sh_liquid" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#88bb88" stop-opacity="0.25"/>
            <stop offset="100%" stop-color="#668866" stop-opacity="0.45"/>
        </linearGradient>
    </defs>
    <ellipse cx="{cx}" cy="{h - 30}" rx="35" ry="5" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Jar -->
    <rect x="{cx - 38}" y="35" width="76" height="160" rx="6"
          fill="#aaddaa11" stroke="{p['border']}" stroke-width="0.8"/>
    <rect x="{cx - 35}" y="50" width="70" height="140" rx="4" fill="url(#sh_liquid)"/>
    <!-- Heart -->
    <path d="M{cx},{180} C{cx - 20},{155} {cx - 30},{130} {cx - 15},{118}
             C{cx - 5},{110} {cx},{118} {cx},{125}
             C{cx},{118} {cx + 5},{110} {cx + 15},{118}
             C{cx + 30},{130} {cx + 20},{155} {cx},{180} Z"
          fill="#993333" fill-opacity="0.8" stroke="#772222" stroke-width="0.8"/>
    <!-- Aorta stub -->
    <rect x="{cx - 5}" y="112" width="10" height="12" rx="3" fill="#884444" opacity="0.7"/>
    <!-- Cork -->
    <rect x="{cx - 40}" y="30" width="80" height="10" rx="4" fill="#aa9977" stroke="{p['border']}" stroke-width="0.5"/>
    <!-- Label -->
    <rect x="{cx - 25}" y="192" width="50" height="16" rx="2" fill="{p['label_bg']}" opacity="0.85"/>
    <text x="{cx}" y="203" font-family="Georgia,serif" font-size="6" fill="{p['label_text']}" text-anchor="middle">Subject 23</text>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9" fill="{p['text']}" text-anchor="middle">Heart in Formaldehyde</text>
    </svg>'''


def _spec_brain(p, w, h):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <ellipse cx="{cx}" cy="{h - 30}" rx="45" ry="5" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Flat display case -->
    <rect x="{cx - 50}" y="60" width="100" height="130" rx="4"
          fill="#ccbbaa11" stroke="{p['border']}" stroke-width="0.8"/>
    <rect x="{cx - 47}" y="63" width="94" height="124" rx="3" fill="#aa998822"/>
    <!-- Brain slice -->
    <ellipse cx="{cx}" cy="125" rx="35" ry="28" fill="#ccaa88" stroke="#aa8866" stroke-width="0.8"/>
    <!-- Sulci -->
    <path d="M{cx - 20},110 Q{cx - 10},118 {cx},110 Q{cx + 10},102 {cx + 20},112"
          fill="none" stroke="#aa8866" stroke-width="0.8" opacity="0.6"/>
    <path d="M{cx - 25},125 Q{cx - 15},132 {cx},125 Q{cx + 15},118 {cx + 25},127"
          fill="none" stroke="#aa8866" stroke-width="0.8" opacity="0.6"/>
    <path d="M{cx - 15},138 Q{cx},145 {cx + 15},138"
          fill="none" stroke="#aa8866" stroke-width="0.6" opacity="0.5"/>
    <!-- White matter -->
    <ellipse cx="{cx}" cy="125" rx="15" ry="12" fill="#ddc8aa" opacity="0.6"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9" fill="{p['text']}" text-anchor="middle">Brain Cross-Section</text>
    </svg>'''


def _spec_blood_rack(p, w, h):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <ellipse cx="{cx}" cy="{h - 32}" rx="55" ry="5" fill="{p['shadow']}" opacity="0.3"/>
    <!-- Wooden rack -->
    <rect x="{cx - 52}" y="130" width="104" height="8" rx="2" fill="#5a3a1a" stroke="{p['border']}" stroke-width="0.5"/>
    <rect x="{cx - 52}" y="165" width="104" height="8" rx="2" fill="#5a3a1a" stroke="{p['border']}" stroke-width="0.5"/>
    <!-- 12 vials with varying blood colors and fill levels -->
    <g>
        <rect x="{cx - 46}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx - 45}" y="80" width="6" height="55" rx="2" fill="#cc0000" opacity="0.7"/>
        <rect x="{cx - 38}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx - 37}" y="85" width="6" height="50" rx="2" fill="#aa0000" opacity="0.65"/>
        <rect x="{cx - 30}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx - 29}" y="75" width="6" height="60" rx="2" fill="#880000" opacity="0.6"/>
        <rect x="{cx - 22}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx - 21}" y="90" width="6" height="45" rx="2" fill="#660000" opacity="0.7"/>
        <rect x="{cx - 14}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx - 13}" y="70" width="6" height="65" rx="2" fill="#bb1111" opacity="0.65"/>
        <rect x="{cx - 6}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx - 5}" y="82" width="6" height="53" rx="2" fill="#991111" opacity="0.6"/>
        <rect x="{cx + 2}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx + 3}" y="88" width="6" height="47" rx="2" fill="#770000" opacity="0.7"/>
        <rect x="{cx + 10}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx + 11}" y="78" width="6" height="57" rx="2" fill="#aa2222" opacity="0.6"/>
        <rect x="{cx + 18}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx + 19}" y="92" width="6" height="43" rx="2" fill="#550000" opacity="0.75"/>
        <rect x="{cx + 26}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx + 27}" y="72" width="6" height="63" rx="2" fill="#cc1100" opacity="0.6"/>
        <rect x="{cx + 34}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx + 35}" y="85" width="6" height="50" rx="2" fill="#881111" opacity="0.65"/>
        <rect x="{cx + 42}" y="55" width="8" height="85" rx="3" fill="#aa000022" stroke="{p['border']}" stroke-width="0.3"/>
        <rect x="{cx + 43}" y="95" width="6" height="40" rx="2" fill="#440000" opacity="0.8"/>
    </g>
    <!-- S.C. labels -->
    <g font-family="Georgia,serif" font-size="4" fill="{p['text_dim']}" opacity="0.5">
        <text x="{cx - 42}" y="52" text-anchor="middle">S.C.</text>
        <text x="{cx - 26}" y="52" text-anchor="middle">S.C.</text>
        <text x="{cx - 10}" y="52" text-anchor="middle">S.C.</text>
        <text x="{cx + 6}" y="52" text-anchor="middle">S.C.</text>
        <text x="{cx + 22}" y="52" text-anchor="middle">S.C.</text>
        <text x="{cx + 38}" y="52" text-anchor="middle">S.C.</text>
    </g>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9" fill="{p['text']}" text-anchor="middle">Blood Sample Rack</text>
    </svg>'''


def _spec_eyes(p, w, h):
    return _spec_default(p, w, h, label="Eyeball Collection")

def _spec_hand(p, w, h):
    return _spec_default(p, w, h, label="Articulated Hand")

def _spec_wax(p, w, h):
    return _spec_default(p, w, h, label="Wax Moulage")


def _spec_default(p, w, h, label="Specimen"):
    cx = w // 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    <ellipse cx="{cx}" cy="{h - 30}" rx="30" ry="4" fill="{p['shadow']}" opacity="0.3"/>
    <rect x="{cx - 35}" y="40" width="70" height="150" rx="6"
          fill="#aaddcc11" stroke="{p['border']}" stroke-width="0.8"/>
    <rect x="{cx - 32}" y="55" width="64" height="130" rx="4" fill="#88aa8822"/>
    <rect x="{cx - 37}" y="35" width="74" height="10" rx="4" fill="#aa9977" stroke="{p['border']}" stroke-width="0.5"/>
    <text x="{cx}" y="{h - 10}" font-family="Georgia,serif" font-size="9"
          fill="{p['text']}" text-anchor="middle">{label}</text>
    </svg>'''
