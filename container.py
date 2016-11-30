
"""container.py

=== Credit ===

Allan Chang
    1003235983
Isaac Seah
    1001753051
Last edited: Oct 14, 2016

=== Classes ===

Container
    Container is used to represent an object that carries objects. Container
    will not be accessed by the client. Container will not be instantialised.
PriorityQueue
    Container that sorts objects as it gets added. Container can be accessed by
    client or scheduler.py.
"""


class Container:
    """A container that holds Objects.

    This is an abstract class.  Only child classes should be instantiated.
    """
    def add(self, item):
        """Add <item> to this Container.

        === Parameter and Return Types ===

        @type self: Container
        @type item: Object
        @rtype: None
        """
        raise NotImplementedError

    def remove(self):
        """Remove and return a single item from this Container.

        === Parameter and Return Types ===

        @type self: Container
        @rtype: Object
        """
        raise NotImplementedError

    def is_empty(self):
        """Return True iff this Container is empty.

        === Parameter and Return Types ===

        @type self: Container
        @rtype: bool
        """
        raise NotImplementedError


class PriorityQueue(Container):
    """A queue of items that operates in FIFO-priority order.

    Items are removed from the queue according to priority; the item with the
    highest priority is removed first.  Ties are resolved in first-in-first-out
    (FIFO) order, meaning the item which was inserted *earlier* is the first one
    to be removed.

    Priority is defined by the <less_than> function that is provided at time
    of construction.  If x < y, then x has a *HIGHER* priority than y.
    (Intuitively, something with "priority 1" is more important than something
    with "priority 10".)

    All objects in the container must be of the same type.

    === Private Attributes ===

    @type _queue: List
        The end of the list represents the *front* of the queue, that is,
        the next item to be removed.
    @type _less_than: Callable[[Object, Object], bool]
        If _less_than(x, y) is true, then x has higher priority than y
        and should be removed from the queue before y.

    === Representation Invariants ===

    - all elements of _queue are of the same type
    - the elements of _queue are appropriate arguments for function less_than
    - the elements of _queue are in order according to function less_than.
    """

    def __init__(self, less_than):
        """Initialize this to an empty PriorityQueue.

        === Parameter and Return Types ===

        @type self: PriorityQueue
        @type less_than: Callable[[Object, Object], bool]
            Determines the relative priority of two elements of the queue.
            If less_than(x, y) is true, then x has higher priority than y.
        @rtype: None
        """
        self._queue = []
        self._less_than = less_than

    def add(self, item):
        """Add <item> to this PriorityQueue.

        === Preconditions ===

        Unless there are 0 items in <self._queue>,
            type(item) == type(self._queue[0])

        === Examples ===

        >>> def shorter(a, b):
        ...    return len(a) < len(b)
        ...
        >>>
        >>> # Define a PriorityQueue with priority on shorter strings.
        >>> # I.e., when we remove, we get the shortest remaining string.
        >>> pq = PriorityQueue(shorter)
        >>> pq.add('fred')
        >>> pq.add('arju')
        >>> pq.add('monalisa')
        >>> pq.add('hat')
        >>> pq._queue
        ['monalisa', 'arju', 'fred', 'hat']
        >>> pq.remove()
        'hat'
        >>> pq._queue
        ['monalisa', 'arju', 'fred']
        """

        # Wants to place item at the end of _queue list first
        queue_placement = len(self._queue)
        higher_priority = False
        if queue_placement == 0:
            # If there are no items in the list, just add the item into the list
            self._queue.append(item)
        else:
            # While the program there are still items to compare
            while queue_placement >= 1 and higher_priority is False:
                # If item has a higher priority, stop searching. Else, continue
                # searching a lower priority object
                higher_priority = self.\
                    _less_than(item, self._queue[queue_placement - 1])
                if higher_priority is False:
                    queue_placement -= 1
            self._queue.insert(queue_placement, item)

    def remove(self):
        """Remove and return the next item from this PriorityQueue.

        === Preconditions ===

        len(self._queue) > 0

        === Examples ===

        >>> def shorter(a, b):
        ...    return len(a) < len(b)
        ...
        >>>
        >>> # When we hit the tie, the one that was added first will be
        >>> # removed first.
        >>> pq = PriorityQueue(shorter)
        >>> pq.add('fred')
        >>> pq.add('arju')
        >>> pq.add('monalisa')
        >>> pq.add('hat')
        >>> pq.remove()
        'hat'
        >>> pq.remove()
        'fred'
        >>> pq.remove()
        'arju'
        >>> pq.remove()
        'monalisa'
        """
        return self._queue.pop()

    def is_empty(self):
        """Return True iff this PriorityQueue is empty.

        === Examples ===

        >>> def lt(a, b):
        ...    return a < b
        ...
        >>>
        >>> pq = PriorityQueue(lt)
        >>> pq.is_empty()
        True
        >>> pq.add('fred')
        >>> pq.is_empty()
        False
        """
        return not self._queue


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config='.pylintrc')
