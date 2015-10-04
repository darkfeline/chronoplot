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


class _Time:

    def __init__(self, scalar, value):
        self.value = value
        self._scalar = scalar

    @property
    def scaled(self):
        return round(self.value * self._scalar)


def _box_cost(width, scalar, event):
    """Calculate cost (extra space) for drawing event.

    Cost 0 means the text fits snugly into the box.
    Cost 1 means the box has an extra blank line.
    Cost -1 means the text overflows by one line.

    """
    lines = textwrap.wrap(event.text, width - 4)
    height = _Time(scalar, event.stop - event.start).scaled
    return height - len(lines) - 2


class _Timeline(tline.Timeline):

    @classmethod
    def load(cls, timeline):
        new = cls()
        new.events = timeline.events
        new.groups = timeline.groups
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


def _format_event(event, width, scalar):
    """Format an event.

    Returns a list of strings that is the event formatted into a text box.

    """
    start = _Time(scalar, event.start)
    # Build box.
    lines = ['|{}|'.format(' ' * (width - 2))
             for _ in range(start.scaled,
                            _Time(scalar, event.stop).scaled + 1)]
    hrule = '+{}+'.format('-' * (width - 2))
    lines[0] = hrule
    lines[-1] = hrule

    # Format text.
    text_lines = textwrap.wrap(event.text, width - 4)
    text_lines = [format(x, '^{}'.format(width - 4)) for x in text_lines]
    text_lines = ['| ' + x + ' |' for x in text_lines]

    # Insert text into center of box.
    diff = (len(lines) - len(text_lines)) // 2
    for i, x in enumerate(text_lines):
        lines[diff + i] = x
    return start, lines


def text_draw(timeline):
    timeline = _Timeline.load(timeline)
    box_width = 20
    # Calculate height/time scalar.
    scalar = timeline.calculate_scalar(box_width)
    # Calculate width for timeline.
    start, stop = timeline.range()
    start = _Time(scalar, start)
    stop = _Time(scalar, stop)
    _LOGGER.debug('Start: %s, scaled: %s', start.value, start.scaled)
    _LOGGER.debug('Stop: %s, scaled: %s', stop.value, stop.scaled)

    # Make timeline.
    lines = [format(x / scalar)
             for x in range(start.scaled, stop.scaled + 1)]
    timeline_width = max(len(x) for x in lines)
    lines = [format(x, '>{}'.format(timeline_width)) + ' -'
             if i % 5 == 0 else
             ' ' * timeline_width + ' |'
             for i, x in enumerate(lines)]

    # Add events.
    for _, events in timeline.groups.items():
        group_lines = [' ' * (box_width) for _ in lines]
        # Use boxes to draw events.
        for event in events:
            box_start, box_lines = _format_event(event, box_width, scalar)
            _LOGGER.debug('%s %s', start.scaled, box_start.scaled)
            for i, x in enumerate(box_lines):
                _LOGGER.debug(x)
                group_lines[-start.scaled + box_start.scaled + i] = x
        # Add group events to timeline.
        lines = [' '.join(x) for x in zip(lines, group_lines)]
    # Print lines.
    for x in lines:
        print(x)
