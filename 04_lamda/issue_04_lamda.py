import itertools
import funcy
import copy
import collections
from collections import Iterable


def ilen(iterable: iter):
    """
    >>> foo = (x for x in range(10))
    >>> ilen(foo)
    10

    >>> ilen([1,3,4,5,6])
    5

    """
    return len(list(iterable))


def flatten(iterable: iter):
    """
    >>> list(flatten([0, [1, [2, 3]]]))
    [0, 1, 2, 3]
    """
    for el in iterable:
        if isinstance(el, Iterable):
            yield from flatten(el)
        else:
            yield el


def distinct(iterable: iter):
    """
    >>> list(distinct([1, 2, 0, 1, 3, 0, 2]))
    [1, 2, 0, 3]
    """
    # for el in {x:None for x in iterable}.keys():
    #     yield el
    # yield collections.OrderedDict.fromkeys(iterable)
    # yeild set(iterable)
    #
    dub = set()
    for el in iterable:
        if el not in dub:
            dub.add(el)
            yield el
    # yield dict.fromkeys(iterable)


def groupby(keys, iterable: iter):
    """
    >>> users = [{'gender': 'female', 'age': 33},{'gender': 'male', 'age': 20},{'gender': 'female', 'age': 21}]
    >>> groupby('gender', users) # doctest: +NORMALIZE_WHITESPACE
    {'female': [{'gender': 'female', 'age': 33}, {'gender': 'female', 'age': 21}], 'male': [{'gender': 'male', 'age': 20}]}

    >>> groupby('age', users) # doctest: +NORMALIZE_WHITESPACE
    {33: [{'gender': 'female', 'age': 33}],
    20: [{'gender': 'male', 'age': 20}],
    21: [{'gender': 'female', 'age': 21}]}

    """
    res = {}
    # for key, group in itertools.groupby(list(iterable), key=lambda x, y=keys: x[y]):
    #     if key not in res:
    #         res[key] = list(group)
    #     else:
    #         res[key].append(tuple(group)[0])
    # return res
    for item in iterable:
        for key, value in item.items():
            if key == keys:
                l = res.get(value, [])
                l.append(item)
                res[value] = l

    return res


def chunks(size: int, iterable):
    """
    >>> list(chunks(3, [0, 1, 2, 3, 4]))
    [(0, 1, 2), (3, 4)]
    """
    # return funcy.chunks(size,iterable)
    it = iter(iterable)
    while True:
        grouper = tuple(itertools.islice(it, size))
        if not grouper:
            return
        yield grouper


def first(iterable: iter):
    """
    >>> foo = (x for x in range(10))
    >>> first(foo)
    0
    >>> print(first(range(0)))
    None
    """
    # return funcy.first(iterable)
    try:
        return next(iterable, None)
    except TypeError:
        return None


def last(iterable: Iterable):
    """
    >>> foo = (x for x in range(10))
    >>> last(foo)
    9
    >>> print(last(range(0)))
    None
    """
    # return funcy.last(iterable)
    it = None
    try:
        for it in iterable:
            pass
        return it
    except TypeError:
        return None
    except StopIteration:
        return None


def islice(iterable: Iterable, start, stop):
    """
    >>> foo = (x for x in range(10))
    >>> islice(foo, None, 3)
    [0, 1, 2]
    >>> foo = (x for x in range(10))
    >>> islice(foo, -3, None)
    [7, 8, 9]
    """
    it, iterable = itertools.tee(iterable)
    return list(it)[slice(start, stop)]
