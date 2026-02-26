"""AgriChain – modules/map_utils.py  — Folium India map builder."""

import folium
import requests
import streamlit as st
import re

INDIA_GEOJSON_URL = "https://raw.githubusercontent.com/datameet/maps/master/Country/india-composite.geojson"
MH_GEOJSON_URL    = "https://raw.githubusercontent.com/datameet/maps/master/Districts/maharashtra.geojson"

CROP_EMOJI = {
    "Wheat": "🌾", "Tomato": "🍅", "Onion": "🧅",
    "Potato": "🥔", "Rice": "🍚",
}

# All Maharashtra district centres (lat, lon)
DISTRICT_CENTERS = {
    "Ahmednagar":     [19.0948, 74.7480], "Akola":         [20.7090, 77.0082],
    "Amravati":       [20.9320, 77.7523], "Aurangabad":    [19.8762, 75.3433],
    "Beed":           [18.9890, 75.7601], "Bhandara":      [21.1667, 79.6500],
    "Buldhana":       [20.5293, 76.1849], "Chandrapur":    [19.9615, 79.2961],
    "Dhule":          [20.9013, 74.7749], "Gadchiroli":    [20.1809, 80.0000],
    "Gondia":         [21.4605, 80.1967], "Hingoli":       [19.7176, 77.1498],
    "Jalgaon":        [21.0046, 75.5618], "Jalna":         [19.8347, 75.8816],
    "Kolhapur":       [16.7099, 74.2433], "Latur":         [18.4088, 76.5604],
    "Mumbai City":    [18.9388, 72.8353], "Mumbai Suburban":[19.1136, 72.8697],
    "Nagpur":         [21.1458, 79.0882], "Nanded":        [19.1383, 77.3210],
    "Nandurbar":      [21.3682, 74.2432], "Nashik":        [19.9975, 73.7898],
    "Osmanabad":      [18.1820, 76.0359], "Palghar":       [19.6967, 72.7656],
    "Parbhani":       [19.2704, 76.7742], "Pune":          [18.5204, 73.8567],
    "Raigad":         [18.5152, 73.1806], "Ratnagiri":     [16.9902, 73.3120],
    "Sangli":         [16.8524, 74.5815], "Satara":        [17.6805, 74.0183],
    "Sindhudurg":     [16.3500, 73.9500], "Solapur":       [17.6599, 75.9064],
    "Thane":          [19.2183, 72.9781], "Wardha":        [20.7453, 78.6022],
    "Washim":         [20.1107, 77.1326], "Yavatmal":      [20.3888, 78.1204],
}

MANDIS = {
    "Nagpur":     [21.1458, 79.0882], "Solapur":    [17.6599, 75.9064],
    "Pune":       [18.5204, 73.8567], "Akola":      [20.7090, 77.0082],
    "Nashik":     [19.9975, 73.7898], "Jalgaon":    [21.0046, 75.5618],
    "Satara":     [17.6805, 74.0183], "Sangli":     [16.8524, 74.5815],
    "Kolhapur":   [16.7099, 74.2433], "Latur":      [18.4088, 76.5604],
}

@st.cache_data(ttl=3600, show_spinner=False)
def _fetch(url: str) -> dict:
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()

def _dist_name(feature: dict) -> str:
    p = feature.get("properties", {})
    for k in ["district", "DISTRICT", "dtname", "NAME_2", "Dist_Name", "name"]:
        if p.get(k):
            return str(p[k]).strip()
    return ""

def _dist_field(data: dict) -> str:
    if data.get("features"):
        p = data["features"][0].get("properties", {})
        for k in ["district", "DISTRICT", "dtname", "NAME_2", "Dist_Name", "name"]:
            if k in p:
                return k
    return "district"

def _is_mh(feature: dict) -> bool:
    p = feature.get("properties", {})
    v = (p.get("st_nm") or p.get("NAME_1") or p.get("STATE") or "").lower()
    return "maharashtra" in v

