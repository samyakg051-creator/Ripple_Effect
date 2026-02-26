"""AgriChain – modules/sidebar.py — Shared sidebar components & session state."""

import streamlit as st
from datetime import date
from modules.translations import t, CROP_EMOJI

CROPS    = ["Wheat", "Tomato", "Onion", "Potato", "Rice"]
STORAGE  = ["cold_storage", "warehouse", "covered_shed", "open_yard", "none"]
LANGS    = ["English", "हिंदी"]

def init_session_state():
    defaults = {
        "crop":         "Wheat",
        "district":     None,
        "sowing_date":  None,
        "quantity":     10,
        "storage_type": "warehouse",
        "language":     "English",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def _common_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0a1a0a!important;color:#d4f0c0!important;}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:#0a1a0a!important;}
.main,.main>div,.block-container{background:#0a1a0a!important;}
section[data-testid="stSidebar"]{background:#091409!important;border-right:1px solid #1e3a1e;}
.stButton>button{background:#6ee86e;color:#0a1a0a;border:none;border-radius:24px;
  padding:.6rem 1.6rem;width:100%;font-weight:700;font-size:.95rem;transition:background .2s;}
.stButton>button:hover{background:#8ff58f;}
div[data-testid="stSelectbox"]>div>div{background:#112011!important;border:1px solid #2a4a2a!important;
  border-radius:8px!important;color:#d4f0c0!important;}
div[data-testid="stSelectbox"] label,div[data-testid="stSlider"] label,
div[data-testid="stDateInput"] label,div[data-testid="stNumberInput"] label{
  color:#6ee86e!important;font-weight:600!important;font-size:.85rem!important;}
input[data-testid],div[data-testid="stDateInput"] input{
  background:#112011!important;border:1px solid #2a4a2a!important;
  border-radius:8px!important;color:#d4f0c0!important;}
.agri-card{background:#112011;border-radius:12px;border:1px solid #2a4a2a;
  padding:1.1rem 1.2rem;margin-bottom:.8rem;}
.risk-low{background:#1a3a1a;border-left:4px solid #6ee86e;border-radius:8px;padding:.8rem 1rem;color:#d4f0c0;}
.risk-med{background:#2a200a;border-left:4px solid #f4a261;border-radius:8px;padding:.8rem 1rem;color:#ffd699;}
.risk-high{background:#2a0a0a;border-left:4px solid #f44336;border-radius:8px;padding:.8rem 1rem;color:#ffb3b3;}
[data-testid="stMetricValue"] {font-size: 1.4rem !important;}
[data-testid="stMetricLabel"] {font-size: 0.85rem !important; color: #52b788 !important;}
#MainMenu,footer,[data-testid="stDecoration"]{visibility:hidden;}
hr{border-color:#1e3a1e!important;}
</style>""", unsafe_allow_html=True)


def render_brand(lang: str):
    st.markdown(f"""
<div style="text-align:center;padding:.5rem 0 .8rem;">
  <div style="font-size:2rem;">🌾</div>
  <div style="font-size:1.25rem;font-weight:800;color:#2d6a4f;">{t('app_title', lang)}</div>
  <div style="font-size:.75rem;color:#52b788;">{t('app_subtitle', lang)}</div>
</div>
<hr style="border:none;border-top:1px solid #b7e4c7;margin:.5rem 0 1rem;">
""", unsafe_allow_html=True)

def render_summary_card(lang: str):
    if not st.session_state.get("district"):
        return
    crop     = st.session_state.get("crop", "—")
    district = st.session_state.get("district", "—")
    sowing   = st.session_state.get("sowing_date")
    qty      = st.session_state.get("quantity", "—")
    storage  = st.session_state.get("storage_type", "—").replace("_", " ").title()
    emoji    = CROP_EMOJI.get(crop, "🌱")
    sowing_s = sowing.strftime("%b %d, %Y") if sowing else "—"
    st.markdown(f"""
<div style="background:#fff;border-left:4px solid #2d6a4f;border-radius:10px;
            padding:.9rem 1rem;font-size:.83rem;box-shadow:0 2px 6px rgba(45,106,79,.08);">
  <div style="font-weight:700;color:#2d6a4f;margin-bottom:.5rem;">🌾 {t('summary_title', lang)}</div>
  <div style="color:#1b4332;line-height:1.8;">
    {emoji} <b>{crop}</b><br>
    📍 {district}<br>📅 {sowing_s}<br>
    📦 {qty} qtl &nbsp;|&nbsp; 🏚️ {storage}
  </div>
</div>""", unsafe_allow_html=True)

def render_page(title: str, lang: str, show_inputs: bool = False):
    """Common page setup — call at top of every page."""
    init_session_state()
    _common_css()
    lang = st.session_state.get("language", "English")

    with st.sidebar:
        render_brand(lang)

        if show_inputs:
            st.session_state.language = st.selectbox(
                t("language", lang), LANGS,
                index=LANGS.index(st.session_state.get("language", "English")),
                key="lang_sel",
            )
            lang = st.session_state.language

            st.session_state.crop = st.selectbox(
                t("crop", lang), CROPS,
                index=CROPS.index(st.session_state.get("crop", "Wheat")),
            )
            sowing_val = st.date_input(
                t("sowing_date", lang),
                value=st.session_state.get("sowing_date") or date.today(),
            )
            st.session_state.sowing_date = sowing_val

            st.session_state.quantity = st.number_input(
                t("quantity", lang),
                min_value=1, max_value=10000,
                value=int(st.session_state.get("quantity", 10)),
            )
            st.session_state.storage_type = st.selectbox(
                t("storage", lang), STORAGE,
                index=STORAGE.index(st.session_state.get("storage_type", "warehouse")),
                format_func=lambda x: x.replace("_", " ").title(),
            )

        st.markdown("<hr style='border:none;border-top:1px solid #b7e4c7;margin:.8rem 0;'>", unsafe_allow_html=True)
        render_summary_card(lang)

    return lang
