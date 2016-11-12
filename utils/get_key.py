#!/bin/python

import music21
import sys

for filename in sys.argv[1:]:
    score = music21.converter.parseFile(filename)
    key = score.analyze('key')
    print('{0} -> {1}'.format(filename, key))
