"""

This module generates random parcel and truck data and writes each to a file.
Values defined in the module control the amount of data, the range of possible
values, etc.

"""
from random import randint, choice


def main():
    """Generate random truck and parcel data.
    """

    # Set constants for names of the output files
    parcel_filename = 'data/demo-parcel-data-small.txt'
    truck_filename = 'data/demo-truck-data-some_can_fit.txt'

    # Set constants controlling parcel data
    num_ids_to_pick_from = 5000
    num_ids = 5
    cities = ['Belleville', 'Guelph', 'Hamilton', 'Toronto']
    min_volume = 1
    max_volume = 35

    # Generate some random parcels
    ids = list(range(num_ids_to_pick_from))
    with open(parcel_filename, 'w') as file:
        for dummy in range(num_ids):
            # Pick a random id from among those left and remove it so we
            # don't pick it again.
            id_ = choice(ids)
            ids.remove(id_)
            source = choice(cities)
            temp = cities.copy()
            temp.remove(source)
            destination = choice(temp)
            volume = randint(min_volume, max_volume)
            file.write("%s, %s, %s, %s\n" % (id_, source, destination, volume))

    # Set constants controlling truck data
    num_ids_to_pick_from = 1000
    num_ids = 5
    min_volume = 30
    max_volume = 50

    # Generate some random trucks
    ids = list(range(num_ids_to_pick_from))
    with open(truck_filename, 'w') as file:
        for dummy in range(num_ids):
            # Pick a random id from among those left and remove it so we
            # don't pick it again.
            id_ = choice(ids)
            ids.remove(id_)
            volume = randint(min_volume, max_volume)
            file.write("%s, %s\n" % (id_, volume))

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='.pylintrc')
    main()
