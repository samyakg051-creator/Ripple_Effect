"""AgriChain – app.py  |  Page 1: Home + India Map + Farm Setup"""

import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_folium import st_folium

from modules.sidebar import render_page, init_session_state
from modules.map_utils import (
    build_map, extract_district_from_click,
    DISTRICT_CENTERS, CROP_EMOJI,
)
from modules.translations import t
from modules.ai_assistant import get_ai_response
from modules.price_analysis import analyse_prices
from modules.scoring import generate_score
from modules.weather import get_weather_score
from modules.explanation import generate_explanation

load_dotenv()

st.set_page_config(
    page_title="AgriChain – Home",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

lang = render_page("Home", lang="English", show_inputs=False)

# ── Title banner ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,#112011,#1e3a1e);border-radius:12px;
            padding:1rem 1.5rem;margin-bottom:1.2rem;border:1px solid #2a4a2a;">
  <span style="font-size:1.5rem;font-weight:800;color:#6ee86e;">🌾 AgriChain</span>
  <span style="font-size:.85rem;color:#52b788;margin-left:1rem;">Farm-to-Market Intelligence · Maharashtra</span>
</div>""", unsafe_allow_html=True)

# ── Two-column layout : LEFT = inputs  |  RIGHT = map ─────────────────────────
col_left, col_right = st.columns([1, 2], gap="medium")

current_district = st.session_state.get("district")
current_crop     = st.session_state.get("crop", "Wheat")
current_sowing   = st.session_state.get("sowing_date")
current_storage  = st.session_state.get("storage_type", "warehouse")
current_qty      = int(st.session_state.get("quantity", 10))

CROPS   = ["Wheat", "Tomato", "Onion", "Potato", "Rice"]
STORAGE = ["cold_storage", "warehouse", "covered_shed", "open_yard", "none"]

with col_left:
    # ── Map title label ────────────────────────────────────────────────────────
    st.markdown("""
<div style="background:#112011;border:1px solid #2a4a2a;border-radius:10px;
            padding:.7rem 1rem;margin-bottom:1rem;font-size:.82rem;color:#6ee86e;font-weight:600;">
  🗺️ INDIA · MAHARASHTRA DISTRICT SELECTOR<br>
  <span style="font-weight:400;color:#52b788;font-size:.75rem;">(PoK &amp; Aksai Chin — Integral part of India)</span>
</div>""", unsafe_allow_html=True)

    # Select Crop
    crop_idx = CROPS.index(current_crop) if current_crop in CROPS else 0
    selected_crop = st.selectbox("Select Crop", CROPS, index=crop_idx, key="crop_sel")
    if selected_crop != st.session_state.get("crop"):
        st.session_state.crop = selected_crop

    # Sowing Date
    from datetime import date
    sowing_val = st.date_input(
        "Sowing Date",
        value=current_sowing or date.today(),
        key="sowing_sel",
    )
    st.session_state.sowing_date = sowing_val

    # Storage & Quantity (compact)
    with st.expander("⚙️ More Options", expanded=False):
        st.session_state.storage_type = st.selectbox(
            "Storage Type", STORAGE,
            index=STORAGE.index(current_storage) if current_storage in STORAGE else 1,
            format_func=lambda x: x.replace("_", " ").title(),
            key="storage_sel",
        )
        st.session_state.quantity = st.number_input(
            "Quantity (quintals)", min_value=1, max_value=10000,
            value=current_qty, key="qty_sel",
        )
        st.session_state.language = st.selectbox(
            "Language", ["English", "हिंदी"],
            index=0 if st.session_state.get("language", "English") == "English" else 1,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Get Recommendation", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Analysis result  ──────────────────────────────────────────────────────
    if run_btn:
        with st.spinner("Analysing..."):
            try:
                # Pick mandi with most data for the selected crop
                import pandas as _pd
                _tmpdf = _pd.read_csv("data/mandi_prices.csv")
                _tmpdf.columns = [c.strip() for c in _tmpdf.columns]
                _crop_df = _tmpdf[_tmpdf["Crop"].str.strip().str.lower() == selected_crop.lower()]
                if _crop_df.empty:
                    st.warning(f"No price data for {selected_crop} in dataset.")
                    st.stop()
                mandi = _crop_df["Mandi"].value_counts().index[0]
                from modules.map_utils import DISTRICT_CENTERS
                dist = st.session_state.get("district", "Sangli")
                coords = DISTRICT_CENTERS.get(dist, [16.8524, 74.5815])
                lat, lon = coords[0], coords[1]
                price_r   = analyse_prices(crop=selected_crop, mandi=mandi)
                weather_r = get_weather_score(latitude=lat, longitude=lon)
                score_r   = generate_score(
                    price_score=price_r.price_score,
                    weather_score=weather_r.weather_score,
                    storage_type=st.session_state.storage_type,
                    distance_km=100.0,
                )
                tl    = score_r.traffic_light
                col_c = {"Green": "#6ee86e", "Yellow": "#f4a261", "Red": "#f44336"}.get(tl, "#6ee86e")
                icon  = {"Green": "🟢", "Yellow": "🟡", "Red": "🔴"}.get(tl, "🟢")

                # ── Plain-language verdict card ──────────────────────────────
                is_hindi  = st.session_state.get("language") == "हिंदी"
                score_val = int(score_r.final_score)

                if tl == "Green":
                    verdict    = "अभी बेचें! 🌾" if is_hindi else "SELL NOW 🌾"
                    v_sub      = "बाजार अनुकूल है" if is_hindi else "Market conditions are favourable"
                elif tl == "Yellow":
                    verdict    = "3–5 दिन प्रतीक्षा करें" if is_hindi else "WAIT 3–5 DAYS"
                    v_sub      = "कीमत और सुधर सकती है" if is_hindi else "Prices may improve slightly"
                else:
                    verdict    = "तुरंत कदम उठाएं ⚠️" if is_hindi else "ACT URGENTLY ⚠️"
                    v_sub      = "कीमतें गिर रही हैं" if is_hindi else "Prices are declining"

                st.markdown(f"""
<div style="background:#112011;border:2px solid {col_c};border-radius:12px;
            padding:1.1rem;margin-bottom:.8rem;">
  <div style="font-size:1.3rem;font-weight:800;color:{col_c};">{icon} {verdict}</div>
  <div style="font-size:.8rem;color:#52b788;margin-bottom:.6rem;">{v_sub}</div>
  <div style="font-size:2.5rem;font-weight:800;color:{col_c};line-height:1;">{score_val}</div>
  <div style="font-size:.65rem;color:#52b788;text-transform:uppercase;">/100 Readiness Score</div>
</div>""", unsafe_allow_html=True)

                # Score sub-components in plain labels
                reasons = []
                p = price_r.price_score
                w = score_r.weather_score
                s = score_r.storage_score
                reasons.append(("📈 Prices", "Rising ↑" if p >= 20 else "Stable" if p >= 14 else "Falling ↓", "#6ee86e" if p >= 20 else "#f4a261" if p >= 14 else "#f44336"))
                reasons.append(("🌤️ Weather", "Good" if w >= 24 else "Moderate" if w >= 15 else "Risky", "#6ee86e" if w >= 24 else "#f4a261" if w >= 15 else "#f44336"))
                reasons.append(("📦 Storage", "Excellent" if s >= 18 else "OK" if s >= 10 else "Upgrade needed", "#6ee86e" if s >= 18 else "#f4a261" if s >= 10 else "#f44336"))

                for label, status, rc in reasons:
                    st.markdown(f"""
<div style="display:flex;justify-content:space-between;font-size:.78rem;
            padding:.25rem .4rem;border-bottom:1px solid #1e3a1e;color:#d4f0c0;">
  <span>{label}</span><span style="color:{rc};font-weight:700;">{status}</span>
</div>""", unsafe_allow_html=True)

                # Why section
                why = []
                if p >= 20:
                    why.append("Prices rose 8–15% in the last 7 days" if not is_hindi else "पिछले 7 दिनों में कीमत 8-15% बढ़ी है")
                elif p < 14:
                    why.append("7-day prices are below 30-day average" if not is_hindi else "7-दिन की कीमत 30-दिन से कम है")
                if weather_r.today_rain_prob > 60:
                    why.append(f"Rain likely ({weather_r.today_rain_prob:.0f}%) — transport risk" if not is_hindi else f"बारिश की संभावना {weather_r.today_rain_prob:.0f}% — परिवहन में खतरा")
                if weather_r.today_humidity > 75:
                    why.append("High humidity — grain quality risk" if not is_hindi else "उच्च नमी — अनाज की गुणवत्ता को खतरा")
                if not why:
                    why.append("All indicators are balanced" if not is_hindi else "सभी संकेतक संतुलित हैं")

                st.markdown(f"""
<div style="background:#1a3a1a;border-left:3px solid #6ee86e;border-radius:6px;
            padding:.6rem .8rem;margin-top:.6rem;font-size:.75rem;color:#52b788;">
  <b style="color:#6ee86e;">{'क्यों?' if is_hindi else 'Why?'}</b><br>
  {'<br>'.join(f"• {r}" for r in why)}
</div>""", unsafe_allow_html=True)

            except ValueError as e:
                st.warning(f"Data: {e}")
            except Exception as e:
                st.error(f"Error: {str(e)[:100]}")


with col_right:
    # ── Folium map ────────────────────────────────────────────────────────────
    m = build_map(
        selected_district=current_district,
        crop=current_crop,
        sowing_date=current_sowing,
        show_mandis=False,
        show_all_markers=True,
    )
    map_data = st_folium(m, width="100%", height=500, key="home_map", returned_objects=[])

    # Capture map click → update district
    clicked = extract_district_from_click(map_data or {})
    if clicked and clicked in DISTRICT_CENTERS and clicked != st.session_state.get("district"):
        st.session_state.district = clicked
        st.rerun()

    # District dropdown BELOW map
    all_districts = sorted(DISTRICT_CENTERS.keys())
    dd_idx = all_districts.index(current_district) if current_district in all_districts else 0
    selected_dd = st.selectbox(
        "📍 District", all_districts, index=dd_idx, key="district_dd",
        help="Click a district on the map above or select here",
    )
    if selected_dd != st.session_state.get("district"):
        st.session_state.district = selected_dd
        st.rerun()

# ── AI Assistant (full width, below) ─────────────────────────────────────────
groq_key = os.environ.get("GROQ_API_KEY", "").strip()
if groq_key and not groq_key.startswith("your_groq"):
    st.divider()
    st.markdown("#### 🤖 Ask AgriChain AI")
    if "home_chat" not in st.session_state:
        st.session_state.home_chat = []
    for msg in st.session_state.home_chat:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask about your crop, weather, or selling timing..."):
        ctx = f"Crop:{selected_crop}, District:{st.session_state.get('district')}, Storage:{st.session_state.get('storage_type')}"
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    reply = get_ai_response(groq_key, prompt, ctx, st.session_state.home_chat)
                    st.write(reply)
                    st.session_state.home_chat.append({"role": "user", "content": prompt})
                    st.session_state.home_chat.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"AI error: {str(e)[:120]}")
