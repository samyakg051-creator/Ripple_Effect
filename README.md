├── modules/ (6100 tokens)
    ├── __init__.py
    ├── ai_assistant.py (900 tokens)
    ├── price_analysis.py (1100 tokens)
    ├── explanation.py (1200 tokens)
    ├── weather.py (1400 tokens)
    └── scoring.py (1500 tokens)
├── requirements.txt
├── .env.example
├── .streamlit/ (100 tokens)
    └── config.toml
├── .gitignore
├── data/ (400 tokens)
    └── mandi_prices.csv (400 tokens)
└── app.py (5200 tokens)


/modules/__init__.py:
--------------------------------------------------------------------------------
1 | # AgriChain modules package
2 | 


--------------------------------------------------------------------------------
/requirements.txt:
--------------------------------------------------------------------------------
1 | streamlit>=1.32.0
2 | pandas>=2.0.0
3 | requests>=2.31.0
4 | groq>=0.9.0
5 | python-dotenv>=1.0.0
6 | 


--------------------------------------------------------------------------------
/.env.example:
--------------------------------------------------------------------------------
1 | # AgriChain Environment Variables
2 | # Copy this file to .env and fill in your values
3 | # Never commit .env to GitHub!
4 | 
5 | GROQ_API_KEY=your_groq_api_key_here
6 | 


--------------------------------------------------------------------------------
/.streamlit/config.toml:
--------------------------------------------------------------------------------
1 | [theme]
2 | base                   = "dark"
3 | backgroundColor        = "#0c1a0c"
4 | secondaryBackgroundColor = "#112011"
5 | textColor              = "#d4f0c0"
6 | primaryColor           = "#6ee86e"
7 | font                   = "sans serif"
8 | 


--------------------------------------------------------------------------------
/.gitignore:
--------------------------------------------------------------------------------
 1 | # Python
 2 | __pycache__/
 3 | *.py[cod]
 4 | *.pyo
 5 | *.pyd
 6 | .Python
 7 | *.egg-info/
 8 | dist/
 9 | build/
10 | 
11 | # Environment variables — NEVER commit this
12 | .env
13 | 
14 | # Streamlit
15 | .streamlit/secrets.toml
16 | 
17 | # VS Code
18 | .vscode/
19 | 
20 | # OS
21 | .DS_Store
22 | Thumbs.db
23 | 


--------------------------------------------------------------------------------
/data/mandi_prices.csv:
--------------------------------------------------------------------------------
 1 | Crop,Mandi,Price,Date
 2 | Wheat,Sangli,3600,08-12-2023
 3 | Wheat,Palghar,3045,08-12-2023
 4 | Wheat,Ulhasnagar,3250,08-12-2023
 5 | Wheat,Vasai,3350,09-12-2023
 6 | Wheat,Ulhasnagar,3250,09-12-2023
 7 | Wheat,Sangli,3550,09-12-2023
 8 | Wheat,Ulhasnagar,3400,10-12-2023
 9 | Wheat,Palghar,3025,11-12-2023
10 | Wheat,Ulhasnagar,3250,11-12-2023
11 | Wheat,Sangli,3500,11-12-2023
12 | Wheat,Palghar,3220,12-12-2023
13 | Wheat,Sangli,3450,01-01-2024
14 | Wheat,Ulhasnagar,3400,01-01-2024
15 | Wheat,Palghar,3025,01-01-2024
16 | Wheat,Kille Dharur,3021,01-01-2024
17 | Wheat,Ulhasnagar,3400,02-01-2024
18 | Wheat,Ulhasnagar,3400,03-01-2024
19 | Wheat,Ulhasnagar,3400,04-01-2024
20 | Wheat,Palghar,3220,04-01-2024
21 | Wheat,Kille Dharur,2890,05-01-2024
22 | Wheat,Vasai,3320,05-01-2024
23 | Wheat,Ulhasnagar,3400,05-01-2024
24 | Wheat,Sangli,3425,05-01-2024
25 | Wheat,Vasai,3260,06-01-2024
26 | Wheat,Sangli,3500,06-01-2024
27 | Wheat,Palghar,3150,08-01-2024
28 | Wheat,Kille Dharur,3331,08-01-2024
29 | Wheat,Ulhasnagar,3400,08-01-2024
30 | Wheat,Ulhasnagar,3250,09-01-2024
31 | Wheat,Sangli,3500,09-01-2024
32 | Wheat,Sangli,3500,10-01-2024
33 | Wheat,Ulhasnagar,3400,11-01-2024
34 | Wheat,Palghar,2950,11-01-2024
35 | Wheat,Sangli,3600,11-01-2024
36 | Wheat,Palghar,3045,12-01-2024
37 | Wheat,Sangli,3600,01-02-2024
38 | Wheat,Palghar,3170,01-02-2024
39 | Wheat,Vasai,3460,02-02-2024
40 | Wheat,Palghar,3155,02-02-2024
41 | Wheat,Kille Dharur,3000,02-02-2024
42 | Wheat,Sangli,3625,02-02-2024
43 | Wheat,Vasai,3420,03-02-2024
44 | Wheat,Ulhasnagar,3600,03-02-2024
45 | Wheat,Kille Dharur,3300,03-02-2024
46 | Wheat,Ulhasnagar,3300,04-02-2024
47 | Wheat,Palghar,3170,05-02-2024
48 | Wheat,Ulhasnagar,3400,05-02-2024
49 | Wheat,Ulhasnagar,3600,06-02-2024
50 | Wheat,Palghar,3250,06-02-2024
51 | 


--------------------------------------------------------------------------------
/modules/ai_assistant.py:
--------------------------------------------------------------------------------
  1 | """
  2 | AgriChain – modules/ai_assistant.py
  3 | Groq-powered AI assistant for farmer queries.
  4 | """
  5 | 
  6 | from groq import Groq
  7 | 
  8 | 
  9 | # ---------------------------------------------------------------------------
 10 | # System prompt
 11 | # ---------------------------------------------------------------------------
 12 | 
 13 | _SYSTEM_PROMPT = """You are AgriChain AI, a friendly and practical assistant for Indian farmers.
 14 | You help farmers make smart decisions about when to harvest and sell their crops.
 15 | Keep answers short, clear and actionable. Avoid jargon. Use simple language.
 16 | When relevant, refer to the farm analysis data provided in the context.
 17 | Always be encouraging and empathetic — farming is hard work.
 18 | Respond in the same language the farmer uses (Hindi or English)."""
 19 | 
 20 | 
 21 | # ---------------------------------------------------------------------------
 22 | # Public entry point
 23 | # ---------------------------------------------------------------------------
 24 | 
 25 | def get_ai_response(
 26 |     api_key: str,
 27 |     user_message: str,
 28 |     context: str = "",
 29 |     chat_history: list[dict] | None = None,
 30 | ) -> str:
 31 |     """
 32 |     Send a message to Groq and return the AI response.
 33 | 
 34 |     Parameters
 35 |     ----------
 36 |     api_key      : str  – Groq API key
 37 |     user_message : str  – The farmer's question
 38 |     context      : str  – Current analysis context (scores, weather, prices)
 39 |     chat_history : list – Previous messages for multi-turn conversation
 40 | 
 41 |     Returns
 42 |     -------
 43 |     str – AI assistant response text
 44 |     """
 45 |     client = Groq(api_key=api_key)
 46 | 
 47 |     system_content = _SYSTEM_PROMPT
 48 |     if context:
 49 |         system_content += f"\n\nCurrent Farm Analysis:\n{context}"
 50 | 
 51 |     messages = [{"role": "system", "content": system_content}]
 52 | 
 53 |     # Include previous turns for context
 54 |     if chat_history:
 55 |         messages.extend(chat_history[-6:])  # last 3 exchanges
 56 | 
 57 |     messages.append({"role": "user", "content": user_message})
 58 | 
 59 |     response = client.chat.completions.create(
 60 |         model="llama-3.1-8b-instant",
 61 |         messages=messages,
 62 |         max_tokens=400,
 63 |         temperature=0.7,
 64 |     )
 65 | 
 66 |     return response.choices[0].message.content.strip()
 67 | 
 68 | 
 69 | def build_context(
 70 |     crop: str,
 71 |     mandi: str,
 72 |     price_result=None,
 73 |     weather_result=None,
 74 |     score_result=None,
 75 |     storage_type: str = "",
 76 |     distance_km: float = 0,
 77 | ) -> str:
 78 |     """
 79 |     Build a plain-text context string from the current analysis results
 80 |     to pass to the AI assistant.
 81 |     """
 82 |     parts = [
 83 |         f"Crop: {crop}",
 84 |         f"Target Mandi: {mandi}",
 85 |         f"Storage Type: {storage_type}",
 86 |         f"Distance to Mandi: {distance_km} km",
 87 |     ]
 88 | 
 89 |     if price_result:
 90 |         parts += [
 91 |             f"Last 7-Day Avg Price: ₹{price_result.last_7_avg:,.2f}",
 92 |             f"Last 30-Day Avg Price: ₹{price_result.last_30_avg:,.2f}",
 93 |             f"Price Trend: {price_result.trend_percent:+.2f}%",
 94 |             f"Price Score: {price_result.price_score}/30",
 95 |         ]
 96 | 
 97 |     if weather_result:
 98 |         parts += [
 99 |             f"Weather Score: {weather_result.weather_score}/30",
100 |             f"Hot Days Forecast (>35°C): {weather_result.hot_days_count}",
101 |             f"Rainy Days Forecast (>60%): {weather_result.rainy_days_count}",
102 |         ]
103 | 
104 |     if score_result:
105 |         parts += [
106 |             f"Storage Score: {score_result.storage_score}/20",
107 |             f"Transport Score: {score_result.transport_score}/20",
108 |             f"FINAL Harvest Readiness Score: {score_result.final_score}/100",
109 |             f"Market Status: {score_result.traffic_light}",
110 |         ]
111 | 
112 |     return "\n".join(parts)
113 | 


