from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import itertools

def geocode_address(geolocator, address):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        return None

def validate_address(address):
    geolocator = Nominatim(user_agent="address_validator")
    
    # Attempt to geocode the entire address first
    location = geocode_address(geolocator, address)
    if location:
        return True, location.raw.get('address', {})
    
    # Break down the address into components
    address_parts = [part.strip() for part in address.split(',')]
    
    # Try different combinations of address components
    for i in range(len(address_parts), 0, -1):
        for combo in itertools.combinations(address_parts, i):
            combo_address = ', '.join(combo)
            location = geocode_address(geolocator, combo_address)
            if location:
                return True, location.raw.get('address', {})
    
    return False, "Address not found or invalid."

address = "Strada Splaiul Unirii nr. 80-82, etaj 1, Bucuresti"
is_valid, details = validate_address(address)
if is_valid:
    print(f"Address is valid. Details: {details}")
else:
    print(f"Address validation failed. Reason: {details}")
