from __future__ import unicode_literals
from . import iy
from . import questions
import youtube_dl


class MyLogger(object):
    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def main():
    default_opts = {
        'progress_hooks': [my_hook],
        'verbose': False,
        'http_chunk_size': 2097152000,
    }

    url = questions.start_1()
    user_opts = iy.opts(url)
    ydl_opts = dict(default_opts, **user_opts)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