--------------------------------------------------------------------------------
/modules/price_analysis.py:
--------------------------------------------------------------------------------
  1 | """
  2 | AgriChain – modules/price_analysis.py
  3 | Loads mandi price CSV data and computes price trend score.
  4 | """
  5 | 
  6 | import pandas as pd
  7 | from dataclasses import dataclass
  8 | from pathlib import Path
  9 | 
 10 | 
 11 | # ---------------------------------------------------------------------------
 12 | # Data container
 13 | # ---------------------------------------------------------------------------
 14 | 
 15 | @dataclass
 16 | class PriceAnalysisResult:
 17 |     last_7_avg:    float   # Average price over the last 7 days of available data
 18 |     last_30_avg:   float   # Average price over the last 30 days of available data
 19 |     trend_percent: float   # % change: (last_7_avg - last_30_avg) / last_30_avg * 100
 20 |     price_score:   float   # 0–30 score derived from trend
 21 | 
 22 | 
 23 | # ---------------------------------------------------------------------------
 24 | # CSV path
 25 | # ---------------------------------------------------------------------------
 26 | 
 27 | _CSV_PATH = Path(__file__).parent.parent / "data" / "mandi_prices.csv"
 28 | 
 29 | 
 30 | # ---------------------------------------------------------------------------
 31 | # Internal helpers
 32 | # ---------------------------------------------------------------------------
 33 | 
 34 | def _load_data() -> pd.DataFrame:
 35 |     """Load and parse the mandi prices CSV."""
 36 |     df = pd.read_csv(_CSV_PATH)
 37 |     df["Crop"]  = df["Crop"].str.strip()
 38 |     df["Mandi"] = df["Mandi"].str.strip()
 39 |     df["Date"]  = pd.to_datetime(df["Date"], dayfirst=True)
 40 |     df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
 41 |     df = df.dropna(subset=["Price", "Date"])
 42 |     return df
 43 | 
 44 | 
 45 | def filter_by_crop_mandi(df: pd.DataFrame, crop: str, mandi: str) -> pd.DataFrame:
 46 |     """Filter dataframe by crop and mandi (case-insensitive)."""
 47 |     mask = (
 48 |         df["Crop"].str.strip().str.lower() == crop.strip().lower()
 49 |     ) & (
 50 |         df["Mandi"].str.strip().str.lower() == mandi.strip().lower()
 51 |     )
 52 |     filtered = df[mask].copy()
 53 |     if filtered.empty:
 54 |         raise ValueError(
 55 |             f"No data found for Crop='{crop}' and Mandi='{mandi}'"
 56 |         )
 57 |     return filtered
 58 | 
 59 | 
 60 | def _compute_price_score(trend_percent: float) -> float:
 61 |     """
 62 |     Convert a price trend percentage into a score out of 30.
 63 | 
 64 |     Scoring logic
 65 |     -------------
 66 |     trend >= +10%  → 30   (strong upward momentum)
 67 |     trend >= +5%   → 25
 68 |     trend >= 0%    → 20   (stable / slight upward)
 69 |     trend >= -5%   → 15
 70 |     trend >= -10%  → 10
 71 |     trend < -10%   →  5   (significant downward trend)
 72 |     """
 73 |     if trend_percent >= 10:
 74 |         return 30.0
 75 |     elif trend_percent >= 5:
 76 |         return 25.0
 77 |     elif trend_percent >= 0:
 78 |         return 20.0
 79 |     elif trend_percent >= -5:
 80 |         return 15.0
 81 |     elif trend_percent >= -10:
 82 |         return 10.0
 83 |     else:
 84 |         return 5.0
 85 | 
 86 | 
 87 | # ---------------------------------------------------------------------------
 88 | # Public entry point
 89 | # ---------------------------------------------------------------------------
 90 | 
 91 | def analyse_prices(crop: str, mandi: str) -> PriceAnalysisResult:
 92 |     """
 93 |     Analyse price trends for a given crop and mandi.
 94 | 
 95 |     Parameters
 96 |     ----------
 97 |     crop  : str – crop name (e.g. 'Wheat')
 98 |     mandi : str – mandi name (e.g. 'Sangli')
 99 | 
100 |     Returns
101 |     -------
102 |     PriceAnalysisResult with last_7_avg, last_30_avg, trend_percent, price_score.
103 | 
104 |     Raises
105 |     ------
106 |     ValueError – if no data exists for the given crop/mandi combination.
107 |     FileNotFoundError – if the CSV file is missing.
108 |     """
109 |     df       = _load_data()
110 |     filtered = filter_by_crop_mandi(df, crop, mandi)
111 | 
112 |     # Sort chronologically and use all available data
113 |     filtered  = filtered.sort_values("Date")
114 |     prices    = filtered["Price"].tolist()
115 | 
116 |     # Use last 7 records as proxy for "last 7 days" and all as "last 30 days"
117 |     last_7    = prices[-7:]  if len(prices) >= 7  else prices
118 |     last_30   = prices[-30:] if len(prices) >= 30 else prices
119 | 
120 |     last_7_avg  = round(sum(last_7)  / len(last_7),  2)
121 |     last_30_avg = round(sum(last_30) / len(last_30), 2)
122 | 
123 |     if last_30_avg == 0:
124 |         trend_percent = 0.0
125 |     else:
126 |         trend_percent = round(((last_7_avg - last_30_avg) / last_30_avg) * 100, 2)
127 | 
128 |     price_score = _compute_price_score(trend_percent)
129 | 
130 |     return PriceAnalysisResult(
131 |         last_7_avg=last_7_avg,
132 |         last_30_avg=last_30_avg,
133 |         trend_percent=trend_percent,
134 |         price_score=price_score,
135 |     )
136 | 
137 | 
138 | # ---------------------------------------------------------------------------
139 | # Quick smoke-test  (python -m modules.price_analysis)
140 | # ---------------------------------------------------------------------------
141 | 
142 | if __name__ == "__main__":
143 |     result = analyse_prices(crop="Wheat", mandi="Sangli")
144 |     print(result)
145 | 


