from aggregate import Aggregate

def test_create_aggregate():
    aggregate = Aggregate(name='TestAggr')
    assert aggregate.name == 'TestAggr'

