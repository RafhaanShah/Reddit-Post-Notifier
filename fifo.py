"""FIFO Set implementation.

This module provides a FIFOSet class, which behaves like a set
with a maximum size and first-in-first-out eviction policy.
"""

from collections import OrderedDict


class FIFOSet:
    """A set with FIFO eviction and a maximum size.

    When the set exceeds the configured maximum size,
    the oldest element is removed automatically.
    """

    def __init__(self, max_size=100):
        """Initialize the FIFOSet.

        Args:
            max_size (int): Maximum number of items to retain.
        """
        self.max_size = max_size
        self.data = OrderedDict()

    def add(self, item):
        """Add an item to the set.

        If the item is already present, it is ignored.
        If the set is full, the oldest item is evicted.

        Args:
            item: The item to add.
        """
        if item in self.data:
            return
        if len(self.data) >= self.max_size:
            self.data.popitem(last=False)
        self.data[item] = None

    def __contains__(self, item):
        """Check if an item is in the set (O(1))."""
        return item in self.data

    def __len__(self):
        """Return the number of items in the set."""
        return len(self.data)

    def __iter__(self):
        """Iterate over the items in FIFO order."""
        return iter(self.data)

    def __repr__(self):
        """Return a string representation of the set."""
        return f"FIFOSet({list(self.data.keys())})"