--------------------------------------------------------------------------------
/modules/explanation.py:
--------------------------------------------------------------------------------
  1 | """
  2 | AgriChain – modules/explanation.py
  3 | Generates a human-readable, farmer-friendly harvest readiness explanation.
  4 | """
  5 | 
  6 | 
  7 | # ---------------------------------------------------------------------------
  8 | # Internal helpers
  9 | # ---------------------------------------------------------------------------
 10 | 
 11 | def _price_explanation(trend_percent: float) -> str:
 12 |     direction = "upward" if trend_percent >= 0 else "downward"
 13 |     sign      = "+" if trend_percent >= 0 else ""
 14 |     return (
 15 |         f"Prices are trending {direction} by {sign}{trend_percent:.2f}% "
 16 |         f"compared to the last 30-day average."
 17 |     )
 18 | 
 19 | 
 20 | def _weather_explanation(hot_days: int, rainy_days: int) -> str:
 21 |     parts = []
 22 | 
 23 |     if hot_days == 0:
 24 |         parts.append("No extreme heat days are forecast in the next 5 days.")
 25 |     elif hot_days == 1:
 26 |         parts.append("1 day with temperatures above 35°C is forecast — monitor crop stress.")
 27 |     else:
 28 |         parts.append(
 29 |             f"{hot_days} days with temperatures above 35°C are forecast — "
 30 |             f"high heat may affect crop quality during transport."
 31 |         )
 32 | 
 33 |     if rainy_days == 0:
 34 |         parts.append("No heavy rainfall is predicted — conditions look clear for market movement.")
 35 |     elif rainy_days == 1:
 36 |         parts.append("1 day with high rainfall probability (>60%) is forecast — plan transport accordingly.")
 37 |     else:
 38 |         parts.append(
 39 |             f"{rainy_days} days with high rainfall probability (>60%) are forecast — "
 40 |             f"consider delaying transport to avoid spoilage and road delays."
 41 |         )
 42 | 
 43 |     return " ".join(parts)
 44 | 
 45 | 
 46 | def _storage_explanation(storage_type: str) -> str:
 47 |     low_risk  = {"cold_storage", "warehouse"}
 48 |     high_risk = {"open_yard", "none"}
 49 |     key       = storage_type.lower().strip()
 50 | 
 51 |     if key in low_risk:
 52 |         label = "Cold storage" if key == "cold_storage" else "Warehouse storage"
 53 |         return (
 54 |             f"{label} is available — spoilage risk is significantly reduced "
 55 |             f"and crop quality can be maintained until market conditions improve."
 56 |         )
 57 |     elif key in high_risk:
 58 |         label = "Open yard storage" if key == "open_yard" else "No storage facility"
 59 |         return (
 60 |             f"{label} is in use — spoilage risk is higher. "
 61 |             f"It is advisable to move produce to market as soon as possible."
 62 |         )
 63 |     else:
 64 |         return (
 65 |             f"Storage type '{storage_type}' is noted. "
 66 |             f"Ensure proper storage conditions to minimise spoilage risk."
 67 |         )
 68 | 
 69 | 
 70 | def _transport_explanation(distance_km: float) -> str:
 71 |     if distance_km < 50:
 72 |         return (
 73 |             f"The mandi is {distance_km:.0f} km away — a short distance. "
 74 |             f"Transport cost and spoilage risk during transit are minimal."
 75 |         )
 76 |     elif distance_km <= 150:
 77 |         return (
 78 |             f"The mandi is {distance_km:.0f} km away — a moderate distance. "
 79 |             f"Transport is feasible but plan for fuel costs and timely departure."
 80 |         )
 81 |     else:
 82 |         return (
 83 |             f"The mandi is {distance_km:.0f} km away — a long distance. "
 84 |             f"Higher transport costs and increased spoilage risk should be factored "
 85 |             f"into your selling decision."
 86 |         )
 87 | 
 88 | 
 89 | # ---------------------------------------------------------------------------
 90 | # Public entry point
 91 | # ---------------------------------------------------------------------------
 92 | 
 93 | def generate_explanation(
 94 |     price_result,
 95 |     weather_result,
 96 |     storage_type: str,
 97 |     distance_km: float,
 98 | ) -> str:
 99 |     """
100 |     Generate a plain-text, farmer-friendly explanation of harvest readiness.
101 | 
102 |     Parameters
103 |     ----------
104 |     price_result   : PriceAnalysisResult – output from analyse_prices()
105 |     weather_result : WeatherResult       – output from get_weather_score()
106 |     storage_type   : str                 – storage facility type
107 |     distance_km    : float               – road distance to target mandi
108 | 
109 |     Returns
110 |     -------
111 |     str – multi-line explanation covering price, weather, storage, and transport.
112 |     """
113 |     sections = [
114 |         "📈 Price Outlook:\n"   + _price_explanation(price_result.trend_percent),
115 |         "🌤️ Weather Conditions:\n" + _weather_explanation(
116 |             weather_result.hot_days_count,
117 |             weather_result.rainy_days_count,
118 |         ),
119 |         "🏚️ Storage Conditions:\n" + _storage_explanation(storage_type),
120 |         "🚛 Transport Assessment:\n" + _transport_explanation(distance_km),
121 |     ]
122 | 
123 |     return "\n\n".join(sections)
124 | 
125 | 
126 | # ---------------------------------------------------------------------------
127 | # Quick smoke-test
128 | # ---------------------------------------------------------------------------
129 | 
130 | if __name__ == "__main__":
131 |     from types import SimpleNamespace
132 | 
133 |     mock_price   = SimpleNamespace(trend_percent=6.2,  last_7_avg=2150.0, last_30_avg=2025.0, price_score=22.5)
134 |     mock_weather = SimpleNamespace(weather_score=21.0, hot_days_count=1,  rainy_days_count=2)
135 | 
136 |     print(generate_explanation(mock_price, mock_weather, "warehouse", 120))
137 | 


