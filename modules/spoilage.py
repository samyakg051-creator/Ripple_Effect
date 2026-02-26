"""AgriChain – modules/spoilage.py — Accurate spoilage risk using real weather data."""

from dataclasses import dataclass

# ── Shelf life (days) by crop + storage ───────────────────────────────────────
SHELF_LIFE = {
    "Tomato":  {"cold_storage": 30,  "warehouse": 7,   "covered_shed": 4,   "open_yard": 2,  "none": 1},
    "Onion":   {"cold_storage": 180, "warehouse": 90,  "covered_shed": 45,  "open_yard": 20, "none": 10},
    "Wheat":   {"cold_storage": 730, "warehouse": 365, "covered_shed": 180, "open_yard": 60, "none": 30},
    "Potato":  {"cold_storage": 180, "warehouse": 60,  "covered_shed": 30,  "open_yard": 15, "none": 7},
    "Rice":    {"cold_storage": 365, "warehouse": 180, "covered_shed": 90,  "open_yard": 30, "none": 14},
}

STORAGE_PENALTY = {
    "cold_storage": -15, "warehouse": 0,
    "covered_shed": 10,  "open_yard": 22, "none": 35,
}

# Grain crops are highly sensitive to humidity (mold/fungus risk)
HUMIDITY_SENSITIVE = {"Wheat", "Rice"}

@dataclass
class SpoilageResult:
    crop: str
    storage_type: str
    shelf_life_days: int
    transport_hours: float
    spoilage_risk_pct: float
    risk_level: str
    recommendation: str
    # Breakdown for display
    base_risk: float
    temp_penalty: float
    humidity_penalty: float
    rain_penalty: float
    storage_adj: float


def calculate_spoilage_risk(
    crop: str,
    storage_type: str,
    distance_km: float,
    hot_days: int = 0,
    rainy_days: int = 0,
    avg_temp_c: float = 25.0,
    avg_humidity_pct: float = 50.0,
    rain_prob_pct: float = 0.0,
) -> SpoilageResult:
    shelf          = SHELF_LIFE.get(crop, SHELF_LIFE["Wheat"]).get(storage_type, 30)
    transport_hrs  = round((distance_km / 100) * 2.5, 1)
    transport_days = transport_hrs / 24

    # Base risk from transport time vs shelf life
    base_risk = min((transport_days / shelf) * 100, 60) if shelf > 0 else 60

    # Temperature penalty — every °C above 30°C reduces shelf by ~8%/°C for veggies
    if avg_temp_c > 30:
        excess       = avg_temp_c - 30
        temp_penalty = min(excess * (6 if crop in {"Tomato","Potato"} else 3), 30)
    elif avg_temp_c > 35:
        temp_penalty = min((avg_temp_c - 30) * 8, 35)
    else:
        temp_penalty = 0.0

    # Humidity penalty — critical for grain crops
    if avg_humidity_pct > 75 and crop in HUMIDITY_SENSITIVE:
        humidity_penalty = min((avg_humidity_pct - 75) * 2.0, 20)
    elif avg_humidity_pct > 85:
        humidity_penalty = min((avg_humidity_pct - 75) * 1.2, 15)
    else:
        humidity_penalty = 0.0

    # Rain probability penalty
    rain_penalty = min(rain_prob_pct * 0.12, 12)

    # Storage adjustment
    storage_adj = STORAGE_PENALTY.get(storage_type, 0)

    total = base_risk + temp_penalty + humidity_penalty + rain_penalty + storage_adj
    risk_pct = round(min(max(total, 0), 100), 1)

    if risk_pct < 25:
        level = "Low"
        rec   = (f"✅ Safe to hold. Shelf life: {shelf} days. "
                 f"Transport within {max(1, shelf // 4)} days for best price.")
    elif risk_pct < 55:
        level = "Medium"
        rec   = (f"⚠️ Plan transport soon — sell within {max(1, shelf // 3)} days. "
                 f"{'Reduce humidity exposure. ' if humidity_penalty > 5 else ''}"
                 f"{'Keep cool — high temp accelerates spoilage.' if temp_penalty > 5 else ''}")
    else:
        level = "High"
        rec   = (f"🚨 Sell immediately or upgrade to cold storage. "
                 f"{'Humidity is causing mold risk for ' + crop + '. ' if humidity_penalty > 5 else ''}"
                 f"{'Extreme heat is accelerating decay. ' if temp_penalty > 10 else ''}"
                 f"Shelf life at current conditions: ~{max(1, shelf // 4)} days.")

    return SpoilageResult(
        crop=crop, storage_type=storage_type,
        shelf_life_days=shelf, transport_hours=transport_hrs,
        spoilage_risk_pct=risk_pct, risk_level=level, recommendation=rec,
        base_risk=round(base_risk, 1),
        temp_penalty=round(temp_penalty, 1),
        humidity_penalty=round(humidity_penalty, 1),
        rain_penalty=round(rain_penalty, 1),
        storage_adj=float(storage_adj),
    )
