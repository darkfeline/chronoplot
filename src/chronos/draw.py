# Copyright (C) 2015  Allen Li
#
# This file is part of chronos.
#
# chronos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# chronos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with chronos.  If not, see <http://www.gnu.org/licenses/>.

import textwrap
import logging

_LOGGER = logging.getLogger(__name__)


def _box_cost(width, scalar, event):
    """Calculate cost (extra space) for drawing event."""
    lines = textwrap.wrap(event.title, width - 4)
    height = round((event.stop - event.start) * scalar)
    return height - len(lines)


def _min_cost(width, scalar, timeline):
    """Calculate minimum cost for events in timeline."""
    return min(_box_cost(width, scalar, event) for event in timeline.events)


def _calculate_scalar(width, timeline):
    """Calculate optimal height scalar for boxes.

    We are trying to minimize the lowest box cost, without any negative costs.

    """
    scalar = 1
    min = float('-inf')
    max = float('inf')

    while True:
        _LOGGER.debug('Trying %s', scalar)
        cost = _min_cost(width, scalar, timeline)
        if cost > 0:
            # Lower scalar.
            _LOGGER.debug('Too big: %s', cost)
            max = scalar
            if min == float('-inf'):
                scalar /= 2
            else:
                scalar = (min + scalar) / 2
        elif cost < 0:
            # Increase scalar.
            _LOGGER.debug('Too small: %s', cost)
            min = scalar
            if max == float('inf'):
                scalar *= 2
            else:
                scalar = (max + scalar) / 2
        else:
            _LOGGER.debug('Just right: %s', cost)
            return scalar


class _Box:

    def __init__(self, text):
        self.width = 20
        self.height = 0
        self.text = text

    def format(self):
        lines = textwrap.wrap(self.text, self.width - 4)
        lines = ['| ' + x + ' |' for x in lines]
        hrule = '+' + '-' * (self.width - 2)
        lines.insert(hrule, 0)
        lines.append(hrule)


def text_draw(timeline):
    print(timeline.events)
    width = 20
    scalar = _calculate_scalar(width, timeline)
    print(scalar)
