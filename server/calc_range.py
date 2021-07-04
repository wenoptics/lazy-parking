import typing
from typing import Dict

from server.utils import lat_lon_2_distance

LLTuple = typing.Tuple[float, float]

class RangeFinder:

    def __init__(
            self,
            zone_list: typing.List,
            get_lat_lon: typing.Callable[..., LLTuple] = None
    ):
        if get_lat_lon is None:
            get_lat_lon = self._default_get_ll
        self.__get_lat_lon = get_lat_lon
        # self.zone_list: typing.List[LLTuple] = [
        #     get_lat_lon(d) for d in zone_map
        # ]
        self.zone_list = list(zone_list)

    @staticmethod
    def _default_get_ll(data: Dict) -> LLTuple:
        d = data.get('zoneInfo', {})
        return (
            d.get('latitude', None),
            d.get('longitude', None)
        )

    def find_zone_in_range(self, lat, lon, radius):
        ret = []
        idx = 0
        for z in map(self.__get_lat_lon, self.zone_list):
            if lat_lon_2_distance(lat, lon, *z) <= radius:
                ret.append(self.zone_list[idx])
            idx += 1
        return ret
