#!/bin/python

from music21.interval import Interval
from music21.pitch import Pitch
from music21.converter import parseFile

from os.path import basename
import sys

def get_interval(key):
    if key.mode == 'major':
        return Interval(key.tonic, Pitch('C'))

    if key.mode == 'minor':
        return Interval(key.tonic, Pitch('A'))

    return None

for filename in sys.argv[1:]:
    score = parseFile(filename)
    key = score.analyze('key')
    interval = get_interval(key)
    score.transpose(interval)
    score.write('musicxml', basename(filename) + '.xml')
