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

import shlex
import argparse
import logging

from . import draw
from . import timeline as tline


def parse_timeline(file):
    timeline = tline.Timeline()
    for line in file:
        start, stop, group, text = shlex.split(line)
        start = float(start)
        stop = float(stop)
        event = tline.Event(start, stop, group, text)
        timeline.add_event(event)
    return timeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level='DEBUG')
    else:
        logging.basicConfig(level='INFO')
    with open(args.file) as file:
        timeline = parse_timeline(file)
    draw.text_draw(timeline)
