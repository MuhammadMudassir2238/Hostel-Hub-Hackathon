from models import get_all_hostels
from recommandation import recommend_hostels


def run_test():

    hostels = get_all_hostels()

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

    results = recommend_hostels(
        hostels,
        preferences
    )

    print("\n==============================")
    print("RECOMMENDATION TEST")
    print("==============================")

    print(f"Total hostels tested: {len(results)}")

    assert len(results) == 20

    for result in results:

        assert 0 <= result["match_score"] <= 100

    scores = [
        result["match_score"]
        for result in results
    ]

    assert scores == sorted(
        scores,
        reverse=True
    )

    print("Ranking order: PASS")
    print("Score range: PASS")

    print("\nTOP 5 RECOMMENDATIONS")
    print("------------------------------")

    for index, hostel in enumerate(results[:5], 1):

        print(
            f"{index}. "
            f"{hostel['name']} | "
            f"Rs.{hostel['rent']} | "
            f"{hostel['room_type']} | "
            f"Score: {hostel['match_score']}"
        )

    print("\nALL TESTS PASSED")


if __name__ == "__main__":
    run_test()