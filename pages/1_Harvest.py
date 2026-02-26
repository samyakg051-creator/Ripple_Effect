"""AgriChain – pages/1_Harvest.py  |  Page 2: Harvest Window (no map)"""

import streamlit as st
from datetime import date

from modules.sidebar import render_page
from modules.map_utils import DISTRICT_CENTERS
from modules.harvest import calculate_harvest_window, CROP_DURATIONS
from modules.translations import t, CROP_EMOJI
from modules.weather import get_weather_score

st.set_page_config(page_title="AgriChain – Harvest", page_icon="🌿", layout="wide")

lang = render_page("Harvest", lang="English", show_inputs=False)

crop     = st.session_state.get("crop")
district = st.session_state.get("district")
sowing   = st.session_state.get("sowing_date")

if not (crop and district and sowing):
    st.warning(f"🌾 {t('setup_first', lang)}")
    st.stop()

emoji = CROP_EMOJI.get(crop, "🌱")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#112011,#1e3a1e);border-radius:12px;
            padding:1.1rem 1.6rem;margin-bottom:1.2rem;border:1px solid #2a4a2a;">
  <div style="font-size:1.4rem;font-weight:800;color:#6ee86e;">{emoji} Harvest Window</div>
  <div style="color:#52b788;font-size:.85rem;">{crop} · {district}</div>
</div>""", unsafe_allow_html=True)

# ── Two columns: Harvest info LEFT | Live Weather RIGHT ───────────────────────
col_h, col_w = st.columns([3, 2], gap="medium")

with col_h:
    hw  = calculate_harvest_window(crop, sowing)
    pct = hw.progress_pct
    bar_color = (
        "#f4a261" if hw.status == "window"
        else ("#6ee86e" if hw.status == "upcoming" else "#f44336")
    )

    st.markdown(f"""
<div style="background:#112011;border:1px solid #2a4a2a;border-radius:12px;padding:1.2rem;margin-bottom:1rem;">
  <div style="font-weight:700;color:#6ee86e;margin-bottom:.8rem;">📅 Growing Progress — {pct:.0f}%</div>
  <div style="background:#1e3a1e;border-radius:20px;height:16px;overflow:hidden;">
    <div style="background:{bar_color};width:{pct}%;height:100%;border-radius:20px;"></div>
  </div>
  <div style="display:flex;justify-content:space-between;font-size:.73rem;color:#52b788;margin-top:.4rem;">
    <span>🌱 Sown {sowing.strftime('%b %d')}</span>
    <span>🌿 Harvest period</span>
    <span>✅ Matured</span>
  </div>
</div>""", unsafe_allow_html=True)

    # Status badge
    if hw.status == "upcoming":
        bg,bc = "#1a3a1a","#6ee86e"
        msg = f"🟢 Not yet due — <b>{hw.days_until_start} days</b> until harvest opens"
        sub = f"Window: <b>{hw.harvest_start.strftime('%b %d')} – {hw.harvest_end.strftime('%b %d, %Y')}</b>"
    elif hw.status == "window":
        bg,bc = "#2a200a","#f4a261"
        msg = f"🟡 <b>Harvest window is OPEN</b> — {abs(hw.days_until_end)} days remaining"
        sub = f"Ideal harvest: <b>{hw.ideal_harvest.strftime('%b %d, %Y')}</b>"
    else:
        bg,bc = "#2a0a0a","#f44336"
        msg = f"🔴 <b>Window closed</b> — {abs(hw.days_until_end)} days past ideal harvest"
        sub = "Sell remaining stock as soon as possible to avoid losses"

    st.markdown(f"""
<div style="background:{bg};border-left:4px solid {bc};border-radius:8px;
            padding:.9rem 1.1rem;margin-bottom:1rem;color:#d4f0c0;">
  <div style="font-size:.95rem;">{msg}</div>
  <div style="font-size:.78rem;color:#52b788;margin-top:.2rem;">{sub}</div>
</div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("🌱 Sowing",       sowing.strftime("%b %d, %Y"))
    c2.metric("🌿 Window Opens", hw.harvest_start.strftime("%b %d, %Y"))
    c3.metric("✅ Ideal Date",   hw.ideal_harvest.strftime("%b %d, %Y"))

    info = CROP_DURATIONS.get(crop, {"min": 90, "max": 120})
    st.markdown(f"""
<div style="background:#112011;border:1px solid #2a4a2a;border-radius:10px;
            padding:.85rem 1rem;margin-top:.6rem;font-size:.83rem;color:#d4f0c0;">
  <b style="color:#6ee86e;">{emoji} {crop}</b> grows in
  <b>{info['min']}–{info['max']} days</b>.
  Check colour, firmness, and grain moisture before cutting.
</div>""", unsafe_allow_html=True)

