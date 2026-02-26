"""
AgriChain – app.py
Streamlit frontend for the Harvest Readiness Score dashboard.
"""

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from modules.price_analysis import analyse_prices
from modules.scoring import generate_score
from modules.weather import get_weather_score
from modules.explanation import generate_explanation
from modules.ai_assistant import get_ai_response, build_context

# Load .env file automatically (works locally; on cloud use platform secrets)
load_dotenv()


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AgriChain – Harvest Readiness Intelligence",
    page_icon="🌾",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS – Match screenshot theme
# ---------------------------------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0c1a0c !important;
    color: #d4f0c0 !important;
}
.stApp {
    background-color: #0c1a0c !important;
}
.main, .main > div, .block-container {
    background-color: #0c1a0c !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #0c1a0c !important;
}
[data-testid="stHeader"] {
    background-color: #0c1a0c !important;
    border-bottom: 1px solid #1e3a1e !important;
}
.main > div { padding-top: 1rem !important; }
section[data-testid="stSidebar"] { background-color: #091409; border-right: 1px solid #1e3a1e; }
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem; }

/* ── Sidebar brand ── */
.sidebar-brand {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 0.2rem;
}
.sidebar-brand-name {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem; font-weight: 800;
    color: #6ee86e;
}
.sidebar-subtitle {
    font-size: 0.78rem; color: #4a7a4a;
    font-weight: 500; margin-bottom: 1.5rem;
}
.sidebar-divider { border: none; border-top: 1px solid #1e3a1e; margin: 1.2rem 0; }

/* ── Sidebar input labels ── */
.input-label {
    font-size: 0.78rem; font-weight: 600; color: #6ee86e;
    text-transform: uppercase; letter-spacing: 0.07em;
    margin-bottom: 0.3rem; display: flex; align-items: center; gap: 6px;
}
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stTextInput"] label {
    color: #6ee86e !important; font-size: 0.82rem !important; font-weight: 600 !important;
}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] > div > div {
    background-color: #112011 !important;
    border: 1px solid #2a4a2a !important;
    border-radius: 8px !important;
    color: #d4f0c0 !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
    background-color: #6ee86e !important;
}

