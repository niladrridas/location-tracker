import datetime
import logging

# Set up logging
logging.basicConfig(filename='logs/location_tracker.log', level=logging.DEBUG)


def get_current_timestamp():
    """Get the current timestamp."""
    return datetime.datetime.now()


def convert_timestamp_to_string(timestamp):
    """Convert a timestamp to a formatted string."""
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


def log_info(message):
    """Log an informational message."""
    logging.info(message)


def log_warning(message):
    """Log a warning message."""
    logging.warning(message)


def log_error(message):
    """Log an error message."""
    logging.error(message)


def log_exception(exception):
    """Log an exception."""
    logging.exception(exception)


def validate_coordinates(latitude, longitude):
    """Validate latitude and longitude coordinates."""
    if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180):
        raise ValueError("Invalid latitude or longitude values")


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two geographic coordinates using Haversine formula."""
    from math import radians, sin, cos, sqrt, atan2

    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Calculate the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Apply Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Calculate the distance
    distance = R * c

    return distance


if __name__ == "__main__":
    # Example usage of utility functions
    timestamp = get_current_timestamp()
    log_info("Application started")
    log_warning("Low battery level detected")
    try:
        raise Exception("Example exception")
    except Exception as e:
        log_exception(e)
    print("Current timestamp:", convert_timestamp_to_string(timestamp))
    validate_coordinates(37.7749, -122.4194)
    print("Distance between San Francisco and New York:", calculate_distance(37.7749, -122.4194, 40.7128, -74.0060))
