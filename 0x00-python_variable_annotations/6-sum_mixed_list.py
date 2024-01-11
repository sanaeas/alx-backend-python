#!/usr/bin/env python3
"""A type-annotated function sum_mixed_list"""
from typing import List, Union


def sum_mixed_list(mxd_lst: List[Union[int, float]]) -> float:
    """Returns the sum of a list of integers and floats"""
    return sum(mxd_lst)
