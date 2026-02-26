"""AgriChain – pages/3_Spoilage.py  |  Page 4: Spoilage Risk (no map)"""

import streamlit as st

from modules.sidebar import render_page
from modules.map_utils import DISTRICT_CENTERS
from modules.translations import t, CROP_EMOJI
from modules.spoilage import calculate_spoilage_risk
from modules.weather import get_weather_score
from modules.preservation import get_preservation_actions

st.set_page_config(page_title="AgriChain – Spoilage", page_icon="⚠️", layout="wide")

lang = render_page("Spoilage", lang="English", show_inputs=False)

crop     = st.session_state.get("crop")
district = st.session_state.get("district")
storage  = st.session_state.get("storage_type", "warehouse")
qty      = int(st.session_state.get("quantity", 10))

if not (crop and district):
    st.warning(f"🌾 {t('setup_first', lang)}")
    st.stop()

emoji = CROP_EMOJI.get(crop, "🌱")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#2a0a0a,#5a1a00);border-radius:12px;
            padding:1.1rem 1.6rem;color:#ffd699;margin-bottom:1.2rem;border:1px solid #8b2500;">
  <div style="font-size:1.4rem;font-weight:800;">⚠️ Spoilage Risk</div>
  <div style="opacity:.85;font-size:.85rem;">{emoji} {crop} · {district} · {storage.replace('_',' ').title()}</div>
</div>""", unsafe_allow_html=True)

# ── Layout: LEFT = weather + inputs | RIGHT = risk ────────────────────────────
col_left, col_right = st.columns([3, 2], gap="medium")

# ── Fetch live weather ────────────────────────────────────────────────────────
pos           = DISTRICT_CENTERS.get(district, [19.7515, 75.7139])
avg_temp      = 28.0
avg_humidity  = 55.0
rain_prob     = 30.0
hot_days      = 0
rainy_days    = 0
wx            = None

try:
    with st.spinner("Fetching live weather..."):
        wx          = get_weather_score(latitude=pos[0], longitude=pos[1])
    avg_temp     = wx.today_max_temp
    avg_humidity = wx.avg_humidity
    rain_prob    = wx.today_rain_prob
    hot_days     = wx.hot_days_count
    rainy_days   = wx.rainy_days_count
except Exception as e:
    col_left.warning(f"⚠️ Weather unavailable ({str(e)[:60]}) — using moderate defaults.")

with col_left:
    # ── Live weather cards ─────────────────────────────────────────────────────
    st.markdown("<div style='font-weight:700;color:#f4a261;margin-bottom:.6rem;'>🌤️ Current Weather — " + district + "</div>", unsafe_allow_html=True)

    temp_col = "#f44336" if avg_temp > 38 else ("#f4a261" if avg_temp > 32 else "#6ee86e")
    hum_col  = "#f44336" if avg_humidity > 80 else ("#f4a261" if avg_humidity > 65 else "#6ee86e")
    rain_col = "#f44336" if rain_prob > 70 else ("#f4a261" if rain_prob > 40 else "#6ee86e")
    wind_val = f"{wx.today_wind_speed:.0f}" if wx else "—"

    st.markdown(f"""
<div style="background:#112011;border:1px solid #2a4a2a;border-radius:12px;padding:1rem;margin-bottom:1rem;">
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.6rem;">
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.4rem;">🌡️</div>
      <div style="font-size:1.5rem;font-weight:800;color:{temp_col};">{avg_temp:.0f}°C</div>
      <div style="font-size:.7rem;color:#52b788;">Temperature</div>
      <div style="font-size:.68rem;color:{'#f44336' if avg_temp>35 else '#52b788'};">
        {"🔥 Extreme heat" if avg_temp>38 else "⚠️ High temp" if avg_temp>32 else "✅ Comfortable"}
      </div>
    </div>
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.4rem;">💧</div>
      <div style="font-size:1.5rem;font-weight:800;color:{hum_col};">{avg_humidity:.0f}%</div>
      <div style="font-size:.7rem;color:#52b788;">Humidity</div>
      <div style="font-size:.68rem;color:{'#f44336' if avg_humidity>80 else '#f4a261' if avg_humidity>65 else '#52b788'};">
        {"🦠 Mold risk!" if avg_humidity>80 else "⚠️ High humidity" if avg_humidity>65 else "✅ Acceptable"}
      </div>
    </div>
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.4rem;">🌧️</div>
      <div style="font-size:1.5rem;font-weight:800;color:{rain_col};">{rain_prob:.0f}%</div>
      <div style="font-size:.7rem;color:#52b788;">Rain Chance</div>
      <div style="font-size:.68rem;color:{'#f44336' if rain_prob>70 else '#f4a261' if rain_prob>40 else '#52b788'};">
        {"🌧️ Avoid transport!" if rain_prob>70 else "⚠️ Plan ahead" if rain_prob>40 else "✅ Clear roads"}
      </div>
    </div>
  </div>
  <div style="text-align:center;margin-top:.6rem;font-size:.75rem;color:#52b788;">
    💨 Wind: <b>{wind_val} km/h</b> &nbsp;|&nbsp;
    🌡️ 5-day avg humidity: <b>{avg_humidity:.0f}%</b>
  </div>