--------------------------------------------------------------------------------
/modules/weather.py:
--------------------------------------------------------------------------------
  1 | """
  2 | AgriChain – modules/weather.py
  3 | Fetches 5-day weather forecast from Open-Meteo and computes a weather score.
  4 | """
  5 | 
  6 | import requests
  7 | from dataclasses import dataclass
  8 | 
  9 | 
 10 | # ---------------------------------------------------------------------------
 11 | # Constants
 12 | # ---------------------------------------------------------------------------
 13 | 
 14 | OPEN_METEO_URL       = "https://api.open-meteo.com/v1/forecast"
 15 | FORECAST_DAYS        = 5
 16 | TEMP_THRESHOLD       = 35.0   # °C – days above this are penalised
 17 | RAIN_THRESHOLD       = 60.0   # %  – days above this are penalised
 18 | PENALTY_PER_HOT_DAY  = 3
 19 | PENALTY_PER_RAIN_DAY = 3
 20 | MAX_SCORE            = 30
 21 | 
 22 | 
 23 | # ---------------------------------------------------------------------------
 24 | # Data container
 25 | # ---------------------------------------------------------------------------
 26 | 
 27 | @dataclass
 28 | class WeatherResult:
 29 |     weather_score:    float   # 0–30
 30 |     hot_days_count:   int     # days with max temp > 35°C
 31 |     rainy_days_count: int     # days with precipitation probability > 60%
 32 | 
 33 | 
 34 | # ---------------------------------------------------------------------------
 35 | # API fetch
 36 | # ---------------------------------------------------------------------------
 37 | 
 38 | def _fetch_forecast(latitude: float, longitude: float) -> dict:
 39 |     """
 40 |     Call the Open-Meteo forecast endpoint and return the parsed JSON response.
 41 | 
 42 |     Parameters
 43 |     ----------
 44 |     latitude  : float – location latitude
 45 |     longitude : float – location longitude
 46 | 
 47 |     Returns
 48 |     -------
 49 |     dict – raw JSON response from Open-Meteo
 50 | 
 51 |     Raises
 52 |     ------
 53 |     requests.HTTPError    – on non-2xx HTTP response
 54 |     requests.Timeout      – if the request times out
 55 |     requests.RequestException – on any other network error
 56 |     """
 57 |     params = {
 58 |         "latitude":    latitude,
 59 |         "longitude":   longitude,
 60 |         "daily":       "temperature_2m_max,precipitation_probability_max",
 61 |         "forecast_days": FORECAST_DAYS,
 62 |         "timezone":    "auto",
 63 |     }
 64 | 
 65 |     response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
 66 |     response.raise_for_status()
 67 |     return response.json()
 68 | 
 69 | 
 70 | # ---------------------------------------------------------------------------
 71 | # Parsing
 72 | # ---------------------------------------------------------------------------
 73 | 
 74 | def _parse_daily(data: dict) -> tuple[list[float], list[float]]:
 75 |     """
 76 |     Extract temperature and precipitation lists from the API response.
 77 | 
 78 |     Returns
 79 |     -------
 80 |     (temperatures, precipitation_probabilities) – parallel lists, one value per day.
 81 | 
 82 |     Raises
 83 |     ------
 84 |     KeyError  – if expected keys are absent in the API response.
 85 |     """
 86 |     daily         = data["daily"]
 87 |     temperatures  = daily["temperature_2m_max"]
 88 |     precipitation = daily["precipitation_probability_max"]
 89 |     return temperatures, precipitation
 90 | 
 91 | 
 92 | # ---------------------------------------------------------------------------
 93 | # Scoring
 94 | # ---------------------------------------------------------------------------
 95 | 
 96 | def _compute_score(
 97 |     temperatures: list[float],
 98 |     precipitation: list[float],
 99 | ) -> tuple[float, int, int]:
100 |     """
101 |     Apply penalty rules and return (weather_score, hot_days, rainy_days).
102 | 
103 |     Rules
104 |     -----
105 |     - Start at MAX_SCORE (30).
106 |     - Each day with temperature > 35°C  → -3 points.
107 |     - Each day with precipitation > 60% → -3 points.
108 |     - Score is clamped to [0, 30].
109 | 
110 |     A single day can trigger both penalties independently.
111 |     """
112 |     score      = float(MAX_SCORE)
113 |     hot_days   = 0
114 |     rainy_days = 0
115 | 
116 |     for temp, precip in zip(temperatures, precipitation):
117 |         if temp is not None and temp > TEMP_THRESHOLD:
118 |             score    -= PENALTY_PER_HOT_DAY
119 |             hot_days += 1
120 | 
121 |         if precip is not None and precip > RAIN_THRESHOLD:
122 |             score      -= PENALTY_PER_RAIN_DAY
123 |             rainy_days += 1
124 | 
125 |     final_score = round(min(max(score, 0.0), float(MAX_SCORE)), 4)
126 |     return final_score, hot_days, rainy_days
127 | 
128 | 
129 | # ---------------------------------------------------------------------------
130 | # Public entry point
131 | # ---------------------------------------------------------------------------
132 | 
133 | def get_weather_score(latitude: float, longitude: float) -> WeatherResult:
134 |     """
135 |     Fetch a 5-day weather forecast and compute a harvest-readiness weather score.
136 | 
137 |     Parameters
138 |     ----------
139 |     latitude  : float – decimal latitude of the farm / mandi location
140 |     longitude : float – decimal longitude of the farm / mandi location
141 | 
142 |     Returns
143 |     -------
144 |     WeatherResult dataclass with:
145 |         weather_score    (float, 0–30)
146 |         hot_days_count   (int)
147 |         rainy_days_count (int)
148 | 
149 |     Raises
150 |     ------
151 |     requests.HTTPError        – on non-2xx API response
152 |     requests.Timeout          – if the API call times out (10 s limit)
153 |     requests.RequestException – on network-level failures
154 |     KeyError                  – if the API response is missing expected fields
155 |     """
156 |     raw_data                  = _fetch_forecast(latitude, longitude)
157 |     temperatures, precip      = _parse_daily(raw_data)
158 |     weather_score, hot, rainy = _compute_score(temperatures, precip)
159 | 
160 |     return WeatherResult(
161 |         weather_score=weather_score,
162 |         hot_days_count=hot,
163 |         rainy_days_count=rainy,
164 |     )
165 | 
166 | 
167 | # ---------------------------------------------------------------------------
168 | # Quick smoke-test  (python -m modules.weather)
169 | # ---------------------------------------------------------------------------
170 | 
171 | if __name__ == "__main__":
172 |     # Coordinates for New Delhi, India
173 |     result = get_weather_score(latitude=28.6139, longitude=77.2090)
174 |     print(result)
175 | 


