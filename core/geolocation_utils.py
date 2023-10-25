from geopy.geocoders import Nominatim

def geocode_address(address):
    geolocator = Nominatim(user_agent="MarketPoint")
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
        print(location.latitude)
        print(location.longitude)
    else:
        return None, None