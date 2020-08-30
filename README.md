# iydl 
![](https://img.shields.io/badge/Release-v1.0-greeny.svg)

> A simple interactive youtube video and playlist downloader written in python.
> Interactively select the quality and format for youtube-dl.

A [youtube-dl](https://github.com/ytdl-org/youtube-dl) wrapper, which helps you to download a specific format and also support playlists. 


# Why?
Because remembering CLI flags is hard.  

# Features

- Lets you download Videos, Playlist or Audio only.
- Search Videos and Playlist.
- Interactively select quality.
- Thumbnail embedding supported for mp3 and opus (default) format

 
# Dependencies

- youtube-dl
- ffmpeg
- PyInquirer
- youtubesearchpython
- pyperclip

# Install

- iydl is available on pypi
```
pip3 install iydl
```

# Usage

Once installed you can run

```
iydl 
```
Tip: Copy video or playlist url before running iydl



# Inspired by 
[youtube-dl-interactive](https://github.com/synox/youtube-dl-interactive) which is written in js.


# Todo
- Add Comments in code ;-)
- Add support for config file.
- Better README.
- Error handling.
- And lots more.