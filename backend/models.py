import sqlite3

DATABASE = "hostel.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS hostels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            rent INTEGER NOT NULL,
            room_type TEXT NOT NULL,
            facilities TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            available_rooms INTEGER DEFAULT 0,
            description TEXT,
            owner_name TEXT,
            owner_phone TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hostel_id INTEGER NOT NULL,

            applicant_name TEXT NOT NULL,
            applicant_phone TEXT NOT NULL,

            room_type TEXT NOT NULL,
            move_in_date TEXT NOT NULL,

            status TEXT DEFAULT 'Pending',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (hostel_id)
            REFERENCES hostels(id)
        )
    """)

    conn.commit()
    conn.close()


# ============================================================
# HOSTEL FUNCTIONS
# ============================================================

def get_all_hostels():
    conn = get_db_connection()

    hostels = conn.execute("""
        SELECT *
        FROM hostels
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(hostel) for hostel in hostels]


def get_hostel_by_id(hostel_id):
    conn = get_db_connection()

    hostel = conn.execute("""
        SELECT *
        FROM hostels
        WHERE id = ?
    """, (hostel_id,)).fetchone()

    conn.close()

    if hostel:
        return dict(hostel)

    return None


def create_hostel(data):
    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO hostels (
            name,
            location,
            rent,
            room_type,
            facilities,
            latitude,
            longitude,
            available_rooms,
            description,
            owner_name,
            owner_phone
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["location"],
        data["rent"],
        data["room_type"],
        data["facilities"],
        data.get("latitude"),
        data.get("longitude"),
        data.get("available_rooms", 0),
        data.get("description", ""),
        data.get("owner_name", ""),
        data.get("owner_phone", "")
    ))

    conn.commit()

    hostel_id = cursor.lastrowid

    conn.close()

    return hostel_id


# ============================================================
# BOOKING FUNCTIONS
# ============================================================

def create_booking(data):

    conn = get_db_connection()

    cursor = conn.execute("""
        INSERT INTO bookings (
            hostel_id,
            applicant_name,
            applicant_phone,
            room_type,
            move_in_date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["hostel_id"],
        data["applicant_name"],
        data["applicant_phone"],
        data["room_type"],
        data["move_in_date"],
        "Pending"
    ))

    conn.commit()

    booking_id = cursor.lastrowid

    conn.close()

    return booking_id


def get_booking_by_id(booking_id):

    conn = get_db_connection()

    booking = conn.execute("""
        SELECT
            bookings.*,
            hostels.name AS hostel_name,
            hostels.location AS hostel_location,
            hostels.rent AS hostel_rent,
            hostels.owner_name,
            hostels.owner_phone
        FROM bookings
        JOIN hostels
            ON bookings.hostel_id = hostels.id
        WHERE bookings.id = ?
    """, (booking_id,)).fetchone()
    

    conn.close()

    if booking:
        return dict(booking)

    return None


def get_all_bookings():

    conn = get_db_connection()

    bookings = conn.execute("""
        SELECT
            bookings.*,
            hostels.name AS hostel_name,
            hostels.location AS hostel_location,
            hostels.rent AS hostel_rent
        FROM bookings
        JOIN hostels
            ON bookings.hostel_id = hostels.id
        ORDER BY bookings.id DESC
    """).fetchall()

    conn.close()

    return [dict(booking) for booking in bookings]
def get_bookings_by_phone(phone):

    conn = get_db_connection()

    bookings = conn.execute("""
        SELECT
            bookings.*,
            hostels.name AS hostel_name,
            hostels.location AS hostel_location,
            hostels.rent AS hostel_rent,
            hostels.owner_name,
            hostels.owner_phone
        FROM bookings
        JOIN hostels
            ON bookings.hostel_id = hostels.id
        WHERE bookings.applicant_phone = ?
        ORDER BY bookings.id DESC
    """, (phone,)).fetchall()

    conn.close()

    return [dict(booking) for booking in bookings]


def update_booking_status(booking_id, status):

    conn = get_db_connection()

    cursor = conn.execute("""
        UPDATE bookings
        SET status = ?
        WHERE id = ?
    """, (
        status,
        booking_id
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated
def update_hostel(hostel_id, data):
    conn = get_db_connection()

    cursor = conn.execute("""
        UPDATE hostels
        SET
            name = ?,
            location = ?,
            rent = ?,
            room_type = ?,
            facilities = ?,
            available_rooms = ?,
            description = ?,
            owner_name = ?,
            owner_phone = ?
        WHERE id = ?
    """, (
        data["name"],
        data["location"],
        data["rent"],
        data["room_type"],
        data["facilities"],
        data["available_rooms"],
        data.get("description", ""),
        data.get("owner_name", ""),
        data.get("owner_phone", ""),
        hostel_id
    ))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated
def update_hostel(hostel_id, data):
    conn = get_db_connection()

    cursor = conn.execute("""
        UPDATE hostels
        SET
            name = ?,
            location = ?,
            rent = ?,
            room_type = ?,
            facilities = ?,
            available_rooms = ?,
            description = ?,
            owner_name = ?,
            owner_phone = ?
        WHERE id = ?
    """, (
        data["name"],
        data["location"],
        data["rent"],
        data["room_type"],
        data["facilities"],
        data["available_rooms"],
        data.get("description", ""),
        data.get("owner_name", ""),
        data.get("owner_phone", ""),
        hostel_id
    ))

    conn.commit()
    updated = cursor.rowcount
    conn.close()

    return updated
def update_hostel_availability(hostel_id, available_rooms):
    conn = get_db_connection()

    cursor = conn.execute("""
        UPDATE hostels
        SET available_rooms = ?
        WHERE id = ?
    """, (
        available_rooms,
        hostel_id
    ))

    conn.commit()

    updated = cursor.rowcount

    conn.close()

    return updated