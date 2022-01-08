from pathlib import Path

from mutagen.mp4 import MP4

from edict import Edict


def write_tags(base: Path, song:str, entry: Edict):
    filepath = base / song
    if not filepath.exists():
        return

    status = ""

    tags = MP4(filepath).tags
    if entry.name is not None:
        tags['\xa9nam'] = entry.name
        status += "N"
    if entry.artist is not None:
        tags['\xa9ART'] = entry.artist
        status += "A"

    tags['\xa9gen'] = 'Nightcore'
    tags['\xa9alb'] = song.split('.')[0]
    tags.save(filepath)
    entry.status = status

