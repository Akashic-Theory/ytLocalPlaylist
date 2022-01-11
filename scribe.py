from pathlib import Path

from mutagen.mp4 import MP4, MP4Cover

from edict import Edict


def write_tags(base: Path, song: str, entry: Edict):
    filepath = base / song
    if not filepath.exists():
        return

    status = ''

    tags = MP4(filepath).tags
    if entry.name is not None:
        tags['\xa9nam'] = entry.name
        status += "N"
    if entry.artist is not None:
        tags['\xa9ART'] = entry.artist
        status += "A"
    if entry.image is not None:
        ipath = Path(entry.image)
        if ipath.exists():
            with open(ipath, 'rb') as ifile:
                idata = ifile.read()
            cover = MP4Cover(idata)
            tags['covr'] = [cover]
            print(f'Set cover - {song}')
    tags['\xa9gen'] = 'Nightcore'
    tags['\xa9alb'] = song.split('.')[0]
    tags.save(filepath)
    entry.status = status

