import re
from typing import Optional, Generic, TypeVar

import PySimpleGUI as sg

from songdb import SongDB


def framed(elem: sg.Element, *args: object, **kwargs: object) -> sg.Frame:
    return sg.Frame(*args, layout=[[elem]], **kwargs)


T = TypeVar('T')


class Display(Generic[T]):
    data: T
    disp: str

    def __init__(self, data: object, disp: str):
        self.data = data
        self.disp = disp

    def __str__(self):
        return self.disp


class Regex:
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


class ChannelData:
    id: str
    name: str
    count: Optional[int]

    def __init__(self, id: str, name: str, count: Optional[int] = 1):
        self.id = id
        self.name = name
        self.count = count

    def __str__(self):
        if self.count is not None:
            return f'[{self.count:3}] {self.name}'
        return self.name

    def inc(self):
        if self.count is not None:
            self.count += 1


class Transform:
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
