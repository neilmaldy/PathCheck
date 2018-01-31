from myLogging import printToLog

debugit = 0


class Aggregate:
    def __init__(self, name):
        self.name = name
        self.plexes = []
        self.plex_names = []
        if debugit > 1:
            printToLog('Creating new aggregate ' + self.name)

    def add_plex(self, plex):
        if plex.name not in self.plex_names and plex not in self.plexes:
            self.plexes.append(plex)
            self.plex_names.append(plex.name)
            if debugit > 1:
                printToLog('Adding ' + plex.name + ' to ' + self.name)
        else:
            printToLog('Warning ' + plex + ' already in ' + self.name)

    def is_offline(self, down_ports):
        if down_ports:
            for plex in self.plexes:
                if plex.is_online(down_ports):
                    return False
            return True
        else:
            return False


class Plex:
    def __init__(self, name):
        self.name = name
        self.luns = []
        self.lun_names = []
        if debugit > 1:
            printToLog('Creating new plex ' + self.name)

    def add_lun(self, lun):
        if lun.name not in self.lun_names and lun not in self.luns:
            self.lun_names.append(lun.name)
            self.luns.append(lun)
            if debugit > 1:
                printToLog('Adding ' + lun.name + ' to ' + self.name)
        else:
            printToLog('Warning trying to add ' + lun.name + ' to ' + self.name + ' but already there')

    def is_online(self, down_ports):
        if down_ports:
            for lun in self.luns:
                if lun.is_offline(down_ports):
                    return False
        return True


class Lun:
    def __init__(self, name):
        self.name = name
        self.paths = []
        self.switch_ports = []

    def set_paths(self, paths):
        if len(self.paths) > 0:
            printToLog("Warning called set_paths after paths already set for " + self.name)
        if len(paths) != 2:
            printToLog("Warning unexpected path count " + str(len(paths)) + " for " + self.name)
        self.paths = paths[:]
        for path in paths:
            if '_' in path and '.' in path.split('_')[1]:
                self.switch_ports.append(path.split('_')[1].split('.')[0])
            else:
                raise ValueError('Unexpected path format, should be hostname_port.Lnnn, but found ' + path)

    def is_offline(self, down_ports):
        if down_ports:
            for port in self.switch_ports:
                if port not in down_ports:
                    return False
            return True
        else:
            return False


class PathCheckObject:
    def __init__(self, asup_lines):
        self.aggregates = []

        path_to_lun = {}
        lun_to_paths = {}
        ports = []

        hostname = ''
        aggregate = None

        for line in asup_lines:
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
                self.aggregates.append(aggregate)
                continue
            if 'Plex' in line:
                plex_name = line.split()[1]
                if debugit > 2:
                    printToLog(plex_name)
                plex = Plex(plex_name)
                aggregate.add_plex(plex)
                continue
            if 'data' in line and 'LUN' in line:
                path = hostname + '_' + line.split()[1]
                if path in path_to_lun:
                    if path_to_lun[path] not in plex.lun_names:
                        lun = Lun(path_to_lun[path])
                        if lun.name in lun_to_paths:
                            lun.set_paths(lun_to_paths[lun.name])
                        plex.add_lun(lun)
                    else:
                        printToLog(
                            'Warning trying to add ' + path_to_lun[path] + ' to ' + plex.name + ' but already exists')

                if debugit > 2:
                    printToLog(path)
                continue

        with open('path_check.csv', mode='w') as fp:
            print >> fp, ('aggr,plex,hostlun,hostpath,lun,path,port,count')
            for aggregate in self.aggregates:
                for plex in aggregate.plexes:
                    for lun in plex.luns:
                        for path in lun.paths:
                            print >> fp, (','.join(
                                [aggregate.name, plex.name, lun.name, path, lun.name.split('_')[1], path.split('_')[1],
                                 path.split('_')[1].split('.')[0], '1']))
                        else:
                            print >> fp, (','.join(
                                [aggregate.name, plex.name, lun.name, 'null', lun.name.split('_')[1], 'null', 'null', '1']))

    def check(self, down_ports=None):
        offline_aggregates = []
        offline_plexes = []

        for aggregate in self.aggregates:
            for plex in aggregate.plexes:
                if plex.is_online(down_ports):
                    if debugit:
                        printToLog(plex.name + ' plex is online')
                else:
                    if debugit:
                        printToLog(plex.name + ' plex is offline')
                    offline_plexes.append(plex.name)

            if aggregate.is_offline(down_ports):
                if debugit:
                    printToLog(aggregate.name + ' aggr is offline')
                offline_aggregates.append(aggregate.name)
            else:
                if debugit:
                    printToLog(aggregate.name + ' aggr is online')

        return offline_aggregates, offline_plexes
