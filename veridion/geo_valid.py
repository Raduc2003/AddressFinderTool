from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import itertools

def geocode_address(geolocator, address):
    try:
        return geolocator.geocode(address, addressdetails=True)
    except GeocoderTimedOut:
        return None

def extract_address_details(raw_data):
    address = raw_data.get("address", {})
    address_details = {
        "country": address.get("country"),
        "region": address.get("state") or address.get("region"),
        "city": address.get("city") or address.get("town") or address.get("village"),
        "postcode": address.get("postcode"),
        "road": address.get("road"),
        "road_number": address.get("house_number"),
        "longitude": raw_data.get("lon"),
        "latitude": raw_data.get("lat")
    }
    return address_details

def validate_address(address, timeout=10):
    # Ensure the timeout is at least one second
    effective_timeout = max(1, timeout)
    
    geolocator = Nominatim(user_agent="geo_valid", timeout=effective_timeout)
    
    # Attempt to geocode the entire address first
    location = geocode_address(geolocator, address)
    if location:
        # print(f"Geocoded full address: {address}")
        return True, extract_address_details(location.raw)
    
    # Break down the address into components
    address_parts = [part.strip() for part in address.split(',')]
    
    # Try different combinations of address components
    for i in range(len(address_parts), 0, -1):
        for combo in itertools.combinations(address_parts, i):
            combo_address = ', '.join(combo)
            # print(f"Trying combination: {combo_address}")  # Debugging info
            location = geocode_address(geolocator, combo_address)
            if location:
                # print(f"Geocoded combination: {combo_address}")
                return True, extract_address_details(location.raw)
    
    return False, "Address not found or invalid."

# address = "11550 Poema Place, Unit 101 Chatsworth"
# is_valid, details = validate_address(address, timeout=10)
# if is_valid:
#     print(f"Address is valid. Details: {details}")
# else:
#     print(f"Address validation failed. Reason: {details}")
