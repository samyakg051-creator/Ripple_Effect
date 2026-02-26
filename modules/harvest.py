"""AgriChain – modules/harvest.py — Harvest window calculator."""

from datetime import date, timedelta
from dataclasses import dataclass

CROP_DURATIONS = {
    "Wheat":   {"min": 120, "max": 150},
    "Tomato":  {"min": 60,  "max": 90},
    "Onion":   {"min": 90,  "max": 120},
    "Potato":  {"min": 75,  "max": 100},
    "Rice":    {"min": 120, "max": 150},
}

@dataclass
class HarvestResult:
    crop: str
    sowing_date: date
    harvest_start: date
    harvest_end: date
    ideal_harvest: date
    days_until_start: int
    days_until_end: int
    status: str        # "upcoming" | "window" | "overdue"
    progress_pct: float

def calculate_harvest_window(crop: str, sowing_date: date) -> HarvestResult:
    info = CROP_DURATIONS.get(crop, {"min": 90, "max": 120})
    harvest_start  = sowing_date + timedelta(days=info["min"])
    harvest_end    = sowing_date + timedelta(days=info["max"])
    ideal_harvest  = sowing_date + timedelta(days=(info["min"] + info["max"]) // 2)
    today          = date.today()
    days_grown     = (today - sowing_date).days
    progress_pct   = min(max(days_grown / info["max"] * 100, 0), 100)

    if today < harvest_start:
        status = "upcoming"
    elif today <= harvest_end:
        status = "window"
    else:
        status = "overdue"

    return HarvestResult(
        crop=crop,
        sowing_date=sowing_date,
        harvest_start=harvest_start,
        harvest_end=harvest_end,
        ideal_harvest=ideal_harvest,
        days_until_start=(harvest_start - today).days,
        days_until_end=(harvest_end - today).days,
        status=status,
        progress_pct=round(progress_pct, 1),
    )
