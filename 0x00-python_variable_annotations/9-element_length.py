#!/usr/bin/env python3
"""A type-annotated function element_length"""
from typing import Iterable, Sequence, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples containing elements and their lengths"""
    return [(i, len(i)) for i in lst]
