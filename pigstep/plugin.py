__all__ = [
    "beet_default",
    "pigstep",
]


from typing import Iterable, cast

from beet import Context, Plugin
from beet.core.utils import JsonDict


def beet_default(ctx: Context):
    config = ctx.meta.get("pigstep", cast(JsonDict, {}))

    load = config.get("load", ())

    ctx.require(pigstep(load))


def pigstep(load: Iterable[str] = ()) -> Plugin:
    """Return the configured pigstep plugin."""

    def plugin(ctx: Context):
        pass

    return plugin
