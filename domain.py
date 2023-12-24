""" Domain classes
"""

from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    # It must be consistent with the Fleet class docstring examples below.
    """A parcel.

    === Public Attributes ===
    id: unique id of this parcel
    volume: volume of this parcel in cubic centimetres
    source: name of the city where this came from
    dest: name of the city where this must be delivered to

    === Sample Usage ===
    >>> p = Parcel(1, 3, 'Toronto', 'Barrie')
    >>> p.dest
    'Barrie'
    >>> p.volume
    3
    """
    id: int
    volume: int
    source: str
    dest: str

    def __init__(self, p_id: int, volume: int, source: str, dest: str) -> None:
        """Create a parcel with a unique id, volume, source and destination
        cities.
        """
        self.id = p_id
        self.volume = volume
        self.source = source
        self.dest = dest


class Truck:
    # It must be consistent with the Fleet class docstring examples below.
    """A truck.

    === Public Attributes ===
    id: unique id of this truck
    vol_cap: volume capacity of this truck in cubic centimetres
    route: cities that this truck must go to
    vol_used: current volume used by parcels
    parcels: list of parcels inside this truck

    === Sample Usage ===
    >>> t = Truck(1234, 300, 'Toronto')
    >>> t.route
    ['Toronto']
    >>> t.vol_cap
    300
    """
    id: int
    vol_cap: int
    route: list
    vol_used: int
    parcels: list

    def __init__(self, t_id: int, vol_cap: int, depot: str) -> None:
        """Create a truck with a unique id t_id, volume capacity vol_cap,
        and depot city depot.
        """
        self.id = t_id
        self.vol_cap = vol_cap
        self.route = [depot]
        self.vol_used = 0
        self.parcels = []

    def pack(self, p: Parcel) -> bool:
        """Pack parcel p onto this truck if there is enough space. Return True
         if p is packed onto the truck.
        """
        if p.volume <= (self.vol_cap - self.vol_used):
            self.parcels.append(p)
            self.vol_used += p.volume
            if len(self.route) > 1:
                self.route.pop()
            if p.dest not in self.route:
                self.route.append(p.dest)
            self.route.append(self.route[0])
            return True
        return False

    def fullness(self) -> None:
        """Return the percentage of used space in this truck.

        >>> t = Truck(1234, 100, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> t.fullness()
        5.0

        """
        percent = (self.vol_used / self.vol_cap) * 100
        return round(percent, 1)


class Fleet:
    """ A fleet of trucks for making deliveries.

    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.

        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

        # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet
        """
        return 'trucks: ' + str(self.trucks)

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        count = 0
        for truck in self.trucks:
            if truck.vol_used > 0:
                count += 1
        return count

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        d = {}
        for truck in self.trucks:
            parcels = []
            for parcel in truck.parcels:
                parcels.append(parcel.id)
            d[truck.id] = parcels
        return d

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        unused_space = 0
        for truck in self.trucks:
            unused_space += (truck.vol_cap - truck.vol_used)
        return unused_space

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        fullness = 0
        for truck in self.trucks:
            fullness += truck.fullness()
        return fullness

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        total_fullness = 0
        count = 0
        for truck in self.trucks:
            if truck.vol_used > 0:
                total_fullness += truck.fullness()
                count += 1
        return total_fullness / count

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        total_distance = 0
        for truck in self.trucks:
            if len(truck.route) < 3:
                total_distance = 0
            else:
                i = 0
                while i < len(truck.route) - 1:
                    total_distance += dmap.distance(truck.route[i],
                                                    truck.route[i + 1])
                    i += 1
        return total_distance

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Include in the average only trucks that have actually travelled some
        non-zero distance.

        Preconditions:
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> from distance_map import DistanceMap
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        total_distance = self.total_distance_travelled(dmap)
        count = 0
        for truck in self.trucks:
            truck_distance = 0
            if len(truck.route) < 3:
                truck_distance = 0
            else:
                i = 0
                while i < len(truck.route) - 1:
                    truck_distance += dmap.distance(truck.route[i],
                                                    truck.route[i + 1])
                    i += 1
            if truck_distance > 0:
                count += 1
        return total_distance / count


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
