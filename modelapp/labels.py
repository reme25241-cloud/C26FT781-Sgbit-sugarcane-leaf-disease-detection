# modelapp\labels.py
LABEL_INFO = {
    "good sugarcane leaves": {
        "key": "healthy", "display": "Healthy", "severity": "none",
        "recommendation": "No signs of disease. Continue routine monitoring.",
    },
    "Smut Disease of Sugar Cane ": {
        "key": "smut", "display": "Smut Disease", "severity": "high",
        "recommendation": "Remove and burn infected clumps. Use disease-free setts and resistant varieties for next planting.",
    },
    "Sugar Cane Fungal Diseases": {
        "key": "fungal", "display": "Fungal Disease", "severity": "medium",
        "recommendation": "Apply an appropriate fungicide and improve field drainage to reduce humidity around the base.",
    },
    "Sugar Cane Grassy Shoot": {
        "key": "grassy_shoot", "display": "Grassy Shoot Disease", "severity": "high",
        "recommendation": "Rogue out and destroy infected stools immediately; this spreads via infected setts and leafhoppers.",
    },
    "Sugar Cane Mosaic": {
        "key": "mosaic", "display": "Mosaic Virus", "severity": "medium",
        "recommendation": "Control aphid vectors and use virus-free planting material.",
    },
    "Sugar Cane Rust": {
        "key": "rust", "display": "Rust", "severity": "medium",
        "recommendation": "Apply a protectant fungicide at first sign and avoid excess nitrogen fertilization.",
    },
    "Sugar Cane Scald disease": {
        "key": "scald", "display": "Leaf Scald", "severity": "high",
        "recommendation": "Remove infected plants, disinfect cutting tools between plants, and avoid waterlogging.",
    },
    "SugarCane Borer": {
        "key": "borer", "display": "Stem/Leaf Borer", "severity": "medium",
        "recommendation": "Deploy pheromone traps and release Trichogramma as biocontrol; consider targeted insecticide if severe.",
    },
    "SugarCane Pests": {
        "key": "pests", "display": "General Pest Damage", "severity": "low",
        "recommendation": "Inspect closely to identify the specific pest and treat accordingly.",
    },
    "SugarCane Red Rot": {
        "key": "red_rot", "display": "Red Rot", "severity": "high",
        "recommendation": "Uproot and destroy infected plants, avoid ratooning the field, and rotate with a non-host crop.",
    },
}

ALL_CLASS_KEYS = [v["key"] for v in LABEL_INFO.values()]

def get_label_info(raw_label: str):
    info = LABEL_INFO.get(raw_label)
    if info:
        return info
    return {"key": "unknown", "display": raw_label, "severity": "low", "recommendation": "No recommendation available."}