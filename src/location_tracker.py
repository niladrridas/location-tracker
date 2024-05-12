import sqlite3
import datetime
import json

class LocationTracker:
    def __init__(self, database_path='data/location_data.db'):
        self.database_path = database_path
        self.create_connection()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.cursor = self.conn.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print("Error connecting to database:", e)

    def create_table(self):
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS location_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            timestamp TEXT
        )
        """
        try:
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print("Error creating table:", e)

    def track_location(self, device_id, latitude, longitude):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_sql = """
        INSERT INTO location_data (device_id, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?)
        """
        try:
            self.cursor.execute(insert_sql, (device_id, latitude, longitude, timestamp))
            self.conn.commit()
            print("Location tracked successfully.")
        except sqlite3.Error as e:
            print("Error tracking location:", e)

    def get_location(self, device_id):
        select_sql = """
        SELECT latitude, longitude, timestamp
        FROM location_data
        WHERE device_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """
        try:
            self.cursor.execute(select_sql, (device_id,))
            location = self.cursor.fetchone()
            if location:
                return {
                    'latitude': location[0],
                    'longitude': location[1],
                    'timestamp': location[2]
                }
            else:
                print("No location found for the device.")
                return None
        except sqlite3.Error as e:
            print("Error retrieving location:", e)

    def retrieve_location_data(self, device_id, start_date, end_date):
        select_sql = """
        SELECT latitude, longitude, timestamp
        FROM location_data
        WHERE device_id = ? AND timestamp >= ? AND timestamp <= ?
        ORDER BY timestamp
        """
        try:
            self.cursor.execute(select_sql, (device_id, start_date, end_date))
            location_data = self.cursor.fetchall()
            if location_data:
                return [{'latitude': loc[0], 'longitude': loc[1], 'timestamp': loc[2]} for loc in location_data]
            else:
                print("No location data found for the device within the specified time range.")
                return None
        except sqlite3.Error as e:
            print("Error retrieving location data:", e)

    def close_connection(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    tracker = LocationTracker()
    tracker.track_location(device_id='device1', latitude=37.7749, longitude=-122.4194)
    tracker.track_location(device_id='device1', latitude=40.7128, longitude=-74.0060)
    print("Current location:", tracker.get_location(device_id='device1'))
    print("Location history:", tracker.retrieve_location_data(device_id='device1', start_date='2024-01-01', end_date='2024-12-31'))
    tracker.close_connection()
