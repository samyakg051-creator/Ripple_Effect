"""
AgriChain – modules/preservation.py
Suggests post-harvest preservation actions ranked by cost & effectiveness.
Directly addresses problem statement: "suggest preservation actions ranked by
cost and effectiveness".
"""

from dataclasses import dataclass
from typing import List


@dataclass
class PreservationAction:
    rank: int
    action: str           # Plain language action name
    action_hi: str        # Hindi
    cost_label: str       # e.g. "Free", "₹15–25/qtl"
    days_gained: int      # Additional shelf life days
    difficulty: str       # "Easy" | "Medium" | "Hard"
    tip: str              # One-line plain language tip
    tip_hi: str           # Hindi tip


# ── Master action library by crop ─────────────────────────────────────────────
_ACTIONS = {
    "Wheat": [
        PreservationAction(1, "Sun dry for 2–3 days", "2-3 दिन धूप में सुखाएं",
            "Free / मुफ्त", 30, "Easy",
            "Spread wheat on a clean surface in sunlight. Reduces moisture below 12%, preventing mold.",
            "गेहूं को धूप में फैलाएं। नमी कम होने से फफूंद नहीं लगती।"),
        PreservationAction(2, "Store in gunny/jute bags", "बोरी में भंडारण",
            "₹15–25/qtl", 60, "Easy",
            "Clean, dry jute bags in a cool, shaded room. Keep bags 30cm off floor and walls.",
            "साफ-सूखी बोरी में ठंडी जगह रखें। जमीन से 30 सेमी ऊपर रखें।"),
        PreservationAction(3, "Hermetic / PICS bags", "हर्मेटिक बैग (PICS)",
            "₹60–90/bag", 180, "Easy",
            "Airtight plastic bags suffocate insects without chemicals. One bag = 100 kg wheat.",
            "हवाबंद बैग से कीड़े मर जाते हैं, बिना दवा के। एक बैग में 100 किलो।"),
        PreservationAction(4, "Warehouse with fumigation", "धूमन सहित गोदाम",
            "₹30–50/qtl/month", 365, "Medium",
            "Govt/private warehouses fumigate with phosphine tablets. Get a warehouse receipt for loans.",
            "सरकारी/निजी गोदाम में फ्यूमिगेशन होती है। वेयरहाउस रसीद से लोन मिलता है।"),
        PreservationAction(5, "Cold storage", "शीत भंडारण",
            "₹80–120/qtl/month", 730, "Medium",
            "Best for long-term holding. Check e-NWR (National Warehouse Receipt) for financing options.",
            "लंबे समय के लिए सबसे अच्छा। e-NWR से कर्ज लेने की सुविधा।"),
    ],
    "Tomato": [
        PreservationAction(1, "Sort and remove damaged fruits", "खराब टमाटर अलग करें",
            "Free / मुफ्त", 3, "Easy",
            "One rotten tomato spreads ethylene gas that ripens all others. Remove immediately.",
            "एक सड़ा टमाटर बाकी सभी को जल्दी पकाता है। तुरंत हटाएं।"),
        PreservationAction(2, "Store at room temp, not refrigerated", "कमरे के तापमान पर रखें",
            "Free / मुफ्त", 5, "Easy",
            "Unripe tomatoes go 5–7 days at room temp. Cold kills flavour and damages texture.",
            "कच्चे टमाटर 5-7 दिन टिकते हैं। फ्रिज में स्वाद खराब हो जाता है।"),
        PreservationAction(3, "Cold room / pre-cooling (8–12°C)", "कोल्ड रूम (8-12°C)",
            "₹40–60/qtl/day", 21, "Medium",
            "Pre-cool within 4 hours of harvest to remove field heat. Doubles shelf life.",
            "कटाई के 4 घंटे के अंदर ठंडा करें। शेल्फ जीवन दोगुना हो जाता है।"),
        PreservationAction(4, "Controlled atmosphere storage", "नियंत्रित वातावरण गोदाम",
            "₹80–150/qtl/month", 45, "Hard",
            "Low oxygen, high CO₂ slows ripening. Best for bulk export-quality tomatoes.",
            "कम ऑक्सीजन से पकना धीमा होता है। निर्यात के लिए उपयुक्त।"),
    ],
    "Onion": [
        PreservationAction(1, "Cure in shade for 10–14 days", "छाया में 10-14 दिन सुखाएं",
            "Free / मुफ्त", 60, "Easy",
            "Hang onions in net bags or spread in single layer. Good air circulation prevents rot.",
            "जाली बोरी में लटकाएं या एक परत में रखें। हवा से सड़न नहीं होती।"),
        PreservationAction(2, "Ventilated bamboo/wire crates", "हवादार टोकरी / क्रेट",
            "₹20–40/qtl", 90, "Easy",
            "Never store in sealed bags. Onions need airflow. Stack crates with gaps between rows.",
            "बंद बोरी में कभी न रखें। ढेर के बीच हवा का रास्ता रखें।"),
        PreservationAction(3, "Cold storage (0–2°C, 65% humidity)", "शीत भंडारण 0-2°C",
            "₹50–80/qtl/month", 180, "Medium",
            "Government-subsidised cold storages available under NHB scheme. Check district horticulture office.",
            "NHB योजना के तहत सब्सिडी वाला शीत भंडारण उपलब्ध है।"),
    ],
    "Potato": [
        PreservationAction(1, "Cure at 15–20°C for 1 week", "एक हफ्ते 15-20°C पर रखें",
            "Free / मुफ्त", 14, "Easy",
            "Curing heals skin cuts and reduces rot. Dark room prevents greening (solanine).",
            "ठीक होने की प्रक्रिया से कटाव भरता है। अंधेरी जगह में हरापन नहीं आता।"),
        PreservationAction(2, "Store in dark, cool room (10–15°C)", "ठंडी-अंधेरी जगह रखें",
            "Free / मुफ्त", 30, "Easy",
            "Never store near onions — onion ethylene causes potatoes to sprout.",
            "प्याज के पास न रखें — प्याज से आलू में अंकुर जल्दी आते हैं।"),
        PreservationAction(3, "Cold storage (3–4°C)", "शीत भंडारण 3-4°C",
            "₹40–60/qtl/month", 180, "Medium",
            "Govt cold storages available in most districts. Recommended for holding beyond 30 days.",
            "अधिकांश जिलों में सरकारी शीत भंडारण उपलब्ध है।"),
        PreservationAction(4, "CIPC sprout inhibitor treatment", "अंकुरण रोधी उपचार",
            "₹8–12/qtl", 60, "Medium",
            "Approved chemical that delays sprouting. Apply before storage. Available at agri-input shops.",
            "अंकुरण रोकने की दवा। भंडारण से पहले लगाएं। कृषि दुकान पर मिलती है।"),
    ],
    "Rice": [
        PreservationAction(1, "Dry paddy to 12–14% moisture", "12-14% नमी तक सुखाएं",
            "Free / मुफ्त", 30, "Easy",
            "Sun dry on tarpaulin for 2–3 days. Bite test: grain should crack cleanly.",
            "तिरपाल पर 2-3 दिन धूप में सुखाएं। दांत से तोड़ने पर साफ टूटना चाहिए।"),
        PreservationAction(2, "Store in gunny bags on pallets", "पट्टों पर बोरी में भंडारण",
            "₹15–25/qtl", 60, "Easy",
            "Keep bags 30cm off floor, 50cm from walls. Stack max 10 bags high.",
            "जमीन से 30 सेमी, दीवार से 50 सेमी ऊपर। 10 बोरी तक ढेर लगाएं।"),
        PreservationAction(3, "Hermetic / PICS bags", "हर्मेटिक / PICS बैग",
            "₹60–90/bag", 180, "Easy",
            "Airtight bags kill stored-grain pests without chemicals. Ideal for small farmers.",
            "हवाबंद बैग कीड़ों को बिना दवा मार देते हैं। छोटे किसानों के लिए आदर्श।"),
        PreservationAction(4, "Warehouse with fumigation", "धूमन सहित गोदाम",
            "₹30–50/qtl/month", 365, "Medium",
            "Registered warehouse gives e-NWR receipt — use for pledge loan from bank.",
            "रजिस्टर्ड गोदाम से e-NWR रसीद — बैंक से प्लेज लोन लें।"),
        PreservationAction(5, "Rice mill cold storage", "चावल मिल शीत भंडारण",
            "₹60–100/qtl/month", 730, "Medium",
            "Some rice mills offer cold storage along with milling. Ask about milling + storage package.",
            "कुछ राइस मिल मिलिंग के साथ ठंडा भंडारण देती हैं। पैकेज पूछें।"),
    ],
}

_DEFAULT = [
    PreservationAction(1, "Dry before storage", "भंडारण से पहले सुखाएं",
        "Free / मुफ्त", 30, "Easy",
        "Always remove excess moisture before storing any crop.",
        "भंडारण से पहले हमेशा अतिरिक्त नमी हटाएं।"),
    PreservationAction(2, "Covered shed storage", "ढके हुए शेड में रखें",
        "₹20–40/qtl", 60, "Easy",
        "Keep crop off the floor on wooden pallets or boards.",
        "फसल को लकड़ी के पट्टों पर जमीन से ऊपर रखें।"),
    PreservationAction(3, "Cold storage", "शीत भंडारण",
        "₹50–100/qtl/month", 180, "Medium",
        "Best long-term solution. Available in most districts.",
        "सबसे अच्छा दीर्घकालिक समाधान। अधिकांश जिलों में उपलब्ध।"),
]


def get_preservation_actions(crop: str) -> List[PreservationAction]:
    """Return ranked preservation actions for a given crop."""
    return _ACTIONS.get(crop, _DEFAULT)
