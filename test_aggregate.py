from aggregate import Aggregate, Plex, Lun
from pytest import raises


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
