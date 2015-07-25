__author__ = 'hanks'

from math import sin, asin, cos, degrees

# use haversine formula to compute the range

EARTH_RADIUS = 6371 # earth's radius
DISTANCE = 0.5 # 500m

def get_range(longitude, latitude):
  dlng = 2 * asin(sin(DISTANCE / (2 * EARTH_RADIUS)) / cos(latitude))
  dlng = degrees(dlng)
  dlat = DISTANCE / EARTH_RADIUS
  dlat = degrees(dlat)
  location_range = (longitude - dlng, longitude + dlng, latitude - dlat, latitude + dlat)
  return location_range

