import joblib
import pandas as pd

from models import init_db, get_all_hostels
from recommandation import (
    calculate_budget_score,
    calculate_location_score,
    calculate_room_score,
    calculate_facility_score,
    calculate_availability_score,
    build_features,
)


MODEL_FILE = "hostel_recommender.pkl"


# ============================================================
# RULE-BASED BASELINE
# ============================================================
def rule_based_score(hostel, preferences):
    budget_score = calculate_budget_score(
        hostel["rent"],
        preferences["budget"]
    )

    location_score = calculate_location_score(
        hostel,
        preferences["location"]
    )

    facility_score = calculate_facility_score(
        hostel,
        preferences["facilities"]
    )

    room_score = calculate_room_score(
        hostel,
        preferences["room_type"]
    )

    availability_score = calculate_availability_score(
        hostel["available_rooms"]
    )

    score = (
        budget_score * 0.30
        + location_score * 0.20
        + facility_score * 0.20
        + room_score * 0.15
        + availability_score * 0.15
    )

    return round(score, 2)


def get_rule_based_recommendations(
    hostels,
    preferences
):
    results = []

    for hostel in hostels:

        score = rule_based_score(
            hostel,
            preferences
        )

        results.append({
            "id": hostel["id"],
            "name": hostel["name"],
            "rent": hostel["rent"],
            "room_type": hostel["room_type"],
            "score": score
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    for index, item in enumerate(
        results,
        start=1
    ):
        item["rank"] = index

    return results


# ============================================================
# ML RECOMMENDATIONS
# ============================================================

def get_ml_recommendations(
    hostels,
    preferences,
    model_package
):
    model = model_package["model"]
    feature_names = model_package["features"]

    results = []

    for hostel in hostels:

        features = build_features(
            hostel,
            preferences
        )

        feature_dataframe = pd.DataFrame(
            [features],
            columns=feature_names
        )

        score = model.predict(
            feature_dataframe
        )[0]

        score = max(
            0,
            min(
                100,
                score
            )
        )

        results.append({
            "id": hostel["id"],
            "name": hostel["name"],
            "rent": hostel["rent"],
            "room_type": hostel["room_type"],
            "score": round(score, 2)
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    for index, item in enumerate(
        results,
        start=1
    ):
        item["rank"] = index

    return results


# ============================================================
# RANKING COMPARISON
# ============================================================

def compare_rankings(
    rule_results,
    ml_results
):

    rule_positions = {
        item["id"]: item["rank"]
        for item in rule_results
    }

    ml_positions = {
        item["id"]: item["rank"]
        for item in ml_results
    }

    comparison = []

    for item in ml_results:

        hostel_id = item["id"]

        comparison.append({
            "id": hostel_id,
            "name": item["name"],
            "rule_rank": rule_positions[
                hostel_id
            ],
            "ml_rank": ml_positions[
                hostel_id
            ],
            "rank_difference":
                rule_positions[hostel_id]
                -
                ml_positions[hostel_id]
        })

    return comparison


# ============================================================
# MAIN
# ============================================================

print("=" * 75)
print("RULE-BASED vs ML RECOMMENDATION COMPARISON")
print("=" * 75)


# ------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------

init_db()

hostels = get_all_hostels()

print()
print(
    f"Hostels available: {len(hostels)}"
)


# ------------------------------------------------------------
# LOAD MODEL
# ------------------------------------------------------------

print()
print("Loading trained ML model...")

package = joblib.load(
    MODEL_FILE
)

print(
    f"Model: "
    f"{type(package['model']).__name__}"
)

print(
    f"Features: "
    f"{len(package['features'])}"
)


# ------------------------------------------------------------
# TEST USER
# ------------------------------------------------------------

preferences = {
    "budget": 10000,
    "location": "Chitral Town",
    "room_type": "Shared",
    "facilities": [
        "WiFi",
        "Mess",
        "Heating"
    ]
}


print()
print("=" * 75)
print("USER PREFERENCES")
print("=" * 75)

print(
    f"Budget     : Rs. "
    f"{preferences['budget']}"
)

print(
    f"Location   : "
    f"{preferences['location']}"
)

print(
    f"Room Type  : "
    f"{preferences['room_type']}"
)

print(
    f"Facilities : "
    f"{', '.join(preferences['facilities'])}"
)


# ------------------------------------------------------------
# RUN BOTH SYSTEMS
# ------------------------------------------------------------

rule_results = get_rule_based_recommendations(
    hostels,
    preferences
)

ml_results = get_ml_recommendations(
    hostels,
    preferences,
    package
)


# ------------------------------------------------------------
# RULE-BASED TOP 5
# ------------------------------------------------------------

print()
print("=" * 75)
print("RULE-BASED TOP 5")
print("=" * 75)

for item in rule_results[:5]:

    print(
        f"{item['rank']}. "
        f"{item['name']}"
    )

    print(
        f"   Score: "
        f"{item['score']}"
    )

    print(
        f"   Rent: Rs. "
        f"{item['rent']}"
    )

    print(
        f"   Room: "
        f"{item['room_type']}"
    )


# ------------------------------------------------------------
# ML TOP 5
# ------------------------------------------------------------

print()
print("=" * 75)
print("ML TOP 5")
print("=" * 75)

for item in ml_results[:5]:

    print(
        f"{item['rank']}. "
        f"{item['name']}"
    )

    print(
        f"   Score: "
        f"{item['score']}"
    )

    print(
        f"   Rent: Rs. "
        f"{item['rent']}"
    )

    print(
        f"   Room: "
        f"{item['room_type']}"
    )


# ------------------------------------------------------------
# RANKING COMPARISON
# ------------------------------------------------------------

comparison = compare_rankings(
    rule_results,
    ml_results
)


print()
print("=" * 75)
print("RANKING COMPARISON")
print("=" * 75)

print(
    f"{'Hostel':35}"
    f"{'Rule':>8}"
    f"{'ML':>8}"
    f"{'Change':>10}"
)

print("-" * 75)

for item in comparison:

    print(
        f"{item['name'][:34]:35}"
        f"{item['rule_rank']:>8}"
        f"{item['ml_rank']:>8}"
        f"{item['rank_difference']:>10}"
    )


# ------------------------------------------------------------
# TOP-5 OVERLAP
# ------------------------------------------------------------

rule_top5 = {
    item["id"]
    for item in rule_results[:5]
}

ml_top5 = {
    item["id"]
    for item in ml_results[:5]
}

overlap = rule_top5.intersection(
    ml_top5
)

overlap_percentage = (
    len(overlap) / 5
) * 100


print()
print("=" * 75)
print("TOP-5 RANKING OVERLAP")
print("=" * 75)

print(
    f"Common hostels: "
    f"{len(overlap)} / 5"
)

print(
    f"Overlap: "
    f"{overlap_percentage:.1f}%"
)


# ------------------------------------------------------------
# SCORE CORRELATION
# ------------------------------------------------------------

rule_scores = {
    item["id"]: item["score"]
    for item in rule_results
}

ml_scores = {
    item["id"]: item["score"]
    for item in ml_results
}

score_dataframe = pd.DataFrame({
    "rule_score": [
        rule_scores[item["id"]]
        for item in ml_results
    ],
    "ml_score": [
        ml_scores[item["id"]]
        for item in ml_results
    ]
})

correlation = (
    score_dataframe[
        "rule_score"
    ].corr(
        score_dataframe[
            "ml_score"
        ]
    )
)


print()
print("=" * 75)
print("SCORE CORRELATION")
print("=" * 75)

print(
    f"Pearson correlation: "
    f"{correlation:.4f}"
)


# ------------------------------------------------------------
# FINAL
# ------------------------------------------------------------

print()
print("=" * 75)
print("COMPARISON COMPLETE")
print("=" * 75)

print()
print("The comparison shows:")
print("- Rule-based weighted scoring")
print("- Trained Random Forest recommendation")
print("- Ranking differences")
print("- Top-5 overlap")
print("- Score correlation")

print()
print("=" * 75)

