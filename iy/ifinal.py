from __future__ import unicode_literals
from rich import print
from halo import Halo
import youtube_dl
import humanfriendly
import re
import sys


video_quality_list = {
    '18': '360p',
    '22': '720p',
    '37': '1080p',
    '38': '4K',
    '160': '144p',
    '133': '240p',
    '134': '360p',
    '135': '480p',
    '136': '720p',
    '298': '720p 60fps',
    '137': '1080p',
    '299': '1080p 60fps',
    '264': '1440p',
    '138': '2160p',
    '266': '2160p 60fps',
    '82': '360p',
    '83': '480p',
    '84': '720p',
    '85': '1080p',
    '394': '144p',
    '395': '240p',
    '396': '360p',
    '397': '480p',
    '398': '720p',
    '399': '1080p',
    '400': '1440p',
    '401': '2160p',
    '402': '2880p',
    # webm below
    '242': '240p',
    '243': '360p',
    '244': '480p',
    '247': '720p',
    '302': '720p 60fps',
    '248': '1080p',
    '303': '1080p 60fps',
    '271': '1440p',
    '308': '1440p 60fps',
    '313': '2160p',
    '315': '2160p 60fps',
    '272': '4320p (DASH Video)',
    '100': '360p (3D) ',
    '101': '480p (3D) ',
    '102': '720p (3D) ',
    '330': '144p 60fps (HDR)',
    '331': '240p 60fps (HDR)',
    '332': '360p 60fps (HDR)',
    '333': '480p 60fps (HDR)',
    '334': '720p 60fps (HDR)',
    '335': '1080p 60fps (HDR)',
    '336': '1440p 60fps (HDR)',
    '337': '2160p 60fps (HDR)',
    '219': '144p',
    '278': '144p',
    '167': '360p',
    '168': '480p',
    '218': '480p',
    '245': '480p',
    '246': '480p',
    '169': '1080p',
}


def option_with_filesize(url):
    spinner = Halo(text='Fetching available video qualities.', spinner='dots')
    spinner.start()
    options = {}  # return variable
    ydl_opts = {}  # youtube-dl options
    video_audio, only_video = [], []  # to store video size quality and format_id
    audio = {}  # to store audio filesize
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    meta = None
    try:
        meta = ydl.extract_info(url, download=False)
    except:
        spinner.stop()
        print("[bold red]  Something went wrong.[/bold red]")
        sys.exit(1)

    for i in meta['formats']:
        readable_size = None
        new_format_id = None
        video_size = None
        audio_size = None
        video_quality = None

        # only greater than 1080p and video only
        if i['ext'] == 'webm' and re.findall('(271|272|308|313|315|336|337)', i['format_id']):
            video_quality = video_quality_list[i['format_id']]
            format_id = i['format_id']
            if i['filesize'] == None:  # kaka
                readable_size = ""
                readable_size_without_audio = ""
                new_format_id = f"{i['format_id']}+{list(audio.keys())[-1]}"
                video_size = 0
            else:
                video_size = i['filesize']
                audio_size = list(audio.values())[-1]
                final_size = video_size + audio_size
                readable_size = f"({humanfriendly.format_size(final_size, binary=True)})"
                readable_size_without_audio = f"({humanfriendly.format_size(int(i['filesize']), binary=True)})"
                new_format_id = f"{i['format_id']}+{list(audio.keys())[-1]}"
            video_audio.append(
                {'name': f"{video_quality} {readable_size}", 'value': new_format_id})
            only_video.append(
                {'name': f"{video_quality} {readable_size_without_audio}", 'value': format_id})

        # if i['ext'] == 'mp4' and re.findall('avc1', i['vcodec']) and re.findall('(38|133|134|135|136|137|138|160|212|213|214|215|216|217|264|266|298|299)',i['format_id']): #mp4 video only
        # mp4 video only
        if i['ext'] == 'mp4' and re.findall('(38|133|134|135|136|137|138|160|212|213|214|215|216|217|264|266|298|299)', i['format_id']):

            video_quality = video_quality_list[i['format_id']]
            audio_size = list(audio.values())[-1]
            # filesize in human friendly format (video + audio)
            readable_size = None
            new_format_id = None  # itag (video+audio)
            video_size = None
            audio_size = None
            format_id = i['format_id']  # itag
            # filesize in human friendly format (only video)
            readable_size_without_audio = None

            if re.findall('38', str(i['format'])):
                if i['filesize'] == None:  # baba
                    # print("baba")
                    readable_size = ""
                    new_format_id = i['format_id']
                    video_size = 0
                    readable_size_without_audio = ""
                else:
                    readable_size = f"({humanfriendly.format_size(i['filesize'], binary=True)})"
                    readable_size_without_audio = f"({humanfriendly.format_size(int(i['filesize']), binary=True)})"
                    new_format_id = i['format_id']
                    video_size = i['filesize']
            else:
                video_quality = video_quality_list[i['format_id']]
                if i['filesize'] == None:
                    readable_size = ""
                    readable_size_without_audio = ""
                    new_format_id = f"{i['format_id']}+{list(audio.keys())[-1]}"
                    video_size = 0
                else:
                    video_size = i['filesize']
                    audio_size = list(audio.values())[-1]
                    final_size = video_size + audio_size
                    readable_size = f"({humanfriendly.format_size(final_size, binary=True)})"
                    readable_size_without_audio = f"({humanfriendly.format_size(int(i['filesize']), binary=True)})"
                    new_format_id = f"{i['format_id']}+{list(audio.keys())[-1]}"
            # itag 18,22 contain video+audio in mp4 format also filesize is large and sometimes
            # filesize also not availabe.
            if not re.findall('(18|22|37)', str(new_format_id)):
                video_audio.append(
                    {'name': f"{video_quality} {readable_size}", 'value': new_format_id})
                only_video.append(
                    {'name': f"{video_quality} {readable_size_without_audio}", 'value': format_id})

        elif re.findall('(139|140|141)', str(i['format_id'])):
            audio[i['format_id']] = i['filesize']
    options['video_audio'] = video_audio
    options['only_video'] = only_video
    spinner.stop()
    return options