</div>""", unsafe_allow_html=True)

    # 5-day strip
    if wx and wx.forecast:
        st.markdown("<div style='font-size:.78rem;color:#52b788;margin-bottom:.3rem;font-weight:600;'>📅 5-Day Outlook</div>", unsafe_allow_html=True)
        dcols = st.columns(5)
        for i, (dc, day) in enumerate(zip(dcols, wx.forecast)):
            label  = "Today" if i == 0 else day.date[5:]
            r_col  = "#f44336" if day.rain_prob > 70 else ("#f4a261" if day.rain_prob > 40 else "#6ee86e")
            dc.markdown(f"""
<div style="background:#1e3a1e;border-radius:8px;padding:.45rem;text-align:center;font-size:.7rem;">
  <div style="color:#52b788;font-size:.65rem;">{label}</div>
  <div>{"☀️" if day.rain_prob < 30 else "🌦️" if day.rain_prob < 65 else "🌧️"}</div>
  <div style="color:#d4f0c0;font-weight:700;">{day.max_temp:.0f}°</div>
  <div style="color:{r_col};">{day.rain_prob:.0f}%</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    distance_km = st.slider("🚛 Distance to nearest Mandi (km)", 0, 500, 100, 10)

with col_right:
    # ── Spoilage risk calculation ──────────────────────────────────────────────
    result = calculate_spoilage_risk(
        crop=crop, storage_type=storage,
        distance_km=float(distance_km),
        hot_days=hot_days, rainy_days=rainy_days,
        avg_temp_c=avg_temp,
        avg_humidity_pct=avg_humidity,
        rain_prob_pct=rain_prob,
    )

    level    = result.risk_level
    risk_pct = result.spoilage_risk_pct
    gc       = {"Low": "#6ee86e", "Medium": "#f4a261", "High": "#f44336"}[level]
    ri       = {"Low": "🟢",       "Medium": "🟡",       "High": "🔴"}[level]
    rl       = {"Low": "LOW RISK", "Medium": "MODERATE", "High": "HIGH RISK"}[level]

    # Risk gauge
    st.markdown(f"""
<div style="background:#112011;border:2px solid {gc};border-radius:14px;
            padding:1.6rem;text-align:center;margin-bottom:.8rem;">
  <div style="font-size:4rem;font-weight:800;color:{gc};line-height:1;">{risk_pct:.0f}%</div>
  <div style="font-size:.72rem;color:#52b788;text-transform:uppercase;letter-spacing:.1em;">Spoilage Risk</div>
  <div style="margin-top:.5rem;font-size:1.1rem;font-weight:700;color:{gc};">{ri} {rl}</div>
  <div style="background:#1e3a1e;border-radius:20px;height:10px;overflow:hidden;margin-top:.8rem;">
    <div style="background:{gc};width:{risk_pct}%;height:100%;border-radius:20px;"></div>
  </div>
</div>""", unsafe_allow_html=True)

    # Recommendation
    rec_bg = {"Low":"#1a3a1a","Medium":"#2a200a","High":"#2a0a0a"}[level]
    st.markdown(f"""
<div style="background:{rec_bg};border-left:4px solid {gc};border-radius:8px;
            padding:.9rem 1rem;margin-bottom:1rem;font-size:.85rem;color:#d4f0c0;">
  {result.recommendation}
</div>""", unsafe_allow_html=True)

    # Key metrics
    m1, m2 = st.columns(2)
    m1.metric("📦 Shelf Life", f"{result.shelf_life_days} days")
    m2.metric("🚛 Transit",    f"{result.transport_hours:.1f} hrs")
    m3, m4 = st.columns(2)
    m3.metric("📦 Quantity",   f"{qty} qtl")

    # Risk breakdown
    st.markdown("""
<div style="font-size:.78rem;color:#52b788;font-weight:600;margin-top:.6rem;margin-bottom:.4rem;">
  📊 Risk Breakdown
</div>""", unsafe_allow_html=True)

    factors = [
        ("Base (transport)", result.base_risk, "#52b788"),
        ("Temperature",      result.temp_penalty,     "#f44336" if result.temp_penalty > 10 else "#f4a261"),
        ("Humidity",         result.humidity_penalty, "#f44336" if result.humidity_penalty > 8 else "#f4a261"),
        ("Rain Probability", result.rain_penalty,     "#6baed6"),
        ("Storage Type",     result.storage_adj,      "#6ee86e" if result.storage_adj < 0 else "#f4a261"),
    ]
    for label, val, color in factors:
        sign = "+" if val >= 0 else ""
        st.markdown(f"""
<div style="display:flex;justify-content:space-between;align-items:center;
            padding:.22rem .5rem;font-size:.78rem;color:#d4f0c0;border-bottom:1px solid #1e3a1e;">
  <span>{label}</span>
  <span style="font-weight:700;color:{color};">{sign}{val:.1f}%</span>
</div>""", unsafe_allow_html=True)

    # Upgrade tip
    if level in ["Medium", "High"]:
        upgrade = {
            "none":"covered shed or warehouse", "open_yard":"covered shed or warehouse",
            "covered_shed":"warehouse or cold storage", "warehouse":"cold storage",
        }.get(storage)
        if upgrade:
            st.info(f"💡 Upgrading to **{upgrade.title()}** could meaningfully reduce your risk.")

