from enum import Enum

from geographiclib.geodesic import Geodesic
import math

__GEOD = Geodesic.WGS84


class StackRouteException(Exception):
    pass


class Route(object):
    """
    ルート情報
    """

    def __init__(self, lat1, lon1, lat2, lon2, at, ut):
        self.p1 = Point(lat1, lon1)
        self.p2 = Point(lat2, lon2)
        self.lines = _stack_line(lat1, lon1, lat2, lon2, at, ut)


class Line(object):
    """
    2点間のライン情報
    """

    def __init__(self, lat1, lon1, lat2, lon2, azi1, azi2, s12, a12, st, et):
        self.p1 = Point(lat1, lon1)
        self.p2 = Point(lat2, lon2)
        self.azi1 = azi1
        self.azi2 = azi2
        self.ds = s12
        self.ads = a12
        self.st = st
        self.et = et


class Point(object):
    """
    ポイント情報
        self.lat float: 緯度（度）0 ~ 180
        self.lon float: 経度（度）0 ~ 360
    """

    def __init__(self, lat, lon):
        self.lat = _to_normalize(lat)
        self.lon = _to_normalize(lon, True)


def _stack_line(lat1, lon1, lat2, lon2, at, ut):
    """
    総時間を分割時間で分割した分割数の1、2点間のlineを分割

    Args:
        lat1: 1点目の緯度
        lon1: 1点目の経度
        lat2: 2点目の緯度
        lon2: 2点目の経度
        at  : 総時間
        ut  : 分割時間
    Returns:
        [Line...]
    """

    lines = []
    gl = __GEOD.InverseLine(lat1, lon1, lat2, lon2)
    sd = _stack_ds(at=at, ut=ut, ad=gl.s13)
    for i in range(1, len(sd)):
        p1 = gl.Position(sd[i - 1]['d'], Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        p2 = gl.Position(sd[i]['d'], Geodesic.STANDARD | Geodesic.LONG_UNROLL)
        _lat1, _lon1 = [lat1, lon1] if i == 1 else [p1['lat2'], p1['lon2']]
        _lat2, _lon2 = [lat2, lon2] if len(sd) - 1 <= i else [p2['lat2'], p2['lon2']]
        _azi1, _azi2, _s12, _a12, _st, _et = p2['azi1'], p2['azi2'], p2['s12'], p2['a12'], sd[i - 1]['t'], sd[i]['t']
        lines.append(Line(lat1, lon1, lat2, lon2, _azi1, _azi2, _s12, _a12, _st, _et))
    return lines


def _stack_ds(at, ut, ad):
    """
    総時間を分割時間で分割した分割数で総距離を分割
    積み上げ時間、距離を算出

    Args:
        at : 総時間
        ut : 分割時間
        ad : 総距離
    Returns:
        [dict[t, d]...]
            t: 時間 * i
            d: 距離 * i
    Raises:
        StackRouteOutOfBoundsException: If _t or _ut or _ds is 0 or less
    """
    if min(at, ut, ad) <= 0:
        raise StackRouteException(f't:{at} or ut:{ut} or ds:{ad} is 0 or less.')
    u = int(math.ceil(at / ut))
    q, mod = divmod(ad, u)
    print(q, mod)
    ud = int(ad / u if mod < q * 0.3 else math.ceil(ad / u))
    return [{'t': min(ut * i, at), 'd': ad if u <= i else ud * i} for i in range(u + 1)]


def _to_normalize(d, is_lon=False):
    """
    緯度/経度の位相を変換（精度:1e-12）

    Args:
        d      : 緯度/経度
        is_lon : 経度フラグ（True:経度/False:緯度）
    Returns:
        緯度（度）: 0〜180 → -90〜90
        経度（度）: 0〜360 → -180〜180
    Raises:
        StackRouteOutOfBoundsException: If _d < 0 or [180 or 360] < _d
    """

    up = 360 if is_lon else 180
    if d < 0 or up < d:
        raise StackRouteException(f'{d} is range 0 to {up} out of bounds.')
    return round(d - up / 2, 12)
