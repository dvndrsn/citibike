import math


class location(object):

    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    def to_radians(self):
        rad_lat = self.lat * math.pi / 180.
        rad_lng = self.lng * math.pi / 180.
        return rad_lat, rad_lng

    @staticmethod
    def harversine(point1, point2, R=6371000.):
        """ Returns thet distance along an arc between two locations.
        Default R is radius of earth in meters
        """
        lat1, lng1 = point1.to_radians()
        lat2, lng2 = point2.to_radians()
        delta_lat = lat2 - lat1
        delta_lng = lng2 - lng1

        a = (math.sin(delta_lat / 2.) * math.sin(delta_lat / 2.) +
             math.cos(lat1) * math.cos(lat2) *
             math.sin(delta_lng / 2.) * math.sin(delta_lng / 2.))

        c = 2. * math.atan2(math.sqrt(a), math.sqrt(1. - a))

        distance = R * c

        return distance

    def harversine(self, point2, R=6371000.):
        """ Returns thet distance along an arc between this location and another.
        Default R is radius of earth in meters.
        """
        lat1, lng1 = self.to_radians()
        lat2, lng2 = point2.to_radians()
        delta_lat = lat2 - lat1
        delta_lng = lng2 - lng1

        a = (math.sin(delta_lat / 2.) * math.sin(delta_lat / 2.) +
             math.cos(lat1) * math.cos(lat2) *
             math.sin(delta_lng / 2.) * math.sin(delta_lng / 2.))

        c = 2. * math.atan2(math.sqrt(a), math.sqrt(1. - a))

        distance = R * c

        return distance

    def __str__(self):
        return "({lat:.2f}, {lng:.2f})".format(lat=self.lat, lng=self.lng)

    def __repr__(self):
        return self.__str__()


def main():
    loc1 = location(50, 50)
    loc2 = location(25, 25)
    loc3 = location(75, 75)

    print("{} - {}".format(loc1, loc1.to_radians()))
    print("Haversine distance from {} - {}: {}".format(
        loc1, loc2, loc1.harversine(loc2)))
    print("Haversine distance from {} - {}: {}".format(
        loc1, loc3, loc1.harversine(loc3)))
    print("Haversine distance (static) from {} - {}: {}".format(
        loc2, loc1, location.harversine(loc2, loc1)))


if __name__ == '__main__':
    main()
