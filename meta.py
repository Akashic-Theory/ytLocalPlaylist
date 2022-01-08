import json
import re
from pathlib import Path
from typing import Union, Tuple, List, Optional, Dict

from config import Config
from edict import Edict
import PySimpleGUI as sg

from songdb import SongDB
from util import framed


class Meta:
    _handler_path: Path
    handlers: Edict
    regexes: 'Dict[str, Meta._Regex]'

    class _Regex:
        name: str
        pattern: str
        repl: str

        def __init__(self, name: str, pattern: str, repl: str):
            self.name = name
            self.pattern = pattern
            self.repl = repl

        def __str__(self):
            return self.name

        def parse(self, payload: str) -> Optional[str]:
            if re.match(self.pattern, payload) is None:
                return None
            return re.sub(self.pattern, self.repl, payload)

    class _ChannelData:
        id: str
        name: str
        count: int

        def __init__(self, id: str, name: str):
            self.id = id
            self.name = name
            self.count = 1

        def __str__(self):
            return f'[{self.count:3}] {self.name}'

        def inc(self):
            self.count += 1

    class _Transform:
        id: str
        title: str
        result: Optional[str]

        def __init__(self, id: str, db: SongDB = SongDB()):
            self.id = id
            self.title = db.db[id].title
            self.result = None

        def __str__(self):
            if self.result is None:
                return f'✗|{self.title}'
            return f'✓|{self.result}'

    def __init__(self):
        config = Config()
        self.handler_path = Path(config.config.paths.nameHandlers)
        self.regexes = {}
        if not self.handler_path.exists():
            self.handlers = Edict({
                'regex': {},
                'channels': {}
            })
            self.save()
        else:
            with open(self.handler_path, 'r', encoding='utf-8') as handlers:
                self.handlers = Edict(json.load(handlers))
        for name, regex in self.handlers.regex.items():
            self.regexes[name] = self._Regex(name, regex.pattern, regex.repl)

    def save(self):
        with open(self.handler_path, 'w') as handlers:
            json.dump(self.handlers, handlers, indent=2)

    def get_name(self, title: str, id: str) -> Union[str, None]:
        print(self.handlers.keys())
        if id not in self.handlers.keys():
            print("skipping")
            return None

        print(self.handlers[id].items())
        for key, value in self.handlers[id].items():
            print(key)
            print(value)

    def handle_event(self, window: sg.Window, event: 'Tuple[Meta, str]', values: dict):
        def update_ui(channel: Meta._ChannelData):
            window[(self, 'RE-ACTIVE')].update([r for r in self.handlers.channels[channel.id]])
            songs = [self._Transform(id) for id in db.songs_by_channel[channel.id]
                     if db.db[id].name is None]
            regexes = [self.regexes[regex] for regex in self.handlers.channels[channel.id]]
            for song in songs:
                for regex in regexes:
                    if song.result is not None:
                        continue
                    song.result = regex.parse(song.title)
            window[(self, 'NAMES')].update(songs)

        _, action = event
        db = SongDB()
        if action == 'CHANNELS':
            channel: Meta._ChannelData
            channel, = values[event]
            print(channel)
            if channel.id not in self.handlers.channels:
                self.handlers.channels[channel.id] = []
            update_ui(channel)

        elif action == 'BTN-ADD-RE':
            channel: Meta._ChannelData
            regex: str
            try:
                channel, = values[(self, 'CHANNELS')]
                regex, = values[(self, 'RE')]
            except ValueError:
                return
            if regex not in self.handlers.channels[channel.id]:
                self.handlers.channels[channel.id].append(regex)
            update_ui(channel)
            self.save()
        elif action == 'BTN-RM-RE':
            channel: Meta._ChannelData
            regex: str
            try:
                channel, = values[(self, 'CHANNELS')]
                regex, = values[(self, 'RE-ACTIVE')]
            except ValueError:
                return
            self.handlers.channels[channel.id].remove(regex)
            update_ui(channel)
            self.save()
        elif action == 'BTN-RENAME':
            channel: Meta._ChannelData
            songs: List[Meta._Transform]
            songs = values[(self, 'NAMES')]
            channel, = values[(self, 'CHANNELS')]
            print(len(db.missing_names))
            for song in songs:
                if song.result is not None:
                    db.db[song.id].name = song.result
                    db.missing_names.remove(song.id)
            print(len(db.missing_names))
            db.save()
            update_ui(channel)

    def get_naming_window(self) -> sg.Window:
        db = SongDB()
        pending_names = [(id, db.db[id].title, db.db[id].ownerId) for id in db.missing_names]
        channel_map = {id: name for id, name in db.channels}
        channels = {}
        for song_id, _, channel_id in pending_names:
            if channel_id in channels.keys():
                channels[channel_id].inc()
            else:
                channels[channel_id] = self._ChannelData(channel_id, channel_map[channel_id])
        layout = [
            [
                framed(title='Channels',
                       elem=sg.Listbox(size=(40, 10), no_scrollbar=True, enable_events=True, expand_x=True,
                                       select_mode=sg.SELECT_MODE_BROWSE,
                                       values=[channel for channel in channels.values()], k=(self, 'CHANNELS'))),
                sg.Frame(title='Regexes', layout=[
                    [
                        sg.Listbox(size=(25, 8), no_scrollbar=True,
                                   select_mode=sg.SELECT_MODE_BROWSE,
                                   values=[], k=(self, 'RE-ACTIVE'))
                    ],
                    [
                        sg.Button(button_text='Add Regex', k=(self, 'BTN-ADD-RE')),
                        sg.Button(button_text='Remove Regex', k=(self, 'BTN-RM-RE'))
                    ]
                ]),
                sg.Frame(title="Submit", layout=[
                   [sg.Button(size=(25, 4), button_text='Regex Rename', k=(self, 'BTN-RENAME'))],
                   [sg.Button(size=(25, 4), button_text='Manual Rename', k=(self, 'BTN-RENAME-MAN'))],
                ])
            ],
            [
                framed(title="Regex",
                       elem=sg.Listbox(size=(20, 25), no_scrollbar=True,
                                       select_mode=sg.SELECT_MODE_BROWSE,
                                       values=[x for x in self.regexes.keys()], k=(self, 'RE'))),
                framed(title='Names',
                       elem=sg.Listbox(size=(80, 25), no_scrollbar=True,
                                       select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
                                       values=[], k=(self, 'NAMES')))
            ]
        ]
        window = sg.Window('Rename Tool', layout=layout, finalize=True)
        return window
