from hypothesis import given, strategies


def inc(x):
    return x + 1 if x != 2 else x + 2


@given(strategies.integers())
def test_add(x):
    assert inc(x) == x + 1
