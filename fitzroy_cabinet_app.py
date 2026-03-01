"""
🧪 The Fitzroy Cabinet
A Victorian Apothecary Experience
Standalone Streamlit App — Crimson Rose Series

Explore Dr. Alistair Fitzroy's private collection of medicines,
instruments, and specimens. Every bottle tells a story.
"""

import streamlit as st
import streamlit.components.v1 as components
from cabinet_content import (
    BOTTLES, INSTRUMENTS, SPECIMENS, PERSONAL_ITEMS,
    MIXING_RECIPES, CABINET_SECRETS, SHELF_LABELS,
    get_item_by_id, get_mixing_result, get_bottles_for_mixing,
    check_cabinet_secret,
)
from cabinet_3d import get_cabinet_3d
from cabinet_2d_bottles import bottle_svg, mixing_result_svg, get_mode_palette

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="The Fitzroy Cabinet",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# SESSION STATE
# =============================================================================

defaults = {
    "mode": "gaslight",
    "intensity": 3,
    "examined_items": [],
    "examined_specimens": [],
    "mixed_recipes": [],
    "discovered_secrets": [],
    "selected_bottles": [],
    "current_item": None,
    "uv_mode": False,
    "hidden_drawer_unlocked": False,
    "total_interactions": 0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# =============================================================================
# THEME SYSTEM
# =============================================================================

THEMES = {
    "gaslight": {
        "bg": "#0a0705", "bg2": "#12100c", "card": "#1a1510", "card_hover": "#221d15",
        "text": "#d4a574", "text_dim": "#8a7a6a", "text_bright": "#f0d0a0",
        "accent": "#b8860b", "accent2": "#d4a06a", "border": "#3a2a1a",
        "danger": "#cc4422", "success": "#6a8a4a", "secret": "#b8860b",
        "uv": "#bb88ff", "uv_bg": "#0a0020",
        "gradient": "linear-gradient(135deg, #0a0705 0%, #1a1510 50%, #0a0705 100%)",
        "shelf_bg": "#1f1a12", "glow": "rgba(184,134,11,0.15)",
    },
    "gothic": {
        "bg": "#050505", "bg2": "#0a0505", "card": "#120808", "card_hover": "#1a0a0a",
        "text": "#cc4444", "text_dim": "#773333", "text_bright": "#ff6666",
        "accent": "#8b0000", "accent2": "#cc0000", "border": "#330000",
        "danger": "#ff0000", "success": "#446644", "secret": "#cc0000",
        "uv": "#bb88ff", "uv_bg": "#0a0020",
        "gradient": "linear-gradient(135deg, #050505 0%, #120808 50%, #050505 100%)",
        "shelf_bg": "#0f0505", "glow": "rgba(139,0,0,0.2)",
    },
    "clinical": {
        "bg": "#e8e8e8", "bg2": "#f0f0f0", "card": "#ffffff", "card_hover": "#f5f5f5",
        "text": "#2f4f4f", "text_dim": "#778899", "text_bright": "#1a1a2e",
        "accent": "#4a6670", "accent2": "#2f4f4f", "border": "#cccccc",
        "danger": "#cc3333", "success": "#338833", "secret": "#4a6670",
        "uv": "#6644aa", "uv_bg": "#1a1a2e",
        "gradient": "linear-gradient(135deg, #e8e8e8 0%, #f0f0f0 50%, #e8e8e8 100%)",
        "shelf_bg": "#f5f5f0", "glow": "rgba(74,102,112,0.1)",
    },
}


def get_theme():
    return THEMES[st.session_state.mode]


# =============================================================================
# CSS INJECTION
# =============================================================================

def inject_css():
    t = get_theme()
    mode = st.session_state.mode
    intensity = st.session_state.intensity

    # Progressive intensity effects
    vignette_opacity = 0.3 + intensity * 0.08 if mode != "clinical" else 0.05
    glow_spread = intensity * 2
    text_shadow = f"0 0 {intensity * 3}px {t['accent']}44" if mode != "clinical" else "none"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400&display=swap');

    /* === GLOBAL === */
    .stApp {{
        background: {t['gradient']};
        color: {t['text']};
        font-family: 'EB Garamond', Georgia, serif;
    }}
    .stApp > header {{ background: transparent !important; }}

    /* Main block container */
    .block-container {{
        padding-top: 1.5rem !important;
        max-width: 1200px;
    }}

    /* === TITLE === */
    .cabinet-title {{
        text-align: center;
        padding: 1.2rem 0 0.3rem 0;
        font-family: 'Cormorant Garamond', serif;
    }}
    .cabinet-title h1 {{
        font-size: 2.2rem;
        font-weight: 300;
        letter-spacing: 6px;
        text-transform: uppercase;
        color: {t['text_bright']};
        text-shadow: {text_shadow};
        margin: 0;
    }}
    .cabinet-title .subtitle {{
        font-size: 0.85rem;
        letter-spacing: 4px;
        color: {t['text_dim']};
        font-style: italic;
        margin-top: 4px;
    }}

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0;
        background: {t['card']};
        border-radius: 6px 6px 0 0;
        border-bottom: 1px solid {t['border']};
        padding: 0 0.5rem;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.95rem;
        letter-spacing: 1px;
        color: {t['text_dim']};
        padding: 0.7rem 1.2rem;
        border: none;
        background: transparent;
    }}
    .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: {t['text_bright']};
        border-bottom: 2px solid {t['accent']};
        background: {t['card_hover']};
    }}
    .stTabs [data-baseweb="tab-panel"] {{
        padding-top: 0.5rem;
    }}

    /* === CARDS === */
    .item-card {{
        background: {t['card']};
        border: 1px solid {t['border']};
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'EB Garamond', serif;
    }}
    .item-card:hover {{
        background: {t['card_hover']};
        border-color: {t['accent']}66;
        box-shadow: 0 0 {glow_spread}px {t['glow']};
    }}
    .item-card.examined {{
        border-left: 3px solid {t['accent']};
    }}
    .item-card .card-name {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        font-weight: 600;
        color: {t['text_bright']};
        margin-bottom: 2px;
    }}
    .item-card .card-sub {{
        font-size: 0.78rem;
        color: {t['text_dim']};
        font-style: italic;
        margin-bottom: 6px;
    }}
    .item-card .card-desc {{
        font-size: 0.88rem;
        color: {t['text']};
        line-height: 1.5;
    }}
    .item-card .card-secret {{
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px solid {t['border']};
        font-style: italic;
        color: {t['secret']};
        font-size: 0.85rem;
    }}
    .item-card .card-uv {{
        margin-top: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem;
        color: {t['uv']};
        letter-spacing: 1px;
        background: {t['uv_bg']};
        padding: 4px 8px;
        border-radius: 3px;
        display: inline-block;
    }}
    .item-card .card-medical {{
        margin-top: 8px;
        padding: 8px 10px;
        background: {t['bg2']};
        border-radius: 4px;
        font-size: 0.82rem;
        color: {t['text_dim']};
        line-height: 1.5;
    }}
    .item-card .card-lore {{
        margin-top: 8px;
        padding-top: 8px;
        border-top: 1px dashed {t['border']};
        font-size: 0.82rem;
        color: {t['text']};
        font-style: italic;
        line-height: 1.5;
    }}

    /* === SHELF HEADER === */
    .shelf-header {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        font-weight: 600;
        color: {t['text_bright']};
        letter-spacing: 2px;
        text-transform: uppercase;
        padding: 0.8rem 0 0.4rem 0;
        border-bottom: 1px solid {t['border']};
        margin-bottom: 0.6rem;
    }}

    /* === MIXING TABLE === */
    .mix-station {{
        background: {t['card']};
        border: 1px solid {t['border']};
        border-radius: 8px;
        padding: 1.2rem;
        text-align: center;
    }}
    .mix-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        color: {t['text_bright']};
        letter-spacing: 2px;
        margin-bottom: 0.8rem;
    }}
    .mix-result {{
        margin-top: 1rem;
        padding: 1rem;
        background: {t['bg2']};
        border: 1px solid {t['accent']}44;
        border-radius: 6px;
    }}
    .mix-result .result-name {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        font-weight: 600;
        color: {t['text_bright']};
        margin-bottom: 4px;
    }}
    .mix-result .result-desc {{
        font-size: 0.88rem;
        color: {t['text']};
        line-height: 1.5;
        margin-bottom: 8px;
    }}
    .mix-result .result-lore {{
        font-style: italic;
        color: {t['secret']};
        font-size: 0.85rem;
        line-height: 1.5;
    }}
    .danger-meter {{
        font-size: 0.82rem;
        color: {t['text_dim']};
        margin: 6px 0;
    }}
    .danger-meter .danger-fill {{
        color: {t['danger']};
    }}

    /* === SECRET PANEL === */
    .secret-panel {{
        background: {t['bg2']};
        border: 1px solid {t['accent']}33;
        border-left: 3px solid {t['accent']};
        border-radius: 4px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
    }}
    .secret-panel .secret-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        font-weight: 600;
        color: {t['accent2']};
        margin-bottom: 6px;
    }}
    .secret-panel .secret-text {{
        font-size: 0.88rem;
        color: {t['text']};
        font-style: italic;
        line-height: 1.6;
    }}

    /* === COUNTER BAR === */
    .counter-bar {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: {t['card']}ee;
        border-top: 1px solid {t['border']};
        padding: 0.4rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.82rem;
        color: {t['text_dim']};
        letter-spacing: 1px;
        backdrop-filter: blur(8px);
    }}
    .counter-bar .counter-secrets {{
        color: {t['accent']};
    }}

    /* === FORMULARY === */
    .formulary-entry {{
        background: {t['card']};
        border: 1px solid {t['border']};
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
    }}
    .formulary-entry .f-name {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
        font-weight: 600;
        color: {t['text_bright']};
    }}
    .formulary-entry .f-sub {{
        font-size: 0.75rem;
        color: {t['text_dim']};
        font-style: italic;
    }}
    .formulary-entry .f-desc {{
        font-size: 0.85rem;
        color: {t['text']};
        margin-top: 6px;
        line-height: 1.5;
    }}
    .formulary-entry .f-medical {{
        font-size: 0.8rem;
        color: {t['text_dim']};
        margin-top: 6px;
        padding: 6px 8px;
        background: {t['bg2']};
        border-radius: 3px;
        line-height: 1.5;
    }}

    /* === SELECTBOX & SLIDER overrides === */
    .stSelectbox label, .stSlider label, .stMultiSelect label {{
        font-family: 'Cormorant Garamond', serif !important;
        color: {t['text_dim']} !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        font-size: 0.8rem !important;
    }}

    /* === EXPANDER === */
    .streamlit-expanderHeader {{
        font-family: 'Cormorant Garamond', serif !important;
        color: {t['text']} !important;
        font-size: 0.95rem !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: {t['bg']}; }}
    ::-webkit-scrollbar-thumb {{ background: {t['border']}; border-radius: 3px; }}

    /* Bottom padding for counter bar */
    .block-container {{ padding-bottom: 3.5rem !important; }}

    /* Hide Streamlit elements */
    #MainMenu, footer, .stDeployButton {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)


