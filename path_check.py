#!/usr/bin/env python

from myLogging import printToLog
from aggregate import Aggregate, Plex, Lun
from itertools import combinations

debugit = 2

aggregates = []
path_to_lun = {}
lun_to_paths = {}
ports = []

with open('asups.txt') as fp:
    asups = fp.read().splitlines()

with open('sysconfig-m.txt') as fp:
    sysconfig_m = fp.read().splitlines()

hostname = ''
aggregate = None

for line in asups:
    if 'System Serial Number:' in line:
        printToLog('Starting sysconfig-a')
        hostname = line.split()[-1][1:-1]
        if debugit > 2:
            printToLog(hostname)
        continue
    if 'HITACHI' in line:
        path = hostname + '_' + line.split()[0]
        port = path.split('_')[1].split('.')[0]
        if port not in ports:
            ports.append(port)

        if debugit > 2:
            printToLog(path)
        lun_name = hostname + '_' + line.split()[-1][1:-1]
        if debugit > 2:
            printToLog(lun_name)
        if path not in path_to_lun:
            path_to_lun[path] = lun_name
        else:
            if lun_name != path_to_lun[path]:
                printToLog("Error! path-lun mismatch " + path + ',' + lun_name + ',' + path_to_lun[path])
        if lun_name not in lun_to_paths:
            lun_to_paths[lun_name] = []
        lun_to_paths[lun_name].append(path)
        if debugit > 1:
            printToLog('Adding ' + path + ' to ' + lun_name)
            printToLog(lun_name + ' path count ' + str(len(lun_to_paths[lun_name])))
        continue

    if 'Aggregate' in line:
        printToLog('Starting sysconfig-m')
        aggregate_name = line.split()[1]
        if debugit > 2:
            printToLog(aggregate_name)
        aggregate = Aggregate(aggregate_name)
        aggregates.append(aggregate)
        continue
    if 'Plex' in line:
        plex_name = line.split()[1]
        if debugit > 2:
            printToLog(plex_name)
        plex = Plex(plex_name)
        aggregate.add_plex(plex)
        continue
    if 'LUN' in line:
        path = hostname + '_' + line.split()[1]
        if path in path_to_lun:
            if path_to_lun[path] not in plex.lun_names:
                lun = Lun(path_to_lun[path])
                if lun.name in lun_to_paths:
                    lun.set_paths(lun_to_paths[lun.name])
                plex.add_lun(lun)
            else:
                printToLog('Warning trying to add ' + path_to_lun[path] + ' to ' + plex.name + ' but already exists')

        if debugit > 2:
            printToLog(path)
        continue

for aggregate in aggregates:
    for plex in aggregate.plexes:
        for lun in plex.luns:
            for path in lun.paths:
                print ','.join([aggregate.name, plex.name, lun.name, path, lun.name.split('_')[1], path.split('_')[1], path.split('_')[1].split('.')[0]])

for down_ports in combinations(ports, 2):
    print 'down_ports=' + ' '.join(down_ports)
    for aggregate in aggregates:
        for plex in aggregate.plexes:
            if plex.is_online(down_ports):
                print plex.name + ' plex is online'
            else:
                print plex.name + ' plex is offline'

        if aggregate.is_offline(down_ports):
            print aggregate.name + ' aggr is offline'
        else:
            print aggregate.name + ' aggr is online'

down_ports = ["nys42ab1:24","nys42ab1:25","nys42ab1:22","nys42ab1:23"]
print 'down_ports=' + ' '.join(down_ports)
for aggregate in aggregates:
    for plex in aggregate.plexes:
        if plex.is_online(down_ports):
            print plex.name + ' plex is online'
        else:
            print plex.name + ' plex is offline'

    if aggregate.is_offline(down_ports):
        print aggregate.name + ' aggr is offline'
    else:
        print aggregate.name + ' aggr is online'

down_ports = ["nys42ab11:24","nys42ab11:22","nys42ab11:23","nys42ab11:25"]
print 'down_ports=' + ' '.join(down_ports)
for aggregate in aggregates:
    for plex in aggregate.plexes:
        if plex.is_online(down_ports):
            print plex.name + ' plex is online'
        else:
            print plex.name + ' plex is offline'

    if aggregate.is_offline(down_ports):
        print aggregate.name + ' aggr is offline'
    else:
        print aggregate.name + ' aggr is online'

down_ports = ["nys42bb1:24","nys42bb1:23","nys42bb1:25","nys42bb1:22"]
print 'down_ports=' + ' '.join(down_ports)
for aggregate in aggregates:
    for plex in aggregate.plexes:
        if plex.is_online(down_ports):
            print plex.name + ' plex is online'
        else:
            print plex.name + ' plex is offline'

    if aggregate.is_offline(down_ports):
        print aggregate.name + ' aggr is offline'
    else:
        print aggregate.name + ' aggr is online'

down_ports = ["nys42bb1:24","nys42bb1:23","nys42bb1:25","nys42bb1:22"]
print 'down_ports=' + ' '.join(down_ports)
for aggregate in aggregates:
    for plex in aggregate.plexes:
        if plex.is_online(down_ports):
            print plex.name + ' plex is online'
        else:
            print plex.name + ' plex is offline'

    if aggregate.is_offline(down_ports):
        print aggregate.name + ' aggr is offline'
    else:
        print aggregate.name + ' aggr is online'

# print '["' + '","'.join(ports) + '"]'

printToLog('Done!')
