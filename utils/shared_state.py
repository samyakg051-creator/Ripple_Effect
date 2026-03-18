"""
utils/shared_state.py — Cross-page session state management.
"""
import streamlit as st
import math

_DEFAULTS = {
    "crop": "Wheat",
    "district": "Pune",
    "mandi": "",
    "storage_type": "warehouse",
    "sowing": None,
    "quantity": 50.0,
    "storage": "Cold Storage",
    "transit": 8,
    "farm_lat": None,
    "farm_lon": None,
    "farm_location_name": "",
}


def init_shared():
    """Initialize shared session state defaults."""
    for k, v in _DEFAULTS.items():
        if f"shared_{k}" not in st.session_state:
            st.session_state[f"shared_{k}"] = v


def get_shared(key: str):
    """Get a shared value with fallback to default."""
    return st.session_state.get(f"shared_{key}", _DEFAULTS.get(key))


def sync_all(**kwargs):
    """Sync values across pages."""
    for k, v in kwargs.items():
        if v is not None:
            st.session_state[f"shared_{k}"] = v


def get_farm_origin(district: str = None):
    """
    Returns (lat, lon) for the farm if set, else district centroid fallback.
    """
    farm_lat = get_shared("farm_lat")
    farm_lon = get_shared("farm_lon")
    if farm_lat is not None and farm_lon is not None:
        return float(farm_lat), float(farm_lon)
    # Fallback to district centroid
    if district:
        from utils.geo import DISTRICT_COORDS
        coords = DISTRICT_COORDS.get(district)
        if coords:
            return coords
    return (19.7515, 75.7139)  # Maharashtra center


def haversine_km(lat1, lon1, lat2, lon2) -> float:
    """Calculate distance in km between two GPS points."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
