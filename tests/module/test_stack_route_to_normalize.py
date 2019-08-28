import pytest
from contextlib import nullcontext as does_not_raise
from src.module import stack_route
from src.module.stack_route import StackRouteException


class TestToNormalize(object):
    """
    to_normalizeのテスト
    """

    lat_data = [
        # @formatter:off
        (-000.000000000001,             None, pytest.raises(StackRouteException)),
        (+000.000000000000, -90.000000000000, does_not_raise()),
        (+000.000000000001, -89.999999999999, does_not_raise()),
        (+090.000000000000, +00.000000000000, does_not_raise()),
        (+179.999999999999, +89.999999999999, does_not_raise()),
        (+180.000000000000, +90.000000000000, does_not_raise()),
        (+180.000000000001,             None, pytest.raises(StackRouteException))
        # @formatter:on
    ]

    @pytest.mark.parametrize('lat,expected,expectation', lat_data)
    def test_to_normalize_default(self, lat, expected, expectation):
        with expectation:
            assert stack_route._to_normalize(d=lat) == expected

    @pytest.mark.parametrize('lat,expected,expectation', lat_data)
    def test_to_normalize_lat(self, lat, expected, expectation):
        with expectation:
            assert stack_route._to_normalize(d=lat, is_lon=False) == expected

    lon_data = [
        # @formatter:off
        (-000.000000000001,              None, pytest.raises(StackRouteException)),
        (+000.000000000000, -180.000000000000, does_not_raise()),
        (+000.000000000001, -179.999999999999, does_not_raise()),
        (+180.000000000000, +000.000000000000, does_not_raise()),
        (+359.999999999999, +179.999999999999, does_not_raise()),
        (+360.000000000000, +180.000000000000, does_not_raise()),
        (+360.000000000001,              None, pytest.raises(StackRouteException))
        # @formatter:on
    ]

    @pytest.mark.parametrize('lon,expected,expectation', lon_data)
    def test_to_normalize_lon(self, lon, expected, expectation):
        with expectation:
            assert stack_route._to_normalize(d=lon, is_lon=True) == expected
