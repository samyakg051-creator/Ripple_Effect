"""
utils/map_selector.py — District selector with inline Folium map.
Shows farm pin if farm location is set in shared state.
"""
import streamlit as st
from streamlit_folium import st_folium
import folium
from utils.geo import DISTRICT_COORDS
from modules.agri_data import CROP_EMOJI, DEFAULT_EMOJI
from utils.shared_state import get_shared


def render_district_selector(
    page_key: str,
    lang_code: str = "en",
    crop: str = "Wheat",
) -> str:
    """
    Render a district dropdown + mini folium map.
    Returns the selected district name.
    """
    districts = sorted(DISTRICT_COORDS.keys())
    _def_dist = get_shared("district")
    idx = districts.index(_def_dist) if _def_dist in districts else 0

    selected = st.selectbox(
        "📍 Select District",
        districts,
        index=idx,
        key=f"district_{page_key}",
    )

    # Determine map center — farm GPS if available, else district centroid
    farm_lat = get_shared("farm_lat")
    farm_lon = get_shared("farm_lon")
    district_center = DISTRICT_COORDS.get(selected, (19.75, 75.71))

    if farm_lat is not None and farm_lon is not None:
        center = (float(farm_lat), float(farm_lon))
    else:
        center = district_center

    m = folium.Map(location=center, zoom_start=8, tiles="CartoDB dark_matter",
                   width="100%", height=260)

    # Crop/district marker
    emoji = CROP_EMOJI.get(crop, DEFAULT_EMOJI)
    folium.Marker(
        district_center,
        icon=folium.DivIcon(
            html=f'<div style="font-size:28px;text-shadow:0 2px 4px rgba(0,0,0,0.6)">{emoji}</div>'
        ),
        tooltip=f"{selected} — {crop}",
    ).add_to(m)

    # Farm pin if location is set
    if farm_lat is not None and farm_lon is not None:
        farm_name = get_shared("farm_location_name") or "My Farm"
        folium.Marker(
            (float(farm_lat), float(farm_lon)),
            icon=folium.DivIcon(
                html='<div style="font-size:28px;text-shadow:0 2px 4px rgba(0,0,0,0.6)">🏠</div>'
            ),
            tooltip=f"🏠 {farm_name}",
        ).add_to(m)

    st_folium(m, key=f"map_{page_key}", width="100%", height=260,
              returned_objects=[])

    return selected
