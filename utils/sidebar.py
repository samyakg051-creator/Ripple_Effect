"""
utils/sidebar.py — Shared sidebar for all AgriChain pages.
Renders branding, language selector, farm location, and navigation links.
The selected language persists in session_state across pages.
"""
import streamlit as st
import requests
from utils.shared_state import get_shared, sync_all


def _nominatim_geocode(query: str):
    """Geocode an address using OpenStreetMap Nominatim. Returns (lat, lon, name) or None."""
    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query + ", Maharashtra, India", "format": "json", "limit": 1},
            headers={"User-Agent": "AgriChain/1.0"},
            timeout=5,
        )
        data = resp.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"].split(",")[0]
    except Exception:
        pass
    return None


def render_sidebar(current_page: str = "") -> str:
    """
    Render the unified sidebar. Returns the selected language code ('en', 'hi', 'mr').

    current_page: one of 'home', 'harvest', 'mandi', 'spoilage', 'map'
                  — that link will be visually highlighted.
    """
    _LANG_MAP = {"English": "en", "हिंदी": "hi", "मराठी": "mr"}

    if "app_language" not in st.session_state:
        st.session_state.app_language = "en"

    with st.sidebar:
        # Hide default Streamlit page navigation
        st.markdown("""
        <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        </style>
        """, unsafe_allow_html=True)

        # ── Branding ──────────────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center;padding:0 0 12px;">
            <span style="font-size:2.2rem;">🌾</span>
            <div style="font-size:1.3rem;font-weight:800;color:#52b788;margin-top:2px;">AgriChain</div>
            <div style="font-size:0.72rem;color:#4a7a4a;margin-top:2px;">Farm-to-Market Intelligence</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── Language selector ─────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.1em;color:#6ee86e;margin-bottom:6px">🌐 भाषा / Language</div>',
            unsafe_allow_html=True,
        )
        lang_choice = st.radio(
            "Language",
            list(_LANG_MAP.keys()),
            index=list(_LANG_MAP.values()).index(st.session_state.app_language)
                  if st.session_state.app_language in _LANG_MAP.values() else 0,
            key="sidebar_lang_radio",
            label_visibility="collapsed",
        )
        st.session_state.app_language = _LANG_MAP[lang_choice]

        st.markdown("---")

        # ── 📍 Farm Location ──────────────────────────────────────────────────
        farm_lat = get_shared("farm_lat")
        farm_lon = get_shared("farm_lon")
        farm_name = get_shared("farm_location_name") or ""

        if farm_lat and farm_lon:
            # Show green badge
            st.markdown(f"""
            <div style="background:#112011;border:1px solid #52b788;border-radius:10px;
                padding:0.5rem 0.8rem;margin-bottom:0.5rem;">
                <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;
                    letter-spacing:0.08em;color:#6ee86e;margin-bottom:2px;">📍 Farm Location</div>
                <div style="font-size:0.82rem;color:#d4f0c0;font-weight:600;">{farm_name or 'Set'}</div>
                <div style="font-size:0.68rem;color:#4a7a4a;">{farm_lat:.4f}°N, {farm_lon:.4f}°E</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✏️ Change Location", key="change_farm_loc", use_container_width=True):
                sync_all(farm_lat=None, farm_lon=None, farm_location_name="")
                st.rerun()
        else:
            with st.expander("📍 Set My Farm Location", expanded=False):
                search_q = st.text_input("🔍 Search village/city", key="farm_search_input",
                                         placeholder="e.g. Sangamner, Nashik...")
                if st.button("Search", key="farm_search_btn", use_container_width=True):
                    result = _nominatim_geocode(search_q)
                    if result:
                        lat, lon, name = result
                        sync_all(farm_lat=lat, farm_lon=lon, farm_location_name=name)
                        st.success(f"📍 Found: {name}")
                        st.rerun()
                    else:
                        st.error("Location not found. Try manual entry below.")

                st.markdown('<div style="font-size:0.7rem;color:#4a7a4a;margin:4px 0">or enter manually:</div>',
                            unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                with c1:
                    m_lat = st.number_input("Lat", value=19.75, format="%.4f", key="farm_lat_input")
                with c2:
                    m_lon = st.number_input("Lon", value=75.71, format="%.4f", key="farm_lon_input")
                if st.button("✅ Use These Coords", key="farm_manual_btn", use_container_width=True):
                    sync_all(farm_lat=m_lat, farm_lon=m_lon, farm_location_name=f"{m_lat:.3f}°N, {m_lon:.3f}°E")
                    st.rerun()

        st.markdown("---")

        # ── Navigation links ─────────────────────────────────────────────────
        _PAGES = [
            ("home",    "🏠", "Home",               "app.py"),
            ("harvest", "🌾", "Harvest Window",     "pages/1_🌾_Harvest.py"),
            ("mandi",   "🏪", "Mandi Ranker",       "pages/2_🏪_Mandi.py"),
            ("spoilage","⚠️", "Spoilage Assessor",  "pages/3_⚠️_Spoilage.py"),
            ("spoilage_prev","🛡️","Spoilage Prevention","pages/2_Spoilage_Prevention.py"),
            ("map",     "🗺️", "Map Explorer",       "pages/4_Map_Explorer.py"),
            ("ai_chat", "🤖", "AI Chat",            "pages/5_🤖_AI_Chat.py"),
        ]

        for key, icon, label, path in _PAGES:
            try:
                st.page_link(path, label=f"{icon}  {label}")
            except Exception:
                pass  # page may not exist yet

        st.markdown("---")

    return st.session_state.app_language
