import pafy
from rich import print
from halo import Halo


def playlist_length(url):
    spinner = Halo(text='Fetching playlist metadata.', spinner='dots')
    spinner.start()
    playlist = None
    try:
        playlist = pafy.get_playlist(url)
    except:
        spinner.stop()
        print("[red bold]  Unable to get Playlist length. Please check your network connectivity and try again.")
    global playlist_length
    playlist_length = len(playlist['items'])
    spinner.stop()

    return playlist_length
