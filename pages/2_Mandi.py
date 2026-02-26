"""AgriChain – pages/2_Mandi.py  |  Page 3: Mandi Ranker + Map"""

import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from modules.sidebar import render_page
from modules.map_utils import build_map, MANDIS
from modules.translations import t, CROP_EMOJI

st.set_page_config(page_title="AgriChain – Mandi", page_icon="🏪", layout="wide")

lang = render_page("Mandi", lang="English", show_inputs=False)

crop     = st.session_state.get("crop")
district = st.session_state.get("district")
sowing   = st.session_state.get("sowing_date")

if not (crop and district):
    st.warning(f"🌾 {t('setup_first', lang)}")
    st.stop()

emoji = CROP_EMOJI.get(crop, "🌱")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#1a1a00,#2a2a00);border-radius:12px;
            padding:1.1rem 1.6rem;color:#ffd699;margin-bottom:1rem;border:1px solid #3a3a00;">
  <div style="font-size:1.4rem;font-weight:800;">🏪 Mandi Price Rankings</div>
  <div style="opacity:.85;font-size:.85rem;">{emoji} {crop} · Market Intelligence</div>
</div>""", unsafe_allow_html=True)

# ── Map with mandi markers ────────────────────────────────────────────────────
m = build_map(
    selected_district=district, crop=crop,
    sowing_date=sowing, show_mandis=True, show_all_markers=False,
)
st_folium(m, width="100%", height=380, key="mandi_map", returned_objects=[])
st.divider()

# ── Mandi price table ─────────────────────────────────────────────────────────
CSV_PATH = "data/mandi_prices.csv"

@st.cache_data(ttl=600)
def load_csv():
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["Crop"]  = df["Crop"].str.strip()
    df["Mandi"] = df["Mandi"].str.strip()
    df["Date"]  = pd.to_datetime(df["Date"], dayfirst=True)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    return df.dropna(subset=["Price"])

try:
    df  = load_csv()
    cdf = df[df["Crop"].str.lower() == crop.lower()].copy()

    if cdf.empty:
        st.info(f"No price data found for **{crop}**. Available crops: "
                f"{', '.join(sorted(df['Crop'].unique()))}")
    else:
        rows = []
        for mandi_name, mgrp in cdf.groupby("Mandi"):
            sorted_g = mgrp.sort_values("Date", ascending=False)
            last7    = sorted_g.head(7)["Price"].mean()
            last30   = sorted_g.head(30)["Price"].mean()
            trend    = round(((last7 - last30) / last30) * 100, 2) if last30 else 0.0
            score    = 25 if trend >= 5 else (20 if trend >= 0 else (15 if trend >= -5 else 10))
            rows.append({
                "Mandi":         mandi_name,
                "7‑Day Avg (₹)": round(last7, 0),
                "30‑Day Avg (₹)":round(last30, 0),
                "Trend %":       trend,
                "Score":         score,
            })

        rank_df = pd.DataFrame(rows).sort_values("Score", ascending=False).reset_index(drop=True)

        st.markdown(f"### Rankings for {emoji} **{crop}**")

        for idx, row in rank_df.iterrows():
            rank       = idx + 1   # 1-based rank
            t_color    = "#6ee86e" if row["Trend %"] >= 0 else "#f44336"
            t_arrow    = "↑" if row["Trend %"] >= 0 else "↓"
            medal      = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"#{rank}")
            on_map     = "🗺️" if row["Mandi"] in MANDIS else ""
            border_col = "#f4a261" if rank == 1 else "#2a4a2a"

            st.markdown(f"""
<div style="background:#112011;border-radius:10px;border:1px solid {border_col};
            border-left:4px solid {border_col};padding:1rem 1.2rem;margin-bottom:.6rem;">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.5rem;">
    <div style="color:#d4f0c0;">
      <span style="font-size:1.1rem;">{medal}</span>
      <strong style="font-size:1rem;margin-left:.5rem;color:#6ee86e;">{row['Mandi']} {on_map}</strong>
    </div>
    <div style="font-size:.83rem;color:#d4f0c0;">
      7d: <b>₹{row['7‑Day Avg (₹)']:.0f}</b> &nbsp;|&nbsp;
      30d: <b>₹{row['30‑Day Avg (₹)']:.0f}</b> &nbsp;|&nbsp;
      <span style="color:{t_color};font-weight:700;">{t_arrow} {abs(row['Trend %']):.2f}%</span>
    </div>
    <div style="background:#1e3a1e;border-radius:20px;padding:.2rem .8rem;
                font-size:.8rem;font-weight:700;color:#6ee86e;">
      Score: {row['Score']}/25
    </div>
  </div>
</div>""", unsafe_allow_html=True)

        st.caption("🗺️ = Location shown on map. Score based on 7-day vs 30-day price trend.")

except FileNotFoundError:
    st.error("❌ Price data file not found: `data/mandi_prices.csv`")
except Exception as e:
    st.error(f"❌ Error loading price data: {e}")
