from base64 import b64decode
from typing import Optional, List

import PySimpleGUI as sg

from config import Config
from songdb import SongDB
from util import Display, framed


class ArtistRetriever:
    _btn_submit: sg.Button
    _target: sg.InputText
    _desc: sg.Multiline
    _song_listbox: sg.Listbox
    _artist_suggestion: sg.Listbox
    _song: Optional[Display[str]]

    def __init__(self):
        self._btn_submit = sg.Button('Submit', size=(30, 2), enable_events=True,
                                     bind_return_key=True, k=(self, 'submit'))
        self._target = sg.InputText(size=(40, 1), enable_events=True, expand_x=True, k=(self, 'input'))
        self._desc = sg.Multiline(size=(50, 30), no_scrollbar=True, disabled=True, expand_x=True,
                                  expand_y=True, k=(self, 'desc'))
        self._song_listbox = sg.Listbox(values=[], no_scrollbar=False, enable_events=True,
                                        size=(30, 10), expand_y=True, k=(self, 'song'))
        self._artist_suggestion = sg.Listbox(values=[], no_scrollbar=False, enable_events=True,
                                             size=(30, 10), expand_y=True, k=(self, 'suggestion'))
        self._song = None

    def update_list(self):
        db = SongDB()
        songs = [Display(id, data.name if data.name is not None else data.title)
                 for id, data
                 in db.db.items()
                 if data.artist is None]
        self._song_listbox.update(songs)

    def get_window(self) -> sg.Window:
        layout = [
            [
                framed(self._song_listbox, title='Songs', expand_y=True),
                framed(self._artist_suggestion, title='Artist?', expand_y=True),
                framed(self._desc, title='Description', expand_x=True, expand_y=True)
            ],
            [
                framed(self._target, title='Artist', expand_x=True),
                self._btn_submit
            ]
        ]
        window = sg.Window('Artist Retrieval', layout=layout, finalize=True)
        self.update_list()

        return window

    def handle_event(self, window: sg.Window, action: str, values: dict):
        match action:
            case 'song':
                songs = values[(self, 'song')]
                if len(songs) > 0:
                    self.select_song(songs[0])
            case 'suggestion':
                artist = values[(self, 'suggestion')][0]
                self._target.update(artist)
            case 'submit':
                db = SongDB()
                if self._song is None:
                    return
                name = values[(self, 'input')]
                if name.strip() == '':
                    return
                db.db[self._song.data].artist = name
                print(f'Set artist\n{self._song.data} ~~> {name}')
                db.save()
                self._song = None
                self._artist_suggestion.update([])
                self._target.update('')
                self.update_list()
                song_list: List[Display[str]] = self._song_listbox.get_list_values()
                if len(song_list) > 0:
                    self.select_song(song_list[0])
                    self._song_listbox.set_value([self._song])
                    self._song_listbox.set_focus()

    def select_song(self, song):
        db = SongDB()
        self._song = song
        desc = b64decode(db.db[self._song.data].description64.encode('utf-8')).decode('utf-8')
        self._desc.update(desc)
        guess = db.db[self._song.data].guessArtist
        self._target.update(guess or '')
        artist_list = Config().last_fm.get_tracks(self._song.disp)
        if guess is not None:
            artist_list.insert(0, guess)
        self._artist_suggestion.update(artist_list)
