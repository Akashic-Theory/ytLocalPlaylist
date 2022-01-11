import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

from edict import Edict

from pyyoutube import Api


class Config:
    _instance = None
    _args: argparse.Namespace
    api_key_yt: str
    api_key_sauce: Optional[str]
    yt: Api

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        parser = argparse.ArgumentParser(description="Manage local playlists based on YouTube playlists")
        parser.add_argument('--yt', default=None)
        parser.add_argument('--sauce', default=None)
        parser.add_argument('-j', '--jobs', type=int, default=1)

        self._args = parser.parse_args()
        # Get YouTube API Key
        if self._args.yt is None:
            if "YT_API_KEY" in os.environ:
                self.api_key_yt = os.environ["YT_API_KEY"]
            else:
                print("No YouTube API Key supplied. Supply an API Key using --yt=<key> or by setting the YT_API_KEY "
                      "environment variable")
                exit(1)
        else:
            self.api_key_yt = self._args.yt

        if self._args.sauce is not None:
            self.api_key_sauce = self._args.sauce
        else:
            self.api_key_sauce = None

        self.yt = Api(api_key=self.api_key_yt)
        self.jobs = self._args.jobs

        if not Path('listconfig.json').exists():
            self.write_default()
        # Load Config
        with open('listconfig.json', 'r') as conf:
            self.config = Edict(json.load(conf))

    @staticmethod
    def write_default():
        base = Path.home() / 'ytListData'
        config = {
            'paths': {
                'songs': f'{base / "songs"}',
                'art': f'{base / "art"}',
                'playlists': f'{base / "playlists"}',
                'nameHandlers': f'{base / "nameHandlers.json"}'
            },
            'playlists': []
        }
        with open('listconfig.json', 'x') as conf:
            json.dump(config, conf, indent=2)
