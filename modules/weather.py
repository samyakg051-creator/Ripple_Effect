"""
AgriChain – modules/weather.py
Fetches 5-day weather forecast from Open-Meteo and computes a weather score.
Returns rich per-day data: temp, humidity, rain probability, wind speed.
"""

import requests
from dataclasses import dataclass, field

OPEN_METEO_URL    = "https://api.open-meteo.com/v1/forecast"
FORECAST_DAYS     = 5
TEMP_THRESHOLD    = 35.0   # °C – above this harms crops
RAIN_THRESHOLD    = 60.0   # %  – above this affects harvest
HUMID_THRESHOLD   = 75.0   # %  – above this, grain spoilage risk rises
MAX_SCORE         = 30


@dataclass
class DayForecast:
    date:       str
    max_temp:   float   # °C
    min_temp:   float   # °C
    rain_prob:  float   # %
    humidity:   float   # %
    wind_speed: float   # km/h
    precip_sum: float   # mm


@dataclass
class WeatherResult:
    # Scores (backward-compatible)
    weather_score:    float
    hot_days_count:   int
    rainy_days_count: int

    # Rich daily forecast
    forecast: list = field(default_factory=list)   # list[DayForecast]

    # Today's snapshot (Day 0)
    today_max_temp:   float = 0.0
    today_min_temp:   float = 0.0
    today_rain_prob:  float = 0.0
    today_humidity:   float = 0.0
    today_wind_speed: float = 0.0
    today_precip_mm:  float = 0.0
    avg_humidity:     float = 0.0   # 5-day average humidity


def get_weather_score(latitude: float, longitude: float) -> WeatherResult:
    """
    Fetch 5-day forecast and return WeatherResult with detailed farmer data.
    Fetches: temp (max/min), precipitation probability, relative humidity, wind speed.
    """
    params = {
        "latitude":     latitude,
        "longitude":    longitude,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_probability_max,"
            "relative_humidity_2m_max,"
            "wind_speed_10m_max,"
            "precipitation_sum"
        ),
        "forecast_days": FORECAST_DAYS,
        "timezone":      "auto",
        "wind_speed_unit": "kmh",
    }
    resp = requests.get(OPEN_METEO_URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    daily      = data["daily"]
    dates      = daily.get("time", [])
    max_temps  = daily.get("temperature_2m_max", [])
    min_temps  = daily.get("temperature_2m_min", [])
    rain_probs = daily.get("precipitation_probability_max", [])
    humidities = daily.get("relative_humidity_2m_max", [])
    winds      = daily.get("wind_speed_10m_max", [])
    precips    = daily.get("precipitation_sum", [])

    # Build daily forecast list
    forecast = []
    for i in range(min(FORECAST_DAYS, len(dates))):
        forecast.append(DayForecast(
            date       = dates[i] if i < len(dates) else "",
            max_temp   = max_temps[i]  if i < len(max_temps)  and max_temps[i]  is not None else 0.0,
            min_temp   = min_temps[i]  if i < len(min_temps)  and min_temps[i]  is not None else 0.0,
            rain_prob  = rain_probs[i] if i < len(rain_probs) and rain_probs[i] is not None else 0.0,
            humidity   = humidities[i] if i < len(humidities) and humidities[i] is not None else 0.0,
            wind_speed = winds[i]      if i < len(winds)      and winds[i]      is not None else 0.0,
            precip_sum = precips[i]    if i < len(precips)    and precips[i]    is not None else 0.0,
        ))

    # Score & counts
    score      = float(MAX_SCORE)
    hot_days   = 0
    rainy_days = 0

    for d in forecast:
        if d.max_temp > TEMP_THRESHOLD:
            score    -= 3
            hot_days += 1
        if d.rain_prob > RAIN_THRESHOLD:
            score      -= 3
            rainy_days += 1
        if d.humidity > HUMID_THRESHOLD:
            score -= 1   # mild humidity penalty

    weather_score = round(min(max(score, 0.0), float(MAX_SCORE)), 2)
    avg_humidity  = round(sum(d.humidity for d in forecast) / len(forecast), 1) if forecast else 0.0

    today = forecast[0] if forecast else DayForecast("", 0, 0, 0, 0, 0, 0)

    return WeatherResult(
        weather_score    = weather_score,
        hot_days_count   = hot_days,
        rainy_days_count = rainy_days,
        forecast         = forecast,
        today_max_temp   = today.max_temp,
        today_min_temp   = today.min_temp,
        today_rain_prob  = today.rain_prob,
        today_humidity   = today.humidity,
        today_wind_speed = today.wind_speed,
        today_precip_mm  = today.precip_sum,
        avg_humidity     = avg_humidity,
    )
