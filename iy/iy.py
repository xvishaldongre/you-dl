from __future__ import print_function, unicode_literals
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
import regex


class RangeValidator(Validator):
    def validate(self, document):
        ok = regex.match(r'^\d+-\d+$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid range (ex 1-10)',
                cursor_position=len(document.text))  # Move cursor to end


class IndexValidator(Validator):
    def validate(self, document):
        ok = regex.match(r'^(?!0*?$)[1-9]+(,[0-9]+)+$', document.text)
        ok1 = regex.match(r'^[1-9]+', document.text)
        if not ok or not ok1:
            raise ValidationError(
                message='Please enter valid index (ex 4 or 4,5)',
                cursor_position=len(document.text))  # Move cursor to end


def link_type(url):
    video = regex.search(r'v=[0-9a-zA-Z]*', url)
    playlist = regex.search(r'list=[0-9a-zA-Z\-_]*', url)

    if playlist:
        type = 'playlist'
        return type
    elif video:
        type = 'video'
        return type


def playlist():
    playlist_option_ques = [
        {
            'type': 'list',
            'name': 'option',
            'message': 'Choose option: ',
            'choices': [
                {
                    'name': 'Whole Playlist',
                    'value': 'all'
                },
                {
                    'name': 'Range (ex 1-5)',
                    'value': 'range'
                },
                {
                    'name': 'Specify Videos (ex 1,3)',
                    'value': 'specific'
                }
            ],

        },
        {
            'type': 'input',
            'name': 'playlist_items',
            'message': 'Enter range (ex 1-5):',
            'validate': RangeValidator,
            'when': lambda answers: answers['option'] == 'range'
        },
        {
            'type': 'input',
            'name': 'playlist_items',
            'message': 'Enter Video index (ex 1,3,):',
            'validate': IndexValidator,
            'when': lambda answers: answers['option'] == 'specific'
        }
    ]
    playlist_option_ans = prompt(playlist_option_ques)
    video_answers = video()
    post_answers = post_playlist_questions()
    final_type = {'type': 'playlist'}
    return(dict(final_type, **playlist_option_ans, **video_answers, **post_answers))


def video_audio_quality():
    vid_aud_quality_ques = {
        'type': 'list',
        'name': 'format',
        'message': 'Choose Quality',
        'choices': [
                {
                    'name': '1080p HD',
                    'value': '137+bestaudio'
                },
            {
                    'name': '720p HD',
                    'value': '22/136+bestaudio'
                },
            {
                    'name': '480p',
                    'value': '135+bestaudio'
                },
            {
                    'name': '360p',
                    'value': '18/134+bestaudio'
                },
            {
                    'name': '240p',
                    'value': '133+bestaudio'
                },
            {
                    'name': '144p',
                    'value': '132+bestaudio/best'
                }
        ],
        # 'when': lambda answers: answers['want'] == 'video_audio'
    }
    vid_aud_quality_ans = prompt(vid_aud_quality_ques)
    return vid_aud_quality_ans


def video_quality():
    video_quality_que = {
        'type': 'list',
        'name': 'format',
        'message': 'Choose Quality',
        'choices': [
                {
                    'name': '1080p HD',
                    'value': '137'
                },
            {
                    'name': '720p HD',
                    'value': '136'
                },
            {
                    'name': '480p',
                    'value': '135'
                },
            {
                    'name': '360p', ['want'] == 'video'
                    'value': '134'
                },
            {
                    'name': '240p',
                    'value': '133'
                },
            {
                    'name': '144p',
                    'value': '132'
                }
        ],
        # 'when': lambda answers: answers['want'] == 'video'
    }
    vid_quality_ans = prompt(video_quality_que)
    return vid_quality_ans


def audio_quality():
    audio_quality_que = {
        'type': 'list',
        'name': 'audio-quality',
        'message': 'Choose Quality',
        'choices': [
                {
                    'name': 'Mp3 (320kbps)',
                    'value': '320'
                },
            {
                    'name': 'Mp3 (256kbps)',
                    'value': '256'
                },
            {
                    'name': 'Mp3 (192kbps)',
                    'value': '192'
                },
            {
                    'name': 'Mp3 (156kbps)',
                    'value': '156',
                }
        ],
        # 'when': lambda answers: answers['want'] == 'audio'
    }

    audio_quality_ans = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '',
        }]
    }
    a = prompt(audio_quality_que)
    audio_quality_ans['postprocessors'][0]['preferredquality'] = a.get(
        'audio-quality')
    return audio_quality_ans


def video():
    video_want_ques = {
        'type': 'list',
        'name': 'want',
        'message': 'What do you want?',
        'choices': [
                {
                    'name': 'Video + Audio',
                    'value': 'video_audio'
                },
            {
                    'name': 'Audio only',
                    'value': 'audio'
                },
            {
                    'name': 'Video (Really! Without audio)',
                    'value': 'video'
                }
        ]
    }
    video_want_answers = prompt(video_want_ques)
    if video_want_answers['want'] == 'video_audio':
        answer = video_audio_quality()
        return(dict(video_want_answers, **answer))
    elif video_want_answers['want'] == 'video':
        answer = video_quality()
        return(dict(video_want_answers, **answer))
    elif video_want_answers['want'] == 'audio':
        answer = audio_quality()
        return(dict(video_want_answers, **answer))
    # return video_want_answers


def post_playlist_questions():
    post_playlist_que = [
        {
            'type': 'confirm',
            'name': 'output1',
            'message': 'Want Video Indexing?',
            'default': False
        },
        {
            'type': 'confirm',
            'name': 'output2',
            'message': 'Playlist videos in separate directory?',
            'default': False
        }
    ]
    post_playlist_ans = prompt(post_playlist_que)
    if post_playlist_ans['output1'] == True and post_playlist_ans['output2'] == True:
        output = {
            'outtmpl': "%(playlist)s/%(playlist_index)s. %(title)s.%(ext)s"}
        return output
    elif post_playlist_ans['output1'] == False and post_playlist_ans['output2'] == True:
        output = {'outtmpl': "%(playlist)s/%(title)s.%(ext)s"}
        return output
    elif post_playlist_ans['output1'] == False and post_playlist_ans['output2'] == False:
        output = {'outtmpl': "%(title)s.%(ext)s"}
        return output
    elif post_playlist_ans['output1'] == True and post_playlist_ans['output2'] == False:
        output = {'outtmpl': "%(playlist_index)s. %(title)s.%(ext)s"}
        return output


def clear_noise(output):
    entries = ('type', 'option', 'want')
    for key in entries:
        if key in output:
            del output[key]
    return output


def opts(url):
    validation = link_type(url)
    if validation == 'playlist':
        options = playlist()
        return clear_noise(options)

    elif validation == 'video':
        options = video()
        return clear_noise(options)
    else:
        options = video()
        return clear_noise(options)
