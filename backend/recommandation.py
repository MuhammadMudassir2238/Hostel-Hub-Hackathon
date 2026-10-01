import os
import joblib
import pandas as pd


# ============================================================
# MODEL CONFIGURATION
# ============================================================

MODEL_FILE = "hostel_recommender.pkl"


# ============================================================
# LOAD TRAINED MODEL
# ============================================================

_model_package = None


def load_model():

    global _model_package

    if _model_package is not None:
        return _model_package

    if not os.path.exists(MODEL_FILE):
        raise FileNotFoundError(
            f"Trained model not found: {MODEL_FILE}"
        )

    _model_package = joblib.load(
        MODEL_FILE
    )

    return _model_package


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(value):

    return str(value).strip().lower()


# ============================================================
# FACILITY MATCH
# ============================================================

def facility_match(
    hostel_facilities,
    required_facility
):

    facilities = [
        item.strip().lower()
        for item in str(
            hostel_facilities
        ).split(",")
    ]

    return (
        normalize_text(required_facility)
        in facilities
    )


# ============================================================
# BUDGET SCORE
# ============================================================

def calculate_budget_score(
    hostel_rent,
    user_budget
):

    if user_budget <= 0:
        return 0

    difference = abs(
        hostel_rent -
        user_budget
    )

    score = 100 - (
        difference /
        user_budget
        * 100
    )

    return max(
        0,
        min(100, score)
    )


# ============================================================
# LOCATION SCORE
# ============================================================

def calculate_location_score(
    hostel_location,
    preferred_location
):

    if not preferred_location:
        return 50

    hostel_location = normalize_text(
        hostel_location
    )

    preferred_location = normalize_text(
        preferred_location
    )

    if (
        hostel_location ==
        preferred_location
    ):
        return 100

    if (
        preferred_location in hostel_location
        or
        hostel_location in preferred_location
    ):
        return 80

    if (
        "chitral" in hostel_location
        and
        "chitral" in preferred_location
    ):
        return 70

    return 30


# ============================================================
# ROOM TYPE SCORE
# ============================================================

def calculate_room_score(
    hostel_room_type,
    preferred_room_type
):

    if not preferred_room_type:
        return 100

    if (
        normalize_text(
            hostel_room_type
        )
        ==
        normalize_text(
            preferred_room_type
        )
    ):
        return 100

    return 0


# ============================================================
# FACILITY SCORE
# ============================================================

def calculate_facility_score(
    hostel,
    required_facilities
):

    if not required_facilities:
        return 100

    matched = 0

    for facility in required_facilities:

        if facility_match(
            hostel["facilities"],
            facility
        ):

            matched += 1

    return (
        matched /
        len(required_facilities)
    ) * 100


# ============================================================
# AVAILABILITY SCORE
# ============================================================

def calculate_availability_score(
    available_rooms
):

    if available_rooms <= 0:
        return 0

    if available_rooms == 1:
        return 60

    if available_rooms <= 3:
        return 80

    return 100


# ============================================================
# BUILD ML FEATURES
# ============================================================

def build_features(
    hostel,
    preferences
):

    user_budget = float(
        preferences["budget"]
    )

    hostel_rent = float(
        hostel["rent"]
    )

    preferred_location = preferences.get(
        "location",
        ""
    )

    preferred_room_type = preferences.get(
        "room_type",
        ""
    )

    required_facilities = preferences.get(
        "facilities",
        []
    )

    # --------------------------------------------------------
    # Individual scores
    # --------------------------------------------------------

    budget_score = calculate_budget_score(
        hostel_rent,
        user_budget
    )

    location_score = calculate_location_score(
        hostel["location"],
        preferred_location
    )

    room_score = calculate_room_score(
        hostel["room_type"],
        preferred_room_type
    )

    facility_score = calculate_facility_score(
        hostel,
        required_facilities
    )

    availability_score = (
        calculate_availability_score(
            hostel["available_rooms"]
        )
    )

    # --------------------------------------------------------
    # Additional features
    # --------------------------------------------------------

    rent_difference = abs(
        hostel_rent -
        user_budget
    )

    budget_ratio = (
        hostel_rent /
        user_budget
        if user_budget > 0
        else 1
    )

    # --------------------------------------------------------
    # Required facilities
    # --------------------------------------------------------

    wifi_required = int(
        "WiFi" in required_facilities
    )

    mess_required = int(
        "Mess" in required_facilities
    )

    heating_required = int(
        "Heating" in required_facilities
    )

    bathroom_required = int(
        "Attached Bathroom"
        in required_facilities
    )

    # --------------------------------------------------------
    # Hostel facilities
    # --------------------------------------------------------

    hostel_has_wifi = int(
        facility_match(
            hostel["facilities"],
            "WiFi"
        )
    )

    hostel_has_mess = int(
        facility_match(
            hostel["facilities"],
            "Mess"
        )
    )

    hostel_has_heating = int(
        facility_match(
            hostel["facilities"],
            "Heating"
        )
    )

    hostel_has_bathroom = int(
        facility_match(
            hostel["facilities"],
            "Attached Bathroom"
        )
    )

    # --------------------------------------------------------
    # Return exact feature order
    # --------------------------------------------------------

    return [
        user_budget,
        hostel_rent,
        rent_difference,
        budget_ratio,
        location_score,
        room_score,
        facility_score,
        availability_score,
        hostel["available_rooms"],
        wifi_required,
        mess_required,
        heating_required,
        bathroom_required,
        hostel_has_wifi,
        hostel_has_mess,
        hostel_has_heating,
        hostel_has_bathroom,
    ]


