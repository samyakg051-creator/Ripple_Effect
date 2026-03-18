"""
pages/2_Spoilage_Prevention.py
AgriChain — Spoilage Risk & Prevention Guide
"""

import streamlit as st
from datetime import date, timedelta
from modules.agri_data import CROP_EMOJI, DEFAULT_EMOJI, CROP_DURATION
from modules.data_loader import build_mandi_price_dict, get_top_mandis_for_crop
from utils.translator import t

st.set_page_config(page_title="AgriChain — Spoilage Prevention", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0c1a0c !important; color: #d4f0c0 !important; }
.stApp, .main, .main > div, .block-container, [data-testid="stAppViewContainer"] { background-color: #0c1a0c !important; }
[data-testid="stHeader"] { background-color: #0c1a0c !important; border-bottom: 1px solid #1e3a1e !important; }
section[data-testid="stSidebar"] { background-color: #0a1a0a !important; border-right: 1px solid #1e3a1e; }
section[data-testid="stSidebar"] > div { padding: 1.2rem 1rem; }
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] div { color: #d4f0c0 !important; }
div[data-testid="stSelectbox"] > div > div { background-color: #0e2a1c !important; border: 1px solid #2d6a4f !important; border-radius: 8px !important; color: #d4f0c0 !important; }
.stButton > button { background-color: #2d6a4f; color: #fff; font-weight: 700; border: none; border-radius: 8px; padding: 0.5rem 1.5rem; width: 100%; cursor: pointer; }
.stButton > button:hover { background-color: #1a3d2e; }
.risk-card { border-radius: 16px; padding: 2rem; text-align: center; margin-bottom: 1.2rem; }
.risk-low    { background: linear-gradient(135deg,#d4edda,#c3e6cb); border: 2px solid #4caf50; }
.risk-medium { background: linear-gradient(135deg,#fff3cd,#ffeeba); border: 2px solid #ffc107; }
.risk-high   { background: linear-gradient(135deg,#f8d7da,#f5c6cb); border: 2px solid #f44336; }
.risk-label  { font-family:'Syne',sans-serif; font-size:3rem; font-weight:800; }
.risk-pct    { font-size:1.2rem; margin-top:4px; opacity:0.8; }
.tip-card  { background:#112011; border:1px solid #1e3a1e; border-radius:12px; padding:1rem 1.2rem; margin-bottom:0.6rem; box-shadow:0 2px 8px #2d6a4f08; }
.tip-title { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.4rem; }
.tip-low    { color:#155724; }
.tip-medium { color:#856404; }
.tip-high   { color:#721c24; }
.section-hd { font-family:'Syne',sans-serif; font-size:1.1rem; font-weight:800; color:#2d6a4f; margin:1.2rem 0 0.5rem; }
.metric-row { display:flex; gap:1rem; flex-wrap:wrap; margin-bottom:1rem; }
.metric-pill { background:#112011; border:1px solid #1e3a1e; border-radius:10px; padding:0.7rem 1rem; flex:1; min-width:130px; box-shadow:0 2px 8px #2d6a4f08; }
.metric-pill .lbl { font-size:0.7rem; color:#52b788; text-transform:uppercase; }
.metric-pill .val { font-size:1.2rem; font-weight:700; color:#d4f0c0; }
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

from utils.sidebar import render_sidebar
lang = render_sidebar(current_page="spoilage")

# ── Session state defaults ────────────────────────────────────────────────────
CROPS    = list(CROP_EMOJI.keys())
STORAGES = ["cold_storage", "warehouse", "covered_shed", "open_yard", "none"]
for k, v in [("crop", CROPS[0]), ("storage_type","warehouse"), ("sowing_date", date.today())]:
    if k not in st.session_state: st.session_state[k] = v

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.2rem;font-weight:800;color:#6ee86e;margin-bottom:0.3rem">&#127807; AgriChain</div>
    <div style="font-size:0.78rem;color:#a8d5ba;margin-bottom:1.2rem">{t('Spoilage Prevention', lang)}</div>
    <hr style="border:none;border-top:1px solid #2d6a4f;margin:0.8rem 0">
    """, unsafe_allow_html=True)

    crop = st.selectbox(f"&#127807; {t('Crop', lang)}", CROPS,
        index=CROPS.index(st.session_state.crop) if st.session_state.crop in CROPS else 0)
    st.session_state.crop = crop

    storage = st.selectbox(f"&#127968; {t('Storage Type', lang)}", STORAGES,
        index=STORAGES.index(st.session_state.storage_type) if st.session_state.storage_type in STORAGES else 1,
        format_func=lambda x: x.replace("_"," ").title())
    st.session_state.storage_type = storage

    sowing = st.date_input(f"&#128197; {t('Sowing Date', lang)}",
        value=st.session_state.sowing_date if isinstance(st.session_state.sowing_date, date) else date.today())
    st.session_state.sowing_date = sowing

    days_stored = st.slider(f"&#128197; {t('Days Since Harvest', lang)}", 0, 90, 7)

    st.markdown('<hr style="border:none;border-top:1px solid #2d6a4f;margin:0.8rem 0">', unsafe_allow_html=True)
    if st.button("&#8592; Harvest Score"):
        st.switch_page("app.py")
    if st.button("&#128506;&#65039; Map Explorer"):
        st.switch_page("pages/4_Map_Explorer.py")

# ── Risk calculation ──────────────────────────────────────────────────────────
STORAGE_PRESERVATION = {
    "cold_storage": 0.10, "warehouse": 0.30, "covered_shed": 0.50,
    "open_yard": 0.75, "none": 0.90,
}
CROP_SENSITIVITY = {
    "Wheat": 0.3, "Tomato": 0.95, "Onion": 0.55, "Potato": 0.60,
    "Corn": 0.45, "Soybean": 0.35, "Cotton": 0.20,
}

base_risk    = CROP_SENSITIVITY.get(crop, 0.5)
storage_mult = STORAGE_PRESERVATION.get(storage, 0.5)
time_factor  = min(days_stored / 30.0, 1.0)

raw_risk = base_risk * storage_mult * (0.4 + 0.6 * time_factor)
risk_pct = min(round(raw_risk * 100, 1), 98.0)

if risk_pct < 30:
    risk_lvl, risk_cls, risk_emoji = "LOW", "risk-low", "&#129001;"
elif risk_pct < 65:
    risk_lvl, risk_cls, risk_emoji = "MEDIUM", "risk-medium", "&#128993;"
else:
    risk_lvl, risk_cls, risk_emoji = "HIGH", "risk-high", "&#128308;"

tip_cls = {"LOW":"tip-low","MEDIUM":"tip-medium","HIGH":"tip-high"}[risk_lvl]

# ── Header ────────────────────────────────────────────────────────────────────
emoji = CROP_EMOJI.get(crop, DEFAULT_EMOJI)
duration = CROP_DURATION.get(crop, 90)
harvest_date = sowing + timedelta(days=duration)
days_to_harvest = (harvest_date - date.today()).days

st.markdown(f'<div class="section-hd">&#127697;&#65039; {t("Spoilage Risk", lang)} — {emoji} {crop}</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="metric-row">
    <div class="metric-pill"><div class="lbl">{t('Storage Type', lang)}</div><div class="val">{storage.replace("_"," ").title()}</div></div>
    <div class="metric-pill"><div class="lbl">{t('Days Since Harvest', lang)}</div><div class="val">{days_stored} {t('days', lang)}</div></div>
    <div class="metric-pill"><div class="lbl">{t('Est. Harvest Date', lang)}</div><div class="val">{harvest_date.strftime("%b %d")}</div></div>
    <div class="metric-pill"><div class="lbl">{t('Days to Harvest', lang)}</div><div class="val">{"Past" if days_to_harvest<0 else f"{days_to_harvest}d"}</div></div>
</div>
""", unsafe_allow_html=True)

# ── Risk card ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="risk-card {risk_cls}">
    <div class="risk-label">{risk_emoji} {t(risk_lvl, lang)} {t('RISK', lang)}</div>
    <div class="risk-pct">{t('Spoilage Probability', lang)}: <strong>{risk_pct}%</strong> — {days_stored} {t('days stored', lang)}</div>
</div>
""", unsafe_allow_html=True)

# ── Crop-specific tips ────────────────────────────────────────────────────────
TIPS: dict[str, dict] = {
    "Tomato":  {"LOW":["Keep at 12–15°C with 90% humidity","Check for soft spots daily"],
                "MEDIUM":["Move to cold storage immediately","Sort and remove bruised ones","Sell within 3–5 days"],
                "HIGH":["Sell at nearest mandi URGENTLY","Consider processing into paste","Losses likely if stored further"]},
    "Onion":   {"LOW":["Store in well-ventilated dry place","Keep at 25–35°C, avoid moisture"],
                "MEDIUM":["Check for sprouting — remove affected","Improve air circulation in storage"],
                "HIGH":["Cull rotting bulbs immediately","Sell remaining stock this week"]},
    "Wheat":   {"LOW":["Maintain moisture below 14%","Store in sealed bags with silica gel"],
                "MEDIUM":["Check for weevils and insects","Apply neem powder to bags"],
                "HIGH":["Fumigate storage area","Move to cold/dry storage ASAP"]},
    "Potato":  {"LOW":["Store at 4–10°C away from light","Avoid stacking more than 3 layers"],
                "MEDIUM":["Remove any green/sprouted tubers","Improve ventilation"],
                "HIGH":["Process into chips/flour if possible","Emergency sale recommended"]},
    "Corn":    {"LOW":["Store dried corn at <14% moisture","Use sealed containers"],
                "MEDIUM":["Check for mold or fungal growth","Apply fungicide if needed"],
                "HIGH":["Sell green corn immediately","Dry remaining stock urgently"]},
    "Soybean": {"LOW":["Store at <13% moisture, cool & dark","Use jute bags for air circulation"],
                "MEDIUM":["Check for discoloration","Avoid mixing old with new stock"],
                "HIGH":["Oil extraction is a good option","Emergency mandi sale advised"]},
    "Cotton":  {"LOW":["Keep away from moisture","Store in bales, protect from rain"],
                "MEDIUM":["Check for moisture seepage in bales","Rewrap damp bales"],
                "HIGH":["Sell at ginning factory now","Risk of fiber grade downgrade"]},
}

crop_tips = TIPS.get(crop, {
    "LOW":["Store in cool dry place","Monitor regularly"],
    "MEDIUM":["Improve storage conditions","Check every 2 days"],
    "HIGH":["Sell immediately","Consult agri expert"]
})

st.markdown(f'<div class="section-hd">&#128736;&#65039; {t("Prevention Tips", lang)}</div>', unsafe_allow_html=True)

def show_tips(level: str):
    for tip in crop_tips.get(level, []):
            icon = {"LOW":"&#9989;","MEDIUM":"&#9888;&#65039;","HIGH":"&#128680;"}[level]
            st.markdown(f"""
        <div class="tip-card">
            <div class="tip-title {tip_cls}">{icon} {t(level, lang)} {t('RISK ACTION', lang)}</div>
            <div style="font-size:0.9rem">{tip}</div>
        </div>""", unsafe_allow_html=True)

show_tips(risk_lvl)
# Also show lower-risk tips as general guidance
if risk_lvl in ("MEDIUM","HIGH"):
    show_tips("LOW")

# ── Preservation Actions — Ranked by Cost & Effectiveness ─────────────────────
st.markdown(f'<div class="section-hd">&#128176; {t("Preservation Actions", lang)}</div>', unsafe_allow_html=True)

PRESERVATION_ACTIONS = {
    "Tomato": [
        ("Move to cold storage (2-4°C)", "₹500-800/day", "⭐⭐⭐⭐⭐", "Immediate", "Extends life by 2-3 weeks"),
        ("Sort & remove damaged ones", "Free", "⭐⭐⭐⭐", "30 min", "Prevents rot from spreading"),
        ("Process into paste/puree", "₹200-400/batch", "⭐⭐⭐⭐", "2-3 hours", "6-month shelf life"),
        ("Sun-dry for tomato flakes", "Free (needs sun)", "⭐⭐⭐", "2-3 days", "Lasts months"),
        ("Ventilated shade storage", "₹50-100/day", "⭐⭐", "Immediate", "Adds 2-4 days"),
    ],
    "Onion": [
        ("Store in well-ventilated dry room", "₹100-200/month", "⭐⭐⭐⭐⭐", "Immediate", "Lasts 3-6 months"),
        ("Remove sprouting/rotting bulbs", "Free", "⭐⭐⭐⭐", "1 hour", "Prevents chain rot"),
        ("Apply maleic hydrazide spray", "₹300-500/acre", "⭐⭐⭐⭐", "Pre-harvest", "Prevents sprouting"),
        ("Cure in shade for 7-10 days", "Free", "⭐⭐⭐", "7-10 days", "Hardens skin, lasts longer"),
        ("Cold storage (0-2°C)", "₹800-1200/month", "⭐⭐⭐⭐⭐", "Immediate", "Lasts 5-8 months"),
    ],
    "Wheat": [
        ("Sun-dry to <14% moisture", "Free", "⭐⭐⭐⭐⭐", "1-2 days", "Safe for months"),
        ("Store in sealed bags", "₹15-30/bag", "⭐⭐⭐⭐", "Immediate", "Keeps insects out"),
        ("Add neem leaves to bags", "Free", "⭐⭐⭐", "Immediate", "Natural insect repellent"),
        ("Hermetic storage (Purdue bags)", "₹80-120/bag", "⭐⭐⭐⭐⭐", "Immediate", "No chemical needed, 6+ months"),
        ("Fumigate with aluminium phosphide", "₹500-800/lot", "⭐⭐⭐⭐", "1-2 days", "Kills all insects"),
    ],
    "Potato": [
        ("Store at 4-8°C in dark", "₹500-700/month", "⭐⭐⭐⭐⭐", "Immediate", "Lasts 3-5 months"),
        ("Remove green/sprouted tubers", "Free", "⭐⭐⭐⭐", "1 hour", "Prevents toxin buildup"),
        ("Apply CIPC sprout inhibitor", "₹200-400/tonne", "⭐⭐⭐⭐", "Immediate", "Prevents sprouting"),
        ("Make chips/dehydrated slices", "₹300-600/batch", "⭐⭐⭐", "3-4 hours", "Months of shelf life"),
        ("Ventilated heap storage", "₹100-200", "⭐⭐", "Immediate", "Adds 1-2 weeks"),
    ],
    "Corn": [
        ("Sun-dry to <14% moisture", "Free", "⭐⭐⭐⭐⭐", "2-3 days", "Months of safe storage"),
        ("Store in metal bins (sealed)", "₹2000-5000 (one-time)", "⭐⭐⭐⭐⭐", "Immediate", "Years of use"),
        ("Apply neem oil coating", "₹100-200/batch", "⭐⭐⭐", "30 min", "Natural pest repellent"),
        ("Hermetic bags (triple layer)", "₹80-120/bag", "⭐⭐⭐⭐", "Immediate", "No insects for months"),
        ("Process into corn flour", "₹400-700/batch", "⭐⭐⭐", "Half day", "Long shelf life"),
    ],
    "Soybean": [
        ("Dry to <13% moisture", "Free", "⭐⭐⭐⭐⭐", "1-2 days", "Months of storage"),
        ("Sealed jute bag storage", "₹20-40/bag", "⭐⭐⭐⭐", "Immediate", "Good air flow, no pests"),
        ("Oil extraction at mill", "₹800-1500/batch", "⭐⭐⭐⭐", "Same day", "Oil + cake both sellable"),
        ("Cold storage (if available)", "₹600-900/month", "⭐⭐⭐⭐⭐", "Immediate", "6+ months"),
        ("Mix with neem leaves", "Free", "⭐⭐⭐", "Immediate", "Natural insect barrier"),
    ],
    "Cotton": [
        ("Store as pressed bales", "₹300-500/bale", "⭐⭐⭐⭐⭐", "Same day", "Protected from moisture"),
        ("Keep under waterproof cover", "₹200-400 (tarpaulin)", "⭐⭐⭐⭐", "Immediate", "Prevents moisture damage"),
        ("Sell to ginning factory", "No cost", "⭐⭐⭐⭐⭐", "Same day", "Direct sale, no storage needed"),
        ("Elevate from ground on pallets", "₹100-200", "⭐⭐⭐", "Immediate", "Avoids ground moisture"),
        ("Re-dry if moisture >10%", "₹200-400/batch", "⭐⭐⭐⭐", "1 day", "Prevents fiber grade loss"),
    ],
}

actions = PRESERVATION_ACTIONS.get(crop, [
    ("Move to cool dry place", "₹100-300/day", "⭐⭐⭐⭐", "Immediate", "General preservation"),
    ("Sort and remove damaged items", "Free", "⭐⭐⭐", "1 hour", "Prevents spread"),
    ("Sell at nearest mandi", "Transport cost only", "⭐⭐⭐⭐⭐", "Same day", "No storage risk"),
])

# Render as styled cards
for rank, (action, cost, effectiveness, time_needed, benefit) in enumerate(actions, 1):
    rank_color = "#6ee86e" if rank <= 2 else ("#ffc107" if rank <= 4 else "#4a7a4a")
    st.markdown(f"""
    <div class="tip-card" style="display:flex;align-items:center;gap:1rem;">
        <div style="font-size:1.6rem;font-weight:800;color:{rank_color};min-width:32px;text-align:center">#{rank}</div>
        <div style="flex:1">
            <div style="font-weight:700;color:#d4f0c0;font-size:0.92rem">{action}</div>
            <div style="display:flex;gap:1.5rem;margin-top:4px;flex-wrap:wrap">
                <span style="font-size:0.78rem;color:#555">💰 {t('Cost', lang)}: <b style="color:#1b1b1b">{cost}</b></span>
                <span style="font-size:0.78rem;color:#555">⭐ {t('Rating', lang)}: <b style="color:#b8860b">{effectiveness}</b></span>
                <span style="font-size:0.78rem;color:#555">⏱️ {t('Time', lang)}: <b style="color:#1b1b1b">{time_needed}</b></span>
            </div>
            <div style="font-size:0.76rem;color:#2d6a4f;margin-top:3px">✅ {benefit}</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Best mandi for emergency sale ─────────────────────────────────────────────
st.markdown(f'<div class="section-hd">&#127978; {t("Best Mandi for Emergency Sale", lang)}</div>', unsafe_allow_html=True)
top_df = get_top_mandis_for_crop(crop, n=3)
if top_df.empty:
    st.info(t("No mandi data available", lang))
else:
    cols = st.columns(len(top_df))
    for i, row in top_df.iterrows():
        with cols[i]:
            st.markdown(f"""
            <div class="tip-card" style="text-align:center">
                <div style="font-size:1.4rem">&#127978;</div>
                <div style="font-weight:700;color:#2d6a4f">{row['Mandi']}</div>
                <div style="font-size:0.82rem;color:#555">{t('Avg', lang)}: &#8377;{row['AvgPrice']:,}/qtl</div>
                <div style="font-size:1.1rem;font-weight:700;margin-top:4px">&#8377;{row['LatestPrice']:,}/qtl</div>
            </div>""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#52b788;font-size:0.76rem;margin-top:1rem">
    {t('Risk disclaimer', lang)}
</div>""", unsafe_allow_html=True)

