"""
Filming locations
"""

from math import radians, cos, sin, asin, sqrt
import argparse
import folium
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
    mark_layer(data, long, lat)


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


def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)

    >>> haversine(-74.0060152, 40.7127281, 24.0315921, 49.841952)
    7174.566532753805
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    add = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    cen = 2 * asin(sqrt(add))
    rad = 6371
    return cen * rad


def sort_entries(input_data: str, lon: float, lat: float) -> list:
    """
    Function to sort entries
    """
    for ind, elem in enumerate(input_data):
        if '(' in elem[-1] or ')' in elem[-1]:
            input_data[ind].pop(-1)

    def loc_sort(data):
        loc = locator(data[-1])

        if loc is False:
            return float('inf')

        if loc is not None:
            return haversine(loc[1], loc[0], float(lon), float(lat))
        else:
            return float('inf')

    return sorted(input_data, key=loc_sort)[:10]


def mark_layer(input_data: str, lon: float, lat: float) -> None:
    """
    1 layer which should be diplayed on the map
    """
    input_data = sort_entries(input_data,lon, lat)

    count = 0
    for elem in input_data:
        loc = locator(elem[-1])
        if loc is not None:
            count += 1
            html_map.add_child(folium.Marker(location=[loc[0], loc[1]],
                            popup=elem[0],
                            icon=folium.Icon()))
        if count == 10:
            break


if __name__ == "__main__":
    main(latitude, longtitude, path)
    html_map.save('Map_Custom_Popup.html')
