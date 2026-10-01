import csv
import random
from models import init_db, get_all_hostels


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_FILE = "training_data.csv"

NUM_SAMPLES = 5000

LOCATIONS = [
    "Chitral Town",
    "University Road",
    "Drosh",
    "Booni",
    "Koghazi",
    "Garum Chashma",
    "Lowari",
    "Torkhow",
]

ROOM_TYPES = [
    "Shared",
    "Single",
    "Double",
]

FACILITIES = [
    "WiFi",
    "Mess",
    "Heating",
    "Attached Bathroom",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(value):
    return str(value).strip().lower()


def facility_match(hostel_facilities, required_facility):
    hostel_facilities = [
        item.strip().lower()
        for item in hostel_facilities.split(",")
    ]

    return (
        normalize_text(required_facility)
        in hostel_facilities
    )


def calculate_budget_score(hostel_rent, user_budget):
    if user_budget <= 0:
        return 0

    difference = abs(
        hostel_rent - user_budget
    )

    relative_difference = (
        difference / user_budget
    )

    score = 100 - (
        relative_difference * 100
    )

    return max(
        0,
        min(100, score)
    )


def calculate_location_score(
    hostel_location,
    preferred_location
):
    hostel_location = normalize_text(
        hostel_location
    )

    preferred_location = normalize_text(
        preferred_location
    )

    if hostel_location == preferred_location:
        return 100

    if (
        preferred_location in hostel_location
        or hostel_location in preferred_location
    ):
        return 80

    if (
        "chitral" in hostel_location
        and "chitral" in preferred_location
    ):
        return 70

    return 30


def calculate_room_score(
    hostel_room_type,
    preferred_room_type
):
    if (
        normalize_text(hostel_room_type)
        ==
        normalize_text(preferred_room_type)
    ):
        return 100

    return 0


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
# GENERATE ONE USER-HOSTEL SAMPLE
# ============================================================

def generate_sample(hostel):

    # --------------------------------------------------------
    # Generate user preferences
    # --------------------------------------------------------

    user_budget = random.randint(
        5000,
        15000
    )

    preferred_location = random.choice(
        LOCATIONS
    )

    preferred_room_type = random.choice(
        ROOM_TYPES
    )

    required_facilities = random.sample(
        FACILITIES,
        random.randint(0, 4)
    )

    # --------------------------------------------------------
    # Calculate individual feature scores
    # --------------------------------------------------------

    budget_score = calculate_budget_score(
        hostel["rent"],
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

    availability_score = calculate_availability_score(
        hostel["available_rooms"]
    )

    # --------------------------------------------------------
    # Additional numerical features
    # --------------------------------------------------------

    rent_difference = abs(
        hostel["rent"] -
        user_budget
    )

    budget_ratio = (
        hostel["rent"] /
        user_budget
        if user_budget > 0
        else 1
    )

    # --------------------------------------------------------
    # Generate target score
    #
    # This is used to create training labels.
    # --------------------------------------------------------

    target_score = (
        budget_score * 0.30
        +
        location_score * 0.20
        +
        facility_score * 0.20
        +
        room_score * 0.15
        +
        availability_score * 0.15
    )

    # --------------------------------------------------------
    # Add small controlled noise
    #
    # This prevents every sample from following
    # exactly the same mathematical equation.
    # --------------------------------------------------------

    noise = random.uniform(
        -3,
        3
    )

    target_score += noise

    target_score = max(
        0,
        min(100, target_score)
    )

    # --------------------------------------------------------
    # Return ML training row
    # --------------------------------------------------------

    return {
        "user_budget": user_budget,

        "hostel_rent": hostel["rent"],

        "rent_difference": rent_difference,

        "budget_ratio": round(
            budget_ratio,
            4
        ),

        "location_score": round(
            location_score,
            2
        ),

        "room_score": round(
            room_score,
            2
        ),

        "facility_score": round(
            facility_score,
            2
        ),

        "availability_score": round(
            availability_score,
            2
        ),

        "available_rooms":
            hostel["available_rooms"],

        "wifi_required":
            int(
                "WiFi" in required_facilities
            ),

        "mess_required":
            int(
                "Mess" in required_facilities
            ),

        "heating_required":
            int(
                "Heating" in required_facilities
            ),

        "bathroom_required":
            int(
                "Attached Bathroom"
                in required_facilities
            ),

        "hostel_has_wifi":
            int(
                facility_match(
                    hostel["facilities"],
                    "WiFi"
                )
            ),

        "hostel_has_mess":
            int(
                facility_match(
                    hostel["facilities"],
                    "Mess"
                )
            ),

        "hostel_has_heating":
            int(
                facility_match(
                    hostel["facilities"],
                    "Heating"
                )
            ),

        "hostel_has_bathroom":
            int(
                facility_match(
                    hostel["facilities"],
                    "Attached Bathroom"
                )
            ),

        "target_score":
            round(
                target_score,
                2
            ),
    }


# ============================================================
# MAIN DATA GENERATION
# ============================================================

def main():

    print("=" * 60)
    print("HOSTEL RECOMMENDATION DATASET GENERATOR")
    print("=" * 60)

    # Initialize database
    init_db()

    # Load hostel records
    hostels = get_all_hostels()

    if not hostels:
        print(
            "ERROR: No hostels found in database."
        )

        print(
            "Run seed.py first."
        )

        return

    print(
        f"Hostels loaded: {len(hostels)}"
    )

    print(
        f"Generating samples: {NUM_SAMPLES}"
    )

    training_rows = []

    # --------------------------------------------------------
    # Generate samples
    # --------------------------------------------------------

    for _ in range(NUM_SAMPLES):

        hostel = random.choice(
            hostels
        )

        sample = generate_sample(
            hostel
        )

        training_rows.append(
            sample
        )

    # --------------------------------------------------------
    # CSV columns
    # --------------------------------------------------------

    fieldnames = [
        "user_budget",
        "hostel_rent",
        "rent_difference",
        "budget_ratio",
        "location_score",
        "room_score",
        "facility_score",
        "availability_score",
        "available_rooms",
        "wifi_required",
        "mess_required",
        "heating_required",
        "bathroom_required",
        "hostel_has_wifi",
        "hostel_has_mess",
        "hostel_has_heating",
        "hostel_has_bathroom",
        "target_score",
    ]

    # --------------------------------------------------------
    # Write CSV
    # --------------------------------------------------------

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            training_rows
        )

    # --------------------------------------------------------
    # Dataset summary
    # --------------------------------------------------------

    scores = [
        row["target_score"]
        for row in training_rows
    ]

    print()
    print("=" * 60)
    print("DATASET GENERATED SUCCESSFULLY")
    print("=" * 60)

    print(
        f"Total samples : {len(training_rows)}"
    )

    print(
        f"Total features: {len(fieldnames) - 1}"
    )

    print(
        f"Minimum score : {min(scores)}"
    )

    print(
        f"Maximum score : {max(scores)}"
    )

    print(
        f"Output file   : {OUTPUT_FILE}"
    )

    print()
    print("First 5 samples:")
    print("-" * 60)

    for row in training_rows[:5]:
        print(row)

    print()
    print("Dataset generation complete.")


if __name__ == "__main__":
    main()