from .features import FEATURES, conv_space

SPEC = (
    (1e3, 1e3, "ns", 1),
    (1e3, 1e3, "µs", 1),  # uses non-ASCII “µs” suffix.
    (1e3, 1e3, "ms", 1),
    (60., 1., "s", 2),
    # 1:01.1 (minutes in code, 1 decimal).
    # 1:01:01 (hours in code, 0 decimal).
)


def __human_duration(val: float, space: str):
    val *= 1e9
    for size, div_next, scale, dec in SPEC:
        r = round(val, dec)
        if r >= size:
            val /= div_next
        elif r % 1. == 0.:
            return '{:.0f}{}{}'.format(r, space, scale)
        elif (r * 10.) % 1. == 0.:
            return '{:.1f}{}{}'.format(r, space, scale)
        else:
            return '{:.2f}{}{}'.format(r, space, scale)

    val = round(val, 1)
    m = val / 60.
    if m < 60.:
        r = val % 60.
        if r % 1. == 0.:
            return '{:.0f}:{:02.0f}'.format(m // 1., r)
        return '{:.0f}:{:04.1f}'.format(m // 1., round(r, 1))
    else:
        return '{:.0f}:{:02.0f}:{:02.0f}'.format(m / 60. // 1., m % 60. // 1., val % 60. // 1.)


def fn_human_duration(space: bool):
    def run(val):
        return __human_duration(val, space)

    space = conv_space(space)
    return run


class HumanDuration(object):
    def __init__(self, value):
        assert value >= 0.
        self._value = value

    @property
    def value(self):
        return self._value

    def as_human(self) -> str:
        """Return a beautiful representation of this duration.
        It dynamically calculates the best scale to use.

        Returns:
            the human friendly representation.

        """
        return fn_human_duration(FEATURES.feature_space)(self._value)

    def __str__(self):
        return self.as_human()

    def __repr__(self):  # pragma: no cover
        return 'HumanDuration{{ value={} }} -> {}'.format(self._value, self)

    def __eq__(self, other):
        return self.__str__() == other