# =============================================================================
# HELPERS (BUG FIX: Strict Array Reassignment)
# =============================================================================

def record_examination(item_id: str, category: str = "item"):
    """Track that a user examined an item using safe state reassignment."""
    if category == "specimen":
        if item_id not in st.session_state.examined_specimens:
            st.session_state.examined_specimens = st.session_state.examined_specimens + [item_id]
    else:
        if item_id not in st.session_state.examined_items:
            st.session_state.examined_items = st.session_state.examined_items + [item_id]
            
    st.session_state.total_interactions += 1
    check_secrets()


def record_mix(recipe_id: str):
    """Track a discovered recipe using safe state reassignment."""
    if recipe_id not in st.session_state.mixed_recipes:
        st.session_state.mixed_recipes = st.session_state.mixed_recipes + [recipe_id]
        
    st.session_state.total_interactions += 1
    check_secrets()


def check_secrets():
    """Evaluate all cabinet secrets against current state using safe state reassignment."""
    for secret in CABINET_SECRETS:
        if secret["id"] not in st.session_state.discovered_secrets:
            if check_cabinet_secret(
                secret,
                st.session_state.examined_items,
                st.session_state.examined_specimens,
                st.session_state.mixed_recipes,
            ):
                st.session_state.discovered_secrets = st.session_state.discovered_secrets + [secret["id"]]


