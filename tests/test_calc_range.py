import json
from pathlib import Path

from server.calc_range import RangeFinder
TEST_DATA = Path(__file__).parent / '..' / 'manual' / 'zone-data.json'

def test_func():
    obj = json.load(open(TEST_DATA))
    rf = RangeFinder(obj.values())
    query_list = rf.find_zone_in_range(
        40.449058,
        -79.950374,
        radius=200
    )

    assert query_list
