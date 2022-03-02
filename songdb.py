import json
import queue
from base64 import b64encode
from os import listdir
from os.path import isfile, join
from pathlib import Path
from queue import Queue
from typing import Union, Set, Callable, Optional, Tuple, List, Dict

import PySimpleGUI as sg
import yt_dlp.utils
from yt_dlp import YoutubeDL, DownloadError

from config import Config
from edict import Edict


class SongDB:
    _instance = None
    songPath: Path
    dbFile: Path
    db: Edict
    files: Set[str]
    channels: Set[Tuple[str, str]]
    songs_by_channel: Dict[str, List[str]]
    missing_names: Set[str]
    missing_artists: Set[str]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SongDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        config = Config()
        self.channels = set()
        self.missing_names = set()
        self.missing_artists = set()
        self.files = set()
        self.songs_by_channel = {}

        self.songPath = Path(config.config.paths.songs)
        self.dbFile = self.songPath / "songDB.json"
        if not self.songPath.exists():
            self.songPath.mkdir(parents=True)
        if not self.dbFile.exists():
            self.db = Edict({})
            self.save()
        else:
            with open(self.dbFile, 'r', encoding='utf-8') as db:
                self.db = Edict(json.load(db))
                self.save()

        self.calc_meta()

    def calc_meta(self):
        self.songs_by_channel = {}
        self.files = set(f[:-4] for f in listdir(self.songPath)
                         if isfile(join(self.songPath, f))
                         and f[-4:] == '.m4a')
        for id, entry in self.db.items():
            if entry.ownerId in self.songs_by_channel:
                self.songs_by_channel[entry.ownerId].append(id)
            else:
                self.songs_by_channel[entry.ownerId] = [id]
            if entry.name is None:
                self.missing_names.add(id)
            if entry.artist is None:
                self.missing_artists.add(id)
            if (entry.ownerId, entry.ownerName) not in self.channels:
                self.channels.add((entry.ownerId, entry.ownerName))

    def save(self):
        data = json.dumps(self.db, indent=2)
        with open(self.dbFile, 'w', encoding='utf-8') as db:
            db.write(data)

    @staticmethod
    def _encode_or_none(data: str) -> Union[str, None]:
        try:
            return b64encode(data.encode('utf-8')).decode('utf-8')
        except AttributeError:
            return None

    def add_song(self, data: Edict):
        song = Edict({
            'name': None,
            'guessName': None,
            'title': data.title,
            'artist': None,
            'guessArtist': None,
            'ownerName': data.ownerName,
            'ownerId': data.ownerId,
            'status': None,
            'description64': self._encode_or_none(data.description),
            'image': None,
            'backups': []
        })
        self.db[data.videoId] = song
        self.get_guesses(data.videoId)

    def get_guesses(self, id: str):
        if id not in self.db.keys():
            return
        if self.db[id].guessName is None or self.db[id].guessArtist is None:
            with YoutubeDL() as ydl:
                try:
                    data = ydl.extract_info(f'https://www.youtube.com/watch?v={id}', download=False, process=False)
                except yt_dlp.utils.ExtractorError:
                    return
                except yt_dlp.utils.DownloadError:
                    return
                if 'track' in data:
                    self.db[id].guessName = data['track']
                if 'artist' in data:
                    self.db[id].guessArtist = data['artist']

    def fetch_song(self, id: str, func: Optional[Callable[[dict], None]]):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192'
            }],
            'outtmpl': f'{self.songPath}/%(id)s.%(ext)s'
        }
        if func is not None:
            ydl_opts['progress_hooks'] = [func]
        with YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f'https://www.youtube.com/watch?v={id}'])
            except DownloadError:
                print(f"Failed downloading {id}")

    def multi_fetch(self, frame: sg.Frame, bar: sg.ProgressBar, inq: 'Queue[str]') -> None:
        def hook(d: dict) -> None:
            try:
                if d['status'] == 'downloading':
                    progress = int(float(d['downloaded_bytes']) / float(d['total_bytes']))
                    bar.update(progress)
                if d['status'] == 'finished':
                    bar.update(100, 100)

            except KeyError:
                return

        while not inq.empty():
            try:
                song_id = inq.get_nowait()
            except queue.Empty:
                return
            frame.update(self.db[song_id]['title'])
            bar.update(0)
            self.fetch_song(song_id, hook)