def render_item_card(item: dict, category: str = "item", show_full: bool = False):
    """Render an item as a styled HTML card."""
    t = get_theme()
    intensity = st.session_state.intensity
    item_id = item["id"]
    is_examined = (item_id in st.session_state.examined_items or
                   item_id in st.session_state.examined_specimens)
    examined_class = "examined" if is_examined else ""

    html = f'<div class="item-card {examined_class}">'
    html += f'<div class="card-name">{item["name"]}</div>'
    if item.get("subtitle"):
        html += f'<div class="card-sub">{item["subtitle"]}</div>'
    html += f'<div class="card-desc">{item["description"]}</div>'

    if show_full:
        # Medical info (always shown in clinical, intensity 2+ otherwise)
        if item.get("medical") and (st.session_state.mode == "clinical" or intensity >= 2):
            html += f'<div class="card-medical">⚕ {item["medical"]}</div>'

        # Secret (intensity 3+)
        if item.get("secret") and intensity >= 3:
            html += f'<div class="card-secret">🔍 {item["secret"]}</div>'

        # Lore (intensity 4+)
        if item.get("lore") and intensity >= 4:
            html += f'<div class="card-lore">📖 {item["lore"]}</div>'

        # UV text (only in UV mode)
        if item.get("uv_text") and st.session_state.uv_mode:
            html += f'<div class="card-uv">🔦 {item["uv_text"]}</div>'

    html += '</div>'
    return html


