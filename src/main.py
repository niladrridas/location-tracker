import time
import logging
from location_tracker import LocationTracker
from database import Database

# Configure logging
logging.basicConfig(filename='logs/location_tracker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Initialize LocationTracker and Database instances
        location_tracker = LocationTracker()
        database = Database('data/location_data.db')

        # Start tracking
        location_tracker.start_tracking()

        # Simulate tracking for 1 hour (for demonstration purposes)
        end_time = time.time() + 3600  # 1 hour
        while time.time() < end_time:
            # Simulate updating location data every 5 seconds
            time.sleep(5)
            location_data = location_tracker.get_location_data()
            database.store_location_data(location_data)
            logging.info(f"Location data stored: {location_data}")

        # Stop tracking
        location_tracker.stop_tracking()
        logging.info("Location tracking stopped.")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
