__all__ = [
    "Note",
    "load_nbs",
    "get_pitch",
]


from dataclasses import dataclass
from typing import Any, Iterator, List, Tuple

import pynbs
from beet.core.utils import FileSystemPath

NBS_DEFAULT_INSTRUMENTS = [
    "block.note_block.harp",
    "block.note_block.bass",
    "block.note_block.basedrum",
    "block.note_block.snare",
    "block.note_block.hat",
    "block.note_block.guitar",
    "block.note_block.flute",
    "block.note_block.bell",
    "block.note_block.chime",
    "block.note_block.xylophone",
    "block.note_block.iron_xylophone",
    "block.note_block.cow_bell",
    "block.note_block.didgeridoo",
    "block.note_block.bit",
    "block.note_block.banjo",
    "block.note_block.pling",
]


@dataclass
class Note:
    """Represents a note produced by a /playsound command."""

    instrument: str = "block.note_block.harp"
    position: str = "^ ^ ^"
    volume: float = 1
    pitch: float = 1

    def play(self, player: str = "@s", source: str = "record") -> str:
        """Return the /playsound command to play the note for the given player."""
        return f"playsound {self.instrument} {source} {player} {self.position} {self.volume} {self.pitch}"


def load_nbs(filename: FileSystemPath) -> Iterator[Tuple[int, List["Note"]]]:
    """Yield all the notes from the given nbs file."""
    song = pynbs.read(filename)
    sounds = NBS_DEFAULT_INSTRUMENTS + [
        instrument.file for instrument in song.instruments
    ]

    for tick, chord in song:
        yield tick, [
            Note(
                instrument=sounds[note.instrument]
                + ("_-1" if note.key <= 32 else "_1" if note.key >= 58 else ""),
                volume=(song.layers[note.layer].volume / 100) * (note.velocity / 100),
                pitch=get_pitch(note),
            )
            for note in chord
        ]


def get_pitch(note: Any) -> float:
    """Get pitch for a given nbs note."""
    key = note.key + note.pitch / 100

    if key < 33:
        key -= 9
    elif key > 57:
        key -= 57
    else:
        key -= 33

    return 2 ** (key / 12) / 2