# ============================================================
# RECOMMENDATION LEVEL
# ============================================================

def get_recommendation_level(score):

    if score >= 85:
        return "Excellent Match"

    if score >= 70:
        return "Good Match"

    if score >= 50:
        return "Moderate Match"

    return "Low Match"


# ============================================================
# GENERATE EXPLANATION
# ============================================================

def generate_explanation(
    hostel,
    preferences,
    scores
):

    explanations = []

    if scores["budget"] >= 85:
        explanations.append(
            "Fits your budget very well"
        )

    elif scores["budget"] >= 65:
        explanations.append(
            "Close to your preferred budget"
        )

    if scores["location"] >= 90:
        explanations.append(
            "Located in your preferred area"
        )

    elif scores["location"] >= 70:
        explanations.append(
            "Located near your preferred area"
        )

    required_facilities = preferences.get(
        "facilities",
        []
    )

    if required_facilities:

        matched_facilities = []

        for facility in required_facilities:

            if facility_match(
                hostel["facilities"],
                facility
            ):
                matched_facilities.append(
                    facility
                )

        if matched_facilities:

            explanations.append(
                f"Matches {len(matched_facilities)} "
                f"of {len(required_facilities)} "
                f"requested facilities"
            )

    if scores["room_type"] >= 90:
        explanations.append(
            "Matches your preferred room type"
        )

    if hostel["available_rooms"] > 0:
        explanations.append(
            "Rooms are currently available"
        )

    else:
        explanations.append(
            "No rooms are currently available"
        )

    return explanations


# ============================================================
# MAIN ML RECOMMENDATION FUNCTION
# ============================================================

def recommend_hostels(
    hostels,
    preferences
):

    package = load_model()

    model = package["model"]

    results = []

    for hostel in hostels:

        features = build_features(
            hostel,
            preferences
        )

        feature_names = package["features"]

        feature_dataframe = pd.DataFrame(
            [features],
            columns=feature_names
        )
        ml_score = model.predict(
            feature_dataframe
        )[0]

        # ----------------------------------------------------
        # Hard availability rule
        # ----------------------------------------------------

        if hostel["available_rooms"] <= 0:
            ml_score *= 0.5

        # ----------------------------------------------------
        # Calculate explanation scores
        # ----------------------------------------------------

        budget_score = calculate_budget_score(
            hostel["rent"],
            preferences["budget"]
        )

        location_score = calculate_location_score(
            hostel["location"],
            preferences.get(
                "location",
                ""
            )
        )

        facility_score = calculate_facility_score(
            hostel,
            preferences.get(
                "facilities",
                []
            )
        )

        room_score = calculate_room_score(
            hostel["room_type"],
            preferences.get(
                "room_type",
                ""
            )
        )

        availability_score = (
            calculate_availability_score(
                hostel["available_rooms"]
            )
        )

        scores = {
            "budget": round(
                budget_score,
                2
            ),

            "location": round(
                location_score,
                2
            ),

            "facilities": round(
                facility_score,
                2
            ),

            "room_type": round(
                room_score,
                2
            ),

            "availability": round(
                availability_score,
                2
            )
        }

        result = hostel.copy()

        result["match_score"] = round(
            ml_score,
            2
        )

        result["recommendation_level"] = (
            get_recommendation_level(
                ml_score
            )
        )

        result["score_breakdown"] = scores

        result["why_recommended"] = (
            generate_explanation(
                hostel,
                preferences,
                scores
            )
        )

        results.append(
            result
        )

    # --------------------------------------------------------
    # Sort by ML prediction
    # --------------------------------------------------------

    results.sort(
        key=lambda item:
            item["match_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # Add ranking
    # --------------------------------------------------------

    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index

    return results