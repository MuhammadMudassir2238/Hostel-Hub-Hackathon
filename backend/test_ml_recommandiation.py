import joblib
import pandas as pd

from models import init_db, get_all_hostels
from recommandation import recommend_hostels


# ============================================================
# TEST CONFIGURATION
# ============================================================

MODEL_FILE = "hostel_recommender.pkl"


# ============================================================
# INITIALIZE
# ============================================================

print("=" * 70)
print("ML HOSTEL RECOMMENDATION VALIDATION")
print("=" * 70)

init_db()


# ============================================================
# LOAD MODEL
# ============================================================

print()
print("Loading trained model...")

package = joblib.load(
    MODEL_FILE
)

model = package["model"]
features = package["features"]

print("Model loaded successfully.")

print(
    f"Model type: {type(model).__name__}"
)

print(
    f"Features: {len(features)}"
)


# ============================================================
# TEST 1 — MODEL DIRECT PREDICTION
# ============================================================

print()
print("=" * 70)
print("TEST 1 — DIRECT MODEL PREDICTION")
print("=" * 70)


test_features = pd.DataFrame(
    [[
        10000,   # user_budget
        10000,   # hostel_rent
        0,       # rent_difference
        1.0,     # budget_ratio
        100,     # location_score
        100,     # room_score
        100,     # facility_score
        100,     # availability_score
        5,       # available_rooms
        1,       # wifi_required
        1,       # mess_required
        1,       # heating_required
        0,       # bathroom_required
        1,       # hostel_has_wifi
        1,       # hostel_has_mess
        1,       # hostel_has_heating
        0        # hostel_has_bathroom
    ]],
    columns=features
)


prediction = model.predict(
    test_features
)[0]


print(
    f"Predicted match score: {prediction:.2f}"
)


if 0 <= prediction <= 100:

    print(
        "TEST 1: PASS"
    )

else:

    print(
        "TEST 1: FAIL"
    )


# ============================================================
# LOAD HOSTELS
# ============================================================

hostels = get_all_hostels()

print()
print(
    f"Hostels available for testing: {len(hostels)}"
)


# ============================================================
# TEST 2 — RECOMMENDATION ENGINE
# ============================================================

print()
print("=" * 70)
print("TEST 2 — RECOMMENDATION ENGINE")
print("=" * 70)


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


recommendations = recommend_hostels(
    hostels,
    preferences
)


print()
print("TOP 5 RECOMMENDATIONS")
print("-" * 70)


for recommendation in recommendations[:5]:

    print(
        f"{recommendation['rank']}. "
        f"{recommendation['name']}"
    )

    print(
        f"   Rent: Rs. "
        f"{recommendation['rent']}"
    )

    print(
        f"   Room: "
        f"{recommendation['room_type']}"
    )

    print(
        f"   Score: "
        f"{recommendation['match_score']}"
    )

    print(
        f"   Level: "
        f"{recommendation['recommendation_level']}"
    )

    print(
        f"   Why: "
        f"{', '.join(recommendation['why_recommended'])}"
    )

    print()


# ============================================================
# VALIDATE RESULTS
# ============================================================

all_scores_valid = all(
    0 <= item["match_score"] <= 100
    for item in recommendations
)

ranking_valid = all(
    recommendations[i]["match_score"]
    >=
    recommendations[i + 1]["match_score"]
    for i in range(
        len(recommendations) - 1
    )
)


if all_scores_valid:

    print(
        "Score range test: PASS"
    )

else:

    print(
        "Score range test: FAIL"
    )


if ranking_valid:

    print(
        "Ranking order test: PASS"
    )

else:

    print(
        "Ranking order test: FAIL"
    )


# ============================================================
# TEST 3 — DIFFERENT USER PREFERENCES
# ============================================================

print()
print("=" * 70)
print("TEST 3 — PERSONALIZATION TEST")
print("=" * 70)


preferences_2 = {
    "budget": 7000,
    "location": "Drosh",
    "room_type": "Single",
    "facilities": [
        "WiFi"
    ]
}


recommendations_2 = recommend_hostels(
    hostels,
    preferences_2
)


print()
print("USER PROFILE 1")
print("-" * 70)

for item in recommendations[:3]:

    print(
        f"{item['name']} "
        f"-> {item['match_score']}"
    )


print()
print("USER PROFILE 2")
print("-" * 70)

for item in recommendations_2[:3]:

    print(
        f"{item['name']} "
        f"-> {item['match_score']}"
    )


# Check whether rankings differ

ranking_1 = [
    item["id"]
    for item in recommendations[:5]
]

ranking_2 = [
    item["id"]
    for item in recommendations_2[:5]
]


if ranking_1 != ranking_2:

    print()
    print(
        "Personalization test: PASS"
    )

else:

    print()
    print(
        "Personalization test: WARNING"
    )

    print(
        "Both profiles produced the same "
        "top-5 ranking."
    )


# ============================================================
# TEST 4 — EXPLAINABILITY
# ============================================================

print()
print("=" * 70)
print("TEST 4 — EXPLAINABILITY")
print("=" * 70)


first = recommendations[0]


required_fields = [
    "match_score",
    "recommendation_level",
    "score_breakdown",
    "why_recommended",
    "rank"
]


missing_fields = [
    field
    for field in required_fields
    if field not in first
]


if not missing_fields:

    print(
        "Explainability fields: PASS"
    )

    print()
    print(
        "Score Breakdown:"
    )

    print(
        first["score_breakdown"]
    )

    print()
    print(
        "Why Recommended:"
    )

    for reason in first[
        "why_recommended"
    ]:

        print(
            f"- {reason}"
        )

else:

    print(
        "Explainability fields: FAIL"
    )

    print(
        f"Missing: {missing_fields}"
    )


# ============================================================
# FINAL RESULT
# ============================================================

print()
print("=" * 70)
print("ML VALIDATION COMPLETE")
print("=" * 70)

if (
    all_scores_valid
    and ranking_valid
    and not missing_fields
):

    print(
        "CORE ML TESTS: PASS"
    )

else:

    print(
        "CORE ML TESTS: CHECK REQUIRED"
    )

print("=" * 70)