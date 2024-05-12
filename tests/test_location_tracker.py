import unittest
from location_tracker import LocationTracker

class TestLocationTracker(unittest.TestCase):
    def setUp(self):
        # Initialize a LocationTracker object for testing
        self.tracker = LocationTracker()
    
    def test_start_tracking(self):
        # Test starting tracking
        self.tracker.start_tracking()
        self.assertTrue(self.tracker.is_tracking)

    def test_stop_tracking(self):
        # Test stopping tracking
        self.tracker.start_tracking()
        self.tracker.stop_tracking()
        self.assertFalse(self.tracker.is_tracking)

    def test_get_location(self):
        # Test getting location of a device
        self.tracker.start_tracking()
        location = self.tracker.get_location("device_id")
        self.assertIsNotNone(location)
        self.assertIsInstance(location, dict)
        self.assertIn("latitude", location)
        self.assertIn("longitude", location)
    
    def test_update_location(self):
        # Test updating location of a device
        self.tracker.start_tracking()
        updated_location = {"latitude": 40.7128, "longitude": -74.0060}
        self.tracker.update_location("device_id", updated_location)
        location = self.tracker.get_location("device_id")
        self.assertEqual(location, updated_location)

    def test_calculate_distance(self):
        # Test calculating distance between two locations
        location1 = {"latitude": 40.7128, "longitude": -74.0060}
        location2 = {"latitude": 34.0522, "longitude": -118.2437}
        distance = self.tracker.calculate_distance(location1, location2)
        self.assertAlmostEqual(distance, 3936.19, places=2)  # Approximate distance in miles
    
    def test_store_and_retrieve_location_data(self):
        # Test storing and retrieving location data from the database
        location_data = {"device_id": "device_id", "latitude": 40.7128, "longitude": -74.0060}
        self.tracker.store_location_data("device_id", location_data)
        retrieved_data = self.tracker.retrieve_location_data("device_id", "2024-05-01", "2024-05-10")
        self.assertIn(location_data, retrieved_data)

if __name__ == '__main__':
    unittest.main()
