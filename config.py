import argparse
import json
import os
from pathlib import Path

from edict import Edict

from pyyoutube import Api


class Config:
    _instance = None
    _args: argparse.Namespace
    api_key: str
    yt: Api

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        parser = argparse.ArgumentParser(description="Manage local playlists based on YouTube playlists")
        parser.add_argument('--yt', default=None)
        parser.add_argument('-j', '--jobs', type=int, default=1)

        self._args = parser.parse_args()

        # Get YouTube API Key
        if self._args.yt is None:
            if "YT_API_KEY" in os.environ:
                self.api_key = os.environ["YT_API_KEY"]
            else:
                print("No YouTube API Key supplied. Supply an API Key using --yt=<key> or by setting the YT_API_KEY "
                      "environment variable")
                exit(1)
        else:
            self.api_key = self._args.yt

        self.yt = Api(api_key=self.api_key)
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
