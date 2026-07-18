from pymongo import MongoClient
from datetime import datetime, timedelta

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['hotel_management']

# Create the rooms collection
rooms_collection = db['rooms']

# Room data to be inserted
rooms_data = []

# Single Bed Facilities
single_bed_facilities = [
    {"icon": "fa-wifi", "name": "Free High-Speed Wi-Fi", "category": "Tech"},
    {"icon": "fa-snowflake", "name": "Air Conditioning", "category": "Comfort"},
    {"icon": "fa-tv", "name": "43\" Smart HD TV", "category": "Entertainment"},
    {"icon": "fa-bed", "name": "Single Premium Bed", "category": "Comfort"},
    {"icon": "fa-shower", "name": "Private Hot Shower", "category": "Bathroom"},
    {"icon": "fa-mug-hot", "name": "Coffee & Tea Maker", "category": "Refreshments"},
    {"icon": "fa-shield-halved", "name": "Digital Safe", "category": "Security"},
    {"icon": "fa-concierge-bell", "name": "24/7 Room Service", "category": "Services"}
]

# Double Bed Facilities
double_bed_facilities = [
    {"icon": "fa-wifi", "name": "Ultra High-Speed Wi-Fi", "category": "Tech"},
    {"icon": "fa-snowflake", "name": "Dual Climate Control", "category": "Comfort"},
    {"icon": "fa-tv", "name": "55\" 4K Smart TV", "category": "Entertainment"},
    {"icon": "fa-bed", "name": "Deluxe King Bed", "category": "Comfort"},
    {"icon": "fa-shower", "name": "Rainfall Hot Shower", "category": "Bathroom"},
    {"icon": "fa-wine-glass-empty", "name": "Mini Bar & Espresso", "category": "Refreshments"},
    {"icon": "fa-shield-halved", "name": "Digital Safe", "category": "Security"},
    {"icon": "fa-bath", "name": "Luxury Bathrobes & Toiletries", "category": "Bathroom"},
    {"icon": "fa-concierge-bell", "name": "24/7 Priority Room Service", "category": "Services"}
]

# Adding 10 rooms for Standard Room - Single Bed (Price: 1000)
for i in range(1, 11):
    room = {
        'room_type': 'Standard Room - Single Bed',
        'room_number': f'SSB-{i}',  # Room numbers SSB-1, SSB-2, ..., SSB-10
        'status': 'available',
        'user_token': None,
        'price_per_day': 1000,
        'free_date': None,
        'facilities': single_bed_facilities
    }
    rooms_data.append(room)

# Adding 10 rooms for Standard Room - Double Bed (Price: 1500)
for i in range(1, 11):
    room = {
        'room_type': 'Standard Room - Double Bed',
        'room_number': f'SDB-{i}',  # Room numbers SDB-1, SDB-2, ..., SDB-10
        'status': 'available',
        'user_token': None,
        'price_per_day': 1500,
        'free_date': None,
        'facilities': double_bed_facilities
    }
    rooms_data.append(room)

# Insert the rooms data into the collection
rooms_collection.insert_many(rooms_data)

print("10 Single Bed rooms and 10 Double Bed rooms with facilities added successfully!")
