from aggregate import Aggregate, Plex, Lun, PathCheckObject
from pytest import raises, fixture


def test_create_lun():
    lun = Lun(name='TestLun')
    assert lun.name == 'TestLun'
    assert lun.paths == []
    assert lun.switch_ports == []


def test_lun_set_paths():
    lun = Lun(name='TestLun')
    paths = ['hostname_port1.L123', 'hostname_port2.L456']
    lun.set_paths(paths=paths)
    assert lun.paths == paths
    assert lun.switch_ports == ['port1', 'port2']


def test_lun_set_paths_exception():
    lun = Lun(name='TestLun')
    paths = ['port1.L123', 'port2.L456']
    with raises(ValueError):
        lun.set_paths(paths=paths)


def test_lun_is_offline_false():
    lun = Lun(name='TestLun')
    paths = ['hostname_port1.L123', 'hostname_port2.L456']
    lun.set_paths(paths=paths)
    assert lun.is_offline(down_ports=['port1']) is False
    assert lun.is_offline(down_ports=['port2']) is False
    assert lun.is_offline(down_ports=['port3']) is False


def test_lun_is_offline_true():
    lun = Lun(name='TestLun')
    paths = ['hostname_port1.L123', 'hostname_port2.L456']
    lun.set_paths(paths=paths)
    assert lun.is_offline(down_ports=['port1', 'port2']) is True


def test_create_plex():
    plex = Plex(name='TestPlex')
    assert plex.name == 'TestPlex'
    assert plex.lun_names == []
    assert plex.luns == []


def test_plex_add_lun():
    lun = Lun(name='TestLun')
    paths = ['hostname_port1.L123', 'hostname_port2.L456']
    lun.set_paths(paths=paths)
    plex = Plex(name='TestPlex')
    plex.add_lun(lun=lun)
    assert (lun in plex.luns) is True
    assert (lun.name in plex.lun_names) is True


def test_plex_is_online_true():
    lun = Lun(name='TestLun')
    paths = ['hostname_port1.L123', 'hostname_port2.L456']
    lun.set_paths(paths=paths)
    plex = Plex(name='TestPlex')
    plex.add_lun(lun=lun)
    assert plex.is_online(down_ports=['port1']) is True
    assert plex.is_online(down_ports=['port2']) is True
    assert plex.is_online(down_ports=['port3']) is True


def test_plex_is_online_false():
    lun = Lun(name='TestLun')
    paths = ['hostname_port1.L123', 'hostname_port2.L456']
    lun.set_paths(paths=paths)
    plex = Plex(name='TestPlex')
    plex.add_lun(lun=lun)
    assert plex.is_online(down_ports=['port1', 'port2']) is False


def test_create_aggregate():
    aggregate = Aggregate(name='TestAggr')
    assert aggregate.name == 'TestAggr'
    assert aggregate.plexes == []
    assert aggregate.plex_names == []


def test_aggregate_add_plex():
    lun1 = Lun(name='TestLun1')
    paths1 = ['hostname_port1.L123', 'hostname_port2.L456']
    lun1.set_paths(paths=paths1)
    plex1 = Plex(name='TestPlex1')
    plex1.add_lun(lun=lun1)

    lun2 = Lun(name='TestLun2')
    paths2 = ['hostname_port1.L123', 'hostname_port4.L456']
    lun2.set_paths(paths=paths2)
    plex2 = Plex(name='TestPlex2')
    plex2.add_lun(lun=lun2)

    aggregate = Aggregate(name='TestAggr')
    aggregate.add_plex(plex=plex1)
    assert (plex1 in aggregate.plexes) is True
    assert (plex1.name in aggregate.plex_names) is True

    aggregate.add_plex(plex=plex2)
    assert (plex1 in aggregate.plexes) is True
    assert (plex1.name in aggregate.plex_names) is True
    assert (plex2 in aggregate.plexes) is True
    assert (plex2.name in aggregate.plex_names) is True


def test_aggregate_is_offline_false():
    lun1 = Lun(name='TestLun1')
    paths1 = ['hostname_port1.L123', 'hostname_port2.L456']
    lun1.set_paths(paths=paths1)
    plex1 = Plex(name='TestPlex1')
    plex1.add_lun(lun=lun1)

    lun2 = Lun(name='TestLun2')
    paths2 = ['hostname_port1.L123', 'hostname_port4.L456']
    lun2.set_paths(paths=paths2)
    plex2 = Plex(name='TestPlex2')
    plex2.add_lun(lun=lun2)

    aggregate = Aggregate(name='TestAggr')
    aggregate.add_plex(plex=plex1)
    aggregate.add_plex(plex=plex2)

    assert aggregate.is_offline(down_ports=['port2']) is False
    assert aggregate.is_offline(down_ports=['port4']) is False
    assert aggregate.is_offline(down_ports=['port3']) is False
    assert aggregate.is_offline(down_ports=['port1', 'port2']) is False
    assert aggregate.is_offline(down_ports=['port1', 'port4']) is False


