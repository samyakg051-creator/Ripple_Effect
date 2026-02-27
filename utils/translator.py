"""
utils/translator.py — Multilingual support for AgriChain pages.
"""
import streamlit as st

TRANSLATIONS = {
    "en": {
        "Select Crop": "Select Crop",
        "Sowing Date": "Sowing Date",
        "Get Recommendation": "Get Recommendation",
        "Best Harvest Window": "Best Harvest Window",
        "Expected Price Premium": "Expected Price Premium",
        "Confidence": "Confidence",
        "High": "High", "Medium": "Medium", "Low": "Low",
        "Score Breakdown": "Score Breakdown",
        "Price Seasonality": "Price Seasonality",
        "Weather Score": "Weather Score",
        "Soil Readiness": "Soil Readiness",
        "Why this recommendation?": "Why this recommendation?",
        "14-Day Price Trend": "14-Day Price Trend",
        "Weather Forecast": "Weather Forecast",
        "Mandi Ranker": "Mandi Ranker",
        "Quantity (Quintals)": "Quantity (Quintals)",
        "Find Best Mandis": "Find Best Mandis",
        "Expected Price": "Expected Price",
        "Transport Cost": "Transport Cost",
        "Net Profit per Qtl": "Net Profit per Qtl",
        "Distance": "Distance",
        "Mandi Net Profit Comparison": "Mandi Net Profit Comparison",
        "Total Earnings": "Total Earnings",
        "Spoilage Assessor": "Spoilage Assessor",
        "Storage Type": "Storage Type",
        "Transit Duration (Hours)": "Transit Duration (Hours)",
        "Assess Spoilage Risk": "Assess Spoilage Risk",
        "Spoilage Risk": "Spoilage Risk",
        "Spoilage Probability": "Probability",
        "Recommended Actions": "Recommended Actions",
        "Cost": "Cost",
        "Effectiveness": "Effectiveness",
        "Full Input Summary": "Full Input Summary",
        "Harvest Window": "Harvest Window",
        "Select District": "Select District",
    },
    "hi": {
        "Select Crop": "फसल चुनें",
        "Sowing Date": "बुवाई की तारीख",
        "Get Recommendation": "सिफारिश पाएं",
        "Best Harvest Window": "सर्वोत्तम कटाई समय",
        "Expected Price Premium": "अपेक्षित मूल्य प्रीमियम",
        "Confidence": "विश्वास",
        "High": "उच्च", "Medium": "मध्यम", "Low": "कम",
        "Score Breakdown": "स्कोर विवरण",
        "Price Seasonality": "मूल्य मौसमीकरण",
        "Weather Score": "मौसम स्कोर",
        "Soil Readiness": "मिट्टी तैयारी",
        "Why this recommendation?": "यह सिफारिश क्यों?",
        "14-Day Price Trend": "14 दिवसीय मूल्य रुझान",
        "Weather Forecast": "मौसम पूर्वानुमान",
        "Mandi Ranker": "मंडी रैंकर",
        "Quantity (Quintals)": "मात्रा (क्विंटल)",
        "Find Best Mandis": "सर्वोत्तम मंडी खोजें",
        "Expected Price": "अपेक्षित मूल्य",
        "Transport Cost": "परिवहन लागत",
        "Net Profit per Qtl": "प्रति क्विंटल शुद्ध लाभ",
        "Distance": "दूरी",
        "Mandi Net Profit Comparison": "मंडी शुद्ध लाभ तुलना",
        "Total Earnings": "कुल कमाई",
        "Spoilage Assessor": "खराबी मूल्यांकन",
        "Storage Type": "भंडारण प्रकार",
        "Transit Duration (Hours)": "पारगमन अवधि (घंटे)",
        "Assess Spoilage Risk": "खराबी जोखिम का आकलन करें",
        "Spoilage Risk": "खराबी जोखिम",
        "Spoilage Probability": "संभावना",
        "Recommended Actions": "अनुशंसित कार्य",
        "Cost": "लागत",
        "Effectiveness": "प्रभावशीलता",
        "Full Input Summary": "पूर्ण इनपुट सारांश",
        "Harvest Window": "कटाई समय",
        "Select District": "जिला चुनें",
    },
    "mr": {
        "Select Crop": "पीक निवडा",
        "Sowing Date": "पेरणी तारीख",
        "Get Recommendation": "शिफारस मिळवा",
        "Best Harvest Window": "सर्वोत्तम कापणी वेळ",
        "Confidence": "विश्वास",
        "High": "उच्च", "Medium": "मध्यम", "Low": "कमी",
        "Mandi Ranker": "बाजार क्रमवारी",
        "Spoilage Assessor": "नासाडी मूल्यांकन",
        "Harvest Window": "कापणी वेळ",
        "Select District": "जिल्हा निवडा",
    },
}


def t(key: str, lang_code: str = "en") -> str:
    """Translate a key into the given language, fallback to English then key."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS["en"]).get(key, 
           TRANSLATIONS["en"].get(key, key))


def render_lang_sidebar() -> str:
    """Render language selector in sidebar and return language code."""
    opts = {"English": "en", "हिंदी": "hi", "मराठी": "mr"}
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "en"
    choice = st.radio(
        "🌐 भाषा / Language / भाषा",
        list(opts.keys()),
        index=list(opts.values()).index(st.session_state.lang_code)
              if st.session_state.lang_code in opts.values() else 0,
        key="lang_selector",
    )
    st.session_state.lang_code = opts[choice]
    return st.session_state.lang_code
