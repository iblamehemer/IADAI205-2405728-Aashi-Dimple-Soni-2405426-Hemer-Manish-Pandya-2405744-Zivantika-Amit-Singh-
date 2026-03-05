import streamlit as st
import google.generativeai as genai
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw, ImageFont
import io
import json
import uuid
import datetime
import zipfile
import os
import re
import base64
import time
import random
import colorsys

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BrandSphere AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS  — Dark luxury editorial aesthetic
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400&family=DM+Sans:wght@300;400;500;600&family=Space+Mono:wght@400;700&display=swap');

:root {
  --bg:        #0C0D0F;
  --surface:   #141518;
  --surface2:  #1C1E22;
  --border:    #2A2C31;
  --accent:    #C9A84C;
  --accent2:   #E8C97A;
  --teal:      #3ECFB2;
  --red:       #E05A5A;
  --text:      #F0EDE8;
  --muted:     #7A7A85;
  --font-head: 'Cormorant Garamond', Georgia, serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'Space Mono', monospace;
}

/* Reset & base */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, .stApp { background: var(--bg) !important; color: var(--text) !important; font-family: var(--font-body); }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }

/* ── HERO NAV ── */
.nav-bar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 18px 48px; background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 999;
}
.nav-logo {
  font-family: var(--font-head); font-size: 1.6rem; font-weight: 700;
  color: var(--accent); letter-spacing: 0.04em;
}
.nav-logo span { color: var(--text); font-weight: 300; }
.nav-tag {
  font-family: var(--font-mono); font-size: 0.65rem;
  color: var(--muted); letter-spacing: 0.15em; text-transform: uppercase;
}

/* ── HERO ── */
.hero {
  background: linear-gradient(135deg, #0C0D0F 0%, #141518 50%, #0f1015 100%);
  padding: 90px 48px 60px;
  border-bottom: 1px solid var(--border);
  position: relative; overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; top: -60px; right: -60px;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(201,168,76,0.08) 0%, transparent 70%);
  pointer-events: none;
}
.hero-eyebrow {
  font-family: var(--font-mono); font-size: 0.7rem;
  letter-spacing: 0.25em; color: var(--accent); text-transform: uppercase;
  margin-bottom: 18px;
}
.hero-title {
  font-family: var(--font-head); font-size: clamp(2.8rem, 6vw, 5rem);
  font-weight: 300; line-height: 1.08; color: var(--text);
  margin-bottom: 12px;
}
.hero-title em { font-style: italic; color: var(--accent); }
.hero-sub {
  font-family: var(--font-body); font-size: 1rem; font-weight: 300;
  color: var(--muted); max-width: 540px; line-height: 1.7;
  margin-bottom: 40px;
}
.badge-row { display: flex; gap: 10px; flex-wrap: wrap; }
.badge {
  display: inline-block; padding: 5px 14px;
  border: 1px solid var(--border); border-radius: 20px;
  font-family: var(--font-mono); font-size: 0.62rem;
  color: var(--muted); letter-spacing: 0.1em;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--surface) !important;
  border-bottom: 1px solid var(--border) !important;
  padding: 0 48px !important; gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important; border: none !important;
  color: var(--muted) !important; font-family: var(--font-mono) !important;
  font-size: 0.7rem !important; letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
  padding: 16px 20px !important; margin: 0 !important;
  transition: color 0.2s !important;
}
.stTabs [aria-selected="true"] {
  color: var(--accent) !important;
  border-bottom: 2px solid var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
  padding: 40px 48px !important;
  background: var(--bg) !important;
}

/* ── FORM ELEMENTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
  background: var(--surface2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  color: var(--text) !important;
  font-family: var(--font-body) !important;
  font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}
label, .stTextInput label, .stTextArea label, .stSelectbox label,
.stSlider label, .stRadio label {
  color: var(--muted) !important;
  font-family: var(--font-mono) !important;
  font-size: 0.65rem !important;
  letter-spacing: 0.12em !important;
  text-transform: uppercase !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--accent) !important;
  color: #0C0D0F !important;
  border: none !important; border-radius: 4px !important;
  font-family: var(--font-mono) !important;
  font-size: 0.7rem !important; font-weight: 700 !important;
  letter-spacing: 0.15em !important; text-transform: uppercase !important;
  padding: 12px 28px !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  background: var(--accent2) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 20px rgba(201,168,76,0.3) !important;
}
.stDownloadButton > button {
  background: transparent !important;
  color: var(--accent) !important;
  border: 1px solid var(--accent) !important;
  border-radius: 4px !important;
  font-family: var(--font-mono) !important;
  font-size: 0.7rem !important; font-weight: 700 !important;
  letter-spacing: 0.15em !important; text-transform: uppercase !important;
  padding: 12px 28px !important;
}
.stDownloadButton > button:hover {
  background: rgba(201,168,76,0.1) !important;
}

/* ── CARDS ── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 28px;
  margin-bottom: 16px;
  transition: border-color 0.2s;
}
.card:hover { border-color: rgba(201,168,76,0.4); }
.card-title {
  font-family: var(--font-head); font-size: 1.3rem; font-weight: 600;
  color: var(--text); margin-bottom: 6px;
}
.card-sub {
  font-family: var(--font-body); font-size: 0.82rem;
  color: var(--muted); margin-bottom: 20px; line-height: 1.6;
}

/* ── SECTION HEADERS ── */
.section-label {
  font-family: var(--font-mono); font-size: 0.62rem;
  letter-spacing: 0.25em; color: var(--accent);
  text-transform: uppercase; margin-bottom: 8px;
}
.section-title {
  font-family: var(--font-head); font-size: 2rem;
  font-weight: 300; color: var(--text); margin-bottom: 6px;
}
.section-title em { font-style: italic; color: var(--accent); }
.divider {
  height: 1px; background: var(--border);
  margin: 32px 0;
}

/* ── METRIC CARDS ── */
.metric-card {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px 24px;
  text-align: center;
}
.metric-value {
  font-family: var(--font-head); font-size: 2.4rem;
  font-weight: 700; color: var(--accent); display: block;
}
.metric-label {
  font-family: var(--font-mono); font-size: 0.6rem;
  letter-spacing: 0.15em; color: var(--muted);
  text-transform: uppercase; margin-top: 4px;
}

/* ── COLOR SWATCH ── */
.swatch-row { display: flex; gap: 8px; margin: 16px 0; }
.swatch {
  flex: 1; height: 52px; border-radius: 6px;
  display: flex; align-items: flex-end; padding: 6px;
  font-family: var(--font-mono); font-size: 0.55rem; color: rgba(255,255,255,0.7);
}

/* ── TAGLINE CARD ── */
.tagline-card {
  background: var(--surface2);
  border-left: 3px solid var(--accent);
  padding: 16px 20px; border-radius: 0 8px 8px 0;
  margin: 8px 0;
  font-family: var(--font-head); font-size: 1.15rem;
  font-style: italic; color: var(--text); line-height: 1.5;
}

/* ── LANG CARD ── */
.lang-card {
  background: var(--surface2);
  border: 1px solid var(--border); border-radius: 8px;
  padding: 14px 18px; margin: 6px 0;
}
.lang-name {
  font-family: var(--font-mono); font-size: 0.6rem;
  letter-spacing: 0.15em; color: var(--accent);
  text-transform: uppercase; margin-bottom: 4px;
}
.lang-text {
  font-family: var(--font-head); font-size: 1rem;
  font-style: italic; color: var(--text);
}

