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

from collections import namedtuple
import shlex
import argparse
import logging

from . import draw

Event = namedtuple('Event', ['start', 'stop', 'group', 'title'])


class Timeline:

    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)


def parse_timeline(file):
    timeline = Timeline()
    for line in file:
        start, stop, group, title = shlex.split(line)
        start = int(start)
        stop = int(stop)
        event = Event(start, stop, group, title)
        timeline.add_event(event)
    return timeline


def main():
    logging.basicConfig(level='DEBUG')
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()
    with open(args.file) as file:
        timeline = parse_timeline(file)
    draw.text_draw(timeline)