/* ── Button ── */
.stButton > button {
    background-color: #6ee86e;
    color: #0c1a0c;
    font-family: 'Syne', sans-serif;
    font-weight: 700; font-size: 0.95rem;
    border: none; border-radius: 8px;
    padding: 0.55rem 1.5rem; width: 100%;
    cursor: pointer; transition: background 0.2s;
}
.stButton > button:hover { background-color: #8ff58f; }

/* ── Hero card ── */
.hero-card {
    background: linear-gradient(135deg, #122112, #0e1a0e);
    border: 1px solid #2a4a2a;
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    display: flex; align-items: center; gap: 16px;
    margin-bottom: 1rem;
}
.hero-logo { font-size: 2.4rem; }
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem; font-weight: 800;
    color: #d4f0c0; margin: 0;
}
.hero-subtitle { color: #4a7a4a; font-size: 0.85rem; margin-top: 2px; }

/* ── Score card ── */
.score-card {
    background: linear-gradient(135deg, #122112, #0e1a0e);
    border: 1px solid #2a4a2a;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1rem;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5.5rem; font-weight: 800;
    line-height: 1; color: #6ee86e;
}
.score-denom { font-size: 1.2rem; color: #4a7a4a; margin-top: 4px; }
.score-badge {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 0.4rem 1.1rem; border-radius: 20px;
    font-size: 0.88rem; font-weight: 600;
    margin: 0.8rem auto 0.4rem auto;
}
.badge-green  { background: #1a3a1a; border: 1px solid #4caf50; color: #4caf50; }
.badge-yellow { background: #2a280a; border: 1px solid #ffc107; color: #ffc107; }
.badge-red    { background: #2a0a0a; border: 1px solid #f44336; color: #f44336; }
.score-tagline { font-size: 0.82rem; color: #4a7a4a; margin-top: 4px; }

/* ── Inline component scores ── */
.component-scores {
    display: flex; justify-content: center; gap: 2rem;
    margin-top: 1.2rem; flex-wrap: wrap;
}
.comp-item { text-align: center; }
.comp-label { font-size: 0.72rem; color: #4a7a4a; text-transform: uppercase; letter-spacing: 0.06em; }
.comp-value { font-size: 1rem; font-weight: 700; color: #d4f0c0; }
.comp-value span { font-size: 0.78rem; color: #4a7a4a; }

/* ── Section card ── */
.section-card {
    background: #112011;
    border: 1px solid #2a4a2a;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}
.section-title {
    font-size: 0.78rem; font-weight: 600;
    color: #6ee86e; text-transform: uppercase;
    letter-spacing: 0.08em; margin-bottom: 1rem;
}

/* ── Metric grid ── */
.metric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
.metric-box {
    background: #0e1a0e; border: 1px solid #1e3a1e;
    border-radius: 10px; padding: 0.9rem 1rem;
}
.metric-lbl { font-size: 0.72rem; color: #4a7a4a; text-transform: uppercase; letter-spacing: 0.06em; }
.metric-val { font-size: 1.3rem; font-weight: 700; color: #d4f0c0; margin-top: 2px; }
.metric-val.positive { color: #6ee86e; }
.metric-val.negative { color: #f44336; }

/* ── Weather badges inline ── */
.weather-row { display: flex; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap; }
.weather-chip {
    background: #0e1a0e; border: 1px solid #1e3a1e;
    border-radius: 8px; padding: 0.6rem 1rem; flex: 1; min-width: 120px;
}
.weather-chip .metric-lbl { margin-bottom: 4px; }

/* ── Explanation section ── */
.explanation-text {
    font-size: 0.88rem; line-height: 1.7; color: #9ec89e;
    white-space: pre-wrap;
}

/* ── Chat area ── */
.chat-card {
    background: #112011;
    border: 1px solid #2a4a2a;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}
.chat-title {
    font-size: 0.78rem; font-weight: 600; color: #6ee86e;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1rem;
}
.chat-msg-user {
    background: #1a3a1a; border-radius: 10px;
    padding: 0.7rem 1rem; margin-bottom: 0.6rem;
    font-size: 0.88rem; color: #d4f0c0;
    text-align: right;
}
.chat-msg-ai {
    background: #0e1a0e; border: 1px solid #1e3a1e;
    border-radius: 10px; padding: 0.7rem 1rem;
    margin-bottom: 0.6rem; font-size: 0.88rem;
    color: #9ec89e; line-height: 1.6;
}
div[data-testid="stTextInput"] input {
    background-color: #0e1a0e !important;
    border: 1px solid #2a4a2a !important;
    border-radius: 8px !important;
    color: #d4f0c0 !important;
    font-size: 0.9rem !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #3a5a3a !important; }

/* ── Info box ── */
.info-box {
    background: #0e1a0e; border: 1px solid #1e3a1e;
    border-radius: 10px; padding: 1.2rem 1.4rem;
    color: #4a7a4a; font-size: 0.88rem; text-align: center;
}

/* ── Hide streamlit default elements ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Mandi → coordinates lookup
# ---------------------------------------------------------------------------

MANDI_COORDINATES: dict[str, tuple[float, float]] = {
    "Sangli":       (16.8524, 74.5815),
    "Palghar":      (19.6967, 72.7656),
    "Ulhasnagar":   (19.2183, 73.1558),
    "Vasai":        (19.3919, 72.8397),
    "Kille Dharur": (18.0500, 76.5667),
    "_default":     (20.5937, 78.9629),
}

STORAGE_ICONS = {
    "cold_storage": "❄️",
    "warehouse":    "🏗️",
    "covered_shed": "🏚️",
    "open_yard":    "🌿",
    "none":         "🚫",
}

def get_mandi_coordinates(mandi: str) -> tuple[float, float]:
    return MANDI_COORDINATES.get(mandi, MANDI_COORDINATES["_default"])

# ---------------------------------------------------------------------------
# Load CSV
# ---------------------------------------------------------------------------

CSV_PATH = "data/mandi_prices.csv"

@st.cache_data
def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Crop"]  = df["Crop"].str.strip()
    df["Mandi"] = df["Mandi"].str.strip()
    return df

try:
    price_df  = load_csv(CSV_PATH)
    all_crops = sorted(price_df["Crop"].dropna().unique().tolist())
except FileNotFoundError:
    st.error(f"📂 CSV not found at '{CSV_PATH}'. Please add the data file and restart.")
    st.stop()
except Exception as e:
    st.error(f"❌ Failed to load price data: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "chat_history"     not in st.session_state: st.session_state.chat_history     = []
if "ai_context"       not in st.session_state: st.session_state.ai_context       = ""
if "analysis_done"    not in st.session_state: st.session_state.analysis_done    = False
if "score_result"     not in st.session_state: st.session_state.score_result     = None
if "price_result"     not in st.session_state: st.session_state.price_result     = None
if "weather_result"   not in st.session_state: st.session_state.weather_result   = None
if "explanation_text" not in st.session_state: st.session_state.explanation_text = ""
if "selected_crop"    not in st.session_state: st.session_state.selected_crop    = ""
if "selected_mandi"   not in st.session_state: st.session_state.selected_mandi   = ""

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

STORAGE = ["cold_storage", "warehouse", "covered_shed", "open_yard", "none"]

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <span style="font-size:1.4rem;">🌾</span>
        <span class="sidebar-brand-name">AgriChain</span>
    </div>
    <div class="sidebar-subtitle">Harvest Readiness Intelligence</div>
    <hr class="sidebar-divider">
    """, unsafe_allow_html=True)

    crop = st.selectbox("🌱  Crop", all_crops, index=0)

    mandis_for_crop = sorted(
        price_df[price_df["Crop"] == crop]["Mandi"].dropna().unique().tolist()
    )
    mandi        = st.selectbox("🏪  Mandi Market", mandis_for_crop, index=0)
    storage_type = st.selectbox(
        "🏚️  Storage Type",
        STORAGE,
        index=0,
        format_func=lambda x: f"{STORAGE_ICONS.get(x, '')}  {x.replace('_', ' ').title()}",
    )
    distance_km  = st.slider("🚛  Distance to Mandi (km)", min_value=0, max_value=500, value=100, step=10)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    run_button = st.button("📊  Calculate Score")


# Read Groq API key solely from .env / environment variable
groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()


# ---------------------------------------------------------------------------
# Hero Card
# ---------------------------------------------------------------------------

crop_label  = crop if crop else "Crop"
mandi_label = mandi if mandi else "Mandi"

st.markdown(f"""
<div class="hero-card">
    <div class="hero-logo">🌾</div>
    <div>
        <div class="hero-title">AgriChain</div>
        <div class="hero-subtitle">Harvest Readiness Intelligence · {crop_label} · {mandi_label}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------------

if run_button:
    try:
        latitude, longitude = get_mandi_coordinates(mandi)

        with st.spinner("Analysing price trends..."):
            price_result = analyse_prices(crop=crop, mandi=mandi)

        with st.spinner(f"Fetching live weather for {mandi}..."):
            weather_result = get_weather_score(latitude=latitude, longitude=longitude)

        score_result = generate_score(
            price_score=price_result.price_score,
            weather_score=weather_result.weather_score,
            storage_type=storage_type,
            distance_km=float(distance_km),
        )

        explanation_text = generate_explanation(
            price_result=price_result,
            weather_result=weather_result,
            storage_type=storage_type,
            distance_km=distance_km,
        )

        # Store in session state
        st.session_state.analysis_done    = True
        st.session_state.score_result     = score_result
        st.session_state.price_result     = price_result
        st.session_state.weather_result   = weather_result
        st.session_state.explanation_text = explanation_text
        st.session_state.selected_crop    = crop
        st.session_state.selected_mandi   = mandi
        st.session_state.chat_history     = []  # reset chat on new analysis
        st.session_state.ai_context       = build_context(
            crop=crop, mandi=mandi,
            price_result=price_result,
            weather_result=weather_result,
            score_result=score_result,
            storage_type=storage_type,
            distance_km=distance_km,
        )

    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
    except ValueError as e:
        st.error(f"Data error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# ---------------------------------------------------------------------------
# Display results (from session state so they persist across chat interactions)
# ---------------------------------------------------------------------------

if st.session_state.analysis_done:
    score_result     = st.session_state.score_result
    price_result     = st.session_state.price_result
    weather_result   = st.session_state.weather_result
    explanation_text = st.session_state.explanation_text

    # ── Score Card ──────────────────────────────────────────────────────────
    tl = score_result.traffic_light
    badge_class = {"Green": "badge-green", "Yellow": "badge-yellow", "Red": "badge-red"}.get(tl, "badge-green")
    badge_dot   = {"Green": "🟢", "Yellow": "🟡", "Red": "🔴"}.get(tl, "🟢")
    badge_text  = {"Green": "Good Time to Sell", "Yellow": "Monitor Conditions", "Red": "Hold — Wait for Better Prices"}.get(tl, "")
    tagline     = {"Green": "Conditions are favourable — sell now", "Yellow": "Mixed signals — proceed with caution", "Red": "Market conditions are unfavourable"}.get(tl, "")

    st.markdown(f"""
    <div class="score-card">
        <div class="score-number">{int(score_result.final_score)}</div>
        <div class="score-denom">/ 100</div>
        <div><span class="score-badge {badge_class}">{badge_dot} {badge_text}</span></div>
        <div class="score-tagline">{tagline}</div>
        <div class="component-scores">
            <div class="comp-item">
                <div class="comp-label">Price</div>
                <div class="comp-value">{price_result.price_score:.1f}<span>/30</span></div>
            </div>
            <div class="comp-item">
                <div class="comp-label">Weather</div>
                <div class="comp-value">{score_result.weather_score:.1f}<span>/30</span></div>
            </div>
            <div class="comp-item">
                <div class="comp-label">Storage</div>
                <div class="comp-value">{score_result.storage_score:.1f}<span>/20</span></div>
            </div>
            <div class="comp-item">
                <div class="comp-label">Transport</div>
                <div class="comp-value">{score_result.transport_score:.1f}<span>/20</span></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two columns: Price + Weather ─────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        trend_sign  = "+" if price_result.trend_percent >= 0 else ""
        trend_cls   = "positive" if price_result.trend_percent >= 0 else "negative"
        st.markdown(f"""
        <div class="section-card">
            <div class="section-title">📈 Price Analysis</div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-lbl">7-Day Avg</div>
                    <div class="metric-val">₹{price_result.last_7_avg:,.0f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-lbl">30-Day Avg</div>
                    <div class="metric-val">₹{price_result.last_30_avg:,.0f}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-lbl">Price Trend</div>
                    <div class="metric-val {trend_cls}">{trend_sign}{price_result.trend_percent:.2f}%</div>
                </div>
                <div class="metric-box">
                    <div class="metric-lbl">Price Score</div>
                    <div class="metric-val">{price_result.price_score:.1f}<span style="font-size:0.82rem;color:#4a7a4a"> /30</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        hot_col  = "#f44336" if weather_result.hot_days_count  > 0 else "#6ee86e"
        rain_col = "#f44336" if weather_result.rainy_days_count > 0 else "#6ee86e"
        st.markdown(f"""
        <div class="section-card">
            <div class="section-title">🌤️ Weather Forecast (5-Day)</div>
            <div class="metric-grid">
                <div class="metric-box">
                    <div class="metric-lbl">Weather Score</div>
                    <div class="metric-val">{weather_result.weather_score:.1f}<span style="font-size:0.82rem;color:#4a7a4a"> /30</span></div>
                </div>
                <div class="metric-box">
                    <div class="metric-lbl">Forecast</div>
                    <div class="metric-val" style="font-size:0.95rem;color:#9ec89e">5 days</div>
                </div>
                <div class="metric-box">
                    <div class="metric-lbl">🌡️ Hot Days &gt;35°C</div>
                    <div class="metric-val" style="color:{hot_col}">{weather_result.hot_days_count}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-lbl">🌧️ Rainy Days &gt;60%</div>
                    <div class="metric-val" style="color:{rain_col}">{weather_result.rainy_days_count}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Explanation ──────────────────────────────────────────────────────────
    with st.expander("📋 Why this recommendation?", expanded=False):
        st.markdown(f'<div class="explanation-text">{explanation_text}</div>', unsafe_allow_html=True)

    # ── AI Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div class="chat-card"><div class="chat-title">🤖 AgriChain AI — Ask About Your Harvest</div>', unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-msg-user">🧑‍🌾 {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-msg-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

    # Input form (prevents full page re-run on Enter)
    with st.form(key="chat_form", clear_on_submit=True):
        col_input, col_send = st.columns([5, 1])
        with col_input:
            user_input = st.text_input(
                "Ask AI",
                placeholder="Ask anything about your harvest...",
                label_visibility="collapsed",
            )
        with col_send:
            send_btn = st.form_submit_button("Send ↑")

    st.markdown('</div>', unsafe_allow_html=True)

    if send_btn and user_input.strip():
        if not groq_api_key:
            st.warning("Please enter your Groq API key in the sidebar to use the AI assistant.")
        else:
            with st.spinner("AgriChain AI is thinking..."):
                try:
                    response = get_ai_response(
                        api_key=groq_api_key,
                        user_message=user_input.strip(),
                        context=st.session_state.ai_context,
                        chat_history=st.session_state.chat_history,
                    )
                    st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.rerun()
                except Exception as e:
                    st.error(f"AI error: {str(e).encode('ascii', errors='replace').decode('ascii')}")

else:
    # ── Welcome state ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="score-card" style="opacity:0.6;">
        <div class="score-number" style="font-size:3rem;color:#2a4a2a;">—</div>
        <div class="score-denom">/ 100</div>
        <div class="score-tagline" style="margin-top:0.8rem;">
            Configure your parameters in the sidebar and click <strong style="color:#6ee86e">Calculate Score</strong> to begin.
        </div>
    </div>
    <div class="info-box">
        🌾 &nbsp; Select your crop, mandi, storage type and distance, then click <strong>Calculate Score</strong>.<br>
        After analysis, the <strong style="color:#6ee86e">AgriChain AI</strong> will answer questions about your harvest.
    </div>
    """, unsafe_allow_html=True)
