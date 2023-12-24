"""Scheduling algorithms
This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.

    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.

        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.

        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.

        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


"===Helper Functions==="

def _lighter(a: Parcel, b: Parcel) -> bool:
    """
    Return True if parcel a is lighter than parcel b.
    """
    return a.volume < b.volume


def _heavier(a: Parcel, b: Parcel) -> bool:
    """
    Return True if parcel a is heavier than parcel b.
    """
    return a.volume > b.volume


def _smaller(a: Parcel, b: Parcel) -> bool:
    """
    Return True if parcel a destination is smaller than parcel b destination.
    """
    return a.dest < b.dest


def _longer(a: Parcel, b: Parcel) -> bool:
    """
    Return True if parcel a destination is longer than parcel b destination.
    """
    return a.dest > b.dest


def _most_space(a: Truck, b: Truck) -> bool:
    return a.vol_cap - a.vol_used > b.vol_cap - b.vol_used


def _least_space(a: Truck, b: Truck) -> bool:
    return a.vol_cap - a.vol_used < b.vol_cap - b.vol_used


class RandomScheduler(Scheduler):
    """A scheduler, deciding what parcels go onto which trucks, and
    what route each truck will take in any possible random order.

    ===== Private Attributes =====
    _parcels:
      List of all parcels objects in this scheduler.
    """
    _parcels: list

    def __init__(self) -> None:
        self._parcels = []

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        for p in parcels:
            self._parcels.append(p)
        shuffle(self._parcels)
        scheduled = []
        trucks2 = []
        for t in trucks:
            trucks2.append(t)
        while len(trucks2) > 0:
            t1 = choice(trucks2)
            for p2 in self._parcels:
                if t1.vol_cap - t1.vol_used >= p2.volume:
                    t1.pack(p2)
                    scheduled.append(p2)
            trucks2.remove(t1)
        for item in scheduled:
            self._parcels.remove(item)
        return self._parcels


class GreedyScheduler(Scheduler):
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take according to the given priorities and
    order parameters to achieve an efficient system.

    ===== Private Attributes =====
    _parcels: List of all parcels objects in this scheduler.
    _trucks: List of all trucks in this scheduler.
    """

    _parcels: list
    _trucks: list

    def __init__(self, config: dict) -> None:
        if config['parcel_priority'] == 'volume':
            if config['parcel_order'] == 'non-decreasing':
                self._parcels = PriorityQueue(_lighter)
            elif config['parcel_order'] == 'non-increasing':
                self._parcels = PriorityQueue(_heavier)
        elif config['parcel_priority'] == 'destination':
            if config['parcel_order'] == 'non-decreasing':
                self._parcels = PriorityQueue(_smaller)
            elif config['parcel_order'] == 'non-increasing':
                self._parcels = PriorityQueue(_longer)
        if config['truck_order'] == 'non-decreasing':
            self._trucks = PriorityQueue(_least_space)
        elif config['truck_order'] == 'non-increasing':
            self._trucks = PriorityQueue(_most_space)

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        for parcel in parcels:
            self._parcels.add(parcel)
        parcels2 = []
        while not self._parcels.is_empty():
            parcels2.append(self._parcels.remove())
        scheduled = []
        for p in parcels2:
            i = 0
            packed = False
            for truck in trucks:
                self._trucks.add(truck)
            trucks2 = []
            while not self._trucks.is_empty():
                trucks2.append(self._trucks.remove())
            for t in trucks2:
                if len(t.route) == 1 and t.vol_cap - t.vol_used >= p.volume and\
                        t.route[len(t.route) - 1] == p.dest and packed is False:
                    t.pack(p)
                    scheduled.append(p)
                    packed = True
                elif len(t.route) > 1 and t.vol_cap - t.vol_used >= p.volume \
                        and t.route[len(t.route) - 2] == p.dest and \
                        packed is False:
                    t.pack(p)
                    scheduled.append(p)
                    packed = True
            while i < len(trucks2) and packed is False:
                if trucks2[i].vol_cap - trucks2[i].vol_used >= p.volume:
                    trucks2[i].pack(p)
                    scheduled.append(p)
                    packed = True
                i += 1
        for item in scheduled:
            parcels2.remove(item)
        return parcels2


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
