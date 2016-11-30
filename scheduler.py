"""scheduler.py

=== Credit ===

Allan Chang
    1003235983
Isaac Seah
    1001753051
Last edited: Oct 14, 2016

=== Classes ===

Scheduler
    Layout for RandomScheduler and GreedyScheduler. Do not instantialise.
RandomScheduler
    Selects packages and trucks randomly. Given a different seed for random, the
    results should change.
GreedyScheduler
    Chooses the first package in a "priority order" and loads it into the best
    truck.
"""
from random import shuffle, choice
from container import PriorityQueue


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels, trucks, verbose=False):
        """Schedule the given parcels onto the given trucks.

        Mutate the trucks so that they store information about which
        parcels they will deliver and what route they will take.
        Do *not* mutate the parcels.

        Return the parcels that do not get scheduled onto any truck, due to
        lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.

        === Parameters and Return Types ===

        @type self: Scheduler
        @type parcels: list[Parcel]
            The parcels to be scheduled for delivery.
        @type trucks: list[Truck]
            The trucks that can carry parcels for delivery.
        @type verbose: bool
            Whether or not to run in verbose mode.
        @rtype: list[Parcel]
            The parcels that did not get scheduled onto any truck due to
            lack of capacity.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """RandomScheduler is a scheduler that selects a parcel and a truck randomly

    === Private Attributes ===

    @type _route_map: DistanceMap
        A map that contains all possible routes. More importantly, the distance
        of each route.
    """

    def __init__(self, route_map):
        """Initialise RandomScheduler

        === Parameter and Return Types ===

        @type self: RandomScheduler
        @type route_map: DistanceMap
            route_map contains the distance of each route.
        @rtype: None
        """
        self._route_map = route_map

    def schedule(self, parcels, trucks, verbose=False):
        """ Random variant of Scheduler

        <trucks> are mutated. Do not reuse <trucks> for another
        scheduler/trial.

        === Local Variables ===

        type temp_parcels: [Parcel]
            Used to avoid mutating <parcels>. Shuffle would have mutated
            <parcels>
        type unused_parcels: [Parcel]
            Accumulating list of unused parcels. Returned at the end
        type one_parcel: Parcel
            An element of <temp_parcels>. The for loop goes through every
            element of <temp_parcels>.
        type trucks_with_space: [Truck]
            An accumulating list of trucks with enough capacity/space.
        type one_truck: Truck
            An element of <trucks>. The for loop runs each element of <trucks>
            once.
        """
        temp_parcels = parcels[:]
        shuffle(temp_parcels)
        unused_parcels = []
        # use every parcel in the list <temp_parcels> once
        for one_parcel in temp_parcels:
            trucks_with_space = []
            # use every truck in the list <trucks> once
            for one_truck in trucks:
                # if truck has enough space
                if one_truck.get_unused_space() >= one_parcel.get_volume():
                    trucks_with_space.append(one_truck)
            # if there are trucks to choose from, choose randomly
            if len(trucks_with_space) > 0:
                chosen_truck = choice(trucks_with_space)
                chosen_truck.load_parcel(one_parcel)
                if verbose:
                    print("Truck #{} has loaded Parcel #{}"
                          .format(chosen_truck.get_id(), one_parcel.get_id()))
            else:
                unused_parcels.append(one_parcel)
                if verbose:
                    print("Parcel #{} was not loaded"
                          .format(one_parcel.get_id()))
        return unused_parcels


class GreedyScheduler(Scheduler):
    """A scheduler that uses greedy strategy for its parcels and trucks

    GreedyScheduler is a scheduler that selects a parcel and a truck in an
    order of priority. The criteria of priority is set when the GreedyScheduler
    is initialised.

    === Private Attributes ===

    @type _route_map: DistanceMap
        A map that contains the distance between two cities.
    @type _truck_order: str
        Truck order priority. 'non-increasing' = larger space is prioritised.
        'non-decreasing' = smaller unused capacity is prioritised.
    @type _greater_priority: Callable[[Parcel, Parcel, bool]
        A function that determines which object has a greater priority. If
        _greater_priority(x, y) returns true, x has a greater priority than y.
    """

    def __init__(self, parcel_priority, parcel_order, truck_order, route_map):
        """Initialise a greedy scheduler

        === Parameter and Return Types ===

        @type self: GreedyScheduler
        @type parcel_priority: str
        @type parcel_order: str
        @type truck_order: str
        @type route_map: DistanceMap
        @rtype: None

        === Representation Invariants ===

        parcel_order = 'non-increasing' or 'non-decreasing'
        parcel_priority = 'volume' or 'destination

        === Local Functions ===

        volume_non_decreasing: Callable[[Parcel, Parcel, bool]
            Determines priority correctly if <parcel_priority> =
            'volume' and <parcel_order> = 'non-decreasing'
        volume_non_increasing: Callable[[Parcel, Parcel, bool]
            Determines priority correctly if <parcel_priority> =
            'volume' and <parcel_order> = 'non-increasing'
        destination_non_decreasing: Callable[[Parcel, Parcel, bool]
            Determines priority correctly if <parcel_priority> =
            'destination' and <parcel_order> = 'non-decreasing'
            'a' has priority over 'z'
        destination_non_increasing: Callable[[Parcel, Parcel, bool]
            Determines priority correctly if <parcel_priority> =
            'destination' and <parcel_order> = 'non-increasing'
            'z' has priority over 'a'
        """
        self._truck_order = truck_order
        self._route_map = route_map

        # non-decreasing = smallest to largest, smaller volume = higher queue
        def volume_non_decreasing(first_element, second_element):
            """ Priority determining function

            Priority is determined correctly if <parcel_priority> =
            'volume' and <parcel_order> = 'non-decreasing'. In other words, the
            parcel with the least volume has the highest priority.

            === Parameter and Return Types ===

            @type first_element: Parcel
            @type second_element: Parcel
            @rtype: bool

            === Examples ===

            Let's say:
            parcel-1.txt.get_volume() = 1
            parcel2.get_volume() = 10
            parcel3.get_volume() = 100

            volume_non_decreasing(parcel-1.txt, parcel2)
                True
            volume_non_decreasing(parcel2, parcel-1.txt)
                False
            volume_non_decreasing(parcel-1.txt, parcel3)
                True
            """
            return first_element.get_volume() < second_element.get_volume()

        # non-increasing = largest to smallest, larger volume = higher queue
        def volume_non_increasing(first_element, second_element):
            """ Priority determining function

            Priority is determined correctly if <parcel_priority> =
            'volume' and <parcel_order> = 'non-increasing'. In other words, the
            parcel with the largest volume has the highest priority.

            === Parameter and Return Types ===

            @type first_element: Parcel
            @type second_element: Parcel
            @rtype: bool

            === Examples ===

            Let's say:
            parcel-1.txt.get_volume() = 1
            parcel2.get_volume() = 10
            parcel3.get_volume() = 100

            volume_non_increasing(parcel-1.txt, parcel2)
                False
            volume_non_increasing(parcel2, parcel-1.txt)
                True
            volume_non_increasing(parcel-1.txt, parcel3)
                False
            """
            return first_element.get_volume() > second_element.get_volume()

        # non-decreasing = smallest to largest
        # smaller alphabetical order = higher queue ('a' < 'z') 'a' has priority
        def destination_non_decreasing(first_element, second_element):
            """ Priority determining function

            Priority is determined correctly if <parcel_priority> =
            'destination' and <parcel_order> = 'non-decreasing'. In other words,
            'a' is prioritised over 'z'. 'a' is prioritised over 'aa'

            === Parameter and Return Types ===

            @type first_element: Parcel
            @type second_element: Parcel
            @rtype: bool

            === Examples ===

            Let's say:
            parcel-1.txt.get_destination() = 'a'
            parcel2.get_destination() = 'aa'
            parcel3.get_destination() = 'z'

            destination_non_decreasing(parcel-1.txt, parcel2)
                True
            destination_non_decreasing(parcel2, parcel-1.txt)
                False
            destination_non_decreasing(parcel-1.txt, parcel3)
                True
            """
            return first_element.get_destination() < \
                second_element.get_destination()

        # non-increasing = largest to smallest
        # larger alphabetical order = higher queue ('z' > 'a') 'z' has priority
        def destination_non_increasing(first_element, second_element):
            """ Priority determining function

            Priority is determined correctly if <parcel_priority> =
            'destination' and <parcel_order> = 'non-increasing'. In other words,
            'z' is prioritised over 'a'. 'aa' is prioritised over 'a'

            === Parameter and Return Types ===

            @type first_element: Parcel
            @type second_element: Parcel
            @rtype: bool

            === Examples ===

            Let's say:
            parcel-1.txt.get_destination() = 'a'
            parcel2.get_destination() = 'aa'
            parcel3.get_destination() = 'z'

            destination_non_increasing(parcel-1.txt, parcel2)
                False
            destination_non_increasing(parcel2, parcel-1.txt)
                True
            destination_non_increasing(parcel-1.txt, parcel3)
                False
            """
            return first_element.get_destination() >\
                second_element.get_destination()

        if parcel_order == 'non-decreasing':
            if parcel_priority == 'volume':
                self._greater_priority = volume_non_decreasing
            else:
                self._greater_priority = destination_non_decreasing
        else:
            if parcel_priority == 'volume':
                self._greater_priority = volume_non_increasing
            else:
                self._greater_priority = destination_non_increasing

    def _choose_load_truck(self, trucks, parcel, verbose):
        """Load parcel into best truck

        === Parameters and Return Types ===

        @type self: GreedyScheduler
        @type trucks: [Truck]
            List of trucks to choose from
        @type parcel: Parcel
        @type verbose: bool
            For debugging purposes. Description of which package loaded into
            which truck
        @rtype: None

        === Precondition ===

        len(trucks) >= 1
        self._truck_order == 'non-decreasing' or 'non-increasing'
        """
        best_space = trucks[0].get_unused_space()
        best_truck = trucks[0]

        # non-decreasing = increasing = smallest has highest priority
        if self._truck_order == 'non-decreasing':
            for one_truck in trucks[1:]:
                if one_truck.get_unused_space() < best_space:
                    best_space = one_truck.get_unused_space()
                    best_truck = one_truck
        else:
            for one_truck in trucks[1:]:
                if one_truck.get_unused_space() > best_space:
                    best_space = one_truck.get_unused_space()
                    best_truck = one_truck

        if verbose:
            print("Truck #{} has loaded Parcel #{}"
                  .format(best_truck.get_id(), parcel.get_id()))
        best_truck.load_parcel(parcel)

    def schedule(self, parcels, trucks, verbose=False):
        """ Schedule parcels greedily

        <trucks> are mutated. Do not reuse <trucks> for another
        scheduler/trial.

        === Local Variables ===

        type queue: PriorityQueue
            Queue of parcels.
        type unused_parcel: [Parcel]
            If the parcel does not fit any truck, the parcel is appended to
            <unused_parcel>
        type one_parcel: Parcel
            An element of <parcels> or <queue>
        type trucks_with_space: [Truck]
            List of trucks with space
        """
        queue = PriorityQueue(self._greater_priority)
        unused_parcel = []
        for one_parcel in parcels:
            queue.add(one_parcel)

        while queue.is_empty() is False:
            one_parcel = queue.remove()

            trucks_with_space = []
            for one_truck in trucks:
                if one_truck.get_unused_space() >= one_parcel.get_volume():
                    trucks_with_space.append(one_truck)

            trucks_with_destination = []
            for one_truck in trucks_with_space:
                if one_truck.city_in_route(one_parcel.get_destination()):
                    trucks_with_destination.append(one_truck)

            # if there is at least 1 suitable truck with the destination,
            # trucks without the destination will not be considered.
            if len(trucks_with_destination) > 0:
                trucks_with_space = trucks_with_destination

            if len(trucks_with_space) > 0:
                self._choose_load_truck(trucks_with_space, one_parcel, verbose)
            else:
                if verbose:
                    print("Parcel #{} was not loaded."
                          .format(one_parcel.get_id()))
                unused_parcel.append(one_parcel)
        return unused_parcel


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='.pylintrc')
