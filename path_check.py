#!/usr/bin/env python

from myLogging import printToLog
from aggregate import PathCheckObject

with open('testasups.txt') as fp:
    asup_lines = fp.read().splitlines()

pco = PathCheckObject(asup_lines=asup_lines)
offline_aggregates, offline_plexes = pco.check(down_ports=['switch1:1', 'switch2:1'])

if offline_aggregates:
    print('\nOffline Aggregates:')
    for aggr in offline_aggregates:
        print(aggr)
else:
    print('\nAll Aggregates online')

if offline_plexes:
    print('\nOffline Plexes:')
    for plex in offline_plexes:
        print(plex)
else:
    print('\nAll Plexes online')

printToLog('Done!')