__author__ = 'hanks'

from math import sin, asin, cos, degrees

# use haversine formula to compute the range

EARTH_RADIUS = 6371 # earth's radius

def get_range(longitude, latitude, distance):
  dlng = 2 * asin(sin(distance / (2 * EARTH_RADIUS)) / cos(latitude))
  dlng = abs(degrees(dlng))
  dlat = distance / EARTH_RADIUS
  dlat = abs(degrees(dlat))

  location_range = (longitude - dlng, longitude + dlng, latitude - dlat, latitude + dlat)
  return location_range

if __name__ == '__main__':
  longitude = 113.3942032
  latitude = 23.2013323
  print get_range(longitude, latitude, 5.0)

