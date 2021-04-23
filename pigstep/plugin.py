__all__ = [
    "beet_default",
    "pigstep",
]


from typing import Iterable, Optional, cast

from beet import Context, Function, Plugin, generate_tree
from beet.core.utils import JsonDict, normalize_string

from .note import load_nbs


def autoload(ctx: Context):
    """Autoload templates."""
    ctx.template.add_package("pigstep")


def beet_default(ctx: Context):
    config = ctx.meta.get("pigstep", cast(JsonDict, {}))

    load = config.get("load", ())
    source = config.get("source", "record")
    templates = config.get("templates")

    ctx.require(pigstep(load, source, templates))


def pigstep(
    load: Iterable[str] = (),
    source: str = "record",
    templates: Optional[JsonDict] = None,
) -> Plugin:
    """Return the configured pigstep plugin."""

    def plugin(ctx: Context):
        ctx.require("beet.contrib.inline_function")
        ctx.require("beet.contrib.inline_function_tag")

        functions = {
            "play": "pigstep/play.mcfunction",
            "pause": "pigstep/pause.mcfunction",
            "stop": "pigstep/stop.mcfunction",
            "tick": "pigstep/tick.mcfunction",
        }

        if templates:
            functions.update(templates)

        for pattern in load:
            for path in ctx.directory.glob(pattern):
                name = normalize_string(path.stem)
                notes = list(load_nbs(path))

                with ctx.generate["song"][name].push():
                    env = {
                        "song_name": name,
                        "song_player": "@s",
                        "song_source": source,
                        "song_notes": notes,
                        "song_play": ctx.generate.id("play"),
                        "song_tick": ctx.generate.objective("tick"),
                        "generate_song": lambda: generate_tree(
                            ctx.meta["render_path"], notes, lambda p: p[0]
                        ),
                    }

                    for func, path in functions.items():
                        ctx.generate(func, render=Function(source_path=path), **env)

    return plugin
