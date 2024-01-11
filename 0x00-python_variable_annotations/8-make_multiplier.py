#!/usr/bin/env python3
"""A type-annotated function make_multiplier"""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function"""
    def multiplier_fun(x: float) -> float:
        """Multiplies a float by the given multiplier"""
        return x * multiplier

    return multiplier_fun
