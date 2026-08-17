from datetime import date

# Typical sugarcane crop cycle stages, as day ranges since planting.
# Total cycle assumed ~360 days for a standard plant crop; adjust for your region/variety.
GROWTH_STAGES = [
    {"key": "germination", "label": "Germination", "min_day": 0, "max_day": 35,
     "tip": "Ensure adequate soil moisture; check for gap filling where setts failed to sprout."},
    {"key": "tillering", "label": "Tillering", "min_day": 36, "max_day": 100,
     "tip": "Apply first split of nitrogen fertilizer; keep the field weed-free to support tiller formation."},
    {"key": "grand_growth", "label": "Grand Growth", "min_day": 101, "max_day": 270,
     "tip": "Peak water and nutrient demand; keep irrigation consistent and watch for borer/pest pressure."},
    {"key": "maturity", "label": "Maturity / Ripening", "min_day": 271, "max_day": 360,
     "tip": "Reduce irrigation and nitrogen to encourage sugar accumulation ahead of harvest."},
    {"key": "harvest_ready", "label": "Harvest Ready", "min_day": 361, "max_day": None,
     "tip": "Crop has passed the standard cycle length — plan harvest to avoid quality loss."},
]

TOTAL_CYCLE_DAYS = 360


def get_growth_stage(days_since_planting: int):
    for stage in GROWTH_STAGES:
        if days_since_planting >= stage["min_day"] and (stage["max_day"] is None or days_since_planting <= stage["max_day"]):
            return stage
    return GROWTH_STAGES[-1]


def compute_growth(planting_date: date, as_of: date = None):
    as_of = as_of or date.today()
    days = max((as_of - planting_date).days, 0)
    stage = get_growth_stage(days)
    progress_pct = min((days / TOTAL_CYCLE_DAYS) * 100, 100.0)

    return {
        "days_since_planting": days,
        "stage_key": stage["key"],
        "stage_label": stage["label"],
        "stage_tip": stage["tip"],
        "progress_pct": round(progress_pct, 1),
        "total_cycle_days": TOTAL_CYCLE_DAYS,
    }