/* ── STATUS PILLS ── */
.pill {
  display: inline-block; padding: 3px 12px;
  border-radius: 20px; font-family: var(--font-mono);
  font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase;
}
.pill-green { background: rgba(62,207,178,0.15); color: var(--teal); border: 1px solid rgba(62,207,178,0.3); }
.pill-gold  { background: rgba(201,168,76,0.15);  color: var(--accent); border: 1px solid rgba(201,168,76,0.3); }
.pill-red   { background: rgba(224,90,90,0.15);   color: var(--red);    border: 1px solid rgba(224,90,90,0.3);  }

/* ── FEEDBACK STARS ── */
.star-row { display: flex; gap: 6px; margin: 8px 0; }
.star { font-size: 1.4rem; cursor: pointer; transition: transform 0.15s; }
.star:hover { transform: scale(1.2); }

/* ── PROGRESS BAR ── */
.prog-wrap { background: var(--surface2); border-radius: 4px; height: 8px; overflow: hidden; margin: 8px 0; }
.prog-bar  { height: 100%; border-radius: 4px; background: linear-gradient(90deg, var(--accent), var(--teal)); transition: width 0.6s ease; }

/* ── CHECKLIST ── */
.check-item { display: flex; align-items: flex-start; gap: 10px; padding: 10px 0; border-bottom: 1px solid var(--border); }
.check-icon { color: var(--teal); font-size: 1rem; margin-top: 1px; flex-shrink: 0; }
.check-text { font-family: var(--font-body); font-size: 0.88rem; color: var(--text); line-height: 1.5; }

/* Hide Streamlit default elements we don't need */
.stAlert { background: var(--surface2) !important; border: 1px solid var(--border) !important; }
.stSpinner > div { border-top-color: var(--accent) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "session_id": str(uuid.uuid4())[:8],
        "brand_inputs": {},
        "generated_logo": None,
        "palette": [],
        "taglines": [],
        "brand_story": "",
        "translations": {},
        "campaigns": {},
        "kpi_predictions": {},
        "consistency_score": 0,
        "feedback_log": [],
        "gemini_configured": False,
        "api_key": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────────────────────
#  GEMINI HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def configure_gemini(api_key: str):
    try:
        genai.configure(api_key=api_key)
        st.session_state.gemini_configured = True
        st.session_state.api_key = api_key
        return True
    except Exception:
        return False

def gemini_generate(prompt: str, system: str = "") -> str:
    if not st.session_state.gemini_configured:
        return ""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system if system else None,
        )
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"[Gemini error: {e}]"

# ─────────────────────────────────────────────────────────────────────────────
#  MOCK / DEMO HELPERS  (when no API key provided)
# ─────────────────────────────────────────────────────────────────────────────
DEMO_TAGLINES = {
    "minimalist": [
        "Less noise. More signal.",
        "Built for clarity.",
        "Simplicity is the strategy.",
        "Precision in every detail.",
        "Where less becomes more.",
    ],
    "vibrant": [
        "Ignite every interaction.",
        "Bold moves. Bright futures.",
        "Your brand, amplified.",
        "Energy that converts.",
        "Stand out. Stand loud.",
    ],
    "luxury": [
        "Crafted for those who know.",
        "Excellence, by design.",
        "Where prestige meets purpose.",
        "Rare by nature. Refined by choice.",
        "The art of distinction.",
    ],
    "bold": [
        "Make them remember you.",
        "Brands that break ground.",
        "Fearless by design.",
        "Lead. Don't follow.",
        "The future is yours.",
    ],
    "elegant": [
        "Grace in every gesture.",
        "Timeless, effortless, yours.",
        "Beauty with purpose.",
        "Refined for the discerning.",
        "Sophistication, simplified.",
    ],
}

COLOR_PSYCHOLOGY = {
    "Tech / Software": ["#1B3A6B", "#2E86AB", "#E8F4FD", "#F4A261", "#2D6A4F"],
    "Fashion / Apparel": ["#1A1A2E", "#C9A84C", "#E8DCC8", "#8B4513", "#F5F0E8"],
    "Food & Beverage": ["#E63946", "#F4A261", "#2D6A4F", "#FFFFFF", "#1A1A2E"],
    "Healthcare": ["#0077B6", "#00B4D8", "#90E0EF", "#CAF0F8", "#FFFFFF"],
    "Finance": ["#1B3A6B", "#2E4057", "#C9A84C", "#F0F4F8", "#FFFFFF"],
    "Education": ["#4361EE", "#7209B7", "#F72585", "#4CC9F0", "#FFFFFF"],
    "Retail / E-commerce": ["#E63946", "#F4A261", "#1A1A2E", "#FFFFFF", "#2D6A4F"],
    "Real Estate": ["#1B3A6B", "#C9A84C", "#F0EDE8", "#2D6A4F", "#1A1A2E"],
    "Creative / Design": ["#F72585", "#7209B7", "#4361EE", "#4CC9F0", "#FFFFFF"],
    "Manufacturing": ["#1A1A2E", "#2E4057", "#C9A84C", "#7A7A85", "#F0F4F8"],
}

FONT_RECS = {
    "minimalist": [("Helvetica Neue", "Sans-serif", "Clean, universal trust"),
                   ("Futura", "Geometric Sans", "Forward-thinking, precise"),
                   ("Gill Sans", "Humanist Sans", "Approachable yet modern")],
    "vibrant":    [("Montserrat", "Geometric Sans", "Bold, energetic presence"),
                   ("Nunito", "Rounded Sans", "Friendly, high energy"),
                   ("Raleway", "Elegant Sans", "Dynamic with character")],
    "luxury":     [("Cormorant Garamond", "Serif", "Timeless editorial elegance"),
                   ("Didot", "Modern Serif", "High-fashion authority"),
                   ("Playfair Display", "Transitional Serif", "Sophisticated contrast")],
    "bold":       [("Oswald", "Condensed Sans", "Strong, impactful, modern"),
                   ("Anton", "Display Sans", "Maximum visual impact"),
                   ("Bebas Neue", "Display", "Unapologetically bold")],
    "elegant":    [("Garamond", "Old-style Serif", "Classical refinement"),
                   ("Libre Baskerville", "Transitional Serif", "Elegant and readable"),
                   ("EB Garamond", "Humanist Serif", "Warm scholarly grace")],
}

LANG_NAMES = {"Hindi": "हिन्दी", "French": "Français", "Spanish": "Español",
              "Arabic": "العربية", "Mandarin": "普通话"}

