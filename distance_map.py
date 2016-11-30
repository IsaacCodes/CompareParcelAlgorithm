"""distance_map.py

=== Credit ===

Allan Chang
    1003235983
Isaac Seah
    1001753051
Last edited: Oct 2, 2016

=== Classes ===

DistanceMap
    DistanceMap is used to represent a map with routes. This class will be
    used to create instances. DistanceMap is expected to be accessed by
    experiment.py.
"""


class DistanceMap:

    """Collection of routes

    DistanceMap is essentially a map. If you want to find the distance from city
    A to city B, you can put in an inquiry to this class.

    === Private Attributes ===

    @type route: dict{str, int}
        Every possible route will have an entry. The key will be in the format
        of CityA_to_CityB. The int will be the distance of the route. It is
        important to note that CityA_to_CityB may be different than
        CityB_to_CityA.
    """

    def __init__(self):
        """Initialise a map

        No information is required when initialising a map. The attribute route
        starts off as empty.

        === Parameter and Return Types ===

        @type self: DistanceMap
            Default parameter
        @rtype: None
            No return is expected.

        === Examples ===

        >>> distance_map = DistanceMap()
        >>> distance_map.get_route_distance("Toronto", "Ottawa")
        >>> distance_map.add_route("Toronto", "Ottawa", 1001)
        >>> distance_map.get_route_distance("Toronto", "Ottawa")
        1001
        >>> distance_map.get_route_distance("Ottawa", "Toronto")
        """
        self.route = {}

    def add_route(self, start_city, destination_city, distance):
        """Add a route

        Add a route to the database. If the route already exists, the new route
        will overwrite the previous route. However, overwriting should not exist
        in a properly designed map-data. The routes will be saved under the key,
        CityX_to_CityY.

        === Parameter and Return Types ===

        @type self: DistanceMap
            Default parameter
        @type start_city: str
            Starting city
        @type destination_city: str
            Destination of route
        @type distance: int
            Route distance
        @rtype: None
            No return is expected

        === Examples ===

        >>> distance_map2 = DistanceMap()
        >>> distance_map2.add_route("Canada", "China", 1001)
        >>> distance_map2.add_route("CanadaC", "hina", 1)
        >>> distance_map2.add_route("Canada", "India", 9999)
        >>> distance_map2.add_route("China", "Canada", 99)
        >>> distance_map2.get_route_distance("Toronto", "Ottawa")
        >>> distance_map2.get_route_distance("Canada", "China")
        1001
        >>> distance_map2.get_route_distance("CanadaC", "hina")
        1
        >>> distance_map2.get_route_distance("China", "Canada")
        99
        >>> distance_map2.get_route_distance("Canada", "India")
        9999
        >>> distance_map2.get_route_distance("India", "Canada")
        >>> distance_map2.get_route_distance("CanadaI", "ndia")
        """
        self.route[start_city + "to" + destination_city] = distance

    def get_route_distance(self, start_city, destination_city):
        """Get a route

        Get a route from the database. If the route does not exist, nothing will
        be returned.

        === Parameter and Return Types ===

        @type self: DistanceMap
            Default parameter
        @type start_city: str
            Starting city
        @type destination_city: str
            Destination of route
        @rtype: int
            Return route distance

        === Examples ===

        >>> distance_map = DistanceMap()
        >>> distance_map.get_route_distance("A", "B")
        >>> distance_map.add_route("A", "B", 1)
        >>> distance_map.add_route("D", "C", 10)
        >>> distance_map.add_route("A", "C", 100)
        >>> distance_map.add_route("A", "B", 1000)
        >>> distance_map.add_route("F", "A", 10000)
        >>> distance_map.add_route("B", "A", 100000)
        >>> distance_map.get_route_distance("A", "B")
        1000
        >>> distance_map.get_route_distance("A", "C")
        100
        >>> distance_map.get_route_distance("C", "A")
        >>> distance_map.get_route_distance("A", "B")
        1000
        >>> distance_map.get_route_distance("F", "A")
        10000
        >>> distance_map.get_route_distance("C", "D")
        >>> distance_map.get_route_distance("D", "C")
        10
        >>> distance_map.get_route_distance("B", "A")
        100000
        >>> distance_map.get_route_distance("Z", "X")
        """
        if start_city + 'to' + destination_city in self.route:
            return self.route[start_city + "to" + destination_city]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='.pylintrc')
