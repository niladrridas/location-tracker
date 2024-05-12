import unittest
import sqlite3
from database import LocationDatabase

class TestLocationDatabase(unittest.TestCase):
    def setUp(self):
        # Set up a temporary in-memory SQLite database for testing
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.database = LocationDatabase(self.connection)
        self.database.create_tables()

    def tearDown(self):
        # Close the database connection after each test
        self.connection.close()

    def test_create_tables(self):
        # Test whether tables are created successfully
        tables = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        table_names = [table[0] for table in tables]
        self.assertIn("devices", table_names)
        self.assertIn("locations", table_names)

    def test_add_device(self):
        # Test adding a device to the database
        device_id = "123456"
        device_name = "Test Device"
        self.database.add_device(device_id, device_name)
        device = self.database.get_device(device_id)
        self.assertIsNotNone(device)
        self.assertEqual(device["device_id"], device_id)
        self.assertEqual(device["device_name"], device_name)

    def test_get_device(self):
        # Test retrieving a device from the database
        device_id = "123456"
        device_name = "Test Device"
        self.database.add_device(device_id, device_name)
        device = self.database.get_device(device_id)
        self.assertIsNotNone(device)
        self.assertEqual(device["device_id"], device_id)
        self.assertEqual(device["device_name"], device_name)

    def test_add_location(self):
        # Test adding a location to the database
        device_id = "123456"
        timestamp = "2024-05-13 12:00:00"
        latitude = 37.7749
        longitude = -122.4194
        altitude = 0
        self.database.add_location(device_id, timestamp, latitude, longitude, altitude)
        location = self.database.get_latest_location(device_id)
        self.assertIsNotNone(location)
        self.assertEqual(location["device_id"], device_id)
        self.assertEqual(location["timestamp"], timestamp)
        self.assertEqual(location["latitude"], latitude)
        self.assertEqual(location["longitude"], longitude)
        self.assertEqual(location["altitude"], altitude)

    def test_get_latest_location(self):
        # Test retrieving the latest location of a device from the database
        device_id = "123456"
        timestamp = "2024-05-13 12:00:00"
        latitude = 37.7749
        longitude = -122.4194
        altitude = 0
        self.database.add_location(device_id, timestamp, latitude, longitude, altitude)
        location = self.database.get_latest_location(device_id)
        self.assertIsNotNone(location)
        self.assertEqual(location["device_id"], device_id)
        self.assertEqual(location["timestamp"], timestamp)
        self.assertEqual(location["latitude"], latitude)
        self.assertEqual(location["longitude"], longitude)
        self.assertEqual(location["altitude"], altitude)

if __name__ == "__main__":
    unittest.main()
