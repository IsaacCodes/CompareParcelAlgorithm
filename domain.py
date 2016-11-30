"""domain.py

=== Credit ===

Allan Chang
    1003235983
Isaac Seah
    1001753051
Last edited: Oct 11, 2016

=== Classes ===

Parcel
    Instances of Parcel represent mail or package. This class will not be
    accessed by the client. Parcel is expected to be accessed by class Truck,
    and file experiment.py, scheduler.py.

Truck
    Instances of Truck represent a delivery truck. This class will not be
    accessed by the client. Truck is expected to be accessed by experiment.py,
    scheduler.py.
"""


class Parcel:
    """A package for a loved individual

    Parcels are goods handled by delivery trucks. Packages have a starting city,
    destination and a volume. At the beginning, the parcels are sent to the
    depot. Therefore, the trucks do not need to pick up parcels at their
    source city.

    === Private Attributes ===

    @type _source_city: str
        The source city of the parcel
    @type _destination_city: str
        The parcel's destination city
    @type _volume: int
        The amount of space the parcel takes
    @type _parcel_id: int
        The parcel's identification number

    === Representation Invariants ===

    _volume >= 0
        Negative volumes do not make sense
    """

    def __init__(self, parcel_id, source_city, destination_city, volume):
        """Initialise a parcel

        Create a parcel with the given information. Sets the private attribute
        values.

        === Parameter and Return Types ===

        @type self: Parcel
        @type parcel_id: int
            Parcel identification
        @type source_city: str
            Parcel starting city
        @type destination_city: str
            Parcel's destination city
        @type volume: int
            Parcel's volume
        @rtype: None

        === Representation Invariants ===

        volume >= 0
            Negative volume just doesn't make sense

        === Examples ===

        >>> parcel = Parcel(1, "Narnia", "Earth", 1000000)
        >>> parcel.get_destination()
        'Earth'
        >>> parcel.get_volume()
        1000000

        >>> parcel = Parcel(1000000, "Earth", "Narnia", 1)
        >>> parcel.get_destination()
        'Narnia'
        >>> parcel.get_volume()
        1
        """
        self._source_city = source_city
        self._destination_city = destination_city
        self._volume = volume
        self._parcel_id = parcel_id

    def get_destination(self):
        """Returns destination of parcel

        === Parameters and Return Types ===

        @type self: Parcel
        @rtype: str

        === Examples ===

        >>> parcel = Parcel(1, "Earth101", "Earth102", 11)
        >>> parcel.get_destination()
        'Earth102'
        >>> parcel.get_volume()
        11

        >>> parcel = Parcel(2, "Earth102", "Earth103", 12)
        >>> parcel.get_destination()
        'Earth103'
        >>> parcel.get_volume()
        12

        >>> parcel = Parcel(3, "Earth103", "Earth101", 0)
        >>> parcel.get_destination()
        'Earth101'
        >>> parcel.get_volume()
        0
        """
        return self._destination_city

    def get_volume(self):
        """Returns destination of parcel

        === Parameters and Return Types ===

        @type self: Parcel
        @rtype: int

        === Examples ===

        >>> parcel = Parcel(1, "Mississauga", "Toronto", 1111)
        >>> parcel2 = Parcel(11, "Mississauga", "Ottawa", 111)
        >>> parcel3 = Parcel(111, "Mississauga", "Montreal", 11)
        >>> parcel4 = Parcel(1111, "Mississauga", "Vancouver", 1)

        >>> parcel.get_destination()
        'Toronto'
        >>> parcel.get_volume()
        1111

        >>> parcel2.get_destination()
        'Ottawa'
        >>> parcel2.get_volume()
        111

        >>> parcel3.get_destination()
        'Montreal'
        >>> parcel3.get_volume()
        11

        >>> parcel4.get_destination()
        'Vancouver'
        >>> parcel4.get_volume()
        1
        """
        return self._volume

    def get_id(self):
        """Returns parcel id

        === Parameters and Return Types ===

        @type self: Parcel
        @rtype: int

        === Examples ===

        >>> parcel = Parcel(1, "Mississauga", "Toronto", 1111)
        >>> parcel2 = Parcel(11, "Mississauga", "Ottawa", 111)
        >>> parcel3 = Parcel(111, "Mississauga", "Montreal", 11)
        >>> parcel4 = Parcel(1111, "Mississauga", "Vancouver", 1)
        >>> parcel.get_id()
        1
        >>> parcel2.get_id()
        11
        >>> parcel3.get_id()
        111
        >>> parcel4.get_id()
        1111
        """
        return self._parcel_id


