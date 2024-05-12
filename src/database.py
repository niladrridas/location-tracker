import sqlite3
from datetime import datetime

class LocationDatabase:
    def __init__(self, db_file='data/location_data.db'):
        self.db_file = db_file
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.cursor = self.connection.cursor()
            print("Connected to database successfully!")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from database.")

    def create_tables(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS locations (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    device_id TEXT NOT NULL,
                                    latitude REAL NOT NULL,
                                    longitude REAL NOT NULL,
                                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                                )''')
            self.connection.commit()
            print("Database tables created successfully!")
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def insert_location(self, device_id, latitude, longitude):
        try:
            self.cursor.execute('''INSERT INTO locations (device_id, latitude, longitude)
                                   VALUES (?, ?, ?)''', (device_id, latitude, longitude))
            self.connection.commit()
            print("Location data inserted successfully!")
        except sqlite3.Error as e:
            print(f"Error inserting location data: {e}")

    def retrieve_locations(self, device_id, start_time=None, end_time=None):
        query = "SELECT * FROM locations WHERE device_id = ?"
        params = (device_id,)

        if start_time:
            query += " AND timestamp >= ?"
            params += (start_time,)

        if end_time:
            query += " AND timestamp <= ?"
            params += (end_time,)

        try:
            self.cursor.execute(query, params)
            rows = self.cursor.fetchall()
            print("Location data retrieved successfully!")
            return rows
        except sqlite3.Error as e:
            print(f"Error retrieving location data: {e}")
            return []

# Example usage
if __name__ == "__main__":
    db = LocationDatabase()
    db.connect()
    db.create_tables()

    # Inserting sample location data
    db.insert_location("device1", 40.7128, -74.0060)
    db.insert_location("device1", 34.0522, -118.2437)
    db.insert_location("device2", 51.5074, -0.1278)

    # Retrieving location data for a specific device within a time range
    start_time = datetime(2024, 5, 1)
    end_time = datetime(2024, 5, 10)
    locations = db.retrieve_locations("device1", start_time, end_time)
    print("Retrieved location data:", locations)

    db.disconnect()
