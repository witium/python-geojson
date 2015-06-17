from decimal import Decimal

from geojson.base import GeoJSON
import sys


class Geometry(GeoJSON):
    """
    Represents an abstract base class for a WGS84 geometry.
    """

    if (sys.version_info[0] == 3):
        # Python 3.x has no long type
        JSON_compliant_types = (float, int, Decimal)
    else:
        JSON_compliant_types = (float, int, Decimal, long)

    def __init__(self, coordinates=None, crs=None, **extra):
        """
        Initialises a Geometry object.

        :param coordinates: Coordinates of the Geometry object.
        :type coordinates: tuple
        :param crs: CRS
        :type crs: CRS object
        """

        super(Geometry, self).__init__(**extra)
        self["coordinates"] = coordinates or []
        self.clean_coordinates(self["coordinates"])
        if crs:
            self["crs"] = self.to_instance(crs, strict=True)

    @classmethod
    def clean_coordinates(cls, coords):
        for coord in coords:
            if isinstance(coord, (list, tuple)):
                cls.clean_coordinates(coord)
            elif not isinstance(coord, cls.JSON_compliant_types):
                raise ValueError("%r is not JSON compliant number" % coord)


class GeometryCollection(GeoJSON):
    """
    Represents an abstract base class for collections of WGS84 geometries.
    """

    def __init__(self, geometries=None, **extra):
        super(GeometryCollection, self).__init__(**extra)
        self["geometries"] = geometries or []


# Marker classes.

class Point(Geometry):
    pass


class MultiPoint(Geometry):
    pass


class LineString(MultiPoint):
    pass


class MultiLineString(Geometry):
    pass


class Polygon(Geometry):
    pass


class MultiPolygon(Geometry):
    pass


class Default(object):
    """
    GeoJSON default object.
    """