class Truck:
    """A truck from a network of trucks.

    Trucks act like realistic delivery trucks. Trucks create a route over time
    and can load parcels. Each truck may have a different storage capacity.

    === Private Attributes ===

    @type _capacity: int
        The maximum volume of parcels a truck can store.
    @type _storage: int
        The current volume of parcels stored in the truck.
    @type _parcel_loaded: [Parcel]
        A cummative list of stored parcels.
    @type _route: [str]
        A list of cities the truck intends to travel to. The truck intends to
        travel to _route[0] first, _route[1] second, _route[2] third and so on.
        _route[0] will always be the starting city/depot.
    @type _truck_id: int
        Truck identification number

    === Representation Invariants ===

    _capacity >= 0
        A negative capacity just makes no sense
    _storage >= 0
        Shouldn't have negative storage
    """

    def __init__(self, truck_id, capacity, starting_city):
        """Create a truck

        Set most attributes of the truck. Most notably the storage capacity of
        the truck.

        === Parameter and Return Types ===

        @type self: Truck
        @type truck_id: int
            Truck identification number
        @type capacity: int
            Truck capacity
        @type starting_city: str
            The starting city of the Truck. In the experiment, the truck should
            start at the depot location.
        @rtype: None

        === Representation Invariants ===

        capacity >= 0
            Negative capacity does not make sense.

        === Examples ===

        >>> cargo = Parcel(1, "London", "Churchill", 1000)
        >>> cargo2 = Parcel(100, "London", "Paris", 1)
        >>> euro_truck = Truck(100, 1000000, "London")
        >>> euro_truck.city_in_route("London")
        True
        >>> euro_truck.city_in_route("Paris")
        False
        >>> euro_truck.get_capacity()
        1000000
        >>> euro_truck.get_unused_space()
        1000000
        >>> euro_truck.get_fullness()
        0.0
        >>> euro_truck.get_volume()
        0
        >>> euro_truck.get_route()
        ['London']
        >>> euro_truck.load_parcel(cargo)
        >>> euro_truck.city_in_route("Churchill")
        True
        >>> euro_truck.city_in_route("Paris")
        False
        >>> euro_truck.get_unused_space()
        999000
        >>> euro_truck.get_fullness()
        0.1
        >>> euro_truck.get_volume()
        1000
        >>> euro_truck.get_route()
        ['London', 'Churchill']
        >>> euro_truck.load_parcel(cargo2)
        >>> euro_truck.city_in_route("Paris")
        True
        >>> euro_truck.get_unused_space()
        998999
        >>> euro_truck.get_fullness()
        0.1001
        >>> euro_truck.get_volume()
        1001
        >>> euro_truck.get_capacity()
        1000000
        >>> euro_truck.get_route()
        ['London', 'Churchill', 'Paris']
        """
        self._capacity = capacity
        self._storage = 0
        self._parcel_loaded = []
        self._route = [starting_city]
        self._truck_id = truck_id

    def load_parcel(self, parcel):
        """Load a parcel

        Simulates how a truck loads a parcel. As a parcel is added, the city if
        not already on the route will be added to the route. The parcel will be
        loaded on and storage will be updated.

        === Precondition ===

        The parcel should be able to fit in the truck. Check beforehand! In
        other words, parcel.get_volume() + self._storage <= self._capacity

        === Parameter and Return Types ===

        @type self: Truck
        @type parcel: Parcel
            <parcel> is loaded onto the truck
        @rtype: None

        === Local Variables ===

        destination: str
            The parcel's destination. If destination is not on the route,
            destination will be added.

        === Representation Invariants ===

        parcel.get_volume() >= 0
            A negative volume does not make sense and poses problems.
        parcel.get_volume() + self._storage <= self._capacity
            Otherwise, the stored volume exceeds capacity.

        === Examples ===

        >>> red_truck = Truck(1, 20, "Toronto")
        >>> red_truck.load_parcel(Parcel(1, "Toronto", "Montreal", 1))
        >>> red_truck.load_parcel(Parcel(2, "Toronto", "Montreal", 2))
        >>> red_truck.load_parcel(Parcel(3, "Toronto", "Toronto", 1))
        >>> red_truck.load_parcel(Parcel(4, "Toronto", "Montreal", 3))
        >>> red_truck.load_parcel(Parcel(5, "Toronto", "Montreal", 1))
        >>> red_truck.load_parcel(Parcel(6, "Toronto", "Toronto", 2))
        >>> red_truck.get_route()
        ['Toronto', 'Montreal']
        >>> red_truck.get_capacity()
        20
        >>> red_truck.get_volume()
        10
        >>> red_truck.get_fullness()
        50.0
        >>> red_truck.get_unused_space()
        10
        >>> red_truck.city_in_route("Montreal")
        True
        >>> red_truck.city_in_route("Chicago")
        False
        >>> red_truck.load_parcel(Parcel(6, "Toronto", "Chicago", 5))
        >>> red_truck.get_route()
        ['Toronto', 'Montreal', 'Chicago']
        >>> red_truck.get_capacity()
        20
        >>> red_truck.get_volume()
        15
        >>> red_truck.get_fullness()
        75.0
        >>> red_truck.get_unused_space()
        5
        >>> red_truck.city_in_route("Montreal")
        True
        >>> red_truck.city_in_route("Chicago")
        True
        """
        self._parcel_loaded.append(parcel)
        destination = parcel.get_destination()
        # city_in_route determines if destination is in route.
        if not self.city_in_route(destination):
            self._route.append(destination)
        self._storage += parcel.get_volume()

    def get_capacity(self):
        """Get truck capacity

        === Parameter and Return Type ===

        @type self: Truck
        @rtype: int

        === Examples ===

        >>> terrible_truck = Truck(1, 0, "Toronto")
        >>> awful_truck = Truck(2, 1, "Toronto")
        >>> poor_truck = Truck(3, 2, "Toronto")
        >>> mediocre_truck = Truck(4, 10, "Toronto")
        >>> decent_truck = Truck(5, 20, "Toronto")
        >>> good_truck = Truck(6, 100, "Toronto")
        >>> pristine_truck = Truck(7, 200, "Toronto")
        >>> excellent_truck = Truck(8, 1000, "Toronto")
        >>> superb_truck = Truck(9, 10000, "Toronto")
        >>> terrible_truck.get_capacity()
        0
        >>> awful_truck.get_capacity()
        1
        >>> poor_truck.get_capacity()
        2
        >>> mediocre_truck.get_capacity()
        10
        >>> decent_truck.get_capacity()
        20
        >>> good_truck.get_capacity()
        100
        >>> pristine_truck.get_capacity()
        200
        >>> excellent_truck.get_capacity()
        1000
        >>> superb_truck.get_capacity()
        10000
        """
        return self._capacity

    def get_volume(self):
        """Get truck volume

        === Parameter and Return Type ===

        @type self: Truck
        @rtype: int

        === Examples ===

        >>> methodic_truck = Truck(1, 100, "Toronto")
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_volume()
        1
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_volume()
        2
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_volume()
        3
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_volume()
        4
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_volume()
        5
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_volume()
        6
        """
        return self._storage

    def get_fullness(self):
        """Get truck volume

        Fullness is the percentage of the truck storage used. Note! Percentage
        means 98.9 if referring to 98.9%. It will not return 0.989. The number
        of decimal places are not controlled.

        === Parameter and Return Type ===

        @type self: Truck
        @rtype: float

        === Examples ===

        >>> methodic_truck = Truck(1, 100, "Toronto")
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_fullness()
        1.0
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_fullness()
        2.0
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_fullness()
        3.0
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_fullness()
        4.0
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_fullness()
        5.0
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_fullness()
        6.0
        """
        if self._capacity > 0:
            return 100 * self._storage / self._capacity
        else:
            # if truck has a capacity of 0, it is technically full
            return 100

    def get_unused_space(self):
        """Get unused volume within the truck

        Unused volume is the space not occupied. It is calculated through
        capacity - storage.

        === Parameter and Return Type ===

        @type self: Truck
        @rtype: float

        === Representation Invariants ===

        self._storage <= self._capacity
            How can you store more than you can physically carry?

        === Examples ===

        >>> methodic_truck = Truck(1, 100, "Toronto")
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_unused_space()
        99
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_unused_space()
        98
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_unused_space()
        97
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_unused_space()
        96
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_unused_space()
        95
        >>> methodic_truck.load_parcel(Parcel(1, "Toronto", "Yellowknife", 1))
        >>> methodic_truck.get_unused_space()
        94
        """
        return self._capacity - self._storage

    def city_in_route(self, city):
        """Check if city is in truck route

        Return true if city is in the truck route.

        === Parameter and Return Type ===

        @type self: Truck
        @type city: str
        @rtype: bool

        === Examples ===

        >>> abstract_truck = Truck(1, 100, "a")
        >>> abstract_truck.load_parcel(Parcel(0, "b", "c", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "c", "b", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "b", "d", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "b", "x", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "z", "A", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "N", "b", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "R", "y", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "q", "M", 1))
        >>> abstract_truck.load_parcel(Parcel(0, "l", "n", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x', 'A', 'y', 'M', 'n']
        >>> abstract_truck.city_in_route('a')
        True
        >>> abstract_truck.city_in_route('b')
        True
        >>> abstract_truck.city_in_route('c')
        True
        >>> abstract_truck.city_in_route('d')
        True
        >>> abstract_truck.city_in_route('e')
        False
        >>> abstract_truck.city_in_route('x')
        True
        >>> abstract_truck.city_in_route('z')
        False
        >>> abstract_truck.city_in_route('A')
        True
        >>> abstract_truck.city_in_route('N')
        False
        >>> abstract_truck.city_in_route('R')
        False
        >>> abstract_truck.city_in_route('y')
        True
        >>> abstract_truck.city_in_route('q')
        False
        >>> abstract_truck.city_in_route('M')
        True
        >>> abstract_truck.city_in_route('l')
        False
        >>> abstract_truck.city_in_route('n')
        True
        """
        return city in self._route

    def get_route(self):
        """Return truck's route

        The first item in the route list will be visited first. The last item
        will be visited last. The first item is the starting city. Generally
        the depot.

        === Parameter and Return Type ===

        @type self: Truck
        @rtype: [str]

        === Examples ===

        >>> abstract_truck = Truck(1, 100, "a")
        >>> abstract_truck.get_route()
        ['a']
        >>> abstract_truck.load_parcel(Parcel(0, "b", "c", 1))
        >>> abstract_truck.get_route()
        ['a', 'c']
        >>> abstract_truck.load_parcel(Parcel(0, "c", "b", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b']
        >>> abstract_truck.load_parcel(Parcel(0, "b", "d", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd']
        >>> abstract_truck.load_parcel(Parcel(0, "b", "x", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x']
        >>> abstract_truck.load_parcel(Parcel(0, "z", "A", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x', 'A']
        >>> abstract_truck.load_parcel(Parcel(0, "N", "b", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x', 'A']
        >>> abstract_truck.load_parcel(Parcel(0, "R", "y", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x', 'A', 'y']
        >>> abstract_truck.load_parcel(Parcel(0, "q", "M", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x', 'A', 'y', 'M']
        >>> abstract_truck.load_parcel(Parcel(0, "l", "n", 1))
        >>> abstract_truck.get_route()
        ['a', 'c', 'b', 'd', 'x', 'A', 'y', 'M', 'n']
        """
        return self._route

    def get_id(self):
        """Return truck id

        === Parameter and Return Types ===

        @type self: Truck
        @rtype: int

        === Examples ===

        >>> terrible_truck = Truck(1, 0, "Toronto")
        >>> awful_truck = Truck(2, 1, "Toronto")
        >>> poor_truck = Truck(3, 2, "Toronto")
        >>> mediocre_truck = Truck(4, 10, "Toronto")
        >>> decent_truck = Truck(5, 20, "Toronto")
        >>> good_truck = Truck(6, 100, "Toronto")
        >>> pristine_truck = Truck(7, 200, "Toronto")
        >>> excellent_truck = Truck(8, 1000, "Toronto")
        >>> superb_truck = Truck(9, 10000, "Toronto")
        >>> terrible_truck.get_id()
        1
        >>> awful_truck.get_id()
        2
        >>> poor_truck.get_id()
        3
        >>> mediocre_truck.get_id()
        4
        >>> decent_truck.get_id()
        5
        >>> good_truck.get_id()
        6
        >>> pristine_truck.get_id()
        7
        >>> excellent_truck.get_id()
        8
        >>> superb_truck.get_id()
        9
        """
        return self._truck_id

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='.pylintrc')
    import doctest
    doctest.testmod()
