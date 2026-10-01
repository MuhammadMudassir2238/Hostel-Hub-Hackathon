from models import get_db_connection, init_db


hostels = [
    {
        "name": "Chitral Palace Hostel",
        "location": "Chitral Town",
        "rent": 10000,
        "room_type": "Shared",
        "facilities": "WiFi,Mess,Heating,Attached Bathroom",
        "latitude": 35.8518,
        "longitude": 71.7864,
        "available_rooms": 8,
        "description": "Affordable hostel near educational institutions.",
        "owner_name": "Ahmad Khan",
        "owner_phone": "03001234567"
    },
    {
        "name": "Hindukush Student Hostel",
        "location": "Chitral Town",
        "rent": 8500,
        "room_type": "Shared",
        "facilities": "WiFi,Mess,Heating",
        "latitude": 35.8542,
        "longitude": 71.7891,
        "available_rooms": 12,
        "description": "Student-friendly hostel with shared rooms.",
        "owner_name": "Sajid Ali",
        "owner_phone": "03011234567"
    },
    {
        "name": "Chitral View Hostel",
        "location": "Chitral Town",
        "rent": 12000,
        "room_type": "Single",
        "facilities": "WiFi,Mess,Heating,Attached Bathroom",
        "latitude": 35.8489,
        "longitude": 71.7832,
        "available_rooms": 5,
        "description": "Comfortable hostel with mountain views.",
        "owner_name": "Naveed Hussain",
        "owner_phone": "03121234567"
    },
    {
        "name": "Khowar Boys Hostel",
        "location": "Chitral Town",
        "rent": 7500,
        "room_type": "Shared",
        "facilities": "Mess,Heating",
        "latitude": 35.8561,
        "longitude": 71.7819,
        "available_rooms": 15,
        "description": "Budget accommodation for students.",
        "owner_name": "Fazal Karim",
        "owner_phone": "03211234567"
    },
    {
        "name": "University Road Hostel",
        "location": "University Road",
        "rent": 11000,
        "room_type": "Shared",
        "facilities": "WiFi,Mess,Heating,Attached Bathroom",
        "latitude": 35.8458,
        "longitude": 71.7972,
        "available_rooms": 10,
        "description": "Located close to University Road.",
        "owner_name": "Usman Khan",
        "owner_phone": "03331234567"
    },
    {
        "name": "Chitral Student Residence",
        "location": "University Road",
        "rent": 9500,
        "room_type": "Shared",
        "facilities": "WiFi,Mess",
        "latitude": 35.8441,
        "longitude": 71.8001,
        "available_rooms": 9,
        "description": "Affordable student accommodation.",
        "owner_name": "Bilal Ahmad",
        "owner_phone": "03451234567"
    },
    {
        "name": "Royal Chitral Hostel",
        "location": "Gol Market",
        "rent": 14000,
        "room_type": "Single",
        "facilities": "WiFi,Mess,Heating,Attached Bathroom",
        "latitude": 35.8502,
        "longitude": 71.7925,
        "available_rooms": 4,
        "description": "Premium single-room accommodation.",
        "owner_name": "Rashid Khan",
        "owner_phone": "03041234567"
    },
    {
        "name": "Mountain Boys Hostel",
        "location": "Gol Market",
        "rent": 9000,
        "room_type": "Shared",
        "facilities": "WiFi,Heating",
        "latitude": 35.8521,
        "longitude": 71.7943,
        "available_rooms": 11,
        "description": "Comfortable shared accommodation.",
        "owner_name": "Shahid Ahmad",
        "owner_phone": "03141234567"
    },
    {
        "name": "Drosh Student Hostel",
        "location": "Drosh",
        "rent": 7000,
        "room_type": "Shared",
        "facilities": "WiFi,Mess,Heating",
        "latitude": 35.5612,
        "longitude": 71.7898,
        "available_rooms": 14,
        "description": "Affordable hostel in Drosh.",
        "owner_name": "Javed Khan",
        "owner_phone": "03221234567"
    },
    {
        "name": "Drosh Comfort Residence",
        "location": "Drosh",
        "rent": 10500,
        "room_type": "Single",
        "facilities": "WiFi,Mess,Attached Bathroom",
        "latitude": 35.5598,
        "longitude": 71.7921,
        "available_rooms": 6,
        "description": "Private rooms with basic facilities.",
        "owner_name": "Irfan Ali",
        "owner_phone": "03341234567"
    },
    {
        "name": "Booni Student Lodge",
        "location": "Booni",
        "rent": 8000,
        "room_type": "Shared",
        "facilities": "WiFi,Mess,Heating",
        "latitude": 36.2532,
        "longitude": 72.2651,
        "available_rooms": 13,
        "description": "Student accommodation in Booni.",
        "owner_name": "Sher Alam",
        "owner_phone": "03461234567"
    },
    {
        "name": "Booni Valley Hostel",
        "location": "Booni",
        "rent": 11500,
        "room_type": "Single",
        "facilities": "WiFi,Heating,Attached Bathroom",
        "latitude": 36.2551,
        "longitude": 72.2682,
        "available_rooms": 5,
        "description": "Quiet private accommodation.",
        "owner_name": "Nasir Hussain",
        "owner_phone": "03051234567"
    },
    {
        "name": "Chitral Central Hostel",
        "location": "Chitral Town",
        "rent": 10000,
        "room_type": "Single",
        "facilities": "WiFi,Mess,Heating",
        "latitude": 35.8491,
        "longitude": 71.7887,
        "available_rooms": 7,
        "description": "Central hostel with easy access.",
        "owner_name": "Zia Ullah",
        "owner_phone": "03151234567"
    },
    {
        "name": "Lowari Student Hostel",
        "location": "Chitral Town",
        "rent": 6500,
        "room_type": "Shared",
        "facilities": "Mess,Heating",
        "latitude": 35.8572,
        "longitude": 71.7902,
        "available_rooms": 16,
        "description": "Low-cost shared accommodation.",
        "owner_name": "Wali Muhammad",
        "owner_phone": "03251234567"
    },
    {
        "name": "Hindukush View Residence",
        "location": "Chitral Town",
        "rent": 13000,
        "room_type": "Single",
        "facilities": "WiFi,Mess,Heating,Attached Bathroom",
        "latitude": 35.8468,
        "longitude": 71.7841,
        "available_rooms": 3,
        "description": "Premium accommodation with scenic views.",
        "owner_name": "Aftab Ahmad",
        "owner_phone": "03351234567"
    },
    {
        "name": "Shandur Hostel",
        "location": "Chitral Town",
        "rent": 9000,
        "room_type": "Shared",
        "facilities": "WiFi,Mess,Heating",
        "latitude": 35.8533,
        "longitude": 71.7872,
        "available_rooms": 10,
        "description": "Popular student accommodation.",
        "owner_name": "Arif Khan",
        "owner_phone": "03471234567"
    },
    {
        "name": "Koghazi Hostel",
        "location": "Koghazi",
        "rent": 8500,
        "room_type": "Shared",
        "facilities": "WiFi,Mess",
        "latitude": 35.8051,
        "longitude": 71.8702,
        "available_rooms": 8,
        "description": "Budget accommodation near Koghazi.",
        "owner_name": "Hamid Khan",
        "owner_phone": "03061234567"
    },
    {
        "name": "Garum Chashma Residence",
        "location": "Garum Chashma",
        "rent": 9500,
        "room_type": "Single",
        "facilities": "WiFi,Heating,Attached Bathroom",
        "latitude": 36.1282,
        "longitude": 71.8301,
        "available_rooms": 4,
        "description": "Private accommodation in Garum Chashma.",
        "owner_name": "Samiullah",
        "owner_phone": "03161234567"
    },
    {
        "name": "Torkhow Student Hostel",
        "location": "Torkhow",
        "rent": 7000,
        "room_type": "Shared",
        "facilities": "Mess,Heating",
        "latitude": 36.2781,
        "longitude": 72.0112,
        "available_rooms": 10,
        "description": "Affordable shared rooms.",
        "owner_name": "Karimullah",
        "owner_phone": "03261234567"
    },
    {
        "name": "Chitral Heights Hostel",
        "location": "Chitral Town",
        "rent": 12500,
        "room_type": "Single",
        "facilities": "WiFi,Mess,Heating,Attached Bathroom",
        "latitude": 35.8475,
        "longitude": 71.7915,
        "available_rooms": 6,
        "description": "Modern accommodation in Chitral Town.",
        "owner_name": "Salman Khan",
        "owner_phone": "03361234567"
    }
]


def seed_database():

    init_db()

    conn = get_db_connection()

    # Remove existing sample data
    conn.execute("DELETE FROM hostels")

    for hostel in hostels:

        conn.execute("""
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
            hostel["name"],
            hostel["location"],
            hostel["rent"],
            hostel["room_type"],
            hostel["facilities"],
            hostel["latitude"],
            hostel["longitude"],
            hostel["available_rooms"],
            hostel["description"],
            hostel["owner_name"],
            hostel["owner_phone"]
        ))

    conn.commit()

    count = conn.execute(
        "SELECT COUNT(*) FROM hostels"
    ).fetchone()[0]

    conn.close()

    print(f"Database seeded successfully.")
    print(f"Total hostels: {count}")


if __name__ == "__main__":
    seed_database()