def test_aggregate_is_offline_true():
    lun1 = Lun(name='TestLun1')
    paths1 = ['hostname_port1.L123', 'hostname_port2.L456']
    lun1.set_paths(paths=paths1)
    plex1 = Plex(name='TestPlex1')
    plex1.add_lun(lun=lun1)

    lun2 = Lun(name='TestLun2')
    paths2 = ['hostname_port1.L123', 'hostname_port4.L456']
    lun2.set_paths(paths=paths2)
    plex2 = Plex(name='TestPlex2')
    plex2.add_lun(lun=lun2)

    aggregate = Aggregate(name='TestAggr')
    aggregate.add_plex(plex=plex1)
    aggregate.add_plex(plex=plex2)

    assert aggregate.is_offline(down_ports=['port1', 'port2', 'port4']) is True


@fixture(scope="module")
def path_check_object():
    with open('testasups.txt') as fp:
        asup_lines = fp.read().splitlines()
    return PathCheckObject(asup_lines=asup_lines)


def test_create_path_check_object_aggregates(path_check_object):
    # check aggr names
    assert (set([aggr.name for aggr in path_check_object.aggregates]) == {'host1a1', 'host1a2', 'host1a0', 'host2a0', 'host2a1'}) is True


def test_create_path_check_object_plexes(path_check_object):
    # check plex names
    for aggr in path_check_object.aggregates:
        if aggr.name == 'host1a1':
            assert (set(aggr.plex_names) == {'/host1a1/plex0', '/host1a1/plex2'}) is True
        elif aggr.name == 'host1a2':
            assert (set(aggr.plex_names) == {'/host1a2/plex0', '/host1a2/plex2'}) is True
        elif aggr.name == 'host1a0':
            assert (set(aggr.plex_names) == {'/host1a0/plex0', '/host1a0/plex2'}) is True
        elif aggr.name == 'host2a0':
            assert (set(aggr.plex_names) == {'/host2a0/plex0', '/host2a0/plex2'}) is True
        elif aggr.name == 'host2a1':
            assert (set(aggr.plex_names) == {'/host2a1/plex0', '/host2a1/plex2'}) is True


def test_create_path_check_object_luns(path_check_object):
    # check lun names
    for aggr in path_check_object.aggregates:
        for plex in aggr.plexes:
            if plex.name == '/host1a1/plex0':
                assert (set(plex.lun_names) == {'hostname1_930425000001', 'hostname1_930425000002'}) is True
            elif plex.name == '/host1a1/plex2':
                assert (set(plex.lun_names) == {'hostname1_930425000003', 'hostname1_930425000004'}) is True
            elif plex.name == '/host1a2/plex0':
                assert (set(plex.lun_names) == {'hostname1_930425000005', 'hostname1_930425000006'}) is True
            elif plex.name == '/host1a2/plex2':
                assert (set(plex.lun_names) == {'hostname1_930425000007', 'hostname1_930425000008'}) is True
            elif plex.name == '/host1a0/plex0':
                assert (set(plex.lun_names) == {'hostname1_930425000009'}) is True
            elif plex.name == '/host1a0/plex2':
                assert (set(plex.lun_names) == {'hostname1_93042500000A'}) is True
            elif plex.name == '/host2a0/plex0':
                assert (set(plex.lun_names) == {'hostname2_930425000011'}) is True
            elif plex.name == '/host1a1/plex0':
                assert (set(plex.lun_names) == {'hostname2_930425000012'}) is True
            elif plex.name == '/host1a1/plex0':
                assert (set(plex.lun_names) == {'hostname2_930425000013', 'hostname2_930425000014'}) is True
            elif plex.name == '/host1a1/plex0':
                assert (set(plex.lun_names) == {'hostname2_930425000015', 'hostname2_930425000016'}) is True


