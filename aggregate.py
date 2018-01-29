from myLogging import printToLog

debugit = 2


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