--------------------------------------------------------------------------------
/modules/scoring.py:
--------------------------------------------------------------------------------
  1 | """
  2 | AgriChain – modules/scoring.py
  3 | Computes storage score, transport score, final weighted score, and traffic light.
  4 | """
  5 | 
  6 | from dataclasses import dataclass
  7 | 
  8 | 
  9 | # ---------------------------------------------------------------------------
 10 | # Data container returned by the scoring module
 11 | # ---------------------------------------------------------------------------
 12 | 
 13 | @dataclass
 14 | class ScoreResult:
 15 |     price_score: float        # 0–30  (supplied externally)
 16 |     weather_score: float      # 0–30  (supplied externally)
 17 |     storage_score: float      # 0–20  (computed here)
 18 |     transport_score: float    # 0–20  (computed here)
 19 |     final_score: float        # 0–100 (weighted composite)
 20 |     traffic_light: str        # "Green" | "Yellow" | "Red"
 21 | 
 22 | 
 23 | # ---------------------------------------------------------------------------
 24 | # Storage scoring
 25 | # ---------------------------------------------------------------------------
 26 | 
 27 | # Storage quality tiers → score out of 20
 28 | _STORAGE_TIERS: dict[str, int] = {
 29 |     "cold_storage":    20,   # refrigerated / controlled atmosphere
 30 |     "warehouse":       15,   # dry, covered warehouse
 31 |     "covered_shed":    10,   # basic covered shed
 32 |     "open_yard":        5,   # open-air storage
 33 |     "none":             0,   # no storage available
 34 | }
 35 | 
 36 | 
 37 | def compute_storage_score(storage_type: str) -> float:
 38 |     """
 39 |     Return a storage score out of 20 based on storage facility type.
 40 | 
 41 |     Parameters
 42 |     ----------
 43 |     storage_type : str
 44 |         One of: 'cold_storage', 'warehouse', 'covered_shed', 'open_yard', 'none'.
 45 |         Case-insensitive.  Unknown values default to 0.
 46 | 
 47 |     Returns
 48 |     -------
 49 |     float  – score in [0, 20]
 50 |     """
 51 |     return float(_STORAGE_TIERS.get(storage_type.lower().strip(), 0))
 52 | 
 53 | 
 54 | # ---------------------------------------------------------------------------
 55 | # Transport scoring
 56 | # ---------------------------------------------------------------------------
 57 | 
 58 | # Distance thresholds (km) → (base_score, penalty_per_km_beyond_threshold)
 59 | _TRANSPORT_BANDS = [
 60 |     (50,   20, 0.00),   # ≤  50 km → full score
 61 |     (150,  15, 0.05),   # 51–150 km → slight penalty
 62 |     (300,  10, 0.03),   # 151–300 km → moderate penalty
 63 |     (500,   5, 0.02),   # 301–500 km → high penalty
 64 | ]
 65 | _TRANSPORT_MIN_SCORE = 0
 66 | 
 67 | 
 68 | def compute_transport_score(distance_km: float) -> float:
 69 |     """
 70 |     Return a transport score out of 20 based on distance to market (km).
 71 | 
 72 |     Shorter distance = higher score (less spoilage / cost risk).
 73 | 
 74 |     Parameters
 75 |     ----------
 76 |     distance_km : float  – road distance to the target mandi in kilometres.
 77 | 
 78 |     Returns
 79 |     -------
 80 |     float  – score in [0, 20]
 81 |     """
 82 |     if distance_km <= 0:
 83 |         return 20.0
 84 | 
 85 |     for threshold, base_score, _ in _TRANSPORT_BANDS:
 86 |         if distance_km <= threshold:
 87 |             return float(base_score)
 88 | 
 89 |     # Beyond 500 km → minimum score
 90 |     return float(_TRANSPORT_MIN_SCORE)
 91 | 
 92 | 
 93 | # ---------------------------------------------------------------------------
 94 | # Final weighted score & traffic light
 95 | # ---------------------------------------------------------------------------
 96 | 
 97 | def compute_final_score(
 98 |     price_score: float,
 99 |     weather_score: float,
100 |     storage_score: float,
101 |     transport_score: float,
102 | ) -> float:
103 |     """
104 |     Weighted composite score (0–100).
105 | 
106 |     Weights
107 |     -------
108 |     Price   : 40 %
109 |     Weather : 30 %
110 |     Storage : 20 %
111 |     Transport: 10 %
112 | 
113 |     Each component is normalised to a 0–100 scale before weighting:
114 |         price_score   / 30 * 100
115 |         weather_score / 30 * 100
116 |         storage_score / 20 * 100
117 |         transport_score / 20 * 100
118 |     """
119 |     normalised_price     = (price_score     / 30) * 100
120 |     normalised_weather   = (weather_score   / 30) * 100
121 |     normalised_storage   = (storage_score   / 20) * 100
122 |     normalised_transport = (transport_score / 20) * 100
123 | 
124 |     final = (
125 |         0.4 * normalised_price
126 |         + 0.3 * normalised_weather
127 |         + 0.2 * normalised_storage
128 |         + 0.1 * normalised_transport
129 |     )
130 |     return round(min(max(final, 0.0), 100.0), 2)
131 | 
132 | 
133 | def get_traffic_light(final_score: float) -> str:
134 |     """
135 |     Convert a final score to a traffic-light colour.
136 | 
137 |     Green  : >= 70
138 |     Yellow : 40 – 69
139 |     Red    : <  40
140 |     """
141 |     if final_score >= 70:
142 |         return "Green"
143 |     elif final_score >= 40:
144 |         return "Yellow"
145 |     else:
146 |         return "Red"
147 | 
148 | 
149 | # ---------------------------------------------------------------------------
150 | # Public entry point
151 | # ---------------------------------------------------------------------------
152 | 
153 | def generate_score(
154 |     price_score: float,
155 |     weather_score: float,
156 |     storage_type: str,
157 |     distance_km: float,
158 | ) -> ScoreResult:
159 |     """
160 |     Master function that assembles all sub-scores into a ScoreResult.
161 | 
162 |     Parameters
163 |     ----------
164 |     price_score   : float – price trend score from price_analysis module (0–30)
165 |     weather_score : float – weather penalty score from weather module     (0–30)
166 |     storage_type  : str   – storage facility type string
167 |     distance_km   : float – road distance to target mandi in km
168 | 
169 |     Returns
170 |     -------
171 |     ScoreResult dataclass with all scores and traffic light label.
172 |     """
173 |     storage_score   = compute_storage_score(storage_type)
174 |     transport_score = compute_transport_score(distance_km)
175 |     final_score     = compute_final_score(price_score, weather_score,
176 |                                           storage_score, transport_score)
177 |     traffic_light   = get_traffic_light(final_score)
178 | 
179 |     return ScoreResult(
180 |         price_score=price_score,
181 |         weather_score=weather_score,
182 |         storage_score=storage_score,
183 |         transport_score=transport_score,
184 |         final_score=final_score,
185 |         traffic_light=traffic_light,
186 |     )
187 | 
188 | 
189 | # ---------------------------------------------------------------------------
190 | # Quick smoke-test (run directly: python -m modules.scoring)
191 | # ---------------------------------------------------------------------------
192 | 
193 | if __name__ == "__main__":
194 |     result = generate_score(
195 |         price_score=22.5,
196 |         weather_score=24.0,
197 |         storage_type="warehouse",
198 |         distance_km=120,
199 |     )
200 |     print(result)
201 | 


