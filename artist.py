from base64 import b64decode
from typing import Optional

import PySimpleGUI as sg

from songdb import SongDB
from util import Display, framed


class ArtistRetriever:
    _btn_submit: sg.Button
    _target: sg.InputText
    _desc: sg.Multiline
    _song_listbox: sg.Listbox
    _song_id: Optional[str]

    def __init__(self):
        self._btn_submit = sg.Button('Submit', size=(30, 2), enable_events=True, k=(self, 'submit'))
        self._target = sg.InputText(size=(40, 1), enable_events=True, expand_x=True, k=(self, 'input'))
        self._desc = sg.Multiline(size=(50, 30), no_scrollbar=True, disabled=True, expand_x=True,
                                  expand_y=True, k=(self, 'desc'))
        self._song_listbox = sg.Listbox(values=[], no_scrollbar=False, enable_events=True,
                                        size=(30, 10), expand_y=True, k=(self, 'song'))
        self._song_id = None

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
        db = SongDB()
        match action:
            case 'song':
                self._song_id = values[(self, 'song')][0].data
                desc = b64decode(db.db[self._song_id].description64.encode('utf-8')).decode('utf-8')
                self._desc.update(desc)
                guess = db.db[self._song_id].guessArtist
                self._target.update(guess or '')
            case 'submit':
                if self._song_id is None:
                    return
                name = values[(self, 'input')]
                if name.strip() != '':
                    db.db[self._song_id].artist = name
                    db.save()
                self._song_id = None
                self._target.update('')
                self.update_list()

