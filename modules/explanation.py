"""
AgriChain – modules/explanation.py
Generates a human-readable, farmer-friendly harvest readiness explanation.
"""


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _price_explanation(trend_percent: float) -> str:
    direction = "upward" if trend_percent >= 0 else "downward"
    sign      = "+" if trend_percent >= 0 else ""
    return (
        f"Prices are trending {direction} by {sign}{trend_percent:.2f}% "
        f"compared to the last 30-day average."
    )


def _weather_explanation(hot_days: int, rainy_days: int) -> str:
    parts = []

    if hot_days == 0:
        parts.append("No extreme heat days are forecast in the next 5 days.")
    elif hot_days == 1:
        parts.append("1 day with temperatures above 35°C is forecast — monitor crop stress.")
    else:
        parts.append(
            f"{hot_days} days with temperatures above 35°C are forecast — "
            f"high heat may affect crop quality during transport."
        )

    if rainy_days == 0:
        parts.append("No heavy rainfall is predicted — conditions look clear for market movement.")
    elif rainy_days == 1:
        parts.append("1 day with high rainfall probability (>60%) is forecast — plan transport accordingly.")
    else:
        parts.append(
            f"{rainy_days} days with high rainfall probability (>60%) are forecast — "
            f"consider delaying transport to avoid spoilage and road delays."
        )

    return " ".join(parts)


def _storage_explanation(storage_type: str) -> str:
    low_risk  = {"cold_storage", "warehouse"}
    high_risk = {"open_yard", "none"}
    key       = storage_type.lower().strip()

    if key in low_risk:
        label = "Cold storage" if key == "cold_storage" else "Warehouse storage"
        return (
            f"{label} is available — spoilage risk is significantly reduced "
            f"and crop quality can be maintained until market conditions improve."
        )
    elif key in high_risk:
        label = "Open yard storage" if key == "open_yard" else "No storage facility"
        return (
            f"{label} is in use — spoilage risk is higher. "
            f"It is advisable to move produce to market as soon as possible."
        )
    else:
        return (
            f"Storage type '{storage_type}' is noted. "
            f"Ensure proper storage conditions to minimise spoilage risk."
        )


def _transport_explanation(distance_km: float) -> str:
    if distance_km < 50:
        return (
            f"The mandi is {distance_km:.0f} km away — a short distance. "
            f"Transport cost and spoilage risk during transit are minimal."
        )
    elif distance_km <= 150:
        return (
            f"The mandi is {distance_km:.0f} km away — a moderate distance. "
            f"Transport is feasible but plan for fuel costs and timely departure."
        )
    else:
        return (
            f"The mandi is {distance_km:.0f} km away — a long distance. "
            f"Higher transport costs and increased spoilage risk should be factored "
            f"into your selling decision."
        )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def generate_explanation(
    price_result,
    weather_result,
    storage_type: str,
    distance_km: float,
) -> str:
    """
    Generate a plain-text, farmer-friendly explanation of harvest readiness.

    Parameters
    ----------
    price_result   : PriceAnalysisResult – output from analyse_prices()
    weather_result : WeatherResult       – output from get_weather_score()
    storage_type   : str                 – storage facility type
    distance_km    : float               – road distance to target mandi

    Returns
    -------
    str – multi-line explanation covering price, weather, storage, and transport.
    """
    sections = [
        "📈 Price Outlook:\n"   + _price_explanation(price_result.trend_percent),
        "🌤️ Weather Conditions:\n" + _weather_explanation(
            weather_result.hot_days_count,
            weather_result.rainy_days_count,
        ),
        "🏚️ Storage Conditions:\n" + _storage_explanation(storage_type),
        "🚛 Transport Assessment:\n" + _transport_explanation(distance_km),
    ]

    return "\n\n".join(sections)


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from types import SimpleNamespace

    mock_price   = SimpleNamespace(trend_percent=6.2,  last_7_avg=2150.0, last_30_avg=2025.0, price_score=22.5)
    mock_weather = SimpleNamespace(weather_score=21.0, hot_days_count=1,  rainy_days_count=2)

    print(generate_explanation(mock_price, mock_weather, "warehouse", 120))
