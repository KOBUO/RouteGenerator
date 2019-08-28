import pytest
from contextlib import nullcontext as does_not_raise
from src.module import stack_route
from src.module.stack_route import StackRouteException


class TestStackDs(object):
    """
    stack_dsのテスト
    """

    data = [
        # at, ut, ad, expected, expectation
        # @formatter:off
        (+3, +4, +110, [{'d': +0,   't': +0},
                        {'d': +110, 't': +3}], does_not_raise()),
        (+3, +3, +110, [{'d': +0,   't': +0},
                        {'d': +110, 't': +3}], does_not_raise()),
        (+3, +2, +110, [{'d': +0,   't': +0},
                        {'d': +55,  't': +2},
                        {'d': +110, 't': +3}], does_not_raise()),
        (+3, +1, +110, [{'d': +0,   't': +0},
                        {'d': +36,  't': +1},
                        {'d': +72,  't': +2},
                        {'d': +110, 't': +3}], does_not_raise()),
        (+3, +1,   +0, None, pytest.raises(StackRouteException)),
        (+0, +1, +110, None, pytest.raises(StackRouteException)),
        (+3, +0, +110, None, pytest.raises(StackRouteException)),
        (+0, +0,   +0, None, pytest.raises(StackRouteException)),
        (+3, +1,   -1, None, pytest.raises(StackRouteException)),
        (-1, +1, +110, None, pytest.raises(StackRouteException)),
        (+3, -1, +110, None, pytest.raises(StackRouteException)),
        (-1, -1,   -1, None, pytest.raises(StackRouteException))
        # @formatter:on
    ]

    @pytest.mark.parametrize('at, ut, ad,expected,expectation', data)
    def test_stack_ds(self, at, ut, ad, expected, expectation):
        with expectation:
            actual = stack_route._stack_ds(at=at, ut=ut, ad=ad)
            assert actual == expected

    @pytest.mark.parametrize('at, ut, ad, expectation', [(0, 1, 2, pytest.raises(StackRouteException))])
    def test_stack_ds_err_message(self, at, ut, ad, expectation):
        with expectation as e:
            stack_route._stack_ds(at=at, ut=ut, ad=ad)
        assert f'at:{at} or ut:{ut} or ad:{ad} is 0 or less.' in e.value.args[0]
