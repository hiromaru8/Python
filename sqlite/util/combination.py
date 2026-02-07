
import itertools


import itertools

def gen_unique_pairs(n):
    """
    Generate unique (src_id, dest_id) pairs from a range of IDs.

    This generator yields all unordered pairs of IDs where:
    - IDs range from 1 to n (inclusive)
    - src_id is always less than dest_id
    - Self-pairs (e.g., (1, 1)) are excluded
    - Duplicate reversed pairs (e.g., (2, 1)) are excluded

    The function is implemented as a generator to avoid holding
    large numbers of combinations in memory, making it suitable
    for large n.

    Args:
        n (int): Total number of IDs. IDs will be generated
            in the range 1 to n (inclusive).

    Yields:
        tuple[int, int]: A tuple (src_id, dest_id) representing
        a unique unordered ID pair.

    Example:
        >>> for src, dest in gen_unique_pairs(4):
        ...     print(src, dest)
        1 2
        1 3
        1 4
        2 3
        2 4
        3 4
    """
    for src_id, dest_id in itertools.product(range(1, n + 1), repeat=2):
        if src_id < dest_id:
            yield src_id, dest_id

            



if __name__ == "__main__" :
    for pair in gen_unique_pairs(4):
        print(pair)
