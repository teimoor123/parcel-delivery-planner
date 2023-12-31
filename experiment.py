"""Running experiments
This module contains class SchedulingExperiment.  It can create an experiment
with input data and an algorithm configuration specified in a dictionary, then
run the experiment, generate statistics as the result of the experiment, and
(optionally) report the statistics.

This module is responsible for all the reading of data from the data files.
"""
from typing import List, Dict, Union
import json
from scheduler import RandomScheduler, GreedyScheduler, Scheduler
from domain import Parcel, Truck, Fleet
from distance_map import DistanceMap


class SchedulingExperiment:
    """An experiment in scheduling parcels for delivery.

    To complete an experiment involves four stages:

    1. Read in all data from necessary files, and create corresponding objects.
    2. Run a scheduling algorithm to assign parcels to trucks.
    3. Compute statistics showing how good the assignment of parcels to trucks
       is.
    4. Report the statistics from the experiment.

    === Public Attributes ===
    verbose:
      If <verbose> is True, print step-by-step details regarding the scheduling
      algorithm as it runs.
    scheduler:
      The scheduler to use in this experiment.
    parcels:
      The parcels to schedule in this experiment.
    fleet:
      The trucks that parcels are scheduled to in this experiment.
    dmap:
      The distances between cities in this experiment.

    === Private Attributes ===
    _stats:
      A dictionary of statistics. <_stats>'s value is undefined until
      <self>._compute_stats is called, at which point it contains keys and
      values.
    _unscheduled:
      A list of parcels. <_unscheduled>'s value is undefined until <self>.run
      is called, at which point it contains the list of parcels that could
      not be scheduled in the experiment.

    === Representation Invariants ===
    - <fleet> contains at least one truck
    - <dmap> contains all of the distances required to compute the length of
      any possible route for the trucks in <fleet> delivering the packages in
      <parcels>.
    """
    verbose: bool
    scheduler: Scheduler
    parcels: List[Parcel]
    fleet: Fleet
    dmap: DistanceMap
    _stats: Dict[str, Union[int, float]]
    _unscheduled: List[Parcel]

    def __init__(self, config: Dict[str, Union[str, bool]]) -> None:
        """Initialize a new experiment with the configuration specified in
        <config>.

        Precondition: <config> contains keys and values.
        """
        self.verbose = config['verbose']

        self.parcels = read_parcels(config['parcel_file'])
        self.fleet = read_trucks(config['truck_file'],
                                 config['depot_location'])
        self.dmap = read_distance_map(config['map_file'])

        if config['algorithm'] == 'greedy':
            self.scheduler = GreedyScheduler(config)
        elif config['algorithm'] == 'random':
            self.scheduler = RandomScheduler()

        self._stats = {}
        self._unscheduled = []

    def run(self, report: bool = False) -> Dict[str, Union[int, float]]:
        """Run the experiment and return statistics on the outcome.

        The return value is a dictionary with keys and values..

        If <report> is True, print a report on the statistics from this
        experiment.  Either way, return the statistics in a dictionary.

        If <self.verbose> is True, print step-by-step details
        regarding the scheduling algorithm as it runs.
        """

        self._unscheduled = self.scheduler.schedule(self.parcels,
                                                    self.fleet.trucks)
        self._compute_stats()
        if report:
            self._print_report()
        return self._stats

    def _compute_stats(self) -> None:
        """Compute the statistics for this experiment, and store in
        <self>.stats.

        Precondition: _run has already been called.
        """
        unused = (self.fleet.num_trucks() - self.fleet.num_nonempty_trucks())
        self._stats = {
            'fleet': self.fleet.num_trucks(),
            'unused_trucks': unused,
            'avg_distance': self.fleet.average_distance_travelled(self.dmap),
            'avg_fullness': self.fleet.average_fullness(),
            'unused_space': self.fleet.total_unused_space(),
            'unscheduled': len(self._unscheduled)
        }

    def _print_report(self) -> None:
        """Report on the statistics for this experiment.

        This method is *only* for debugging purposes for your benefit, so
        the content and format of the report is your choice; we
        will not call your run method with <report> set to True.

        Precondition: _compute_stats has already been called.
        """
        print(self._stats)


    # ----- Helper functions -----


def read_parcels(parcel_file: str) -> List[Parcel]:
    """Read parcel data from <parcel_file> and return.

    Precondition: <parcel_file> is the path to a file containing parcel data.
    """
    p_list = []
    # read and add the parcels to the list.
    with open(parcel_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            pid = int(tokens[0].strip())
            source = tokens[1].strip()
            destination = tokens[2].strip()
            volume = int(tokens[3].strip())
            p_list.append(Parcel(pid, volume, source, destination))
    return p_list


def read_distance_map(distance_map_file: str) -> DistanceMap:
    """Read distance data from <distance_map_file> and return a DistanceMap
    that records it.

    Precondition: <distance_map_file> is the path to a file containing distance
                  data.
    """
    d_map = DistanceMap()
    with open(distance_map_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            c1 = tokens[0].strip()
            c2 = tokens[1].strip()
            distance1 = int(tokens[2].strip())
            distance2 = int(tokens[3].strip()) if len(tokens) == 4 \
                else distance1
            d_map.add_distance(c1, c2, distance1)
            if len(tokens) == 4:
                d_map.add_distance(c1, c2, distance1, distance2)
    return d_map


def read_trucks(truck_file: str, depot_location: str) -> Fleet:
    """Read truck data from <truck_file> and return a Fleet containing these
    trucks, with each truck starting at the <depot_location>.

    Precondition: <truck_file> is a path to a file containing truck data.
    """
    f = Fleet()
    with open(truck_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            tid = int(tokens[0])
            capacity = int(tokens[1])
            f.add_truck(Truck(tid, capacity, depot_location))
    return f


def simple_check(config_file: str) -> None:
    """Configure and run a single experiment on the scheduling problem
    defined in <config_file>.

    Precondition: <config_file> is a json file with keys and values.
    """
    # Read an experiment configuration from a file and build a dictionary
    # from it.
    with open(config_file, 'r') as file:
        configuration = json.load(file)
        # Create and run an experiment with that configuration.
    experiment = SchedulingExperiment(configuration)
    experiment.run(report=True)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['read_parcels', 'read_distance_map', 'read_trucks',
                       '_print_report', 'simple_check'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'json', 'scheduler', 'domain',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    # ------------------------------------------------------------------------
    # The following code can be used as a quick and simple check to see if your
    # experiment can run without errors.
    # ------------------------------------------------------------------------
    simple_check('data/demo.json')
