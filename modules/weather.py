"""
AgriChain – modules/weather.py
Fetches 5-day weather forecast from Open-Meteo and computes a weather score.
"""

import requests
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OPEN_METEO_URL       = "https://api.open-meteo.com/v1/forecast"
FORECAST_DAYS        = 5
TEMP_THRESHOLD       = 35.0   # °C – days above this are penalised
RAIN_THRESHOLD       = 60.0   # %  – days above this are penalised
PENALTY_PER_HOT_DAY  = 3
PENALTY_PER_RAIN_DAY = 3
MAX_SCORE            = 30


# ---------------------------------------------------------------------------
# Data container
# ---------------------------------------------------------------------------

@dataclass
class WeatherResult:
    weather_score:    float   # 0–30
    hot_days_count:   int     # days with max temp > 35°C
    rainy_days_count: int     # days with precipitation probability > 60%


# ---------------------------------------------------------------------------
# API fetch
# ---------------------------------------------------------------------------

def _fetch_forecast(latitude: float, longitude: float) -> dict:
    """
    Call the Open-Meteo forecast endpoint and return the parsed JSON response.

    Parameters
    ----------
    latitude  : float – location latitude
    longitude : float – location longitude

    Returns
    -------
    dict – raw JSON response from Open-Meteo

    Raises
    ------
    requests.HTTPError    – on non-2xx HTTP response
    requests.Timeout      – if the request times out
    requests.RequestException – on any other network error
    """
    params = {
        "latitude":    latitude,
        "longitude":   longitude,
        "daily":       "temperature_2m_max,precipitation_probability_max",
        "forecast_days": FORECAST_DAYS,
        "timezone":    "auto",
    }

    response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _parse_daily(data: dict) -> tuple[list[float], list[float]]:
    """
    Extract temperature and precipitation lists from the API response.

    Returns
    -------
    (temperatures, precipitation_probabilities) – parallel lists, one value per day.

    Raises
    ------
    KeyError  – if expected keys are absent in the API response.
    """
    daily         = data["daily"]
    temperatures  = daily["temperature_2m_max"]
    precipitation = daily["precipitation_probability_max"]
    return temperatures, precipitation


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _compute_score(
    temperatures: list[float],
    precipitation: list[float],
) -> tuple[float, int, int]:
    """
    Apply penalty rules and return (weather_score, hot_days, rainy_days).

    Rules
    -----
    - Start at MAX_SCORE (30).
    - Each day with temperature > 35°C  → -3 points.
    - Each day with precipitation > 60% → -3 points.
    - Score is clamped to [0, 30].

    A single day can trigger both penalties independently.
    """
    score      = float(MAX_SCORE)
    hot_days   = 0
    rainy_days = 0

    for temp, precip in zip(temperatures, precipitation):
        if temp is not None and temp > TEMP_THRESHOLD:
            score    -= PENALTY_PER_HOT_DAY
            hot_days += 1

        if precip is not None and precip > RAIN_THRESHOLD:
            score      -= PENALTY_PER_RAIN_DAY
            rainy_days += 1

    final_score = round(min(max(score, 0.0), float(MAX_SCORE)), 4)
    return final_score, hot_days, rainy_days


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def get_weather_score(latitude: float, longitude: float) -> WeatherResult:
    """
    Fetch a 5-day weather forecast and compute a harvest-readiness weather score.

    Parameters
    ----------
    latitude  : float – decimal latitude of the farm / mandi location
    longitude : float – decimal longitude of the farm / mandi location

    Returns
    -------
    WeatherResult dataclass with:
        weather_score    (float, 0–30)
        hot_days_count   (int)
        rainy_days_count (int)

    Raises
    ------
    requests.HTTPError        – on non-2xx API response
    requests.Timeout          – if the API call times out (10 s limit)
    requests.RequestException – on network-level failures
    KeyError                  – if the API response is missing expected fields
    """
    raw_data                  = _fetch_forecast(latitude, longitude)
    temperatures, precip      = _parse_daily(raw_data)
    weather_score, hot, rainy = _compute_score(temperatures, precip)

    return WeatherResult(
        weather_score=weather_score,
        hot_days_count=hot,
        rainy_days_count=rainy,
    )


# ---------------------------------------------------------------------------
# Quick smoke-test  (python -m modules.weather)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Coordinates for New Delhi, India
    result = get_weather_score(latitude=28.6139, longitude=77.2090)
    print(result)