def test_create_path_check_object_paths_ports(path_check_object):

    # check paths and ports
    paths = dict()
    paths['hostname1_930425000001'] = ['hostname1_switch1:1.126L1', 'hostname1_switch2:1.126L1']
    paths['hostname1_930425000002'] = ['hostname1_switch1:2.126L2', 'hostname1_switch2:2.126L2']
    paths['hostname1_930425000003'] = ['hostname1_switch1:3.126L3', 'hostname1_switch2:3.126L3']
    paths['hostname1_930425000004'] = ['hostname1_switch1:4.126L4', 'hostname1_switch2:4.126L4']
    paths['hostname1_930425000005'] = ['hostname1_switch1:5.126L5', 'hostname1_switch2:5.126L5']
    paths['hostname1_930425000006'] = ['hostname1_switch1:6.126L6', 'hostname1_switch2:6.126L6']
    paths['hostname1_930425000007'] = ['hostname1_switch1:7.126L7', 'hostname1_switch2:7.126L7']
    paths['hostname1_930425000008'] = ['hostname1_switch1:8.126L8', 'hostname1_switch2:8.126L8']
    paths['hostname1_930425000009'] = ['hostname1_switch1:9.126L9', 'hostname1_switch2:9.126L9']
    paths['hostname1_93042500000A'] = ['hostname1_switch1:0.126L0', 'hostname1_switch2:0.126L0']
    paths['hostname2_930425000011'] = ['hostname2_switch1:10.126L11', 'hostname2_switch2:10.126L11']
    paths['hostname2_930425000012'] = ['hostname2_switch1:10.126L12', 'hostname2_switch2:10.126L12']
    paths['hostname2_930425000013'] = ['hostname2_switch1:10.126L13', 'hostname2_switch2:10.126L13']
    paths['hostname2_930425000014'] = ['hostname2_switch1:10.126L14', 'hostname2_switch2:10.126L14']
    paths['hostname2_930425000015'] = ['hostname2_switch1:10.126L15', 'hostname2_switch2:10.126L15']
    paths['hostname2_930425000016'] = ['hostname2_switch1:20.126L16', 'hostname2_switch2:20.126L16']
    ports = dict()
    ports['hostname1_930425000001'] = ['switch1:1', 'switch2:1']
    ports['hostname1_930425000002'] = ['switch1:2', 'switch2:2']
    ports['hostname1_930425000003'] = ['switch1:3', 'switch2:3']
    ports['hostname1_930425000004'] = ['switch1:4', 'switch2:4']
    ports['hostname1_930425000005'] = ['switch1:5', 'switch2:5']
    ports['hostname1_930425000006'] = ['switch1:6', 'switch2:6']
    ports['hostname1_930425000007'] = ['switch1:7', 'switch2:7']
    ports['hostname1_930425000008'] = ['switch1:8', 'switch2:8']
    ports['hostname1_930425000009'] = ['switch1:9', 'switch2:9']
    ports['hostname1_93042500000A'] = ['switch1:0', 'switch2:0']
    ports['hostname2_930425000011'] = ['switch1:10', 'switch2:10']
    ports['hostname2_930425000012'] = ['switch1:10', 'switch2:10']
    ports['hostname2_930425000013'] = ['switch1:10', 'switch2:10']
    ports['hostname2_930425000014'] = ['switch1:10', 'switch2:10']
    ports['hostname2_930425000015'] = ['switch1:10', 'switch2:10']
    ports['hostname2_930425000016'] = ['switch1:20', 'switch2:20']

    for aggr in path_check_object.aggregates:
        for plex in aggr.plexes:
            for lun in plex.luns:
                if lun.name in paths:
                    assert (set(lun.paths) == set(paths[lun.name])) is True
                if lun.name in ports:
                    assert (set(lun.switch_ports) == set(ports[lun.name])) is True


def test_plex_offline(path_check_object):
    offline_aggregates, offline_plexes = path_check_object.check(down_ports=['switch1:1', 'switch2:1'])
    assert (set(offline_plexes) == {'/host1a1/plex0'}) is True
    offline_aggregates, offline_plexes = path_check_object.check(down_ports=['switch1:2', 'switch2:1'])
    assert (set(offline_plexes) == {'/host1a1/plex0'}) is False
    offline_aggregates, offline_plexes = path_check_object.check(down_ports=['switch1:1', 'switch2:1', 'switch1:2', 'switch2:2'])
    assert (set(offline_plexes) == {'/host1a1/plex0', '/host1a1/plex0'}) is True


def test_aggregate_offline(path_check_object):
    offline_aggregates, offline_plexes = path_check_object.check(down_ports=['switch1:1', 'switch2:1'])
    assert (set(offline_aggregates) == {'host1a1'}) is False
    offline_aggregates, offline_plexes = path_check_object.check(down_ports=['switch1:1', 'switch2:1', 'switch1:3', 'switch2:3'])
    assert (set(offline_aggregates) == {'host1a1'}) is True

