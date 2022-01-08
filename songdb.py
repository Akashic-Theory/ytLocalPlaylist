import json
import queue
from base64 import b64encode
from os import listdir
from os.path import isfile, join
from pathlib import Path
from queue import Queue
from typing import Union, Set, Callable, Optional

import PySimpleGUI as sg
from yt_dlp import YoutubeDL, DownloadError

from config import Config
from edict import Edict


class SongDB:
    _instance = None
    songPath: Path
    dbFile: Path
    db: Edict
    files: Set[str]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SongDB, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        config = Config()
        self.songPath = Path(config.config.paths.songs)
        self.dbFile = self.songPath / "songDB.json"
        if not self.songPath.exists():
            self.songPath.mkdir(parents=True)
        if not self.dbFile.exists():
            self.db = Edict({})
            self.save()
        else:
            with open(self.dbFile, 'r') as db:
                self.db = Edict(json.load(db))
                self.save()
        self.files = set(f[:-4] for f in listdir(self.songPath)
                         if isfile(join(self.songPath, f))
                         and f[-4:] == '.m4a')

    def save(self):
        with open(self.dbFile, 'w') as db:
            json.dump(self.db, db, indent=2)

    @staticmethod
    def _encode_or_none(data: str) -> Union[str, None]:
        try:
            return b64encode(data.encode('utf-8')).decode('utf-8')
        except AttributeError:
            return None

    def add_song(self, data: Edict):
        song = {
            'name': None,
            'title': data.title,
            'artist': None,
            'ownerName': data.ownerName,
            'ownerId': data.ownerId,
            'status': None,
            'description64': self._encode_or_none(data.description),
            'backups': []
        }
        self.db[data.videoId] = song

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
            frame.update(self.db[song_id].title)
            bar.update(0)
            self.fetch_song(song_id, hook)