def build_map(
    selected_district: str = None,
    crop: str = None,
    sowing_date=None,
    show_mandis: bool = False,
    show_all_markers: bool = False,
) -> folium.Map:
    # Decide center & zoom
    center, zoom = [19.7515, 75.7139], 7
    if selected_district and not show_all_markers:
        pos = DISTRICT_CENTERS.get(selected_district)
        if pos:
            center, zoom = pos, 9

    m = folium.Map(
        location=center, zoom_start=zoom,
        tiles="CartoDB dark_matter",
        zoom_control=True, scrollWheelZoom=True,
    )

    # India outline
    try:
        india = _fetch(INDIA_GEOJSON_URL)
        folium.GeoJson(
            india,
            style_function=lambda x: {
                "fillColor": "#2d6a4f" if _is_mh(x) else "#f0e6d3",
                "color":     "#2d6a4f",
                "weight":    1.5,
                "fillOpacity": 0.45,
            },
            name="India",
        ).add_to(m)
    except Exception:
        pass

    # Maharashtra districts
    try:
        mh = _fetch(MH_GEOJSON_URL)
        field = _dist_field(mh)

        def dist_style(feature):
            name = _dist_name(feature)
            if name and name.lower() == (selected_district or "").lower():
                return {"fillColor": "#f4a261", "color": "#e76f51", "weight": 3, "fillOpacity": 0.8}
            return {"fillColor": "#52b788", "color": "#2d6a4f", "weight": 1, "fillOpacity": 0.25}

        folium.GeoJson(
            mh,
            style_function=dist_style,
            tooltip=folium.GeoJsonTooltip(
                fields=[field], aliases=[""],
                style="background:#fefae0;border:1px solid #2d6a4f;border-radius:6px;padding:6px 10px;font-size:13px;font-weight:600;",
                sticky=True,
            ),
            name="Districts",
        ).add_to(m)
    except Exception:
        pass

    # Small crop emoji markers on ALL districts
    if show_all_markers and crop:
        emoji = CROP_EMOJI.get(crop, "🌱")
        for dist_name, pos in DISTRICT_CENTERS.items():
            is_selected = dist_name.lower() == (selected_district or "").lower()
            size = "30px" if is_selected else "20px"
            border = "3px solid #6ee86e" if is_selected else "none"
            folium.Marker(
                location=pos,
                icon=folium.DivIcon(
                    html=f'<div style="font-size:{size};filter:drop-shadow(1px 2px 2px rgba(0,0,0,.6));'  
                         f'border-radius:50%;background:rgba(0,0,0,.3);padding:2px;border:{border};'  
                         f'display:inline-block;">{emoji}</div>',
                    icon_size=(36 if is_selected else 28, 36 if is_selected else 28),
                    icon_anchor=(18 if is_selected else 14, 18 if is_selected else 14),
                ),
                popup=folium.Popup(f"<b>{emoji} {dist_name}</b>", max_width=140),
                tooltip=dist_name,
            ).add_to(m)
    elif selected_district and crop:
        # Single marker on selected district only
        pos = DISTRICT_CENTERS.get(selected_district)
        if pos:
            emoji = CROP_EMOJI.get(crop, "🌱")
            label = f"<b>{emoji} {crop}</b><br>📍 {selected_district}"
            if sowing_date:
                label += f"<br>📅 Sowing: {sowing_date}"
            folium.Marker(
                location=pos,
                icon=folium.DivIcon(
                    html=f'<div style="font-size:30px;filter:drop-shadow(1px 2px 2px rgba(0,0,0,.3));">{emoji}</div>',
                    icon_size=(36, 36), icon_anchor=(18, 18),
                ),
                popup=folium.Popup(label, max_width=200),
                tooltip=f"{emoji} {crop}",
            ).add_to(m)

    # Mandi markers
    if show_mandis:
        for name, pos in MANDIS.items():
            folium.Marker(
                location=pos,
                icon=folium.DivIcon(
                    html='<div style="font-size:22px;filter:drop-shadow(1px 1px 1px rgba(0,0,0,.3));">🏪</div>',
                    icon_size=(28, 28), icon_anchor=(14, 14),
                ),
                popup=folium.Popup(f"<b>🏪 {name} Mandi</b>", max_width=160),
                tooltip=f"🏪 {name}",
            ).add_to(m)

    return m

def extract_district_from_click(map_data: dict) -> str | None:
    """Parse district name from st_folium click result."""
    raw = map_data.get("last_object_clicked_tooltip") or ""
    cleaned = re.sub(r"<[^>]+>", "", raw).strip()
    return cleaned if cleaned else None