def danger_meter(level: int) -> str:
    """Render a danger level meter."""
    t = get_theme()
    filled = "◉ " * level
    empty = "○ " * (5 - level)
    return f'<span class="danger-meter">Danger: <span class="danger-fill">{filled}</span>{empty}</span>'


# =============================================================================
# TITLE & CONTROLS
# =============================================================================

inject_css()

st.markdown("""
<div class="cabinet-title">
    <h1>The Fitzroy Cabinet</h1>
    <div class="subtitle">A Victorian Apothecary Collection</div>
</div>
""", unsafe_allow_html=True)

# Controls row
ctrl1, ctrl2, ctrl3, ctrl4 = st.columns([2, 2, 1, 1])
with ctrl1:
    mode = st.selectbox(
        "Mode",
        ["gaslight", "gothic", "clinical"],
        index=["gaslight", "gothic", "clinical"].index(st.session_state.mode),
        key="mode_select",
        format_func=lambda x: {"gaslight": "🕯️ Gaslight", "gothic": "🌹 Gothic", "clinical": "🔬 Clinical"}[x],
    )
    if mode != st.session_state.mode:
        st.session_state.mode = mode
        st.rerun()

with ctrl2:
    intensity = st.slider("Intensity", 1, 5, st.session_state.intensity, key="intensity_slider")
    if intensity != st.session_state.intensity:
        st.session_state.intensity = intensity
        st.rerun()

with ctrl3:
    uv = st.checkbox("🔦 UV", value=st.session_state.uv_mode, key="uv_check")
    if uv != st.session_state.uv_mode:
        st.session_state.uv_mode = uv
        st.rerun()

with ctrl4:
    st.markdown(
        f'<div style="text-align:right;padding-top:28px;font-size:0.85rem;color:{get_theme()["accent"]}">'
        f'🔐 {len(st.session_state.discovered_secrets)}/{len(CABINET_SECRETS)}</div>',
        unsafe_allow_html=True,
    )


