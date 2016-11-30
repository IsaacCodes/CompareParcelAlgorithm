"""experiment.py

=== Credit ===

Allan Chang
    1003235983
Isaac Seah
    1001753051
Last edited: Oct 11, 2016

=== Classes ===

SchedulingExperiment
    This class is capable of conducting tests using external data. This class is
    expected to be accessed by the client. This class requires scheduler.py,
    domain.py and distance_map.py.

=== Helper Functions ===

read_parcels
    Read parcel data from .txt files

read_distance_map
    Read map data from .txt files

read_trucks
    Read truck data from .txt documents

sanity_check
    Run a single experiment using desired settings. Settings can be edited in
    /data/demo.json
"""
from scheduler import RandomScheduler, GreedyScheduler
from domain import Parcel, Truck
from distance_map import DistanceMap


class SchedulingExperiment:
    """An experiment in scheduling parcels for delivery.

    To complete an experiment involves four stages:

    1. Read in all data from necessary files, and create corresponding objects.
        The experiemnt will take in variables from the config file and create
        the following variables:
        1. depot_location
        2. parcel_list
            For each line in parcel data, create a parcel object, append to
            parcel list
            for use in scheduler.
        3. truck_list
            For each line in Truck data, create a truck object and then append
            to Truck list for use in scheduler.
        4. algorithm
            Stores the string to intitate the correct scehduler in Run method.
        5. parcel_priority
            Stores the string to intitate the correct priority of parcel
            scheduling in Greedy scheduler. Available options are: volume or
            destination
        6. parcel_order
            Stores the string to run the correct parcel order in the scheduler.
        7. truck_order
            Stores the string to ruun the correct truck order in the scheduler.

    2. Run a scheduling algorithm to assign parcels to trucks.
    3. Compute statistics showing how good the assignment of parcels to trucks
       is.
    4. Report the statistics from the experiment.

    === Private Attributes ===

    @type _config: dict[str, str]
        A configuration file for the experiment. The configuration changes
        how the scheduler behaves.
    @type _unscheduled: [Parcel]
        A list of unscheduled parcels.
    @type _parcel_list: [Parcel]
        A list of parcels
    @type _truck_list: [Truck]
        A list of trucks
    @type _route_map: DistanceMap
        A map containing route distances
    """
    def __init__(self, config):
        """Initialize a new experiment from a configuration dictionary.

        === Precondition ===

        <config> contains keys and values for "depot_location", "parcel_file"
        "truck_file", "map_file", "algorithm", "parcel_priority", "parcel_order"
        "truck_order", "verbose"

        === Parameter and Return Types ===

        @type self: SchedulingExperiment
        @type config: dict[str, str]
            The configuration for this experiment, including
            the data files and algorithm configuration to use.
        @rtype: None
        """
        self._config = config
        self._unscheduled = []

        self._parcel_list = read_parcels(config['parcel_file'])
        self._truck_list = read_trucks(config['truck_file'],
                                       config['depot_location'])
        self._route_map = read_distance_map(config['map_file'])

    def run(self, report=False):
        """Run the experiment and return statistics on the outcome.

        If <report> is True, print a report on the statistics from this
        experiment.  Either way, return the statistics in a dictionary.

        If <self.verbose> is True, print step-by-step details
        regarding the scheduling algorithm as it runs.

        === Precondition ===

        self._config['parcel_priority'] = 'volume' or 'destination
        self._config['parcel_order'] = 'non-increasing' or 'non-decreasing'
        self._config['truck_order'] = 'non-increasing' or 'non-decreasing'

        === Parameter and Return Types ===

        @type self: SchedulingExperiment
        @type report: bool
            Whether or not to print a report on the statistics. The report
            is printed onto the console.
        @rtype: dict[str, int | float]
            Statistics from this experiment. Keys consist of 'fleet',
            'unused_trucks', 'avg_distance', 'avg_fullness', 'unused_space',
            'unscheduled'
        """

        if self._config['algorithm'] == 'random':
            scheduler = RandomScheduler(self._route_map)
        else:
            scheduler = GreedyScheduler(self._config['parcel_priority'],
                                        self._config['parcel_order'],
                                        self._config['truck_order'],
                                        self._route_map)
        self._unscheduled = scheduler.schedule(
            self._parcel_list, self._truck_list,
            self._config['verbose'] == 'true')
        if report is True:
            print(self._compute_stats())
        return self._compute_stats()

    def _compute_stats(self):
        """Compute the statistics for this experiment.

        === Preconditions ===

        Behaviour _run has already been called.

        === Parameter and Return Types ===

        @type self: SchedulingExperiment
        @rtype: Dict[str, int | float]
            Statistics from this experiment. Keys include 'fleet',
            'unused_trucks', 'avg_distance', 'avg_fullness', 'unused_space',
            'unscheduled'

        === Local Variables ===

        type statistics: Dict[str, int | float]
            All stats are stored into <statistics>
        type unused_trucks: [Truck]
            If a truck has a volume of 0, it is added to <unused_trucks>
        type used_trucks: [Truck]
            If a truck has a volume > 0, it is added to <used_trucks>
        type total_distance: int
            Total distance travelled by all trucks
        type total_fullness: float
            Total fullness of all trucks. Average is calculated by dividing
            <total_fullness> by len(used_trucks)
        type unused_space: int
            Total unused storage space.
        type truck: Truck
            A single truck
        type route_travelled: [str]
            A list of cities to travel to. The truck starts in
            route_travelled[0] and travels to each city within the list in the
            order of the list.
        type travelled_distance: int
            Total distance travelled by a single truck
        type trip: int
            A single trip between 2 cities. The value is a bit abstract. <trip>
            holds the index of <route_travelled>

        === Representation Invariants ===

        total_distance >= 0
            Negative distance does not make sense
        total_fullness > 0
            Negative fullness does not make sense. If fullness was 0%, it would
            not be included in <total_fullness>
        unused_space >= 0
            Negative unused space makes no sense
        travelled_distance >= 0
            Negative distance does not make sense
        trip >= 0
            Index of -1 does not exist
        """
        statistics = {}
        unused_trucks = []
        used_trucks = []
        total_distance = 0
        total_fullness = 0
        unused_space = 0

        statistics['fleet'] = len(self._truck_list)

        for truck in self._truck_list:

            if truck.get_volume() == 0:
                unused_trucks.append(truck)
            else:
                unused_space += truck.get_unused_space()
                used_trucks.append(truck)

        statistics['unused_trucks'] = len(unused_trucks)

        for truck in used_trucks:
            route_travelled = truck.get_route()
            travelled_distance = 0
            for trip in range(len(route_travelled) - 1):
                travelled_distance += self._route_map\
                    .get_route_distance(route_travelled[trip],
                                        route_travelled[trip + 1])

            total_distance += travelled_distance
            total_fullness += truck.get_fullness()

        if len(used_trucks) > 0:
            statistics['avg_distance'] = (total_distance/len(used_trucks))
            statistics['avg_fullness'] = (total_fullness/len(used_trucks))
        else:
            statistics['avg_distance'] = 0
            statistics['avg_fullness'] = 100
        statistics['unused_space'] = unused_space
        statistics['unscheduled'] = len(self._unscheduled)

        return statistics