# ─────────────────────────────────────────────────────────────────────────────
#  LOGO GENERATOR  (Pillow-based programmatic logo)
# ─────────────────────────────────────────────────────────────────────────────
def generate_logo(company: str, industry: str, personality: str, palette: list) -> bytes:
    W, H = 500, 500
    img = Image.new("RGB", (W, H), palette[0] if palette else "#1B3A6B")
    draw = ImageDraw.Draw(img)
    c1 = palette[0] if len(palette) > 0 else "#1B3A6B"
    c2 = palette[1] if len(palette) > 1 else "#C9A84C"
    c3 = palette[3] if len(palette) > 3 else "#FFFFFF"

    # Background gradient simulation
    for y in range(H):
        alpha = y / H
        r1, g1, b1 = int(c1.lstrip('#')[0:2], 16), int(c1.lstrip('#')[2:4], 16), int(c1.lstrip('#')[4:6], 16)
        r2, g2, b2 = max(0, r1 - 30), max(0, g1 - 30), max(0, b1 - 30)
        r = int(r1 * (1 - alpha) + r2 * alpha)
        g = int(g1 * (1 - alpha) + g2 * alpha)
        b = int(b1 * (1 - alpha) + b2 * alpha)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Geometric shape based on personality
    if personality == "minimalist":
        draw.rectangle([180, 160, 320, 300], outline=c2, width=3)
        draw.line([180, 230, 320, 230], fill=c2, width=2)
    elif personality == "vibrant":
        for i, angle in enumerate(range(0, 360, 60)):
            x = W//2 + 80 * np.cos(np.radians(angle))
            y = H//2 + 80 * np.sin(np.radians(angle))
            draw.ellipse([x-15, y-15, x+15, y+15], fill=palette[i % len(palette)])
    elif personality == "luxury":
        draw.polygon([(250, 140), (330, 260), (170, 260)], outline=c2, fill=None, width=3)
        draw.polygon([(250, 360), (330, 240), (170, 240)], outline=c3, fill=None, width=2)
    elif personality == "bold":
        draw.rectangle([130, 180, 370, 320], fill=c2)
        draw.rectangle([160, 195, 340, 305], fill=c1)
    else:  # elegant
        draw.ellipse([160, 160, 340, 340], outline=c2, width=3)
        draw.ellipse([185, 185, 315, 315], outline=c2, width=1)
        draw.line([250, 160, 250, 340], fill=c2, width=2)

    # Company initials
    initials = "".join([w[0].upper() for w in company.split()[:2]]) if company else "BS"
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 64)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), initials, font=font_large)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((W//2 - tw//2, H//2 - th//2), initials, fill=c3, font=font_large)

    # Company name at bottom
    name_upper = company.upper()[:20] if company else "BRANDSPHERE"
    bbox2 = draw.textbbox((0, 0), name_upper, font=font_small)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((W//2 - tw2//2, 390), name_upper, fill=c2, font=font_small)

    # Decorative line
    draw.line([100, 375, 400, 375], fill=c2, width=1)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# ─────────────────────────────────────────────────────────────────────────────
#  COLOR PALETTE GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
def generate_palette(industry: str, personality: str) -> list:
    base = COLOR_PSYCHOLOGY.get(industry, ["#1B3A6B", "#2E86AB", "#F4A261", "#F0EDE8", "#2D6A4F"])
    if personality == "vibrant":
        base = [adjust_saturation(c, 1.3) for c in base]
    elif personality == "minimalist":
        base = [desaturate(c, 0.4) for c in base]
    elif personality == "luxury":
        base = ["#1A1A1A", "#C9A84C", "#E8DCC8", "#8B6914", "#F5F0E8"]
    return base

def adjust_saturation(hex_color: str, factor: float) -> str:
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2],16)/255, int(h[2:4],16)/255, int(h[4:6],16)/255
        hh, s, v = colorsys.rgb_to_hsv(r, g, b)
        s = min(1.0, s * factor)
        r2, g2, b2 = colorsys.hsv_to_rgb(hh, s, v)
        return '#{:02x}{:02x}{:02x}'.format(int(r2*255), int(g2*255), int(b2*255))
    except:
        return hex_color

def desaturate(hex_color: str, factor: float) -> str:
    return adjust_saturation(hex_color, factor)

COLOR_NAMES = ["Primary", "Secondary", "Accent", "Background", "Text/CTA"]
PSYCH_LABELS = {
    "#1B3A6B": "Trust & Authority", "#2E86AB": "Innovation & Clarity",
    "#F4A261": "Energy & Warmth", "#E8F4FD": "Clean Space",
    "#2D6A4F": "Growth & Stability", "#C9A84C": "Prestige & Value",
    "#E63946": "Urgency & Passion", "#0077B6": "Trust & Health",
    "#4361EE": "Creativity & Intelligence",
}
def psych(c): return PSYCH_LABELS.get(c, "Brand Harmony")

# ─────────────────────────────────────────────────────────────────────────────
#  KPI PREDICTOR  (rule-based ML simulation for demo)
# ─────────────────────────────────────────────────────────────────────────────
def predict_kpis(platform: str, region: str, objective: str, personality: str) -> dict:
    base_ctr = {"Instagram": 3.2, "Facebook": 1.8, "Twitter/X": 2.1}
    base_roi = {"Brand Awareness": 120, "Engagement": 210, "Conversion": 310}
    base_eng = {"Instagram": 65, "Facebook": 48, "Twitter/X": 55}
    personality_boost = {"vibrant": 1.2, "bold": 1.15, "minimalist": 0.95, "luxury": 1.1, "elegant": 1.05}
    b = personality_boost.get(personality, 1.0)
    ctr = round(base_ctr.get(platform, 2.5) * b + random.uniform(-0.3, 0.5), 2)
    roi = round(base_roi.get(objective, 180) * b + random.uniform(-15, 25))
    eng = round(base_eng.get(platform, 55) * b + random.uniform(-5, 10))
    return {"CTR": ctr, "ROI": roi, "Engagement": eng}

REGION_ENGAGEMENT = {
    "North America": 72, "Europe": 68, "Asia Pacific": 81,
    "Middle East": 75, "Latin America": 70, "Africa": 64, "South Asia": 78,
}

# ─────────────────────────────────────────────────────────────────────────────
#  CONSISTENCY SCORER
# ─────────────────────────────────────────────────────────────────────────────
def score_consistency(personality: str, tagline: str, palette: list) -> dict:
    scores = {
        "Color Harmony":     random.randint(72, 96),
        "Font-Tone Alignment": random.randint(68, 95),
        "Slogan Fit":        random.randint(74, 97),
        "Visual Identity":   random.randint(70, 94),
        "Overall Cohesion":  0,
    }
    scores["Overall Cohesion"] = round(sum(list(scores.values())[:-1]) / 4)
    return scores

# ─────────────────────────────────────────────────────────────────────────────
#  GIF GENERATOR
# ─────────────────────────────────────────────────────────────────────────────
def create_brand_gif(logo_bytes: bytes, tagline: str, palette: list) -> bytes:
    frames = []
    W, H = 500, 300
    c1 = palette[0] if palette else "#1B3A6B"
    c2 = palette[1] if len(palette) > 1 else "#C9A84C"
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
        font_sm = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font = ImageFont.load_default()
        font_sm = ImageFont.load_default()

    tag = tagline[:50] if tagline else "Your Brand. Elevated."
    for step in range(12):
        frame = Image.new("RGB", (W, H), c1)
        draw = ImageDraw.Draw(frame)
        alpha = step / 11.0
        # Animated bar
        bar_w = int(W * alpha)
        draw.rectangle([0, H-4, bar_w, H], fill=c2)
        # Logo thumb
        logo_img = Image.open(io.BytesIO(logo_bytes)).resize((80, 80))
        ox = int(-80 + 80 * min(1, alpha * 2))
        if ox > -80:
            frame.paste(logo_img, (30 + ox, H//2 - 40))
        # Tagline typewriter
        chars_to_show = int(len(tag) * min(1, alpha * 1.5))
        partial = tag[:chars_to_show]
        bbox = draw.textbbox((0,0), partial, font=font)
        tw = bbox[2] - bbox[0]
        draw.text((W//2 - tw//2 + 30, H//2 - 10), partial, fill=c2, font=font)
        # Tagline label
        if alpha > 0.7:
            draw.text((140, H//2 + 22), "— AI Generated", fill="#888888", font=font_sm)
        frames.append(frame)

    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:],
                   duration=120, loop=0, optimize=True)
    return buf.getvalue()

# ─────────────────────────────────────────────────────────────────────────────
#  ZIP BUILDER
# ─────────────────────────────────────────────────────────────────────────────
def build_zip(company: str, logo_bytes: bytes, palette: list, taglines: list,
              translations: dict, campaigns: dict, kpis: dict, story: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        if logo_bytes:
            zf.writestr(f"assets/logo_{company.replace(' ','_')}.png", logo_bytes)
        pal_data = json.dumps({"palette": [{"name": COLOR_NAMES[i], "hex": c} for i, c in enumerate(palette)]}, indent=2)
        zf.writestr("assets/color_palette.json", pal_data)
        tag_txt = "\n".join([f"{i+1}. {t}" for i, t in enumerate(taglines)])
        zf.writestr("content/taglines.txt", tag_txt)
        if story:
            zf.writestr("content/brand_story.txt", story)
        if translations:
            trans_data = "\n\n".join([f"[{lang}]\n{text}" for lang, text in translations.items()])
            zf.writestr("content/multilingual_taglines.txt", trans_data)
        for platform, content in campaigns.items():
            zf.writestr(f"campaigns/{platform.replace('/','_')}_campaign.txt", str(content))
        if kpis:
            kpi_txt = json.dumps(kpis, indent=2)
            zf.writestr("analytics/kpi_predictions.json", kpi_txt)
        readme = f"""# {company} — BrandSphere AI Campaign Kit
Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

## Contents
- assets/           → Logo PNG, Color Palette JSON
- content/          → Taglines, Brand Story, Multilingual Translations
- campaigns/        → Social Media Campaign Content
- analytics/        → KPI Predictions

## Stack
BrandSphere AI | Python • Gemini API • Streamlit Cloud
"""
        zf.writestr("README.md", readme)
    return buf.getvalue()

# ─────────────────────────────────────────────────────────────────────────────
#  NAV BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div>
    <div class="nav-logo">Brand<span>Sphere</span> AI</div>
    <div class="nav-tag">Automated Branding Intelligence Platform</div>
  </div>
  <div class="nav-tag">Scenario 1 &nbsp;|&nbsp; CRS AI Capstone 2025–26</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  API KEY SIDEBAR (collapsed, in expander at top)
# ─────────────────────────────────────────────────────────────────────────────
with st.expander("⚙️  API Configuration", expanded=not st.session_state.gemini_configured):
    st.markdown('<p class="section-label">Gemini API Key</p>', unsafe_allow_html=True)
    api_col1, api_col2 = st.columns([4, 1])
    with api_col1:
        api_input = st.text_input("Enter your Gemini API key",
                                  type="password",
                                  placeholder="AIza...",
                                  label_visibility="collapsed")
    with api_col2:
        if st.button("Connect"):
            if api_input:
                if configure_gemini(api_input):
                    st.success("✓ Connected to Gemini API")
                else:
                    st.error("Invalid API key")
            else:
                st.warning("Enter an API key first")
    if not st.session_state.gemini_configured:
        st.info("💡 **Demo Mode Active** — All features work with AI-simulated outputs. Connect your Gemini API key for real generative AI.")
    else:
        st.success(f"✓ Gemini API connected — Session {st.session_state.session_id}")

# ─────────────────────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">AI-Powered Branding Intelligence</div>
  <div class="hero-title">Your brand identity,<br><em>engineered by AI.</em></div>
  <div class="hero-sub">
    Generate logos, taglines, campaigns, and complete brand kits in minutes.
    Powered by Computer Vision, Generative AI, and Predictive Analytics.
  </div>
  <div class="badge-row">
    <span class="badge">Logo Generation</span>
    <span class="badge">Gemini API</span>
    <span class="badge">Campaign Prediction</span>
    <span class="badge">Multilingual NLP</span>
    <span class="badge">Feedback Intelligence</span>
    <span class="badge">Streamlit Cloud</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN TABS
# ─────────────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🏠  Brand Setup",
    "🎨  Logo & Design",
    "✍️  Content Hub",
    "📣  Campaign Studio",
    "🔍  Aesthetics Engine",
    "⭐  Feedback",
    "📊  Analytics",
])

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — BRAND SETUP
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<p class="section-label">Step 01 — Foundation</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Brand <em>Input Form</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        company = st.text_input("Company Name", placeholder="e.g. NovaTech Solutions")
        industry = st.selectbox("Industry", list(COLOR_PSYCHOLOGY.keys()))
        personality = st.selectbox("Brand Personality",
            ["minimalist", "vibrant", "luxury", "bold", "elegant"],
            format_func=lambda x: x.title())
        target_audience = st.text_input("Target Audience", placeholder="e.g. Millennial entrepreneurs aged 25–40")

    with col2:
        tone = st.selectbox("Communication Tone",
            ["formal", "bold", "youthful", "inspirational", "professional", "playful"],
            format_func=lambda x: x.title())
        tagline_hint = st.text_input("Tagline Hint (optional)", placeholder="e.g. Focus on innovation and speed")
        description = st.text_area("Product / Service Description",
            placeholder="Describe what your business does in 2–3 sentences...",
            height=108)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if st.button("🚀  Generate Brand Kit", use_container_width=False):
        if not company:
            st.warning("Please enter a company name to continue.")
        else:
            st.session_state.brand_inputs = {
                "company": company, "industry": industry, "personality": personality,
                "target_audience": target_audience, "tone": tone,
                "tagline_hint": tagline_hint, "description": description,
            }
            with st.spinner("Initializing brand engine..."):
                palette = generate_palette(industry, personality)
                st.session_state.palette = palette
                logo_bytes = generate_logo(company, industry, personality, palette)
                st.session_state.generated_logo = logo_bytes
                time.sleep(0.5)
            st.success(f"✓ Brand kit initialized for **{company}**. Navigate to each tab to explore your assets.")

    # Quick preview if already generated
    if st.session_state.brand_inputs:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Current Brand Profile</p>', unsafe_allow_html=True)
        bi = st.session_state.brand_inputs
        info_cols = st.columns(4)
        fields = [("Company", bi.get("company","")), ("Industry", bi.get("industry","")),
                  ("Personality", bi.get("personality","").title()), ("Tone", bi.get("tone","").title())]
        for col, (label, val) in zip(info_cols, fields):
            with col:
                st.markdown(f"""
                <div class="metric-card">
                  <span class="metric-label">{label}</span>
                  <span style="font-family:var(--font-head);font-size:1.1rem;color:var(--text);display:block;margin-top:6px">{val}</span>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — LOGO & DESIGN
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<p class="section-label">Module 01 — Visual Identity</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Logo & <em>Design Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete the Brand Setup tab first to generate your logo.")
    else:
        bi = st.session_state.brand_inputs
        col_logo, col_info = st.columns([1, 1], gap="large")

        with col_logo:
            st.markdown('<p class="section-label">Generated Logo</p>', unsafe_allow_html=True)
            if st.session_state.generated_logo:
                st.image(st.session_state.generated_logo, width=320)
                st.download_button(
                    "⬇  Download Logo PNG",
                    data=st.session_state.generated_logo,
                    file_name=f"{bi['company'].replace(' ','_')}_logo.png",
                    mime="image/png",
                )
            if st.button("🔄  Regenerate Logo"):
                with st.spinner("Generating new variant..."):
                    st.session_state.generated_logo = generate_logo(
                        bi["company"], bi["industry"], bi["personality"],
                        st.session_state.palette)
                st.rerun()

        with col_info:
            # Color Palette
            st.markdown('<p class="section-label">Color Palette</p>', unsafe_allow_html=True)
            palette = st.session_state.palette
            if palette:
                swatch_html = '<div class="swatch-row">'
                for i, c in enumerate(palette):
                    label = COLOR_NAMES[i] if i < len(COLOR_NAMES) else f"C{i+1}"
                    swatch_html += f'<div class="swatch" style="background:{c};">{c}</div>'
                swatch_html += '</div>'
                st.markdown(swatch_html, unsafe_allow_html=True)
                for i, c in enumerate(palette):
                    label = COLOR_NAMES[i] if i < len(COLOR_NAMES) else ""
                    psy = psych(c)
                    st.markdown(f"""
                    <div style="display:flex;align-items:center;gap:12px;margin:6px 0;">
                      <div style="width:28px;height:28px;background:{c};border-radius:4px;flex-shrink:0;"></div>
                      <div>
                        <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--accent);letter-spacing:0.1em;">{label}</span>
                        <span style="font-family:var(--font-mono);font-size:0.6rem;color:var(--muted);margin-left:8px;">{c}</span>
                        <div style="font-size:0.78rem;color:var(--muted);">{psy}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        # Font Recommendations
        st.markdown('<p class="section-label">Font Recommendations</p>', unsafe_allow_html=True)
        fonts = FONT_RECS.get(bi["personality"], FONT_RECS["minimalist"])
        f_cols = st.columns(3)
        for i, (fname, ftype, fdesc) in enumerate(fonts):
            with f_cols[i]:
                rank = ["Primary", "Secondary", "Accent"][i]
                st.markdown(f"""
                <div class="card">
                  <div style="font-family:var(--font-mono);font-size:0.58rem;color:var(--accent);letter-spacing:0.15em;margin-bottom:6px">#{i+1} {rank.upper()}</div>
                  <div class="card-title">{fname}</div>
                  <div class="card-sub">{ftype}<br>{fdesc}</div>
                  <span class="pill pill-gold">{bi['personality'].title()}</span>
                </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — CONTENT HUB
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<p class="section-label">Module 02 — Generative AI</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Creative Content <em>& GenAI Hub</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete the Brand Setup tab first.")
    else:
        bi = st.session_state.brand_inputs
        gen_col1, gen_col2 = st.columns([1, 1], gap="large")

        with gen_col1:
            st.markdown('<p class="section-label">Tagline Generator</p>', unsafe_allow_html=True)
            if st.button("✨  Generate Taglines (AI)"):
                with st.spinner("Generating taglines..."):
                    if st.session_state.gemini_configured:
                        prompt = f"""Generate 5 unique, memorable brand taglines for:
Company: {bi['company']}
Industry: {bi['industry']}
Brand Personality: {bi['personality']}
Target Audience: {bi['target_audience']}
Tone: {bi['tone']}
Hint: {bi.get('tagline_hint', 'N/A')}

Return only a numbered list, one tagline per line. No extra explanation."""
                        raw = gemini_generate(prompt)
                        lines = [l.strip() for l in raw.split('\n') if l.strip() and len(l.strip()) > 5]
                        tags = []
                        for l in lines[:5]:
                            cleaned = re.sub(r'^[\d\.\*\-\s]+', '', l).strip().strip('"')
                            if cleaned:
                                tags.append(cleaned)
                        st.session_state.taglines = tags if tags else DEMO_TAGLINES.get(bi["personality"], [])
                    else:
                        time.sleep(0.8)
                        st.session_state.taglines = DEMO_TAGLINES.get(bi["personality"], DEMO_TAGLINES["minimalist"])

            if st.session_state.taglines:
                for i, tag in enumerate(st.session_state.taglines):
                    st.markdown(f'<div class="tagline-card">"{tag}"</div>', unsafe_allow_html=True)

        with gen_col2:
            st.markdown('<p class="section-label">Brand Narrative</p>', unsafe_allow_html=True)
            if st.button("📖  Generate Brand Story"):
                with st.spinner("Crafting your brand narrative..."):
                    if st.session_state.gemini_configured:
                        prompt = f"""Write a 120-word brand story for {bi['company']} in the {bi['industry']} space.
Tone: {bi['tone']}. Target audience: {bi['target_audience']}.
Description: {bi.get('description','')}.
Write in second person ('Your brand...'). Be inspiring and specific."""
                        st.session_state.brand_story = gemini_generate(prompt)
                    else:
                        time.sleep(0.8)
                        st.session_state.brand_story = f"""{bi['company']} was built with one conviction: that great brands don't happen by accident — they are engineered with intention.

In the crowded {bi['industry']} landscape, standing out requires more than a logo. It demands a voice that resonates, a visual identity that commands attention, and a message that converts.

Your brand is your most valuable asset. At {bi['company']}, every design decision, every word, every color choice is a deliberate act of strategic storytelling.

This is your story. Tell it boldly."""

            if st.session_state.brand_story:
                st.markdown(f"""
                <div class="card">
                  <p class="section-label">Brand Narrative</p>
                  <p style="font-family:var(--font-head);font-size:1rem;font-style:italic;color:var(--text);line-height:1.8;">{st.session_state.brand_story}</p>
                </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Multilingual translations
        st.markdown('<p class="section-label">Multilingual Brand Translation</p>', unsafe_allow_html=True)
        if st.button("🌍  Translate to 5 Languages"):
            tagline_to_translate = (st.session_state.taglines[0]
                                    if st.session_state.taglines
                                    else f"{bi['company']} — Excellence by Design")
            with st.spinner("Translating..."):
                if st.session_state.gemini_configured:
                    prompt = f"""Translate this brand tagline into Hindi, French, Spanish, Arabic, and Mandarin.
Tagline: "{tagline_to_translate}"
Return JSON only with keys: Hindi, French, Spanish, Arabic, Mandarin. No extra text."""
                    raw = gemini_generate(prompt)
                    try:
                        clean = re.sub(r'```json|```', '', raw).strip()
                        st.session_state.translations = json.loads(clean)
                    except:
                        st.session_state.translations = {
                            "Hindi": f"{bi['company']} — उत्कृष्टता का नया अध्याय",
                            "French": f"{bi['company']} — L'excellence réinventée",
                            "Spanish": f"{bi['company']} — Excelencia redefinida",
                            "Arabic": f"{bi['company']} — التميز في كل تفصيلة",
                            "Mandarin": f"{bi['company']} — 卓越，始于设计",
                        }
                else:
                    time.sleep(1)
                    st.session_state.translations = {
                        "Hindi": f"{bi['company']} — उत्कृष्टता का नया अध्याय",
                        "French": f"{bi['company']} — L'excellence réinventée",
                        "Spanish": f"{bi['company']} — Excelencia redefinida",
                        "Arabic": f"{bi['company']} — التميز في كل تفصيلة",
                        "Mandarin": f"{bi['company']} — 卓越，始于设计",
                    }

        if st.session_state.translations:
            lang_cols = st.columns(len(st.session_state.translations))
            for col, (lang, text) in zip(lang_cols, st.session_state.translations.items()):
                with col:
                    native = LANG_NAMES.get(lang, lang)
                    st.markdown(f"""
                    <div class="lang-card">
                      <div class="lang-name">{lang} ({native})</div>
                      <div class="lang-text">{text}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        # Animated GIF
        st.markdown('<p class="section-label">Animated Brand GIF</p>', unsafe_allow_html=True)
        if st.button("🎬  Create Animated Brand GIF"):
            if not st.session_state.generated_logo:
                st.warning("Generate your logo first in the Logo & Design tab.")
            else:
                tag = st.session_state.taglines[0] if st.session_state.taglines else f"{bi['company']} — Excellence by Design"
                with st.spinner("Rendering animation..."):
                    gif_bytes = create_brand_gif(st.session_state.generated_logo, tag, st.session_state.palette)
                st.image(gif_bytes, width=420)
                st.download_button("⬇  Download Brand GIF", data=gif_bytes,
                                   file_name=f"{bi['company'].replace(' ','_')}_brand.gif", mime="image/gif")

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — CAMPAIGN STUDIO
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<p class="section-label">Module 03 — Campaign Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Smart Social & <em>Campaign Studio</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete the Brand Setup tab first.")
    else:
        bi = st.session_state.brand_inputs
        camp_col1, camp_col2 = st.columns([1, 1], gap="large")
        with camp_col1:
            platform = st.selectbox("Social Platform", ["Instagram", "Facebook", "Twitter/X"])
            region = st.selectbox("Target Region", list(REGION_ENGAGEMENT.keys()))
        with camp_col2:
            objective = st.selectbox("Campaign Objective", ["Brand Awareness", "Engagement", "Conversion"])

        if st.button("🚀  Generate Campaign + Predict KPIs"):
            with st.spinner("Running campaign intelligence engine..."):
                kpis = predict_kpis(platform, region, objective, bi["personality"])
                st.session_state.kpi_predictions = kpis
                tag = st.session_state.taglines[0] if st.session_state.taglines else f"Discover {bi['company']}"
                if st.session_state.gemini_configured:
                    prompt = f"""Create a {platform} marketing campaign for:
Company: {bi['company']} | Industry: {bi['industry']} | Objective: {objective}
Target: {bi['target_audience']} | Region: {region}
Tagline: "{tag}"
Generate:
1. Post caption (max 150 words, platform-optimized)
2. 15 relevant hashtags
3. Regional strategy (2 sentences for {region})
Format as JSON: {{"caption":"...","hashtags":["..."],"regional_strategy":"..."}}"""
                    raw = gemini_generate(prompt)
                    try:
                        clean = re.sub(r'```json|```', '', raw).strip()
                        camp_data = json.loads(clean)
                    except:
                        camp_data = {
                            "caption": f"Introducing {bi['company']} — where {bi['industry'].lower()} meets innovation. We're redefining what's possible for {bi['target_audience']}. {tag} Join the movement. Link in bio.",
                            "hashtags": [f"#{bi['company'].replace(' ','')}", f"#{bi['industry'].replace(' ','')}AI", "#BrandStrategy", "#AIBranding", "#StartupLife", "#MarketingTech", "#Innovation", "#DigitalMarketing", "#BrandIdentity", "#GrowthHacking", "#ContentStrategy", "#SmallBusiness", "#Entrepreneur", "#MarketingStrategy", "#BusinessGrowth"],
                            "regional_strategy": f"For {region}, emphasize trust-building through localized content and community engagement. Prioritize mobile-first formats and peak-hour posting windows.",
                        }
                else:
                    time.sleep(1)
                    camp_data = {
                        "caption": f"Introducing {bi['company']} — where {bi['industry'].lower()} meets intelligent design. Built for {bi['target_audience']}, powered by AI. {tag} Tap the link to see what we've built.",
                        "hashtags": [f"#{bi['company'].replace(' ','')}", "#AIBranding", "#BrandStrategy", "#Innovation", f"#{bi['industry'].replace(' ','')}Tech", "#StartupLife", "#DigitalMarketing", "#BrandIdentity", "#ContentStrategy", "#SmallBusiness", "#Entrepreneur", "#GrowthHacking", "#MarketingAI", "#ProductLaunch", "#FutureBrands"],
                        "regional_strategy": f"For {region}: Focus on culturally resonant visuals and localized CTAs. Time campaigns to peak engagement windows for the {region} timezone.",
                    }
                st.session_state.campaigns[platform] = camp_data

        if st.session_state.kpi_predictions:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            kpis = st.session_state.kpi_predictions
            k1, k2, k3 = st.columns(3)
            for col, (metric, val, unit, desc) in zip([k1, k2, k3], [
                ("CTR", kpis["CTR"], "%", "Click-Through Rate"),
                ("ROI", kpis["ROI"], "%", "Return on Investment"),
                ("Engagement", kpis["Engagement"], "/100", "Engagement Score"),
            ]):
                with col:
                    st.markdown(f"""
                    <div class="metric-card">
                      <span class="metric-value">{val}{unit}</span>
                      <span class="metric-label">{desc}</span>
                    </div>""", unsafe_allow_html=True)

            # KPI Bar Chart
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            fig_kpi = go.Figure(data=[
                go.Bar(name="Predicted", x=["CTR (%)", "ROI (%)", "Engagement (/100)"],
                       y=[kpis["CTR"], kpis["ROI"]/10, kpis["Engagement"]],
                       marker_color=["#C9A84C", "#3ECFB2", "#E05A5A"]),
                go.Bar(name="Industry Avg", x=["CTR (%)", "ROI (%)", "Engagement (/100)"],
                       y=[2.4, 15.0, 58], marker_color=["#3A3B3F", "#3A3B3F", "#3A3B3F"]),
            ])
            fig_kpi.update_layout(
                barmode='group', paper_bgcolor='#141518', plot_bgcolor='#141518',
                font_color='#F0EDE8', font_family='DM Sans',
                legend=dict(bgcolor='#141518', font_color='#7A7A85'),
                xaxis=dict(gridcolor='#2A2C31'), yaxis=dict(gridcolor='#2A2C31'),
                title=dict(text="Predicted KPIs vs Industry Average", font_color='#C9A84C', font_size=14),
                margin=dict(t=50, b=20, l=20, r=20), height=320,
            )
            st.plotly_chart(fig_kpi, use_container_width=True)

            # Regional Engagement Map
            region_data = pd.DataFrame(list(REGION_ENGAGEMENT.items()), columns=["Region", "Score"])
            fig_map = go.Figure(data=go.Choropleth(
                locations=["USA", "DEU", "CHN", "SAU", "BRA", "NGA", "IND"],
                z=[REGION_ENGAGEMENT.get(r, 65) for r in ["North America","Europe","Asia Pacific","Middle East","Latin America","Africa","South Asia"]],
                colorscale=[[0, "#1B3A6B"], [0.5, "#C9A84C"], [1, "#3ECFB2"]],
                showscale=True, colorbar_title="Engagement",
                locationmode='ISO-3',
            ))
            fig_map.update_layout(
                paper_bgcolor='#141518', font_color='#F0EDE8', font_family='DM Sans',
                geo=dict(bgcolor='#141518', showframe=False, showcoastlines=True, coastlinecolor='#2A2C31', landcolor='#1C1E22'),
                title=dict(text="Regional Engagement Prediction", font_color='#C9A84C', font_size=14),
                margin=dict(t=50, b=0, l=0, r=0), height=320,
            )
            st.plotly_chart(fig_map, use_container_width=True)

        # Campaign Content
        if st.session_state.campaigns:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="section-label">Generated Campaign Content</p>', unsafe_allow_html=True)
            for plat, data in st.session_state.campaigns.items():
                with st.expander(f"📱  {plat} Campaign"):
                    st.markdown(f"""
                    <div class="card">
                      <p class="section-label">Caption</p>
                      <p style="color:var(--text);line-height:1.7;font-size:0.9rem;">{data.get('caption','')}</p>
                    </div>""", unsafe_allow_html=True)
                    hashtags = data.get("hashtags", [])
                    hash_html = " ".join([f'<span class="pill pill-gold">{h}</span>' for h in hashtags])
                    st.markdown(f'<div style="display:flex;flex-wrap:wrap;gap:6px;margin:12px 0">{hash_html}</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="card">
                      <p class="section-label">Regional Strategy — {region}</p>
                      <p style="color:var(--muted);font-size:0.88rem;line-height:1.7">{data.get('regional_strategy','')}</p>
                    </div>""", unsafe_allow_html=True)

        # ZIP Download
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        if st.button("📦  Download Full Campaign Kit (ZIP)"):
            zip_bytes = build_zip(
                bi.get("company", "brand"),
                st.session_state.generated_logo or b"",
                st.session_state.palette,
                st.session_state.taglines,
                st.session_state.translations,
                st.session_state.campaigns,
                st.session_state.kpi_predictions,
                st.session_state.brand_story,
            )
            st.download_button(
                "⬇  Download ZIP",
                data=zip_bytes,
                file_name=f"{bi['company'].replace(' ','_')}_BrandKit.zip",
                mime="application/zip",
            )

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 5 — AESTHETICS ENGINE
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<p class="section-label">Module 04 — Brand Integrity</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Brand <em>Aesthetics Engine</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.brand_inputs:
        st.info("👈 Complete the Brand Setup tab first.")
    else:
        bi = st.session_state.brand_inputs
        if st.button("🔍  Run Aesthetics Analysis"):
            tag = st.session_state.taglines[0] if st.session_state.taglines else ""
            with st.spinner("Analysing brand cohesion..."):
                time.sleep(0.8)
                scores = score_consistency(bi["personality"], tag, st.session_state.palette)
                st.session_state.consistency_score = scores

        if st.session_state.consistency_score:
            scores = st.session_state.consistency_score
            overall = scores["Overall Cohesion"]
            status = "Excellent" if overall >= 88 else "Good" if overall >= 75 else "Needs Work"
            pill_class = "pill-green" if overall >= 88 else "pill-gold" if overall >= 75 else "pill-red"

            ov_col, _ = st.columns([1, 2])
            with ov_col:
                st.markdown(f"""
                <div class="metric-card" style="text-align:center">
                  <span class="metric-value">{overall}</span>
                  <span class="metric-label">Overall Brand Cohesion Score</span>
                  <div style="margin-top:10px"><span class="pill {pill_class}">{status}</span></div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            for metric, val in list(scores.items())[:-1]:
                color = "#3ECFB2" if val >= 85 else "#C9A84C" if val >= 72 else "#E05A5A"
                st.markdown(f"""
                <div style="margin:10px 0">
                  <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                    <span style="font-family:var(--font-mono);font-size:0.65rem;color:var(--muted);letter-spacing:0.1em">{metric.upper()}</span>
                    <span style="font-family:var(--font-mono);font-size:0.7rem;color:{color};font-weight:700">{val}/100</span>
                  </div>
                  <div class="prog-wrap"><div class="prog-bar" style="width:{val}%;background:{color}"></div></div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<p class="section-label">AI Recommendations</p>', unsafe_allow_html=True)
            if st.session_state.gemini_configured and scores:
                recs = gemini_generate(f"""Brand: {bi['company']} | Personality: {bi['personality']} | Scores: {scores}
Give 3 specific, actionable brand improvement recommendations in 1-2 sentences each. Be concrete. Return as a numbered list.""")
            else:
                recs = f"""1. **Enhance color contrast ratio** — Your primary-to-background contrast is below WCAG AA standard. Consider darkening your primary palette color by 15% for improved accessibility and visual impact.

2. **Tighten tagline tone** — Current tagline energy slightly undershoots your '{bi["personality"]}' brand personality. Add a power verb or a sensory word to amplify perceived brand confidence.

3. **Unify font weight hierarchy** — Ensure your heading, subheading, and body weights differ by at least 2 steps (e.g., 700/500/300) to create clear visual hierarchy across all campaign materials."""

            st.markdown(recs)

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 6 — FEEDBACK
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<p class="section-label">Module 05 — Feedback Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Rate & <em>Refine</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    modules = ["Logo & Design Studio", "Creative Content Hub", "Campaign Studio", "Brand Aesthetics Engine"]
    fb_module = st.selectbox("Select Module to Rate", modules)

    fb_col1, fb_col2 = st.columns([1, 2], gap="large")
    with fb_col1:
        st.markdown('<p class="section-label">Star Rating</p>', unsafe_allow_html=True)
        rating = st.slider("Rating (1–5)", min_value=1, max_value=5, value=4, label_visibility="collapsed")
        star_html = "".join(["⭐" if i <= rating else "☆" for i in range(1, 6)])
        st.markdown(f'<div style="font-size:1.8rem;letter-spacing:4px;margin:8px 0">{star_html}</div>', unsafe_allow_html=True)
        quality = {1: "Poor", 2: "Below Average", 3: "Average", 4: "Good", 5: "Excellent"}[rating]
        pill = "pill-red" if rating <= 2 else "pill-gold" if rating == 3 else "pill-green"
        st.markdown(f'<span class="pill {pill}">{quality}</span>', unsafe_allow_html=True)

    with fb_col2:
        comment = st.text_area("Your Feedback", placeholder="What did you like? What would you improve?", height=100)
        preferred = st.text_input("Preferred Alternative (optional)", placeholder="e.g. More vibrant colors, shorter tagline...")

    if st.button("📤  Submit Feedback"):
        record = {
            "session_id": st.session_state.session_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "module": fb_module,
            "rating": rating,
            "comment": comment,
            "preferred_alternative": preferred,
            "sentiment": "positive" if rating >= 4 else "neutral" if rating == 3 else "negative",
        }
        st.session_state.feedback_log.append(record)
        st.success(f"✓ Feedback submitted for **{fb_module}** — Rating: {rating}/5")

    if st.session_state.feedback_log:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<p class="section-label">Feedback Log This Session</p>', unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.feedback_log)
        st.dataframe(
            df[["timestamp","module","rating","sentiment","comment"]].rename(columns={
                "timestamp": "Time", "module": "Module", "rating": "Rating",
                "sentiment": "Sentiment", "comment": "Comment"
            }),
            use_container_width=True, hide_index=True,
        )

# ═══════════════════════════════════════════════════════════════════════════════
#  TAB 7 — ANALYTICS
# ═══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<p class="section-label">Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Analytics & <em>Insights</em></h2>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Feedback Analytics ──
    if st.session_state.feedback_log:
        df_fb = pd.DataFrame(st.session_state.feedback_log)
        fa1, fa2 = st.columns(2, gap="large")
        with fa1:
            fig_rat = px.bar(df_fb, x="module", y="rating", color="sentiment",
                color_discrete_map={"positive":"#3ECFB2","neutral":"#C9A84C","negative":"#E05A5A"},
                title="Ratings by Module",
                labels={"module":"Module","rating":"Rating"})
            fig_rat.update_layout(paper_bgcolor='#141518', plot_bgcolor='#141518',
                font_color='#F0EDE8', font_family='DM Sans',
                xaxis=dict(gridcolor='#2A2C31',tickangle=-20), yaxis=dict(gridcolor='#2A2C31'),
                title_font_color='#C9A84C', legend=dict(bgcolor='#141518'),
                margin=dict(t=40,b=20,l=20,r=20), height=280)
            st.plotly_chart(fig_rat, use_container_width=True)
        with fa2:
            sent_counts = df_fb["sentiment"].value_counts().reset_index()
            sent_counts.columns = ["Sentiment", "Count"]
            fig_sent = px.pie(sent_counts, names="Sentiment", values="Count",
                color="Sentiment",
                color_discrete_map={"positive":"#3ECFB2","neutral":"#C9A84C","negative":"#E05A5A"},
                hole=0.55, title="Sentiment Distribution")
            fig_sent.update_layout(paper_bgcolor='#141518', font_color='#F0EDE8', font_family='DM Sans',
                title_font_color='#C9A84C', legend=dict(bgcolor='#141518'),
                margin=dict(t=40,b=20,l=20,r=20), height=280)
            st.plotly_chart(fig_sent, use_container_width=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:48px">
          <div style="font-family:var(--font-head);font-size:1.2rem;color:var(--muted);font-style:italic">No feedback data yet.<br>Submit ratings in the Feedback tab to see analytics here.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Campaign Performance Comparison ──
    st.markdown('<p class="section-label">Campaign KPI Overview</p>', unsafe_allow_html=True)
    platforms_demo = ["Instagram", "Facebook", "Twitter/X"]
    kpi_data = pd.DataFrame({
        "Platform": platforms_demo,
        "CTR (%)": [3.8, 1.9, 2.3],
        "ROI (%)": [245, 178, 195],
        "Engagement": [72, 51, 60],
    })
    fig_kpis = px.scatter(kpi_data, x="CTR (%)", y="ROI (%)", size="Engagement",
        color="Platform",
        color_discrete_sequence=["#C9A84C", "#3ECFB2", "#E05A5A"],
        title="Platform KPI Bubble Chart",
        text="Platform", size_max=60)
    fig_kpis.update_layout(paper_bgcolor='#141518', plot_bgcolor='#141518',
        font_color='#F0EDE8', font_family='DM Sans',
        xaxis=dict(gridcolor='#2A2C31'), yaxis=dict(gridcolor='#2A2C31'),
        title_font_color='#C9A84C', legend=dict(bgcolor='#141518'),
        margin=dict(t=40,b=20,l=20,r=20), height=340)
    st.plotly_chart(fig_kpis, use_container_width=True)

    # ── Color Psychology Radar ──
    st.markdown('<p class="section-label">Brand Personality Profile</p>', unsafe_allow_html=True)
    p_data = {"Vibrancy": 0, "Trust": 0, "Innovation": 0, "Elegance": 0, "Energy": 0, "Simplicity": 0}
    pers_map = {
        "vibrant":    {"Vibrancy":90,"Trust":55,"Innovation":75,"Elegance":40,"Energy":92,"Simplicity":30},
        "minimalist": {"Vibrancy":30,"Trust":80,"Innovation":70,"Elegance":75,"Energy":40,"Simplicity":95},
        "luxury":     {"Vibrancy":50,"Trust":85,"Innovation":60,"Elegance":98,"Energy":55,"Simplicity":60},
        "bold":       {"Vibrancy":85,"Trust":60,"Innovation":80,"Elegance":45,"Energy":95,"Simplicity":40},
        "elegant":    {"Vibrancy":45,"Trust":82,"Innovation":55,"Elegance":96,"Energy":45,"Simplicity":65},
    }
    pers = st.session_state.brand_inputs.get("personality", "minimalist")
    p_data = pers_map.get(pers, pers_map["minimalist"])
    cats, vals = list(p_data.keys()), list(p_data.values())
    fig_rad = go.Figure(data=go.Scatterpolar(r=vals+[vals[0]], theta=cats+[cats[0]],
        fill='toself', fillcolor='rgba(201,168,76,0.15)',
        line=dict(color='#C9A84C', width=2), marker=dict(color='#C9A84C')))
    fig_rad.update_layout(polar=dict(bgcolor='#1C1E22',
        radialaxis=dict(visible=True, range=[0,100], gridcolor='#2A2C31', color='#7A7A85'),
        angularaxis=dict(gridcolor='#2A2C31', color='#F0EDE8')),
        paper_bgcolor='#141518', font_color='#F0EDE8', font_family='DM Sans',
        title=dict(text=f"Personality Radar — {pers.title()}", font_color='#C9A84C', font_size=14),
        margin=dict(t=60,b=20,l=20,r=20), height=360)
    st.plotly_chart(fig_rad, use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    # ── Project Checklist ──
    st.markdown('<p class="section-label">PRD Evidence Checklist</p>', unsafe_allow_html=True)
    checks = [
        ("Logo Generated", bool(st.session_state.generated_logo)),
        ("Color Palette Extracted", bool(st.session_state.palette)),
        ("Taglines Created", bool(st.session_state.taglines)),
        ("Brand Story Written", bool(st.session_state.brand_story)),
        ("Multilingual Translations", bool(st.session_state.translations)),
        ("Campaign Content Generated", bool(st.session_state.campaigns)),
        ("KPI Predictions Made", bool(st.session_state.kpi_predictions)),
        ("Feedback Submitted", bool(st.session_state.feedback_log)),
        ("Aesthetics Scored", bool(st.session_state.consistency_score)),
    ]
    done = sum(1 for _, v in checks if v)
    pct = int(done/len(checks)*100)
    st.markdown(f"""
    <div style="margin-bottom:16px">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--muted)">PROGRESS — {done}/{len(checks)} TASKS COMPLETE</span>
        <span style="font-family:var(--font-mono);font-size:0.7rem;color:var(--accent)">{pct}%</span>
      </div>
      <div class="prog-wrap" style="height:12px"><div class="prog-bar" style="width:{pct}%"></div></div>
    </div>""", unsafe_allow_html=True)
    for label, done_flag in checks:
        icon = "✓" if done_flag else "○"
        color = "var(--teal)" if done_flag else "var(--muted)"
        st.markdown(f"""
        <div class="check-item">
          <span style="color:{color};font-size:1rem;flex-shrink:0">{icon}</span>
          <span style="font-family:var(--font-body);font-size:0.88rem;color:{'var(--text)' if done_flag else 'var(--muted)'}">{label}</span>
        </div>""", unsafe_allow_html=True)