--------------------------------------------------------------------------------
/app.py:
--------------------------------------------------------------------------------
  1 | """
  2 | AgriChain – app.py
  3 | Streamlit frontend for the Harvest Readiness Score dashboard.
  4 | """
  5 | 
  6 | import streamlit as st
  7 | import pandas as pd
  8 | import os
  9 | from dotenv import load_dotenv
 10 | from modules.price_analysis import analyse_prices
 11 | from modules.scoring import generate_score
 12 | from modules.weather import get_weather_score
 13 | from modules.explanation import generate_explanation
 14 | from modules.ai_assistant import get_ai_response, build_context
 15 | 
 16 | # Load .env file automatically (works locally; on cloud use platform secrets)
 17 | load_dotenv()
 18 | 
 19 | 
 20 | # ---------------------------------------------------------------------------
 21 | # Page config
 22 | # ---------------------------------------------------------------------------
 23 | 
 24 | st.set_page_config(
 25 |     page_title="AgriChain – Harvest Readiness Intelligence",
 26 |     page_icon="🌾",
 27 |     layout="wide",
 28 | )
 29 | 
 30 | # ---------------------------------------------------------------------------
 31 | # Custom CSS – Match screenshot theme
 32 | # ---------------------------------------------------------------------------
 33 | 
 34 | st.markdown("""
 35 | <style>
 36 | @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');
 37 | 
 38 | /* ── Base ── */
 39 | html, body, [class*="css"] {
 40 |     font-family: 'Inter', sans-serif;
 41 |     background-color: #0c1a0c !important;
 42 |     color: #d4f0c0 !important;
 43 | }
 44 | .stApp {
 45 |     background-color: #0c1a0c !important;
 46 | }
 47 | .main, .main > div, .block-container {
 48 |     background-color: #0c1a0c !important;
 49 | }
 50 | [data-testid="stAppViewContainer"] {
 51 |     background-color: #0c1a0c !important;
 52 | }
 53 | [data-testid="stHeader"] {
 54 |     background-color: #0c1a0c !important;
 55 |     border-bottom: 1px solid #1e3a1e !important;
 56 | }
 57 | .main > div { padding-top: 1rem !important; }
 58 | section[data-testid="stSidebar"] { background-color: #091409; border-right: 1px solid #1e3a1e; }
 59 | section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem; }
 60 | 
 61 | /* ── Sidebar brand ── */
 62 | .sidebar-brand {
 63 |     display: flex; align-items: center; gap: 10px;
 64 |     margin-bottom: 0.2rem;
 65 | }
 66 | .sidebar-brand-name {
 67 |     font-family: 'Syne', sans-serif;
 68 |     font-size: 1.3rem; font-weight: 800;
 69 |     color: #6ee86e;
 70 | }
 71 | .sidebar-subtitle {
 72 |     font-size: 0.78rem; color: #4a7a4a;
 73 |     font-weight: 500; margin-bottom: 1.5rem;
 74 | }
 75 | .sidebar-divider { border: none; border-top: 1px solid #1e3a1e; margin: 1.2rem 0; }
 76 | 
 77 | /* ── Sidebar input labels ── */
 78 | .input-label {
 79 |     font-size: 0.78rem; font-weight: 600; color: #6ee86e;
 80 |     text-transform: uppercase; letter-spacing: 0.07em;
 81 |     margin-bottom: 0.3rem; display: flex; align-items: center; gap: 6px;
 82 | }
 83 | div[data-testid="stSelectbox"] label,
 84 | div[data-testid="stSlider"] label,
 85 | div[data-testid="stTextInput"] label {
 86 |     color: #6ee86e !important; font-size: 0.82rem !important; font-weight: 600 !important;
 87 | }
 88 | 
 89 | /* ── Selectbox ── */
 90 | div[data-testid="stSelectbox"] > div > div {
 91 |     background-color: #112011 !important;
 92 |     border: 1px solid #2a4a2a !important;
 93 |     border-radius: 8px !important;
 94 |     color: #d4f0c0 !important;
 95 | }
 96 | 
 97 | /* ── Slider ── */
 98 | div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
 99 |     background-color: #6ee86e !important;
100 | }
101 | 
102 | /* ── Button ── */
103 | .stButton > button {
104 |     background-color: #6ee86e;
105 |     color: #0c1a0c;
106 |     font-family: 'Syne', sans-serif;
107 |     font-weight: 700; font-size: 0.95rem;
108 |     border: none; border-radius: 8px;
109 |     padding: 0.55rem 1.5rem; width: 100%;
110 |     cursor: pointer; transition: background 0.2s;
111 | }
112 | .stButton > button:hover { background-color: #8ff58f; }
113 | 
114 | /* ── Hero card ── */
115 | .hero-card {
116 |     background: linear-gradient(135deg, #122112, #0e1a0e);
117 |     border: 1px solid #2a4a2a;
118 |     border-radius: 16px;
119 |     padding: 1.4rem 1.8rem;
120 |     display: flex; align-items: center; gap: 16px;
121 |     margin-bottom: 1rem;
122 | }
123 | .hero-logo { font-size: 2.4rem; }
124 | .hero-title {
125 |     font-family: 'Syne', sans-serif;
126 |     font-size: 2rem; font-weight: 800;
127 |     color: #d4f0c0; margin: 0;
128 | }
129 | .hero-subtitle { color: #4a7a4a; font-size: 0.85rem; margin-top: 2px; }
130 | 
131 | /* ── Score card ── */
132 | .score-card {
133 |     background: linear-gradient(135deg, #122112, #0e1a0e);
134 |     border: 1px solid #2a4a2a;
135 |     border-radius: 16px;
136 |     padding: 2rem;
137 |     text-align: center;
138 |     margin-bottom: 1rem;
139 | }
140 | .score-number {
141 |     font-family: 'Syne', sans-serif;
142 |     font-size: 5.5rem; font-weight: 800;
143 |     line-height: 1; color: #6ee86e;
144 | }
145 | .score-denom { font-size: 1.2rem; color: #4a7a4a; margin-top: 4px; }
146 | .score-badge {
147 |     display: inline-flex; align-items: center; gap: 8px;
148 |     padding: 0.4rem 1.1rem; border-radius: 20px;
149 |     font-size: 0.88rem; font-weight: 600;
150 |     margin: 0.8rem auto 0.4rem auto;
151 | }
152 | .badge-green  { background: #1a3a1a; border: 1px solid #4caf50; color: #4caf50; }
153 | .badge-yellow { background: #2a280a; border: 1px solid #ffc107; color: #ffc107; }
154 | .badge-red    { background: #2a0a0a; border: 1px solid #f44336; color: #f44336; }
155 | .score-tagline { font-size: 0.82rem; color: #4a7a4a; margin-top: 4px; }
156 | 
157 | /* ── Inline component scores ── */
158 | .component-scores {
159 |     display: flex; justify-content: center; gap: 2rem;
160 |     margin-top: 1.2rem; flex-wrap: wrap;
161 | }
162 | .comp-item { text-align: center; }
163 | .comp-label { font-size: 0.72rem; color: #4a7a4a; text-transform: uppercase; letter-spacing: 0.06em; }
164 | .comp-value { font-size: 1rem; font-weight: 700; color: #d4f0c0; }
165 | .comp-value span { font-size: 0.78rem; color: #4a7a4a; }
166 | 
167 | /* ── Section card ── */
168 | .section-card {
169 |     background: #112011;
170 |     border: 1px solid #2a4a2a;
171 |     border-radius: 14px;
172 |     padding: 1.4rem 1.6rem;
173 |     margin-bottom: 1rem;
174 | }
175 | .section-title {
176 |     font-size: 0.78rem; font-weight: 600;
177 |     color: #6ee86e; text-transform: uppercase;
178 |     letter-spacing: 0.08em; margin-bottom: 1rem;
179 | }
180 | 
181 | /* ── Metric grid ── */
182 | .metric-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
183 | .metric-box {
184 |     background: #0e1a0e; border: 1px solid #1e3a1e;
185 |     border-radius: 10px; padding: 0.9rem 1rem;
186 | }
187 | .metric-lbl { font-size: 0.72rem; color: #4a7a4a; text-transform: uppercase; letter-spacing: 0.06em; }
188 | .metric-val { font-size: 1.3rem; font-weight: 700; color: #d4f0c0; margin-top: 2px; }
189 | .metric-val.positive { color: #6ee86e; }
190 | .metric-val.negative { color: #f44336; }
191 | 
192 | /* ── Weather badges inline ── */
193 | .weather-row { display: flex; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap; }
194 | .weather-chip {
195 |     background: #0e1a0e; border: 1px solid #1e3a1e;
196 |     border-radius: 8px; padding: 0.6rem 1rem; flex: 1; min-width: 120px;
197 | }
198 | .weather-chip .metric-lbl { margin-bottom: 4px; }
199 | 
200 | /* ── Explanation section ── */
201 | .explanation-text {
202 |     font-size: 0.88rem; line-height: 1.7; color: #9ec89e;
203 |     white-space: pre-wrap;
204 | }
205 | 
206 | /* ── Chat area ── */
207 | .chat-card {
208 |     background: #112011;
209 |     border: 1px solid #2a4a2a;
210 |     border-radius: 14px;
211 |     padding: 1.2rem 1.4rem;
212 |     margin-bottom: 1rem;
213 | }
214 | .chat-title {
215 |     font-size: 0.78rem; font-weight: 600; color: #6ee86e;
216 |     text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 1rem;
217 | }
218 | .chat-msg-user {
219 |     background: #1a3a1a; border-radius: 10px;
220 |     padding: 0.7rem 1rem; margin-bottom: 0.6rem;
221 |     font-size: 0.88rem; color: #d4f0c0;
222 |     text-align: right;
223 | }
224 | .chat-msg-ai {
225 |     background: #0e1a0e; border: 1px solid #1e3a1e;
226 |     border-radius: 10px; padding: 0.7rem 1rem;
227 |     margin-bottom: 0.6rem; font-size: 0.88rem;
228 |     color: #9ec89e; line-height: 1.6;
229 | }
230 | div[data-testid="stTextInput"] input {
231 |     background-color: #0e1a0e !important;
232 |     border: 1px solid #2a4a2a !important;
233 |     border-radius: 8px !important;
234 |     color: #d4f0c0 !important;
235 |     font-size: 0.9rem !important;
236 | }
237 | div[data-testid="stTextInput"] input::placeholder { color: #3a5a3a !important; }
238 | 
239 | /* ── Info box ── */
240 | .info-box {
241 |     background: #0e1a0e; border: 1px solid #1e3a1e;
242 |     border-radius: 10px; padding: 1.2rem 1.4rem;
243 |     color: #4a7a4a; font-size: 0.88rem; text-align: center;
244 | }
245 | 
246 | /* ── Hide streamlit default elements ── */
247 | #MainMenu { visibility: hidden; }
248 | footer { visibility: hidden; }
249 | div[data-testid="stDecoration"] { display: none; }
250 | </style>
251 | """, unsafe_allow_html=True)
252 | 
253 | # ---------------------------------------------------------------------------
254 | # Mandi → coordinates lookup
255 | # ---------------------------------------------------------------------------
256 | 
257 | MANDI_COORDINATES: dict[str, tuple[float, float]] = {
258 |     "Sangli":       (16.8524, 74.5815),
259 |     "Palghar":      (19.6967, 72.7656),
260 |     "Ulhasnagar":   (19.2183, 73.1558),
261 |     "Vasai":        (19.3919, 72.8397),
262 |     "Kille Dharur": (18.0500, 76.5667),
263 |     "_default":     (20.5937, 78.9629),
264 | }
265 | 
266 | STORAGE_ICONS = {
267 |     "cold_storage": "❄️",
268 |     "warehouse":    "🏗️",
269 |     "covered_shed": "🏚️",
270 |     "open_yard":    "🌿",
271 |     "none":         "🚫",
272 | }
273 | 
274 | def get_mandi_coordinates(mandi: str) -> tuple[float, float]:
275 |     return MANDI_COORDINATES.get(mandi, MANDI_COORDINATES["_default"])
276 | 
277 | # ---------------------------------------------------------------------------
278 | # Load CSV
279 | # ---------------------------------------------------------------------------
280 | 
281 | CSV_PATH = "data/mandi_prices.csv"
282 | 
283 | @st.cache_data
284 | def load_csv(path: str) -> pd.DataFrame:
285 |     df = pd.read_csv(path)
286 |     df["Crop"]  = df["Crop"].str.strip()
287 |     df["Mandi"] = df["Mandi"].str.strip()
288 |     return df
289 | 
290 | try:
291 |     price_df  = load_csv(CSV_PATH)
292 |     all_crops = sorted(price_df["Crop"].dropna().unique().tolist())
293 | except FileNotFoundError:
294 |     st.error(f"📂 CSV not found at '{CSV_PATH}'. Please add the data file and restart.")
295 |     st.stop()
296 | except Exception as e:
297 |     st.error(f"❌ Failed to load price data: {e}")
298 |     st.stop()
299 | 
300 | # ---------------------------------------------------------------------------
301 | # Session state
302 | # ---------------------------------------------------------------------------
303 | 
304 | if "chat_history"     not in st.session_state: st.session_state.chat_history     = []
305 | if "ai_context"       not in st.session_state: st.session_state.ai_context       = ""
306 | if "analysis_done"    not in st.session_state: st.session_state.analysis_done    = False
307 | if "score_result"     not in st.session_state: st.session_state.score_result     = None
308 | if "price_result"     not in st.session_state: st.session_state.price_result     = None
309 | if "weather_result"   not in st.session_state: st.session_state.weather_result   = None
310 | if "explanation_text" not in st.session_state: st.session_state.explanation_text = ""
311 | if "selected_crop"    not in st.session_state: st.session_state.selected_crop    = ""
312 | if "selected_mandi"   not in st.session_state: st.session_state.selected_mandi   = ""
313 | 
314 | # ---------------------------------------------------------------------------
315 | # Sidebar
316 | # ---------------------------------------------------------------------------
317 | 
318 | STORAGE = ["cold_storage", "warehouse", "covered_shed", "open_yard", "none"]
319 | 
320 | with st.sidebar:
321 |     st.markdown("""
322 |     <div class="sidebar-brand">
323 |         <span style="font-size:1.4rem;">🌾</span>
324 |         <span class="sidebar-brand-name">AgriChain</span>
325 |     </div>
326 |     <div class="sidebar-subtitle">Harvest Readiness Intelligence</div>
327 |     <hr class="sidebar-divider">
328 |     """, unsafe_allow_html=True)
329 | 
330 |     crop = st.selectbox("🌱  Crop", all_crops, index=0)
331 | 
332 |     mandis_for_crop = sorted(
333 |         price_df[price_df["Crop"] == crop]["Mandi"].dropna().unique().tolist()
334 |     )
335 |     mandi        = st.selectbox("🏪  Mandi Market", mandis_for_crop, index=0)
336 |     storage_type = st.selectbox(
337 |         "🏚️  Storage Type",
338 |         STORAGE,
339 |         index=0,
340 |         format_func=lambda x: f"{STORAGE_ICONS.get(x, '')}  {x.replace('_', ' ').title()}",
341 |     )
342 |     distance_km  = st.slider("🚛  Distance to Mandi (km)", min_value=0, max_value=500, value=100, step=10)
343 | 
344 |     st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
345 |     run_button = st.button("📊  Calculate Score")
346 | 
347 | 
348 | # Read Groq API key solely from .env / environment variable
349 | groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()
350 | 
351 | 
352 | # ---------------------------------------------------------------------------
353 | # Hero Card
354 | # ---------------------------------------------------------------------------
355 | 
356 | crop_label  = crop if crop else "Crop"
357 | mandi_label = mandi if mandi else "Mandi"
358 | 
359 | st.markdown(f"""
360 | <div class="hero-card">
361 |     <div class="hero-logo">🌾</div>
362 |     <div>
363 |         <div class="hero-title">AgriChain</div>
364 |         <div class="hero-subtitle">Harvest Readiness Intelligence · {crop_label} · {mandi_label}</div>
365 |     </div>
366 | </div>
367 | """, unsafe_allow_html=True)
368 | 
369 | # ---------------------------------------------------------------------------
370 | # Run analysis
371 | # ---------------------------------------------------------------------------
372 | 
373 | if run_button:
374 |     try:
375 |         latitude, longitude = get_mandi_coordinates(mandi)
376 | 
377 |         with st.spinner("Analysing price trends..."):
378 |             price_result = analyse_prices(crop=crop, mandi=mandi)
379 | 
380 |         with st.spinner(f"Fetching live weather for {mandi}..."):
381 |             weather_result = get_weather_score(latitude=latitude, longitude=longitude)
382 | 
383 |         score_result = generate_score(
384 |             price_score=price_result.price_score,
385 |             weather_score=weather_result.weather_score,
386 |             storage_type=storage_type,
387 |             distance_km=float(distance_km),
388 |         )
389 | 
390 |         explanation_text = generate_explanation(
391 |             price_result=price_result,
392 |             weather_result=weather_result,
393 |             storage_type=storage_type,
394 |             distance_km=distance_km,
395 |         )
396 | 
397 |         # Store in session state
398 |         st.session_state.analysis_done    = True
399 |         st.session_state.score_result     = score_result
400 |         st.session_state.price_result     = price_result
401 |         st.session_state.weather_result   = weather_result
402 |         st.session_state.explanation_text = explanation_text
403 |         st.session_state.selected_crop    = crop
404 |         st.session_state.selected_mandi   = mandi
405 |         st.session_state.chat_history     = []  # reset chat on new analysis
406 |         st.session_state.ai_context       = build_context(
407 |             crop=crop, mandi=mandi,
408 |             price_result=price_result,
409 |             weather_result=weather_result,
410 |             score_result=score_result,
411 |             storage_type=storage_type,
412 |             distance_km=distance_km,
413 |         )
414 | 
415 |     except FileNotFoundError as e:
416 |         st.error(f"Data file not found: {e}")
417 |     except ValueError as e:
418 |         st.error(f"Data error: {e}")
419 |     except Exception as e:
420 |         st.error(f"Unexpected error: {e}")
421 | 
422 | # ---------------------------------------------------------------------------
423 | # Display results (from session state so they persist across chat interactions)
424 | # ---------------------------------------------------------------------------
425 | 
426 | if st.session_state.analysis_done:
427 |     score_result     = st.session_state.score_result
428 |     price_result     = st.session_state.price_result
429 |     weather_result   = st.session_state.weather_result
430 |     explanation_text = st.session_state.explanation_text
431 | 
432 |     # ── Score Card ──────────────────────────────────────────────────────────
433 |     tl = score_result.traffic_light
434 |     badge_class = {"Green": "badge-green", "Yellow": "badge-yellow", "Red": "badge-red"}.get(tl, "badge-green")
435 |     badge_dot   = {"Green": "🟢", "Yellow": "🟡", "Red": "🔴"}.get(tl, "🟢")
436 |     badge_text  = {"Green": "Good Time to Sell", "Yellow": "Monitor Conditions", "Red": "Hold — Wait for Better Prices"}.get(tl, "")
437 |     tagline     = {"Green": "Conditions are favourable — sell now", "Yellow": "Mixed signals — proceed with caution", "Red": "Market conditions are unfavourable"}.get(tl, "")
438 | 
439 |     st.markdown(f"""
440 |     <div class="score-card">
441 |         <div class="score-number">{int(score_result.final_score)}</div>
442 |         <div class="score-denom">/ 100</div>
443 |         <div><span class="score-badge {badge_class}">{badge_dot} {badge_text}</span></div>
444 |         <div class="score-tagline">{tagline}</div>
445 |         <div class="component-scores">
446 |             <div class="comp-item">
447 |                 <div class="comp-label">Price</div>
448 |                 <div class="comp-value">{price_result.price_score:.1f}<span>/30</span></div>
449 |             </div>
450 |             <div class="comp-item">
451 |                 <div class="comp-label">Weather</div>
452 |                 <div class="comp-value">{score_result.weather_score:.1f}<span>/30</span></div>
453 |             </div>
454 |             <div class="comp-item">
455 |                 <div class="comp-label">Storage</div>
456 |                 <div class="comp-value">{score_result.storage_score:.1f}<span>/20</span></div>
457 |             </div>
458 |             <div class="comp-item">
459 |                 <div class="comp-label">Transport</div>
460 |                 <div class="comp-value">{score_result.transport_score:.1f}<span>/20</span></div>
461 |             </div>
462 |         </div>
463 |     </div>
464 |     """, unsafe_allow_html=True)
465 | 
466 |     # ── Two columns: Price + Weather ─────────────────────────────────────────
467 |     col_left, col_right = st.columns(2)
468 | 
469 |     with col_left:
470 |         trend_sign  = "+" if price_result.trend_percent >= 0 else ""
471 |         trend_cls   = "positive" if price_result.trend_percent >= 0 else "negative"
472 |         st.markdown(f"""
473 |         <div class="section-card">
474 |             <div class="section-title">📈 Price Analysis</div>
475 |             <div class="metric-grid">
476 |                 <div class="metric-box">
477 |                     <div class="metric-lbl">7-Day Avg</div>
478 |                     <div class="metric-val">₹{price_result.last_7_avg:,.0f}</div>
479 |                 </div>
480 |                 <div class="metric-box">
481 |                     <div class="metric-lbl">30-Day Avg</div>
482 |                     <div class="metric-val">₹{price_result.last_30_avg:,.0f}</div>
483 |                 </div>
484 |                 <div class="metric-box">
485 |                     <div class="metric-lbl">Price Trend</div>
486 |                     <div class="metric-val {trend_cls}">{trend_sign}{price_result.trend_percent:.2f}%</div>
487 |                 </div>
488 |                 <div class="metric-box">
489 |                     <div class="metric-lbl">Price Score</div>
490 |                     <div class="metric-val">{price_result.price_score:.1f}<span style="font-size:0.82rem;color:#4a7a4a"> /30</span></div>
491 |                 </div>
492 |             </div>
493 |         </div>
494 |         """, unsafe_allow_html=True)
495 | 
496 |     with col_right:
497 |         hot_col  = "#f44336" if weather_result.hot_days_count  > 0 else "#6ee86e"
498 |         rain_col = "#f44336" if weather_result.rainy_days_count > 0 else "#6ee86e"
499 |         st.markdown(f"""
500 |         <div class="section-card">
501 |             <div class="section-title">🌤️ Weather Forecast (5-Day)</div>
502 |             <div class="metric-grid">
503 |                 <div class="metric-box">
504 |                     <div class="metric-lbl">Weather Score</div>
505 |                     <div class="metric-val">{weather_result.weather_score:.1f}<span style="font-size:0.82rem;color:#4a7a4a"> /30</span></div>
506 |                 </div>
507 |                 <div class="metric-box">
508 |                     <div class="metric-lbl">Forecast</div>
509 |                     <div class="metric-val" style="font-size:0.95rem;color:#9ec89e">5 days</div>
510 |                 </div>
511 |                 <div class="metric-box">
512 |                     <div class="metric-lbl">🌡️ Hot Days &gt;35°C</div>
513 |                     <div class="metric-val" style="color:{hot_col}">{weather_result.hot_days_count}</div>
514 |                 </div>
515 |                 <div class="metric-box">
516 |                     <div class="metric-lbl">🌧️ Rainy Days &gt;60%</div>
517 |                     <div class="metric-val" style="color:{rain_col}">{weather_result.rainy_days_count}</div>
518 |                 </div>
519 |             </div>
520 |         </div>
521 |         """, unsafe_allow_html=True)
522 | 
523 |     # ── Explanation ──────────────────────────────────────────────────────────
524 |     with st.expander("📋 Why this recommendation?", expanded=False):
525 |         st.markdown(f'<div class="explanation-text">{explanation_text}</div>', unsafe_allow_html=True)
526 | 
527 |     # ── AI Chat ──────────────────────────────────────────────────────────────
528 |     st.markdown('<div class="chat-card"><div class="chat-title">🤖 AgriChain AI — Ask About Your Harvest</div>', unsafe_allow_html=True)
529 | 
530 |     # Render chat history
531 |     for msg in st.session_state.chat_history:
532 |         if msg["role"] == "user":
533 |             st.markdown(f'<div class="chat-msg-user">🧑‍🌾 {msg["content"]}</div>', unsafe_allow_html=True)
534 |         else:
535 |             st.markdown(f'<div class="chat-msg-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)
536 | 
537 |     # Input form (prevents full page re-run on Enter)
538 |     with st.form(key="chat_form", clear_on_submit=True):
539 |         col_input, col_send = st.columns([5, 1])
540 |         with col_input:
541 |             user_input = st.text_input(
542 |                 "Ask AI",
543 |                 placeholder="Ask anything about your harvest...",
544 |                 label_visibility="collapsed",
545 |             )
546 |         with col_send:
547 |             send_btn = st.form_submit_button("Send ↑")
548 | 
549 |     st.markdown('</div>', unsafe_allow_html=True)
550 | 
551 |     if send_btn and user_input.strip():
552 |         if not groq_api_key:
553 |             st.warning("Please enter your Groq API key in the sidebar to use the AI assistant.")
554 |         else:
555 |             with st.spinner("AgriChain AI is thinking..."):
556 |                 try:
557 |                     response = get_ai_response(
558 |                         api_key=groq_api_key,
559 |                         user_message=user_input.strip(),
560 |                         context=st.session_state.ai_context,
561 |                         chat_history=st.session_state.chat_history,
562 |                     )
563 |                     st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
564 |                     st.session_state.chat_history.append({"role": "assistant", "content": response})
565 |                     st.rerun()
566 |                 except Exception as e:
567 |                     st.error(f"AI error: {str(e).encode('ascii', errors='replace').decode('ascii')}")
568 | 
569 | else:
570 |     # ── Welcome state ────────────────────────────────────────────────────────
571 |     st.markdown("""
572 |     <div class="score-card" style="opacity:0.6;">
573 |         <div class="score-number" style="font-size:3rem;color:#2a4a2a;">—</div>
574 |         <div class="score-denom">/ 100</div>
575 |         <div class="score-tagline" style="margin-top:0.8rem;">
576 |             Configure your parameters in the sidebar and click <strong style="color:#6ee86e">Calculate Score</strong> to begin.
577 |         </div>
578 |     </div>
579 |     <div class="info-box">
580 |         🌾 &nbsp; Select your crop, mandi, storage type and distance, then click <strong>Calculate Score</strong>.<br>
581 |         After analysis, the <strong style="color:#6ee86e">AgriChain AI</strong> will answer questions about your harvest.
582 |     </div>
583 |     """, unsafe_allow_html=True)
584 | 


--------------------------------------------------------------------------------
