from __future__ import unicode_literals
from rich import print
import youtube_dl
import humanfriendly
import re


video = []
ydl_opts, audio = {}
ydl = youtube_dl.YoutubeDL(ydl_opts)
meta = ydl.extract_info(url, download=False)

for i in meta['formats']:
    readable_size = None
    new_format_id = None
    video_size = None
    audio_size = None
    if i['ext'] == 'mp4' and re.findall('avc1', i['vcodec']):
        audio_size = list(audio.values())[-1]
        readable_size = None
        new_format_id = None
        video_size = None
        audio_size = None
        if re.findall('^(18|22|37|38)', str(i['format'])):
            if i['filesize'] == None:
                readable_size = "Not Available"
                new_format_id = i['format_id']
                video_size = 0
            else:
                readable_size = humanfriendly.format_size(
                    i['filesize'], binary=True)
                new_format_id = i['format_id']
                video_size = i['filesize']
        else:
            if i['filesize'] == None:
                readable_size = "Not Available"
                new_format_id = i['format_id']
                video_size = 0
            else:
                video_size = i['filesize']
                audio_size = list(audio.values())[-1])
                final_size=video_size + audio_size
                readable_size=humanfriendly.format_size(
                    final_size, binary = True)
                new_format_id=f"{i['format_id']}+{list(audio.keys())[-1]}"
        video.append(
            {'name': f"{i['format_note']} ({readable_size})", 'value': new_format_id})
    elif i['format_note'] == 'tiny':
        audio[i['format_id']]=i['filesize']
