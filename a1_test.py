"""
Unittests for Compare Parcel Algorithm.
"""

import unittest
from experiment import SchedulingExperiment


# -----------------------------------------------------------------------------
# Don't change this code!
# Unlike other sets of unit tests, rather than defining them explicitly, we're
# using helpers to generate them automatically.
# Skip down to the bottom of the file to see how you can add new tests.
# -----------------------------------------------------------------------------
class TestExperiment(unittest.TestCase):
    pass


def check_stat(config, stat, val):
    def test(self):
        experiment = SchedulingExperiment(config)
        results = experiment.run()
        self.assertEqual(round(results[stat], 1), round(val, 1))
    return test


def make_test(id, config, expected_stats):
    """Helper for making tests.

    Since all of the tests have the same format, it's useful to use this
    helper function instead of repeating lots of code.
    """
    root = 'test_' + id
    for key, value in expected_stats.items():
        setattr(TestExperiment,
                root + '__' + key,
                check_stat(config, key, value))


# -----------------------------------------------------------------------------
# Add your tests here!
# All tests will be in the form
# make_test(<test-name>, <config_dict>, <expected_stats_dict>)
#
# NOTE: if you get a "FileNotFoundError", try replacing the filename
# with the full path to the file (e.g., "C:\\Users\\David\\Documents\\...")
# -----------------------------------------------------------------------------

# Sample test


make_test('greedy_algorithm, parcel_priority_destination, parcel: non-increasing, truck: non-decreasing',
          {
            'depot_location': 'Toronto',
            'parcel_file': 'data/demo-parcel-data-small.txt',
            'truck_file': 'data/demo-truck-data-some_can_fit.txt',
            'map_file': 'data/map-data-2.txt',
            'algorithm': 'greedy',
            'parcel_priority': 'destination',
            'parcel_order': 'non-increasing',
            'truck_order': 'non-decreasing',
            'verbose': 'false'},
          {
              'fleet': 6,
              'unused_trucks': 3,
              'unused_space': 21,
              'avg_distance': 172,
              'avg_fullness': 80.7,
              'unscheduled': 0
          })
make_test('greedy_algorithm, parcel_priority_destination, parcel: non-decreasing, truck: non-decreasing',
          {
            'depot_location': 'Toronto',
            'parcel_file': 'data/demo-parcel-data-small.txt',
            'truck_file': 'data/demo-truck-data-some_can_fit.txt',
            'map_file': 'data/map-data-2.txt',
            'algorithm': 'greedy',
            'parcel_priority': 'destination',
            'parcel_order': 'non-decreasing',
            'truck_order': 'non-decreasing',
            'verbose': 'false'},
          {
              'fleet': 6,
              'unused_trucks': 2,
              'unused_space': 58,
              'avg_distance': 164.8,
              'avg_fullness': 59.3,
              'unscheduled': 0
          })

make_test('some-can-fit-greedy-nondecreasingparcel-noincreasingtruck',
          {
            'depot_location': 'Toronto',
            'parcel_file': 'data/demo-parcel-data-small.txt',
            'truck_file': 'data/demo-truck-data-some_can_fit.txt',
            'map_file': 'data/map-data-2.txt',
            'algorithm': 'greedy',
            'parcel_priority': 'volume',
            'parcel_order': 'non-decreasing',
            'truck_order': 'non-increasing',
            'verbose': 'false'},
          {
              'fleet': 6,
              'unused_trucks': 2,
              'unused_space': 69,
              'avg_distance': 168.5,
              'avg_fullness': 54.7,
              'unscheduled': 0
          })
make_test('none-can-fit-random',
          {
            'depot_location': 'Toronto',
            'parcel_file': 'data/demo-parcel-data-small.txt',
            'truck_file': 'data/demo-truck-data-none_can_fit.txt',
            'map_file': 'data/map-data-2.txt',
            'algorithm': 'random',
            'parcel_priority': 'volume',
            'parcel_order': 'non-decreasing',
            'truck_order': 'non-decreasing',
            'verbose': 'false'},
          {
              'fleet': 5,
              'unused_trucks': 5,
              'unused_space': 0,
              'avg_distance': 0,
              'avg_fullness': 100,
              'unscheduled': 5
          })
make_test('none-can-fit-greedy',
          {
            'depot_location': 'Toronto',
            'parcel_file': 'data/demo-parcel-data-small.txt',
            'truck_file': 'data/demo-truck-data-none_can_fit.txt',
            'map_file': 'data/map-data-2.txt',
            'algorithm': 'greedy',
            'parcel_priority': 'volume',
            'parcel_order': 'non-decreasing',
            'truck_order': 'non-decreasing',
            'verbose': 'false'},
          {
              'fleet': 5,
              'unused_trucks': 5,
              'unused_space': 0,
              'avg_distance': 0,
              'avg_fullness': 100,
              'unscheduled': 5
          })
make_test('1-small',
          {
            'depot_location': 'Toronto',
            'parcel_file': 'data/parcel-data-small.txt',
            'truck_file': 'data/truck-data-small.txt',
            'map_file': 'data/map-data-2.txt',
            'algorithm': 'greedy',
            'parcel_priority': 'volume',
            'parcel_order': 'non-decreasing',
            'truck_order': 'non-decreasing',
            'verbose': 'false'},
          {
              'fleet': 3,
              'unused_trucks': 0,
              'unused_space': 0,
              'avg_distance': 96.3,
              'avg_fullness': 100,
              'unscheduled': 0
          })

if __name__ == '__main__':
    unittest.main()