# ── Preservation Actions (full width below both columns) ──────────────────────
st.divider()
lang_sel = st.session_state.get("language", "English")
st.markdown(f"""
<div style='font-size:1.1rem;font-weight:700;color:#f4a261;margin-bottom:.8rem;'>
  🛡️ Preservation Actions — {emoji} {crop}
  <span style='font-size:.78rem;font-weight:400;color:#52b788;margin-left:.5rem;'>
    Ranked by cost · each action adds shelf life
  </span>
</div>""", unsafe_allow_html=True)

actions = get_preservation_actions(crop)

diff_cols = {"Easy": "#6ee86e", "Medium": "#f4a261", "Hard": "#f44336"}

for act in actions:
    diff_col = diff_cols.get(act.difficulty, "#52b788")
    tip_text = act.tip_hi if lang_sel == "हिंदी" else act.tip
    action_name = act.action_hi if lang_sel == "हिंदी" else act.action

    ac1, ac2, ac3, ac4 = st.columns([3, 1.5, 1.2, 1])
    with ac1:
        st.markdown(f"""
<div style="background:#112011;border-radius:10px;border:1px solid #2a4a2a;
            padding:.8rem 1rem;height:100%;">
  <div style="font-size:.85rem;font-weight:700;color:#6ee86e;margin-bottom:.3rem;">
    #{act.rank} &nbsp;{action_name}
  </div>
  <div style="font-size:.75rem;color:#52b788;">{tip_text}</div>
</div>""", unsafe_allow_html=True)
    with ac2:
        st.markdown(f"""
<div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;height:100%;">
  <div style="font-size:.7rem;color:#52b788;margin-bottom:.2rem;">💰 Cost</div>
  <div style="font-size:.82rem;font-weight:700;color:#ffd699;">{act.cost_label}</div>
</div>""", unsafe_allow_html=True)
    with ac3:
        st.markdown(f"""
<div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;height:100%;">
  <div style="font-size:.7rem;color:#52b788;margin-bottom:.2rem;">📅 Shelf Life +</div>
  <div style="font-size:.85rem;font-weight:700;color:#6ee86e;">+{act.days_gained}d</div>
</div>""", unsafe_allow_html=True)
    with ac4:
        st.markdown(f"""
<div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;height:100%;">
  <div style="font-size:.7rem;color:#52b788;margin-bottom:.2rem;">🔧 Effort</div>
  <div style="font-size:.8rem;font-weight:700;color:{diff_col};">{act.difficulty}</div>
</div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:.4rem;'></div>", unsafe_allow_html=True)

