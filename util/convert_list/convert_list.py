"""
convert_list.py

"""


def split_list(lst:list, n:int) -> list[list]:
    """Split a list into n nearly equal parts.

    Args:
        lst (list)  : The list to split. example: [1, 2, 3, 4, 5]
        n (int)     : The number of parts to split the list into. example: 3

    Returns:
        list[list]: A list of n sublists. example: [[1, 2], [3, 4], [5]]
    """
    k, m = divmod(len(lst), n)
    return [lst[i*k + min(i,m):(i+1)*k + min(i+1,m)] for i in range(n)]


def chunk_list(lst:list, n:int) -> list[list]:
    """Split a list into chunks of size n.

    Args:
        lst (list): The list to split. example: [1, 2, 3, 4, 5]
        n (int): The size of each chunk. example: 2

    Returns:
        list[list]: A list of chunks. example: [[1, 2], [3, 4], [5]]
    """
    return [lst[i:i+n] for i in range(0, len(lst), n)]

# util/convert_list/convert_list.py
