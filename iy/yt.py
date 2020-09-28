from __future__ import unicode_literals
from halo import Halo
from rich import print
from rich.progress import Progress
from rich.progress import (
    BarColumn,
    DownloadColumn,
    TextColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
    Progress,
    TaskID,
)
import time
import sys
import click
import pyfiglet
import youtube_dl
import re

# from .
from . import iy
from . import questions

# TODO regerous testing and also add doc

progress = Progress(
    TextColumn("[bold blue]{task.description}\n", justify="right"),
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeRemainingColumn(),
    transient=True

)

current_deleting_file = ""


class MyLogger(object):

    def error(self, msg):
        if re.findall("requested format not available", msg):
            print(f"[bold red]ERROR: Requested format not available[/bold red]")
        else:
            print(f"[bold red]{msg}[/bold red]")

    def debug(self, msg):

        global current_deleting_file
        # 0
        # print(msg)

        if re.findall("has already been downloaded", msg):
            print(f" [bold #ADFF2F]{msg}[/bold #ADFF2F]")
        # FIXME if not ffmpeg then
        a = re.findall('\[ffmpeg\].*', msg)
        if a != []:
            if re.findall("Correcting container", a[0]):
                progress.update(0, visible=False)  # t
                print(f"[bold #ADFF2F] {a[0]}[/bold #ADFF2F]")
            elif re.findall("Merging formats", a[0]):
                progress.update(0, visible=False)  # t
                print(
                    f"[bold #ADFF2F]  Done downloading, now converting ...[/bold #ADFF2F]")
                print(f"[bold #00ff00]✔{a[0]}[/bold #00ff00]")
            elif re.findall("Destination:", a[0]):  # t
                progress.update(0, visible=False)
                print(
                    f"[bold #ADFF2F]  Done downloading, now converting ...[/bold #ADFF2F]")
                print(f"[bold #00ff00]✔{a[0]}[/bold #00ff00]")
        if re.findall("Deleting original", msg):
            only_file = ""
            if re.findall('.*(?=\.f)', msg):
                only_file = re.findall('([^/]+)\.*(?=\.f)', msg)
            else:
                only_file = re.findall('([^/]+)\.*(?=\.)', msg)
            if current_deleting_file == "" or current_deleting_file != only_file[0]:
                current_deleting_file = only_file[0]
                print(
                    f"[bold #00ff00]✔ Done converting: [/bold #00ff00][bold #2196f3]{only_file[0]}[/bold #2196f3]")
                print("")
            elif current_deleting_file == only_file[0]:
                current_deleting_file = ""

    def warning(self, msg):
        print(f"  [bold #FF8C00]{msg}[/bold #FF8C00]")


def my_hook(d):
    total_bytes = None
    if "total_bytes_estimate" in d:
        total_bytes = d['total_bytes_estimate']
    elif "total_bytes" in d:
        total_bytes = d['total_bytes']

    if d['status'] == 'finished':
        filename = d['filename']
        slim_filename = re.sub('-[a-zA-Z0-9]+.f[1-9]+', '', filename)

        if "_elapsed_str" in d and re.findall('f\d', filename):
            if re.findall('f[1-3](0|1|3|4|6|7|9)[0-9]', filename) or re.findall('(\.mp4)', filename):
                print(
                    f"  [bold #ADFF2F	]Downloaded: [Video] {slim_filename}[/bold #ADFF2F	] [bold blue]100% of {d['_total_bytes_str']} in {d['_elapsed_str']}")

            elif re.findall('f(139|140|141|600|249|250|251|171|172)', filename) or re.findall('(\.m4a)', filename):
                print(
                    f"  [bold #ADFF2F	]Downloaded: [Audio] {slim_filename}[/bold #ADFF2F	] [bold blue]100% of {d['_total_bytes_str']} in {d['_elapsed_str']}")

            elif re.findall('f[1-3](2|7|8)', filename):
                print(
                    f"  [bold #ADFF2F	]Downloaded: [Video+Audio] {slim_filename}[/bold #ADFF2F	] [bold blue]100% of {d['_total_bytes_str']} in {d['_elapsed_str']}")
        elif re.findall('.mp4', filename):
            print(
                f"[bold #00ff00]✔ Done: [/bold #00ff00][bold #2196f3]{slim_filename}[/bold #2196f3]")
        else:
            print(
                f"  [bold #ADFF2F	]Downloaded: {slim_filename}[/bold #ADFF2F	]")

    if d['status'] == 'downloading':
        downloader_bytes = d['downloaded_bytes']
        filename = d['filename']
        slim_filename = re.sub('-[a-zA-Z0-9]+.f[1-9]+', '', filename)
        more_slim_name = re.sub('.+(?=\/)', '', slim_filename)
        more_slim_name = re.sub('\/', '', more_slim_name)

        if re.findall('f[1-3](0|1|3|4|6|7|9)[0-9]', filename):
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  [Vidio] {more_slim_name}", visible=True)
        elif re.findall('f(139|140|141|600|249|250|251|171|172)', filename):
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  [Audio] {more_slim_name}", visible=True)
        elif re.findall('f(18|22|37|38)', filename):
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  [Vidio+Audio] {more_slim_name}", visible=True)
        else:
            progress.update(0, completed=downloader_bytes, total=total_bytes,
                            description=f"  {more_slim_name}", visible=True)


@click.command()
def run():
    """
    Simple interactive youtube downloader written in python. Interactively select the quality and format for youtube-dl

    Run you-dl thats all you need. :-)
    """

    result = pyfiglet.figlet_format("You-dl", font="slant")
    default_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [my_hook],
        'verbose': False,
        'http_chunk_size': 2097152000,
        'logger': MyLogger(),

        # 'merge_output_format': 'mp4',
    }
    print(f"[bold red]{result}[/bold red]")
    print(f"[bold #fec601]Hi, Welcome to You-dl[/bold #fec601]")
    url = None
    try:
        url = questions.start_1()
    except Exception as e:
        print(e)
        sys.exit(1)
    user_opts = iy.opts(url)
    # print(user_opts)
    if not user_opts:
        print("[bold red]Use keyboard for selection[/bold red]")
        sys.exit(1)

    ydl_opts = dict(default_opts, **user_opts)

    print("")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            with progress:
                time.sleep(0.3)
                task_id = progress.add_task("Loading...", start=False)
                progress.start_task(0)
                ydl.download([url])
    except Exception as e:
        print(f"[bold red] {e}[/bold red]")


def main():
    try:
        run()
    except KeyboardInterrupt:
        #print("it happen")
        sys.exit(1)
    except TypeError:
        #print("[bold red]Check network connection and try again.[/bold red]")
        sys.exit(1)
    except KeyError:
        print("[bold red]Use keyboard for selection[/bold red]")
        sys.exit(1)
    except ValueError:
        print("[bold red]Use keyboard for selection[/bold red]")
        sys.exit(1)
    except Exception as e:
        print(f"[red]{e}[/red]")
        sys.exit(1)


# type error when net is of and Index error when invalid query
# song_name Please try again with a different keyword.
