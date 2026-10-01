from flask import Flask, jsonify, request
from flask_cors import CORS
from recommandation import recommend_hostels
from models import (
    init_db,
    get_all_hostels,
    get_hostel_by_id,
    create_hostel,
    update_hostel,
    update_hostel_availability,
    create_booking,
    get_booking_by_id,
    get_all_bookings,
    update_booking_status,
    get_bookings_by_phone
)

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()


@app.route("/")
def home():
    return jsonify({
        "success": True,
        "message": "Chitral Hostel Finder API is running"
    })


@app.route("/api/health")
def health():
    return jsonify({
        "success": True,
        "status": "healthy"
    })


# GET ALL HOSTELS
@app.route("/api/hostels", methods=["GET"])
def hostels():

    data = get_all_hostels()

    return jsonify({
        "success": True,
        "count": len(data),
        "hostels": data
    })


# GET SINGLE HOSTEL
@app.route("/api/hostels/<int:hostel_id>", methods=["GET"])
def hostel_details(hostel_id):

    hostel = get_hostel_by_id(hostel_id)

    if not hostel:
        return jsonify({
            "success": False,
            "message": "Hostel not found"
        }), 404

    return jsonify({
        "success": True,
        "hostel": hostel
    })


# CREATE HOSTEL
@app.route("/api/hostels", methods=["POST"])
def add_hostel():

    data = request.get_json()

    required_fields = [
        "name",
        "location",
        "rent",
        "room_type",
        "facilities"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "success": False,
                "message": f"{field} is required"
            }), 400

    hostel_id = create_hostel(data)

    return jsonify({
        "success": True,
        "message": "Hostel created successfully",
        "hostel_id": hostel_id
    }), 201
@app.route("/api/recommend", methods=["POST"])
def recommend():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Preferences are required"
        }), 400

    if "budget" not in data:
        return jsonify({
            "success": False,
            "message": "Budget is required"
        }), 400

    preferences = {
        "budget": float(data["budget"]),
        "location": data.get("location", ""),
        "room_type": data.get("room_type", ""),
        "facilities": data.get("facilities", [])
    }

    hostels = get_all_hostels()

    recommendations = recommend_hostels(
        hostels,
        preferences
    )

    return jsonify({
        "success": True,
        "count": len(recommendations),
        "preferences": preferences,
        "recommendations": recommendations
    })
# ============================================================
# BOOKING API
# ============================================================

@app.route("/api/bookings", methods=["POST"])
def add_booking():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Booking data is required"
        }), 400

    required_fields = [
        "hostel_id",
        "applicant_name",
        "applicant_phone",
        "room_type",
        "move_in_date"
    ]

    for field in required_fields:

        if field not in data or not str(data[field]).strip():

            return jsonify({
                "success": False,
                "message": f"{field} is required"
            }), 400

    hostel = get_hostel_by_id(data["hostel_id"])

    if not hostel:

        return jsonify({
            "success": False,
            "message": "Hostel not found"
        }), 404

    if hostel["available_rooms"] <= 0:

        return jsonify({
            "success": False,
            "message": "No rooms are currently available"
        }), 400

    booking_id = create_booking(data)

    return jsonify({
        "success": True,
        "message": "Booking request submitted successfully",
        "booking_id": booking_id,
        "status": "Pending"
    }), 201


@app.route("/api/bookings/<int:booking_id>", methods=["GET"])
def booking_details(booking_id):

    booking = get_booking_by_id(booking_id)

    if not booking:

        return jsonify({
            "success": False,
            "message": "Booking not found"
        }), 404

    return jsonify({
        "success": True,
        "booking": booking
    })


@app.route("/api/bookings", methods=["GET"])
def bookings():

    data = get_all_bookings()

    return jsonify({
        "success": True,
        "count": len(data),
        "bookings": data
    })


@app.route("/api/bookings/<int:booking_id>/status", methods=["PUT"])
def change_booking_status(booking_id):

    data = request.get_json()

    if not data or "status" not in data:

        return jsonify({
            "success": False,
            "message": "Status is required"
        }), 400

    status = data["status"]

    allowed_statuses = [
        "Pending",
        "Accepted",
        "Rejected"
    ]

    if status not in allowed_statuses:

        return jsonify({
            "success": False,
            "message": "Invalid booking status"
        }), 400

    updated = update_booking_status(
        booking_id,
        status
    )

    if updated == 0:

        return jsonify({
            "success": False,
            "message": "Booking not found"
        }), 404

    return jsonify({
        "success": True,
        "message": "Booking status updated successfully",
        "booking_id": booking_id,
        "status": status
    })
@app.route("/api/my-bookings", methods=["GET"])
def my_bookings():

    phone = request.args.get("phone", "").strip()

    if not phone:

        return jsonify({
            "success": False,
            "message": "Phone number is required"
        }), 400

    bookings = get_bookings_by_phone(phone)

    return jsonify({
        "success": True,
        "count": len(bookings),
        "bookings": bookings
    })
@app.route("/api/hostels/<int:hostel_id>", methods=["PUT"])
def edit_hostel(hostel_id):
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Hostel data is required"
        }), 400

    required_fields = [
        "name",
        "location",
        "rent",
        "room_type",
        "facilities",
        "available_rooms"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "message": f"{field} is required"
            }), 400

    hostel = get_hostel_by_id(hostel_id)

    if not hostel:
        return jsonify({
            "success": False,
            "message": "Hostel not found"
        }), 404

    try:
        data["rent"] = int(data["rent"])
        data["available_rooms"] = int(data["available_rooms"])

        if data["rent"] < 0:
            return jsonify({
                "success": False,
                "message": "Rent cannot be negative"
            }), 400

        if data["available_rooms"] < 0:
            return jsonify({
                "success": False,
                "message": "Available rooms cannot be negative"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Rent and available rooms must be numbers"
        }), 400

    update_hostel(hostel_id, data)

    return jsonify({
        "success": True,
        "message": "Hostel listing updated successfully",
        "hostel": get_hostel_by_id(hostel_id)
    })
@app.route(
    "/api/hostels/<int:hostel_id>/availability",
    methods=["PUT"]
)
@app.route(
    "/api/hostels/<int:hostel_id>/availability",
    methods=["PUT"]
)
def update_availability(hostel_id):
    data = request.get_json()

    if not data or "available_rooms" not in data:
        return jsonify({
            "success": False,
            "message": "Available rooms is required"
        }), 400

    hostel = get_hostel_by_id(hostel_id)

    if not hostel:
        return jsonify({
            "success": False,
            "message": "Hostel not found"
        }), 404

    try:
        available_rooms = int(data["available_rooms"])

        if available_rooms < 0:
            return jsonify({
                "success": False,
                "message": "Available rooms cannot be negative"
            }), 400

    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "message": "Available rooms must be a number"
        }), 400

    update_hostel_availability(
        hostel_id,
        available_rooms
    )

    return jsonify({
        "success": True,
        "message": "Availability updated successfully",
        "hostel_id": hostel_id,
        "available_rooms": available_rooms
    })
    

if __name__ == "__main__":
    # app.run(debug=True, port=5000)
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )