from typing import List

import requests

from edict import Edict


class LastFM:
    base_endpoint: str
    base_header: Edict
    base_params: Edict

    def __init__(self, api_key: str):
        self.base_endpoint = "http://ws.audioscrobbler.com/2.0/"
        self.base_header = Edict({
            'Content-Type': 'application/json; charset=utf-8'
        })
        self.base_params = Edict({
            'method': 'track.search',
            'api_key': api_key,
            'format': 'json'
        })

    def get_tracks(self, name: str) -> List[str]:
        params = self.base_params
        params.track = name
        resp = requests.get(self.base_endpoint, params=params, headers=self.base_header)
        if resp.status_code != 200:
            return []
        artist_list = [track.artist
                       for track
                       in Edict(resp.json()).results.trackmatches.track
                       if track.name.lower() == name.lower()]
        artist_list.sort()
        return artist_list