with col_w:
    # ── Live Weather card ──────────────────────────────────────────────────────
    st.markdown("<div style='font-weight:700;color:#6ee86e;margin-bottom:.6rem;'>🌤️ Today's Weather — " + district + "</div>", unsafe_allow_html=True)

    pos = DISTRICT_CENTERS.get(district, [19.7515, 75.7139])
    try:
        with st.spinner("Loading weather..."):
            wx = get_weather_score(latitude=pos[0], longitude=pos[1])

        # Temp color
        temp_col = "#f44336" if wx.today_max_temp > 38 else ("#f4a261" if wx.today_max_temp > 33 else "#6ee86e")
        rain_col = "#f44336" if wx.today_rain_prob > 70 else ("#f4a261" if wx.today_rain_prob > 40 else "#6ee86e")
        hum_col  = "#f44336" if wx.today_humidity > 85 else ("#f4a261" if wx.today_humidity > 70 else "#6ee86e")

        st.markdown(f"""
<div style="background:#112011;border:1px solid #2a4a2a;border-radius:12px;padding:1rem;margin-bottom:.8rem;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:.7rem;">
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.6rem;">🌡️</div>
      <div style="font-size:1.4rem;font-weight:800;color:{temp_col};">{wx.today_max_temp:.0f}°C</div>
      <div style="font-size:.72rem;color:#52b788;">Max Temp</div>
      <div style="font-size:.68rem;color:#52b788;">Min: {wx.today_min_temp:.0f}°C</div>
    </div>
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.6rem;">🌧️</div>
      <div style="font-size:1.4rem;font-weight:800;color:{rain_col};">{wx.today_rain_prob:.0f}%</div>
      <div style="font-size:.72rem;color:#52b788;">Rain Chance</div>
      <div style="font-size:.68rem;color:#52b788;">{wx.today_precip_mm:.1f} mm</div>
    </div>
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.6rem;">💧</div>
      <div style="font-size:1.4rem;font-weight:800;color:{hum_col};">{wx.today_humidity:.0f}%</div>
      <div style="font-size:.72rem;color:#52b788;">Humidity</div>
      <div style="font-size:.68rem;color:#52b788;">Avg 5d: {wx.avg_humidity:.0f}%</div>
    </div>
    <div style="background:#1e3a1e;border-radius:10px;padding:.8rem;text-align:center;">
      <div style="font-size:1.6rem;">💨</div>
      <div style="font-size:1.4rem;font-weight:800;color:#6ee86e;">{wx.today_wind_speed:.0f}</div>
      <div style="font-size:.72rem;color:#52b788;">Wind km/h</div>
      <div style="font-size:.68rem;color:#52b788;">5-day forecast</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        # 5-day strip
        st.markdown("<div style='font-size:.78rem;color:#52b788;margin-bottom:.4rem;font-weight:600;'>📅 5-Day Forecast</div>", unsafe_allow_html=True)
        day_cols = st.columns(5)
        for i, (dc, day) in enumerate(zip(day_cols, wx.forecast)):
            d_label = "Today" if i == 0 else day.date[5:]   # MM-DD
            r_col   = "#f44336" if day.rain_prob > 70 else ("#f4a261" if day.rain_prob > 40 else "#6ee86e")
            dc.markdown(f"""
<div style="background:#1e3a1e;border-radius:8px;padding:.5rem;text-align:center;font-size:.72rem;">
  <div style="color:#52b788;font-weight:600;">{d_label}</div>
  <div style="font-size:1rem;">{"☀️" if day.rain_prob < 30 else ("🌦️" if day.rain_prob < 65 else "🌧️")}</div>
  <div style="color:#d4f0c0;font-weight:700;">{day.max_temp:.0f}°</div>
  <div style="color:{r_col};">{day.rain_prob:.0f}%💧</div>
</div>""", unsafe_allow_html=True)

        # Harvest weather advice
        advice = []
        if wx.today_rain_prob > 60:
            advice.append("🌧️ **High rain chance** — delay harvest if possible to avoid crop damage")
        if wx.today_max_temp > 38:
            advice.append("🔥 **Extreme heat** — harvest early morning to reduce crop stress")
        if wx.today_wind_speed > 40:
            advice.append("💨 **Strong winds** — secure harvested crop to prevent field losses")
        if wx.today_humidity > 80:
            advice.append("💧 **High humidity** — dry grain before storage to prevent mold")
        if not advice:
            advice.append("✅ **Good conditions** — weather is suitable for harvest today")

        st.markdown("<br>", unsafe_allow_html=True)
        for a in advice:
            st.markdown(f'<div style="background:#1a3a1a;border-left:3px solid #6ee86e;border-radius:6px;padding:.5rem .8rem;margin-bottom:.4rem;font-size:.82rem;color:#d4f0c0;">{a}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"Could not load weather: {e}")
