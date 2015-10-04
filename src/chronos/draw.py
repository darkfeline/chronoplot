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
import math

from . import timeline as tline

_LOGGER = logging.getLogger(__name__)


def _scale(scalar, value):
    """Scale an integer value."""
    return round(value * scalar)


def _box_cost(width, scalar, event):
    """Calculate cost (extra space) for drawing event."""
    lines = textwrap.wrap(event.title, width - 4)
    height = _scale(scalar, event.stop - event.start)
    return height - len(lines)


class _Timeline(tline.Timeline):

    @classmethod
    def load(cls, timeline):
        new = cls()
        new.events = timeline.events
        return new

    def min_cost(self, width, scalar):
        """Calculate minimum cost for events in timeline."""
        return min(_box_cost(width, scalar, event) for event in self.events)

    def calculate_scalar(self, width):
        """Calculate optimal height scalar for boxes.

        We are trying to minimize the lowest box cost, without any negative
        costs.

        """
        scalar = 1
        bot_bound = -math.inf
        top_bound = math.inf

        while True:
            _LOGGER.debug('Trying %s', scalar)
            cost = self.min_cost(width, scalar)
            if cost > 0:
                # Lower scalar.
                _LOGGER.debug('Too big: %s', cost)
                top_bound = scalar
                if bot_bound == -math.inf:
                    scalar /= 2
                else:
                    scalar = (bot_bound + scalar) / 2
            elif cost < 0:
                # Increase scalar.
                _LOGGER.debug('Too small: %s', cost)
                bot_bound = scalar
                if top_bound == math.inf:
                    scalar *= 2
                else:
                    scalar = (top_bound + scalar) / 2
            else:
                _LOGGER.debug('Just right: %s', cost)
                return scalar

    def range(self):
        """Calculate width of timeline."""
        start = math.inf
        stop = -math.inf
        for event in self.events:
            if event.start < start:
                start = event.start
            if event.stop > stop:
                stop = event.stop
        return start, stop


class _Box:

    def __init__(self, width, height, text):
        self.width = width
        self.height = height
        self.text = text

    def format(self):
        lines = textwrap.wrap(self.text, self.width - 4)
        lines = ['| ' + x + ' |' for x in lines]
        hrule = '+' + '-' * (self.width - 2)
        lines.insert(hrule, 0)
        lines.append(hrule)
        return lines


def text_draw(timeline):
    timeline = _Timeline.load(timeline)
    box_width = 20
    # Calculate height/time scalar.
    scalar = timeline.calculate_scalar(box_width)
    # Calculate width for timeline.
    start, stop = timeline.range()
    timeline_width = math.ceil(max(math.log10(abs(x)) if x != 0 else 1
                                   for x in (start, stop)))
    # Make timeline.
    lines = [format(_scale(1 / scalar, x), '>{}'.format(timeline_width)) + ' -'
             if x % 5 == 0 else
             ' ' * timeline_width + ' |'
             for x in range(_scale(scalar, start), _scale(scalar, stop) + 1)]
    for x in lines:
        print(x)
