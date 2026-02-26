"""AgriChain – modules/translations.py"""

TEXTS = {
    "English": {
        "app_title": "AgriChain",
        "app_subtitle": "Farm-to-Market Intelligence",
        "crop": "Crop",
        "district": "District (Maharashtra)",
        "sowing_date": "Sowing Date",
        "quantity": "Quantity (quintals)",
        "storage": "Storage Type",
        "language": "Language",
        "analyse": "Analyse Now",
        "summary_title": "My Farm",
        "days_until": "days until harvest",
        "days_past": "days past harvest window",
        "in_window": "Harvest window is OPEN",
        "risk_low": "LOW RISK",
        "risk_med": "MODERATE RISK",
        "risk_high": "HIGH RISK",
        "select_district": "Select District",
        "click_map": "or click directly on the map",
        "setup_first": "Please set up your farm on the Home page first.",
        "no_data": "No price data available for this crop/mandi.",
        "mandi_rank": "Mandi Price Rankings",
        "spoilage_title": "Spoilage Risk Assessment",
        "harvest_title": "Harvest Window",
        "home_title": "Farm Setup",
    },
    "हिंदी": {
        "app_title": "एग्रीचेन",
        "app_subtitle": "खेत से मंडी तक",
        "crop": "फसल",
        "district": "जिला (महाराष्ट्र)",
        "sowing_date": "बुवाई की तारीख",
        "quantity": "मात्रा (क्विंटल)",
        "storage": "भंडारण",
        "language": "भाषा",
        "analyse": "विश्लेषण करें",
        "summary_title": "मेरा खेत",
        "days_until": "दिन बाकी",
        "days_past": "दिन बीत गए",
        "in_window": "कटाई का समय है",
        "risk_low": "कम जोखिम",
        "risk_med": "मध्यम जोखिम",
        "risk_high": "अधिक जोखिम",
        "select_district": "जिला चुनें",
        "click_map": "या नक्शे पर क्लिक करें",
        "setup_first": "पहले होम पेज पर खेत सेटअप करें।",
        "no_data": "इस फसल/मंडी के लिए डेटा उपलब्ध नहीं।",
        "mandi_rank": "मंडी कीमत रैंकिंग",
        "spoilage_title": "खराबी जोखिम",
        "harvest_title": "कटाई विंडो",
        "home_title": "खेत सेटअप",
    },
}

CROP_EMOJI = {
    "Wheat": "🌾", "Tomato": "🍅", "Onion": "🧅",
    "Potato": "🥔", "Rice": "🍚",
}

def t(key: str, lang: str = "English") -> str:
    return TEXTS.get(lang, TEXTS["English"]).get(key, key)
