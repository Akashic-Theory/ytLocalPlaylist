from pathlib import Path
from typing import Tuple, List, Optional

from config import Config
from edict import Edict


class Playlist:
    name: str
    id: str
    location: Path
    file: Path
    playlist_meta: Optional[Edict]
    results: Tuple[List[str], List[str]]

    def __init__(self, name: str, id: str, location: str):
        self.name = name
        self.id = id
        self.location = Path(location)
        self.file = self.location / "playlist.json"
        self.playlist_meta = None
        self.results = [], []

        if not self.location.exists():
            self.location.mkdir(parents=True)
        if not self.file.exists():
            self.song_ids = []
            self.save()
        else:
            with open(self.file, 'r') as f:
                self.song_ids = f.readlines()

    @staticmethod
    def _extract_info(item: dict) -> Tuple[str, Optional[Edict]]:
        video_id = item['contentDetails']['videoId']
        try:
            return video_id, Edict({"videoId": video_id,
                                    "ownerId": item['snippet']['videoOwnerChannelId'],
                                    "title": item['snippet']['title'],
                                    "ownerName": item['snippet']['videoOwnerChannelTitle'],
                                    "description": item['snippet']['description']
                                    })
        except KeyError:
            return video_id, None

    def retrieve_playlist_meta(self) -> Tuple[List[str], List[str]]:
        if self.playlist_meta is not None:
            return self.results
        yt = Config().yt
        playlist = yt.get_playlist_items(playlist_id=self.id, count=None, return_json=True)

        all_meta = [self._extract_info(item) for item in playlist['items']]
        self.playlist_meta, found = zip(*[(y, x) for x, y in all_meta if y is not None])
        fail = [x for x, y in all_meta if y is None]
        self.results = found, fail
        return found, fail

    def save(self):
        with open(self.file, 'w') as f:
            f.writelines(self.song_ids)
