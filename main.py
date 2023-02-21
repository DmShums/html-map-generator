"""
Filming locations
"""

from math import radians, cos, sin, asin, sqrt
import argparse
import folium
# from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="http")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


# input data
parser = argparse.ArgumentParser()
parser.add_argument('year')
parser.add_argument('latitude')
parser.add_argument('longtitude')
parser.add_argument('path')
args = parser.parse_args()

year = args.year
latitude = args.latitude
longtitude = args.longtitude
path = args.path

# map data
html_map = folium.Map(location=[latitude, longtitude],
zoom_start=10)

html_map.add_child(folium.Marker(location=[latitude, longtitude],
                            popup="My location",
                            icon=folium.Icon(color='red')))

# additional layer
folium.TileLayer('Stamen Terrain').add_to(html_map)
folium.TileLayer('Stamen Toner').add_to(html_map)
folium.TileLayer('Stamen Water Color').add_to(html_map)
folium.TileLayer('cartodbpositron').add_to(html_map)
folium.TileLayer('cartodbdark_matter').add_to(html_map)
folium.LayerControl().add_to(html_map)


def main(lat: int, long: str, pth: str) -> None:
    """
    Main function to render html page with all needed layers
    :param input_year: year to output film
    :param lat: latitude
    :param long: longtitude
    :param pth: path
    :return None
    """
    data = read_file(pth)
    # mark_layer(data, long, lat)


def read_file(path_to_file: str) -> list:
    """
    Module to read data from path_to_file and output in str format
    """
    with open(path_to_file, 'r', encoding="utf8", errors='ignore') as file:
        data = file.readlines()
        out_data = []

        for line in data[15:]:
            if not f"({year})" in line:
                continue

            new_line = line.strip().split('\t')
            temporary_arr = []
            for elem in new_line:
                if elem != '':
                    temporary_arr.append(elem)
            out_data.append(temporary_arr)

    return out_data


LOCATIONS = {}
def locator(loc_path: list) -> list:
    """
    Module to convert locations to coords
    >>> locator('New York')
    (40.7127281, -74.0060152)
    """
    if loc_path in LOCATIONS:
        return LOCATIONS[loc_path]

    try:
        location = geolocator.geocode(loc_path)
    except GeocoderTimedOut:
        return False


    if location is not None:
        LOCATIONS[loc_path] = (location.latitude, location.longitude)
        return (location.latitude, location.longitude)

    LOCATIONS[loc_path] = None

if __name__ == "__main__":
    main(latitude, longtitude, path)
    html_map.save('Map_Custom_Popup.html')
