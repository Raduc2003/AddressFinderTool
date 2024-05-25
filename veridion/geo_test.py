from geopy.geocoders import Nominatim
from itertools import combinations


# TO MANY REQUESTS
def identify_location_type(location_string):
    geolocator = Nominatim(user_agent="location_identifier")
    location = geolocator.geocode(location_string)
    if location:
        return location.raw.get('type', 'unknown')
    else:
        return 'unknown'

def real_location(location_string):
    valid_location_types = ['country', 'state', 'region', 'province', 'district', 'county', 
                            'city', 'street', 'road', 'residential', 'industrial', 'town']

    # Check the entire input string first
    location_type = identify_location_type(location_string)
    if location_type in valid_location_types:
        return True, [(location_type, location_string)]

    # Split by common delimiters and check each part
    delimiters = [',', ';', '|']
    for delimiter in delimiters:
        if delimiter in location_string:
            substrings = location_string.split(delimiter)
            for substring in substrings:
                location_type = identify_location_type(substring.strip())
                if location_type in valid_location_types:
                    return True, [(location_type, substring.strip())]

    # Check combinations of words (bigrams, trigrams) to see if they form a valid location
    possible_real_locations = [word for word in location_string.split() if word.isalpha()]
    location_types = []

    for r in range(2, min(4, len(possible_real_locations) + 1)):  # Check bigrams and trigrams
        for combo in combinations(possible_real_locations, r):
            combo_string = ' '.join(combo)
            location_type = identify_location_type(combo_string)
            if location_type in valid_location_types:
                return True, [(location_type, combo_string)]

    # Finally, check individual words as a last resort
    for location in possible_real_locations:
        location_type = identify_location_type(location)
        location_types.append((location_type, location))
        if location_type in valid_location_types:
            return True, location_types

    return False, location_types

location_string = "1959 in Blackpool"
print(real_location(location_string))  # True if it contains a valid location type
