"""
🧪 The Fitzroy Cabinet — 2D SVG Bottle Renderer
Each bottle has a unique hand-crafted SVG design.
Supports gaslight/gothic/clinical modes and UV overlay.

BUG FIXES IMPLEMENTED:
- Stripped newlines from the final SVG returns to prevent Streamlit's 
  Markdown parser from rendering indented SVG lines as raw code blocks.
"""


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
    """Return a complete SVG string for a specific bottle."""
    p = get_mode_palette(mode)
    
    # Handle explicit w/h overrides from the app UI, fallback to size ratios
    if w is None:
        w = size
    if h is None:
        h = int(size * 1.5)
        
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
    inner_svg = renderer(bottle_id, p, w, h, uv)

    uv_attr = 'filter="url(#uvglow)"' if uv else ""

    svg_str = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
    {defs}
    <rect width="{w}" height="{h}" fill="none" stroke="{sel_stroke}" stroke-width="{sel_width}" rx="8"/>
    <g {uv_attr} filter="url(#shadow)">
    {inner_svg}
    </g>
    </svg>'''
    
    # Strip newlines so Streamlit Markdown doesn't parse indented tags as code blocks
    return svg_str.replace('\n', '')


# =============================================================================
# INDIVIDUAL BOTTLE RENDERERS
# =============================================================================

def _laudanum(bid, p, w, h, uv):
    """Tall apothecary bottle — amber glass, ornate label, skull detail"""
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
    """Wide round bottle — dark green, cloth draped, handwritten label"""
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
    """Cobalt blue round bottle — wax-sealed, heavy"""
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
    """Wide-mouth jar — clear glass, cloth over top, shimmer lines"""
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
    """Tiny red vial — locked brass cap, skull and crossbones"""
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
    <line x1="{cx-8}" y1="{h-73}" x2="{cx+8}" y2="{h-68}" stroke="#ff6666" stroke-width="0.6" opacity="0.5"/>
    <line x1="{cx+8}" y1="{h-73}" x2="{cx-8}" y2="{h-68}" stroke="#ff6666" stroke-width="0.6" opacity="0.5"/>
    <text x="{cx}" y="{h-58}" text-anchor="middle" font-family="Georgia,serif" font-size="5" fill="#ff4444" letter-spacing="2" opacity="0.7">POISON</text>
    {"" if not uv else f'<text x="{cx}" y="{h-38}" text-anchor="middle" font-family="monospace" font-size="4.5" fill="#bb88ff">SCHEDULE I</text>'}
    <text x="{cx}" y="{h-10}" text-anchor="middle" font-family="Georgia,serif" font-size="9" fill="{p['text']}">Strychnine</text>
    '''


def _arsenic_wafers(bid, p, w, h, uv):
    """Decorative tin — ornate lid, floral patterns"""
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
    """Brown medicine bottle — standard pharmacy, altered label"""
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
    """Small amber bottle — sleeping child illustration on label"""
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
    """Professional pharmaceutical bottle — printed label, clean design"""
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
    """Dark laboratory vial in leather case"""
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
    """Cut-glass crystal bottle with silver cap"""
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
    """Elegant purple bottle — tapered, ornate, with eye motif"""
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
    """Fallback generic bottle"""
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
    """Render a mixing result as an SVG card."""
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
    
    # Strip newlines so Streamlit Markdown doesn't parse indented tags as code blocks
    return svg_str.replace('\n', '')