# =============================================================================
# TABS
# =============================================================================

tab_cabinet, tab_catalogue, tab_mixing, tab_examination, tab_formulary = st.tabs([
    "🗄️ Cabinet", "📋 Catalogue", "🧪 Mixing Table", "🔬 Examination", "📖 Formulary"
])


# =============================================================================
# TAB 1: 3D CABINET
# =============================================================================

with tab_cabinet:
    cabinet_html = get_cabinet_3d(st.session_state.mode, st.session_state.intensity)
    components.html(cabinet_html, height=650, scrolling=False)

    st.markdown(
        f'<div style="text-align:center;font-size:0.78rem;color:{get_theme()["text_dim"]};'
        f'margin-top:4px;letter-spacing:1px;font-style:italic">'
        f'Drag to orbit · Scroll to zoom · Click items to examine · Use UV button for hidden markings</div>',
        unsafe_allow_html=True,
    )


# =============================================================================
# TAB 2: CATALOGUE
# =============================================================================

with tab_catalogue:
    t = get_theme()

    # Stats bar
    total_items = len(BOTTLES) + len(INSTRUMENTS) + len(SPECIMENS) + len(PERSONAL_ITEMS)
    examined_count = len(st.session_state.examined_items) + len(st.session_state.examined_specimens)
    st.markdown(
        f'<div style="text-align:center;font-size:0.82rem;color:{t["text_dim"]};margin-bottom:1rem">'
        f'Items Examined: <span style="color:{t["accent"]}">{examined_count}</span> / {total_items}'
        f' · Secrets Discovered: <span style="color:{t["accent"]}">'
        f'{len(st.session_state.discovered_secrets)}</span> / {len(CABINET_SECRETS)}'
        f' · Recipes Mixed: <span style="color:{t["accent"]}">'
        f'{len(st.session_state.mixed_recipes)}</span> / {len(MIXING_RECIPES)}</div>',
        unsafe_allow_html=True,
    )

    # Shelf-by-shelf catalogue
    all_shelf_items = {
        0: ("Tinctures & Tonics", [b for b in BOTTLES if b.get("shelf") == 0]),
        1: ("Compounds & Preparations", [b for b in BOTTLES if b.get("shelf") == 1]),
        2: ("Surgical Instruments", INSTRUMENTS),
        3: ("Specimens & Evidence", SPECIMENS),
    }

    for shelf_num, (shelf_name, items) in all_shelf_items.items():
        st.markdown(f'<div class="shelf-header">Shelf {shelf_num + 1} — {shelf_name}</div>',
                    unsafe_allow_html=True)

        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                with st.expander(f"{'✦' if item['id'] in st.session_state.examined_items or item['id'] in st.session_state.examined_specimens else '○'} {item['name']}", expanded=False):
                    st.markdown(render_item_card(item, "item" if shelf_num < 3 else "specimen", show_full=True),
                                unsafe_allow_html=True)
                    cat = "specimen" if shelf_num == 3 else "item"
                    if st.button(f"Mark Examined", key=f"examine_{item['id']}"):
                        record_examination(item["id"], cat)
                        st.rerun()

    # Personal items (bottom drawer)
    if st.session_state.intensity >= 3 or st.session_state.hidden_drawer_unlocked:
        st.markdown('<div class="shelf-header">The Hidden Drawer — Personal Effects</div>',
                    unsafe_allow_html=True)
        cols = st.columns(2)
        for i, item in enumerate(PERSONAL_ITEMS):
            with cols[i % 2]:
                with st.expander(f"{'✦' if item['id'] in st.session_state.examined_items else '○'} {item['name']}", expanded=False):
                    st.markdown(render_item_card(item, "item", show_full=True),
                                unsafe_allow_html=True)
                    if st.button("Mark Examined", key=f"examine_{item['id']}"):
                        record_examination(item["id"], "item")
                        st.rerun()

    # Discovered secrets
    if st.session_state.discovered_secrets:
        st.markdown(f'<div class="shelf-header">Discovered Secrets</div>', unsafe_allow_html=True)
        for secret_id in st.session_state.discovered_secrets:
            secret = next((s for s in CABINET_SECRETS if s["id"] == secret_id), None)
            if secret:
                st.markdown(
                    f'<div class="secret-panel">'
                    f'<div class="secret-title">🔐 {secret["title"]}</div>'
                    f'<div class="secret-text">{secret["content"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# =============================================================================
# TAB 3: MIXING TABLE
# =============================================================================

with tab_mixing:
    t = get_theme()
    mode = st.session_state.mode

    st.markdown(
        f'<div class="mix-title">⚗️ The Mixing Table</div>'
        f'<div style="text-align:center;font-size:0.82rem;color:{t["text_dim"]};margin-bottom:1rem">'
        f'Select two bottles to combine. Some mixtures reveal hidden truths.</div>',
        unsafe_allow_html=True,
    )

    # --- Bottle selector with SVG previews ---
    mix_bottles = get_bottles_for_mixing()
    bottle_names = {b["id"]: b["name"] for b in mix_bottles}
    bottle_ids = [b["id"] for b in mix_bottles]

    mcol1, mcol2 = st.columns(2)

    with mcol1:
        st.markdown(f'<div style="text-align:center;color:{t["text_dim"]};font-size:0.85rem;'
                    f'letter-spacing:2px;margin-bottom:0.5rem">BOTTLE A</div>',
                    unsafe_allow_html=True)
        sel_a = st.selectbox(
            "First ingredient",
            options=["—"] + bottle_ids,
            format_func=lambda x: "Choose a bottle..." if x == "—" else bottle_names.get(x, x),
            key="mix_a",
            label_visibility="collapsed",
        )
        if sel_a != "—":
            svg_a = bottle_svg(sel_a, mode=mode, selected=True, uv=st.session_state.uv_mode)
            st.markdown(
                f'<div style="display:flex;justify-content:center;margin:0.5rem 0">{svg_a}</div>',
                unsafe_allow_html=True,
            )

    with mcol2:
        st.markdown(f'<div style="text-align:center;color:{t["text_dim"]};font-size:0.85rem;'
                    f'letter-spacing:2px;margin-bottom:0.5rem">BOTTLE B</div>',
                    unsafe_allow_html=True)
        # Filter out already-selected bottle
        b_options = ["—"] + [b for b in bottle_ids if b != sel_a]
        sel_b = st.selectbox(
            "Second ingredient",
            options=b_options,
            format_func=lambda x: "Choose a bottle..." if x == "—" else bottle_names.get(x, x),
            key="mix_b",
            label_visibility="collapsed",
        )
        if sel_b != "—":
            svg_b = bottle_svg(sel_b, mode=mode, selected=True, uv=st.session_state.uv_mode)
            st.markdown(
                f'<div style="display:flex;justify-content:center;margin:0.5rem 0">{svg_b}</div>',
                unsafe_allow_html=True,
            )

    # --- Mix button & result ---
    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    if sel_a != "—" and sel_b != "—":
        mix_col1, mix_col2, mix_col3 = st.columns([1, 2, 1])
        with mix_col2:
            if st.button("⚗️  Combine", use_container_width=True, key="mix_btn"):
                recipe = get_mixing_result(sel_a, sel_b)
                if recipe:
                    record_mix(recipe["id"])
                    st.session_state["last_mix_result"] = recipe
                else:
                    st.session_state["last_mix_result"] = {
                        "name": "No Reaction",
                        "description": "These compounds don't interact in any notable way. "
                                       "Perhaps a different combination...",
                        "lore": "",
                        "danger": 0,
                        "result_color": "#888888",
                    }
                st.rerun()

    # Show last result
    last_result = st.session_state.get("last_mix_result")
    if last_result:
        st.markdown("<hr style='border-color:{};opacity:0.3'>".format(t["border"]),
                    unsafe_allow_html=True)

        # SVG result card
        result_svg = mixing_result_svg(last_result, mode=mode, w=500, h=180)
        st.markdown(
            f'<div style="display:flex;justify-content:center;margin:0.8rem 0">{result_svg}</div>',
            unsafe_allow_html=True,
        )

        # Detailed text result
        st.markdown(
            f'<div class="mix-result">'
            f'<div class="result-name">{last_result["name"]}</div>'
            f'{danger_meter(last_result.get("danger", 0))}'
            f'<div class="result-desc">{last_result["description"]}</div>'
            + (f'<div class="result-lore">{last_result["lore"]}</div>' if last_result.get("lore") and st.session_state.intensity >= 3 else "")
            + f'</div>',
            unsafe_allow_html=True,
        )

    # --- Gallery of all bottles ---
    st.markdown(f'<div style="margin-top:1.5rem;padding-top:1rem;border-top:1px solid {t["border"]}">'
                f'<div class="shelf-header">Bottle Collection</div></div>',
                unsafe_allow_html=True)

    bottle_cols = st.columns(4)
    for i, bottle in enumerate(mix_bottles):
        with bottle_cols[i % 4]:
            svg = bottle_svg(bottle["id"], mode=mode, uv=st.session_state.uv_mode, w=100, h=160)
            is_examined = bottle["id"] in st.session_state.examined_items
            border = t["accent"] if is_examined else "transparent"
            st.markdown(
                f'<div style="text-align:center;padding:0.5rem;border:1px solid {border};'
                f'border-radius:6px;margin-bottom:0.5rem;background:{t["card"]}">'
                f'{svg}'
                f'<div style="font-size:0.72rem;color:{t["text"]};margin-top:4px">{bottle["name"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# =============================================================================
# TAB 4: EXAMINATION
# =============================================================================

with tab_examination:
    t = get_theme()

    st.markdown(
        f'<div style="text-align:center;font-size:0.85rem;color:{t["text_dim"]};margin-bottom:1rem">'
        f'Select an item to examine in detail.</div>',
        unsafe_allow_html=True,
    )

    # Build full item list
    all_items = (
        [(b, "Tinctures") for b in BOTTLES]
        + [(inst, "Instruments") for inst in INSTRUMENTS]
        + [(sp, "Specimens") for sp in SPECIMENS]
        + ([(p, "Personal") for p in PERSONAL_ITEMS] if st.session_state.intensity >= 3 else [])
    )
    item_map = {f"{cat}: {item['name']}": item for item, cat in all_items}

    selected_label = st.selectbox(
        "Choose item",
        options=["—"] + list(item_map.keys()),
        key="exam_select",
        label_visibility="collapsed",
    )

    if selected_label != "—":
        item = item_map[selected_label]
        cat = selected_label.split(":")[0].strip()

        # Record examination
        exam_cat = "specimen" if cat == "Specimens" else "item"
        record_examination(item["id"], exam_cat)

        # Two-column layout: SVG bottle (if applicable) + details
        exc1, exc2 = st.columns([1, 2])

        with exc1:
            if item["id"] in [b["id"] for b in BOTTLES]:
                svg = bottle_svg(item["id"], mode=mode, selected=True,
                                 uv=st.session_state.uv_mode, w=160, h=260)
                st.markdown(f'<div style="text-align:center;padding:1rem">{svg}</div>',
                            unsafe_allow_html=True)
            else:
                # Placeholder for non-bottle items
                icon = {"Instruments": "🔪", "Specimens": "🫙", "Personal": "📜"}.get(cat, "📦")
                st.markdown(
                    f'<div style="text-align:center;padding:2rem;font-size:4rem;'
                    f'background:{t["card"]};border-radius:8px;border:1px solid {t["border"]}">'
                    f'{icon}</div>',
                    unsafe_allow_html=True,
                )

        with exc2:
            st.markdown(render_item_card(item, exam_cat, show_full=True),
                        unsafe_allow_html=True)

            # Mixing connections (for bottles)
            if item.get("mixing_tags"):
                st.markdown(f'<div style="margin-top:0.8rem;font-size:0.82rem;color:{t["text_dim"]}">'
                            f'<strong>Properties:</strong> {", ".join(item["mixing_tags"])}</div>',
                            unsafe_allow_html=True)

                # Show known recipes involving this item
                related = [r for r in MIXING_RECIPES if item["id"] in r["ingredients"]]
                if related:
                    discovered = [r for r in related if r["id"] in st.session_state.mixed_recipes]
                    undiscovered = len(related) - len(discovered)
                    if discovered:
                        st.markdown(f'<div style="margin-top:0.5rem;font-size:0.82rem;color:{t["accent"]}">'
                                    f'Known combinations: {", ".join(r["name"] for r in discovered)}</div>',
                                    unsafe_allow_html=True)
                    if undiscovered and st.session_state.intensity >= 4:
                        st.markdown(f'<div style="font-size:0.78rem;color:{t["text_dim"]};font-style:italic">'
                                    f'{undiscovered} undiscovered combination{"s" if undiscovered > 1 else ""}...</div>',
                                    unsafe_allow_html=True)


# =============================================================================
# TAB 5: FORMULARY
# =============================================================================

with tab_formulary:
    t = get_theme()

    st.markdown(
        f'<div style="text-align:center;margin-bottom:1rem">'
        f'<div class="shelf-header">The Formulary</div>'
        f'<div style="font-size:0.82rem;color:{t["text_dim"]};font-style:italic">'
        f'A compendium of every substance in the cabinet.</div></div>',
        unsafe_allow_html=True,
    )

    # Filter
    filter_cat = st.radio(
        "Category",
        ["All", "Tinctures", "Instruments", "Specimens"],
        horizontal=True,
        key="formulary_filter",
        label_visibility="collapsed",
    )

    items_to_show = []
    if filter_cat in ("All", "Tinctures"):
        items_to_show += BOTTLES
    if filter_cat in ("All", "Instruments"):
        items_to_show += INSTRUMENTS
    if filter_cat in ("All", "Specimens"):
        items_to_show += SPECIMENS

    # Search
    search = st.text_input("Search the formulary...", key="formulary_search",
                           label_visibility="collapsed",
                           placeholder="Search by name, description, or property...")
    if search:
        search_lower = search.lower()
        items_to_show = [
            item for item in items_to_show
            if search_lower in item["name"].lower()
            or search_lower in item.get("description", "").lower()
            or search_lower in item.get("subtitle", "").lower()
            or any(search_lower in tag for tag in item.get("mixing_tags", []))
        ]

    for item in items_to_show:
        html = f'<div class="formulary-entry">'
        html += f'<div class="f-name">{item["name"]}</div>'
        if item.get("subtitle"):
            html += f'<div class="f-sub">{item["subtitle"]}</div>'
        html += f'<div class="f-desc">{item["description"]}</div>'
        if item.get("medical") and (st.session_state.mode == "clinical" or st.session_state.intensity >= 2):
            html += f'<div class="f-medical">⚕ {item["medical"]}</div>'
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)


# =============================================================================
# BOTTOM COUNTER BAR
# =============================================================================

t = get_theme()
total_items = len(BOTTLES) + len(INSTRUMENTS) + len(SPECIMENS) + len(PERSONAL_ITEMS)
examined = len(st.session_state.examined_items) + len(st.session_state.examined_specimens)
secrets = len(st.session_state.discovered_secrets)

mode_label = {"gaslight": "🕯️ Gaslight", "gothic": "🌹 Gothic", "clinical": "🔬 Clinical"}[st.session_state.mode]

st.markdown(
    f'<div class="counter-bar">'
    f'<span>{mode_label} · Intensity {st.session_state.intensity}</span>'
    f'<span>Examined: {examined}/{total_items}</span>'
    f'<span>Recipes: {len(st.session_state.mixed_recipes)}/{len(MIXING_RECIPES)}</span>'
    f'<span class="counter-secrets">🔐 Secrets: {secrets}/{len(CABINET_SECRETS)}</span>'
    f'</div>',
    unsafe_allow_html=True,
)
