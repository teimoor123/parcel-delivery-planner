"""Distance map
This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """Distance map of distances between cities.

    === Private Attributes ===
    _distances: distances between city1 and city2

    === Sample Usage ===
    >>> m = DistanceMap()
    >>> m.add_distance('Toronto', 'Ajax', 9)
    >>> m.distance('Toronto', 'Ajax')
    9
    """
    _distances: Dict[tuple, int]

    def __init__(self) -> None:
        self._distances = {}

    def distance(self, city1: str, city2: str) -> int:
        """Return the distance from city1 to city 2 or -1 if they are not
         contained in this map.
         """
        if (city1, city2) in self._distances:
            return self._distances[(city1, city2)]
        if city1 == city2:
            return 0
        return -1

    def add_distance(self, city1: str, city2: str, distance1: int,
                     distance2: int = -1) -> None:
        """Add the distance distance1 for city1 to city2 and distance2 for
        city2 to city1 if provided.
        """
        self._distances[(city1, city2)] = distance1
        self._distances[(city2, city1)] = distance2
        if distance2 == -1:
            self._distances[(city2, city1)] = distance1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
