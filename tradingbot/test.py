# -*- coding: utf-8 -*-
from collections import namedtuple
Car = namedtuple('Car', ['color', 'mileage'])
my_car = Car('red', 3812.4)
values = my_car._asdict().values()
print tuple(values)