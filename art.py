import io
from base64 import b64decode
from typing import Optional, Tuple, Union, Callable, List, Set

import PySimpleGUI as sg
import json
from pathlib import Path
from PIL import Image
import requests
import re

from config import Config
from edict import Edict
from songdb import SongDB
from util import framed, Display


class ArtRetriever:
    img: Optional[Image.Image]
    _sliders: Tuple[sg.Slider, sg.Slider, sg.Slider]
    _img: sg.Image
    _desc: sg.Multiline
    _song_listbox: sg.Listbox
    _dl_sources: sg.Listbox
    _btn_fetch: sg.Button
    _target: sg.Multiline
    _sel_song: sg.Frame
    _btn_confirm: sg.Button
    _img_status: sg.Text

    _cur_song_id: Optional[str]
    _base_links: List[str]
    _extra_links: List[str]

    def __init__(self):
        slider_opts = {
            'resolution': 1,
            'disabled': True,
            'size': (10, 20),
            'enable_events': True
        }
        self.img = None
        self._cur_song_id = None
        self._base_links = []
        self._extra_links = []
        self._img = sg.Image(size=(500, 500), k=(self, "image"))
        self._sliders = (
            sg.Slider(**slider_opts, orientation='h', expand_x=True, k=(self, 'hPos')),
            sg.Slider(**slider_opts, orientation='v', expand_y=True, k=(self, 'vPos')),
            sg.Slider(**slider_opts, orientation='h', expand_x=True, k=(self, 'size')),
        )
        self._song_listbox = sg.Listbox(values=[], no_scrollbar=True, enable_events=True,
                                        size=(30, 10), expand_y=True, k=(self, 'song'))
        self._dl_sources = sg.Listbox(values=[], no_scrollbar=True, enable_events=True,
                                      size=(40, 10), expand_y=True, k=(self, 'sources'))
        self._desc = sg.Multiline(size=(50, 10), no_scrollbar=True,
                                  disabled=True, expand_x=True, expand_y=True, k=(self, 'desc'))
        self._target = sg.Multiline(size=(40, 4), no_scrollbar=True, k=(self, 'target'))
        self._btn_fetch = sg.Button(button_text="Fetch", size=(30, 2), enable_events=True, k=(self, 'fetch'))

        self._btn_confirm = sg.Button(button_text="Confirm", size=(30, 2), enable_events=True, k=(self, 'confirm'))
        self._img_status = sg.Text(text='--')
        self._sel_song = sg.Frame(title="Song", title_location=sg.TITLE_LOCATION_TOP,
                                  k=(self, 'sel_song'), layout=[[self._img_status], [self._btn_confirm]])

    @staticmethod
    def direct_pixiv_artwork(url: str) -> Path:
        target = r'.*urls":({.*?}).*'
        resp = requests.get(url)
        res = re.sub(target, r'\1', resp.text, flags=re.DOTALL)
        j = json.loads(res)
        return ArtRetriever.direct_pixiv_image(j['regular'])

    @staticmethod
    def direct_pixiv_image(url: str) -> Path:
        img_resp = requests.get(url, headers={'referer': f'https://www.pixiv.net/'},
                                stream=True, verify=False)
        filename = Path(f'temp.{url.rsplit(".", 1)[-1]}')
        return ArtRetriever.download_chunks(filename, img_resp)

    @staticmethod
    def direct_imgur_image(url: str) -> Path:
        img_resp = requests.get(url, headers={'referer': "https://imgur.com/"}, stream=True, verify=False)
        filename = Path(f'temp.{url.rsplit(".", 1)[-1]}')
        return ArtRetriever.download_chunks(filename, img_resp)

    @staticmethod
    def direct_imgur_gallery(url: str) -> Path:
        headers = {}
        resp = requests.get(url, headers=headers)
        target = r'.*<script>window\.postDataJSON=(.*?)</script>.*'
        res = re.sub(target, r'\1', resp.text)
        j = json.loads(json.loads(res))
        img_link: str = j['media'][0]['url']
        return ArtRetriever.direct_imgur_image(img_link)

    @staticmethod
    def direct_konachan(url: str) -> Path:
        resp = requests.get(url)
        target = r'.*original-file-changed.*?href="(.*?)".*'
        redirect = re.sub(target, r'\1', resp.text, flags=re.DOTALL)
        img_resp = requests.get(redirect, stream=True, verify=False)
        filename = Path(f'temp.{redirect.rsplit(".", 1)[-1]}')
        return ArtRetriever.download_chunks(filename, img_resp)

    @staticmethod
    def direct_yt(id: str) -> Path:
        url = ArtRetriever.expand_yt_thumb(id)
        resp = requests.get(url)
        path = Path('temp.jpg')
        return ArtRetriever.download_chunks(path, resp)

    @staticmethod
    def expand_yt_thumb(id: str) -> Optional[str]:
        for quality in ['maxresdefault', 'sddefault', 'hqdefault', 'mqdefault', 'default']:
            url = f"https://i.ytimg.com/vi/{id}/{quality}.jpg"
            resp = requests.get(url)
            if resp.status_code == 200:
                print(f'Resolved - {url}')
                return url
        return None

    def lookup_saucenao(self, url: str) -> Optional[Path]:
        config = Config()
        if config.api_key_sauce is None:
            print('SauceNao Lookup Unsupported')
            return None
        params = {
            'db': 999,
            'output_type': 2,
            'url': url,
            'api_key': config.api_key_sauce
        }
        resp = requests.get('https://saucenao.com/search.php', params=params)
        data = Edict(json.loads(resp.text))
        results = [ArtRetriever.expand_pixiv_id(res.data.pixiv_id) for res in data.results if 'pixiv_id' in res.data]
        self._extra_links = results
        self._dl_sources.update(self._base_links + self._extra_links)

    @staticmethod
    def download_chunks(filepath: Path, resp: requests.Response) -> Path:
        with open(filepath, 'wb') as file:
            for block in resp.iter_content(1024):
                if not block:
                    break
                file.write(block)
        return filepath

    @staticmethod
    def expand_pixiv_id(id: str) -> str:
        return f'https://www.pixiv.net/en/artworks/{id}'

    @staticmethod
    def expand_bitly(link: str) -> str:
        resp = requests.get(link)
        target = r'.*long_url": "(.*?)".*'
        res = re.sub(target, r'\1', resp.text, flags=re.DOTALL)
        return res

    def load_image(self, img_path: Union[Path, str]):
        self.img = Image.open(img_path)
        w, h = self.img.size
        x_slider, y_slider, size_slider = self._sliders
        short_size, long_size = (w, h) if w < h else (h, w)
        short_slider, long_slider = (x_slider, y_slider) if w < h else (y_slider, x_slider)

        short_slider.update(0, (0, 0), False)
        long_slider.update(0, (0, long_size - short_size), False)
        size_slider.update(short_size, (short_size / 2, short_size), False)
        size_slider.update(short_size)

    def fix_sliders(self, x, y, s):
        w, h = self.img.size
        x_slider, y_slider, _ = self._sliders
        x_slider.update(range=(0, w - s))
        y_slider.update(range=(0, h - s))
        if w < h:
            x_slider.update(min(x, w - s))
        else:
            y_slider.update(min(y, h - s))

    def draw_image(self, values):
        if not self.img:
            return
        img_bytes = io.BytesIO()
        x, y, s = (values[(self, key)] for key in ('hPos', 'vPos', 'size'))
        self.fix_sliders(x, y, s)
        img = self.img.crop((x, y, x + s, y + s)).resize((500, 500))
        img.save(img_bytes, format='PNG')
        self._img.update(data=img_bytes.getvalue())

    def get_window(self) -> sg.Window:
        if self.img:
            self.img.close()

        db = SongDB()
        x_slider, y_slider, size_slider = self._sliders

        image_frame = sg.Frame(title='Image Positioning', layout=[
            [y_slider, self._img],
            [sg.Image(size=(20, 20)), x_slider],
            [size_slider]
        ])
        display_layout = sg.Column(expand_y=True, layout=[
            [framed(self._song_listbox, title='Songs', expand_y=True), image_frame],
            [framed(self._desc, title='Description', expand_x=True, expand_y=True)]
        ])
        dl_layout = sg.Column(expand_y=True, layout=[
            [framed(self._dl_sources, title='Targets', expand_y=True)],
            [framed(self._target, title='URL')],
            [self._btn_fetch]
        ])
        confirm_layout = sg.Column(expand_y=True, layout=[
            [self._sel_song]
        ])
        layout = [[
            dl_layout,
            display_layout,
            confirm_layout
        ]]

        window = sg.Window('wub', layout=layout, finalize=True)

        songs = [Display(id, data.name if data.name is not None else data.title)
                 for id, data
                 in db.db.items()
                 if data.image is None]
        self._song_listbox.update(songs)

        return window

    def handle_link(self, url: str) -> Optional[Path]:
        try:
            if "pixiv.net/en/artworks/" in url:
                return ArtRetriever.direct_pixiv_artwork(url)
            if "imgur.com/gallery" in url:
                return ArtRetriever.direct_imgur_gallery(url)
            if "i.pximg.net" in url:
                return ArtRetriever.direct_pixiv_image(url)
            if "konachan.net" in url:
                return ArtRetriever.direct_konachan(url)
            if "yt:" in url:
                return self.direct_yt(self._cur_song_id)
            if "sauce:" in url:
                self.lookup_saucenao(ArtRetriever.expand_yt_thumb(self._cur_song_id))
                return None

        except json.decoder.JSONDecodeError:
            print('Failed -- Json Decode -- Is the image deleted?')
            return None
        if any(ext in url for ext in ['.jpg', '.jpeg', '.png']):
            img_resp = requests.get(url, stream=True)
            filename = Path(f'temp.{url.rsplit(".", 1)[-1]}')
            return ArtRetriever.download_chunks(filename, img_resp)

        print(f'Unsupported - {url}')
        return None

    def get_primary_links(self, desc: str) -> List[str]:
        expansion: List[Tuple[str, str, Callable]] = [
            (r'.*?(bit\.ly/.*?)\s.*', r'https://\1+', ArtRetriever.expand_bitly),
            (r'.*pixiv.*illust_id=([0-9]*).*', r'\1', ArtRetriever.expand_pixiv_id)
        ]
        regexes = [
            (r'.*(pixiv\.net/en/artworks/[0-9]*).*', r'https://www.\1'),
            (r'.*(imgur\.com/gallery/.*?)\s.*', r'https://\1'),
            (r'.*(konachan\.net/post/show/[0-9]*).*', r'https://\1')
        ]
        follow_up = [f(re.sub(pattern, repl, desc, flags=re.DOTALL)) for pattern, repl, f in expansion
                     if re.match(pattern, desc, flags=re.DOTALL) is not None]
        results = [re.sub(pattern, repl, desc, flags=re.DOTALL) for pattern, repl in regexes
                   if re.match(pattern, desc, flags=re.DOTALL) is not None]
        print(follow_up)
        for extra in follow_up:
            for pattern, repl in regexes:
                if re.match(pattern, extra):
                    results.append(re.sub(pattern, repl, extra))
        results.extend(['yt:', 'sauce:'])
        self._base_links = results
        return results

    def handle_event(self, window: sg.Window, action: str, values: dict):
        db = SongDB()
        match action:
            case 'song':
                song_id = values[(self, 'song')][0].data
                desc = b64decode(db.db[song_id].description64.encode('utf-8')).decode('utf-8')
                self._desc.update(desc)
                self._dl_sources.update(self.get_primary_links(desc))
            case 'sources':
                source, = values[(self, 'sources')]
                self._target.update(source)
            case 'fetch':
                song_data = values[(self, 'song')][0]
                song_name, song_id = song_data.disp, song_data.data
                self._cur_song_id = song_id
                target = values[(self, 'target')]
                path = self.handle_link(target)
                if path is None:
                    return
                self.load_image(path)
                self._sel_song.update(song_name, True)
                s_text, s_col = ('Image NOT Applied', '#ffbebc') \
                    if db.db[song_id].image is None \
                    else ('Image Applied', '#adf7b6')
                self._img_status.update(value=s_text, text_color=s_col)
                self.draw_image(values)
            case 'confirm':
                if self._cur_song_id is None:
                    return
                x, y, s = (values[(self, key)] for key in ('hPos', 'vPos', 'size'))
                config = Config()
                fp = Path(config.config.paths.art) / f'{self._cur_song_id}.jpg'
                self.img.crop((x, y, x + s, y + s)).resize((300, 300)).convert('RGB').save(fp, format='JPEG')
                db.db[self._cur_song_id].image = str(fp)
                db.save()
                self._img_status.update('Image Applied', text_color='#adf7b6')
        self.draw_image(values)
