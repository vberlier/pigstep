__all__ = [
    "beet_default",
    "pigstep",
]


from importlib.resources import read_binary
from typing import Iterable, Optional, Set, cast

from beet import Context, Function, Plugin, Sound, generate_tree
from beet.core.utils import JsonDict, normalize_string

from .note import load_nbs

EXTRA_NOTES = {
    "block.note_block.banjo_-1": "banjo_-1.ogg",
    "block.note_block.banjo_1": "banjo_1.ogg",
    "block.note_block.basedrum_-1": "basedrum_-1.ogg",
    "block.note_block.basedrum_1": "basedrum_1.ogg",
    "block.note_block.bassattack_-1": "bassattack_-1.ogg",
    "block.note_block.bassattack_1": "bassattack_1.ogg",
    "block.note_block.bell_-1": "bell_-1.ogg",
    "block.note_block.bell_1": "bell_1.ogg",
    "block.note_block.bit_-1": "bit_-1.ogg",
    "block.note_block.bit_1": "bit_1.ogg",
    "block.note_block.cow_bell_-1": "cow_bell_-1.ogg",
    "block.note_block.cow_bell_1": "cow_bell_1.ogg",
    "block.note_block.didgeridoo_-1": "didgeridoo_-1.ogg",
    "block.note_block.didgeridoo_1": "didgeridoo_1.ogg",
    "block.note_block.flute_-1": "flute_-1.ogg",
    "block.note_block.flute_1": "flute_1.ogg",
    "block.note_block.guitar_-1": "guitar_-1.ogg",
    "block.note_block.guitar_1": "guitar_1.ogg",
    "block.note_block.harp_-1": "harp_-1.ogg",
    "block.note_block.harp_1": "harp_1.ogg",
    "block.note_block.hat_-1": "hat_-1.ogg",
    "block.note_block.hat_1": "hat_1.ogg",
    "block.note_block.icechime_-1": "icechime_-1.ogg",
    "block.note_block.icechime_1": "icechime_1.ogg",
    "block.note_block.iron_xylophone_-1": "iron_xylophone_-1.ogg",
    "block.note_block.iron_xylophone_1": "iron_xylophone_1.ogg",
    "block.note_block.pling_-1": "pling_-1.ogg",
    "block.note_block.pling_1": "pling_1.ogg",
    "block.note_block.snare_-1": "snare_-1.ogg",
    "block.note_block.snare_1": "snare_1.ogg",
    "block.note_block.xylobone_-1": "xylobone_-1.ogg",
    "block.note_block.xylobone_1": "xylobone_1.ogg",
}


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

        instruments: Set[str] = set()

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

                instruments.update(
                    note.instrument for _, chord in notes for note in chord
                )

        sounds = ctx.assets["minecraft"].sounds

        for instrument in instruments:
            if sound_file := EXTRA_NOTES.get(instrument):
                sounds[instrument.replace(".", "/")] = Sound(
                    read_binary("pigstep.sounds", sound_file),
                    event=instrument,
                    subtitle="subtitles.block.note_block.note",
                )

    return plugin
