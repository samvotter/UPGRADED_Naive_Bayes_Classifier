__author__="Sam Van Otterloo"

from numbers import Number
from math import e


# squashing function
def squash(
        x: float,
        **kwargs
) -> float:
    options = {
        'curve_center': 0,
        'flatten': 1,
        'max_value': 1
    }
    for arg in kwargs:
        if arg in options:
            options[arg] = kwargs[arg]
        else:
            print(f"ERROR! {arg} is not a valid option!")
            return 0.0
        if not isinstance(options[arg], Number):
            print(f"ERROR! {arg} must be a number.")
            return 0.0
    return (1/(1 + e ** ((-x + options['curve_center'])/options['flatten'])))*options['max_value']