# ----- Helper functions -----


def read_parcels(parcel_file):
    """Read parcel data from <parcel_file> and returns a list of parcels.

    === Parameter and Return Types ===

    @type parcel_file: str
        The name of a file containing parcel data in the form specified in
        Assignment 1.
    @rtype: [Parcel]
        Returns a list of parcels

    === Local Variables ===

    type parcel_list: [Parcel]
        A list that stores parcels
    type file: _io.TextIOWrapper
    type line: str
        A single line from the data file
    type tokens: [str]
        A list that separates strings by commasand stores useful data. The
        phrase 'David, Toronto' may be stored in tokens as ['David', 'Toronto']
    type pid: int
        Parcel identification number.
    type source: int
        Parcel source.
    type destination: Truck
        Parcel destination
    type volume
        Parcel volume
    type one_parcel
        A parcel that will be added to <parcel_list>

    === Representation Invariants ===

    volume >= 0
        Negative volume does not make sense.
    """
    parcel_list = []

    with open(parcel_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            pid = int(tokens[0].strip())
            source = tokens[1].strip()
            destination = tokens[2].strip()
            volume = int(tokens[3].strip())
            one_parcel = Parcel(pid, source, destination, volume)

            parcel_list.append(one_parcel)

    return parcel_list


def read_distance_map(distance_map_file):
    """Read distance data from <distance_map_file>

    A file containing route data is added to a map object. The returned map
    object contains all routes present in the .txt file.

    === Parameter and Return Types ===

    @type distance_map_file: str
        The name of a file containing distance data in the form specified in
        Assignment 1.
    @rtype: DistanceMap
        Returns a map that contains the distances between cities.

    === Local Variables ===

    type route_map: DistanceMap
        A map that stores routes
    type file: _io.TextIOWrapper
    type line: str
        A single line from the data file
    type tokens: [str]
        A list that separates and stores useful data. The phrase
        'Isaac, Toronto' may be stored in tokens as ['Isaac', 'Toronto']
    type c1: int
        Starting city of the route
    type c2: int
        Route's destination
    type dist: Truck
        The distance from <c1> to <c2>. Note, <c1> to <c2> may have a different
        distance compared to <c2> to <c1>. Imagine it like a one way route.

    === Representation Invariants ===

    dist >= 0
        Negative distance does not make sense.
    """

    route_map = DistanceMap()
    with open(distance_map_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            c1 = tokens[0].strip()
            c2 = tokens[1].strip()
            dist = int(tokens[2].strip())
            route_map.add_route(c1, c2, dist)

    return route_map


def read_trucks(truck_file, depot_location):
    """Read truck data from <truck_file>

    Data from a .txt document is converted into truck objects. The returned
    value is a list of truck objects.

    === Parameter and Return Types ===

    @type truck_file: str
        The name of a file containing truck data in the form specified in
        Assignment 1.
    @type depot_location: str
        The city where all the trucks (and packages) are at the start of the
        experiment.
    @rtype: [Truck]
        Returns a list of trucks.

    === Local Variables ===

    type trucks: [Truck]
        Accumulating list of trucks
    type file: _io.TextIOWrapper
    type line: str
        A single line from the data file
    type tokens: [str]
        A list that separates commas and stores useful data. The phrase
        'Allan, Toronto' may be stored in tokens as ['Allan', 'Toronto']
    type tid: int
        Truck id
    type capacity: int
        Truck capacity
    type one_truck: Truck
        A truck that will be added to <trucks>

    === Representation Invariants ===

    capacity >= 0
        Negative capacity does not make sense.
    """
    trucks = []

    with open(truck_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            tid = int(tokens[0])
            capacity = int(tokens[1])
            one_truck = Truck(tid, capacity, depot_location)
            trucks.append(one_truck)
    return trucks


def sanity_check(config_file):
    """Configure and run a single experiment on the scheduling problem
    defined in <config_file>

    Precondition: <config_file> is a json file with keys and values
    as in the dictionary format defined in Assignment 1.

    @type config_file: str
    @rtype: None
    """
    # Read an experiment configuration from a file and build a dictionary
    # from it.
    import json
    with open(config_file, 'r') as file:
        configuration = json.load(file)
    # Create and run an experiment with that configuration.
    experiment = SchedulingExperiment(configuration)
    experiment.run(report=True)

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='.pylintrc')
