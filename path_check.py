#!/usr/bin/env python

from myLogging import printToLog
from aggregate import PathCheckObject
from itertools import combinations

with open('asups.txt') as fp:
    asup_lines = fp.read().splitlines()

pco = PathCheckObject(asup_lines=asup_lines)

port_list = ['nys42ab1:24', 'nys42ab1:25', 'nys42ab1:22', 'nys42ab1:23', 'nys42ab11:24', 'nys42ab11:22', 'nys42ab11:23', 'nys42ab11:25', 'nys42bb1:24',
             'nys42bb1:23', 'nys42bb1:25', 'nys42bb1:22', 'nys42bb11:22', 'nys42bb11:23', 'nys42bb11:25', 'nys42bb11:24']

if False:
    for r in range(3):
        for port_combination in combinations(port_list, r):
            print('\nDown ports = ' + ' '.join(port_combination))
            offline_aggregates, offline_plexes = pco.check(down_ports=port_combination)

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

port_list = ['nys42ab1:24', 'nys42ab1:25', 'nys42ab1:22', 'nys42ab1:23']
for port_combination in combinations(port_list, 3):
    print('\nDown ports = ' + ' '.join(port_combination))
    offline_aggregates, offline_plexes = pco.check(down_ports=port_combination)

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

port_list = ['nys42ab11:24', 'nys42ab11:22', 'nys42ab11:23', 'nys42ab11:25']
for port_combination in combinations(port_list, 3):

    print('\nDown ports = ' + ' '.join(port_combination))
    offline_aggregates, offline_plexes = pco.check(down_ports=port_combination)

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

port_list = ['nys42bb1:24', 'nys42bb1:23', 'nys42bb1:25', 'nys42bb1:22']
for port_combination in combinations(port_list, 3):

    print('\nDown ports = ' + ' '.join(port_combination))
    offline_aggregates, offline_plexes = pco.check(down_ports=port_combination)

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

port_list = ['nys42bb11:24', 'nys42bb11:23', 'nys42bb11:25', 'nys42bb11:24']
for port_combination in combinations(port_list, 3):

    print('\nDown ports = ' + ' '.join(port_combination))
    offline_aggregates, offline_plexes = pco.check(down_ports=port_combination)

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