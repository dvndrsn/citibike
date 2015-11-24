#!/usr/bin/env python

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import json
import math
import urllib
import sys

try:
    # For Python 3.0 and later
    import configparser
except ImportError:
    # Fall back to Python 2's urllib2
    import ConfigParser as configparser

from location import location

# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as pyplot
# import numpy as np

# from datetime import datetime
# from datetime import timedelta

# API Key is set through ini file
GOOGLE_API_KEY = None


def get_jsonparsed_data(url):
    """Receive the content of ``url``, parse it as JSON and return the
       object.
    """
    response = urlopen(url)
    data = str(response.read().decode("utf-8"))
    return json.loads(data)


def get_citibike_station_data():
    """Returns the web service response from citibike station status
    """
    citiurl = 'http://www.citibikenyc.com/stations/json'

    citidata = get_jsonparsed_data(citiurl)

    return citidata['stationBeanList']


def get_geocode_data(address, GOOGLE_API_KEY):
    """Returns the lat/long from the web service response from
       Google Maps Geocode UI.
    """
    geourl = 'https://maps.googleapis.com/maps/api/geocode/json'
    values = {'address': address,
              'key': GOOGLE_API_KEY}

    data = urllib.parse.urlencode(values).replace('%2C', ',')
    url = geourl + '?' + data

    return get_jsonparsed_data(url)


def get_geo_location(geodata):
    """Takes parsed response from Google Maps Geocode API and returns the
       latitude and longitide values in location
    """
    lat = geodata['results'][0]['geometry']['location']['lat']
    lng = geodata['results'][0]['geometry']['location']['lng']

    return location(lng, lat)


def distance(point1, point2):
    """Provides euclidian distnace betweenTakes two lat/long (location) and
       provides the distance
    """
    return math.sqrt(
        pow(point2.lat - point1.lat, 2) + pow(point2.lng - point1.lat, 2))


def get_station_locations(stationdata):
    locations = []

    for station in stationdata:
        locations.append(location(station['latitude'],
                         station['longitude']))

    return locations


def get_closest_stations(stationdata, loc, num_stations=5):
    """Filters the station data from citibike for the stations which are closet to
    the specified location (lat/long).
    """
    closest_stations = sorted(
        stationdata, key=lambda station:
        location.harversine(
            location(station['longitude'], station['latitude']),
            loc))[:num_stations]

    return closest_stations


def display_station_docks(stations):
    for station in stations:
        print("{name}. Open docks: {remaining} / {total} ({updated})".format(
            name=station['stationName'], remaining=station['availableDocks'],
            total=station['totalDocks'],
            updated=station['lastCommunicationTime']))


def display_station_bikes(stations):
    for station in stations:
        print("{name}. Open bikes: {remaining} / {total} ({updated})".format(
            name=station['stationName'], total=station['totalDocks'],
            remaining=station['totalDocks']-station['availableDocks'],
            updated=station['lastCommunicationTime']))

# def display_stations(locations):
#     map = BaseMap(projection='merc', lat_0=57, lon_0=-135,
#                   resolution='h', area_thresh=0.1,
#                   llcrnrlon=-136.25, llcrnrlat=56.0,
#                   urcrnrlon=-134.25, urcrnrlat=57.75)

#     x, y = map(locations[:].lon, locations[:].lat)


def main(argv):
    config_file = 'citibike.ini' if argv[0] is None else argv[0]
    config = configparser.ConfigParser()
    config.read(config_file)

    GOOGLE_API_KEY = config.get('API_KEYS', 'Google')

    address = '455 Broadway, New York, NY'
    print("Geocoding address {addy}".format(addy=address))
    geodata = get_geocode_data(address, GOOGLE_API_KEY)
    source = get_geo_location(geodata)
    print("Geocoded address {addy} to {loc}".format(
        addy=address, loc=source))

    address = '7 Word Trade Center, New York, NY'
    print("Geocoding address {addy}".format(addy=address))
    geodata = get_geocode_data(address, GOOGLE_API_KEY)
    destination = get_geo_location(geodata)
    print("Geocoded address {addy} to {loc}".format(
        addy=address, loc=destination))

    distance = location.harversine(source, destination)
    print("Distance (as the crow flies) between source and destination " +
          "is {dist:.2f} meters.".format(dist=distance))

    print("Fetching Citibike Station data..")
    stationdata = get_citibike_station_data()

    print("\nClosest stations to source")
    closest_stations = get_closest_stations(stationdata, source)
    display_station_bikes(closest_stations)

    print("\nClosest stations to destination")
    closest_stations = get_closest_stations(stationdata, destination)
    display_station_docks(closest_stations)

    # station_locations = get_station_locations(stationdata)
    # display_stations(station_locations)


if __name__ == '__main__':
    main(sys.argv[1:])
