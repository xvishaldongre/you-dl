from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
import regex
import re
import sys
##################
#from . 
from . import ifinal
from . import dummy
##################

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#8B64CE bold',
    Token.Instruction: '#EBF2FA',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '#00ff00 bold',
})


class RangeValidator(Validator):
    def validate(self, document):

        ok = re.match('^\d+-\d+$', document.text)
        if ok:
            start = re.findall('^\d+(?=-)', document.text)[0]
            end = int(re.findall('(?<=-)\d+', document.text)[0])
            vaild_start = int(start) > 0 and int(start) < int(playlist_len - 1)
            vaild_end = int(end) > int(start) and int(end) <= (playlist_len)
            if not (ok and vaild_start and vaild_end):
                raise ValidationError(
                    message=f"Please enter a range between 1-{playlist_len}",
                    cursor_position=len(document.text))  # Move cursor to end
        else:
            raise ValidationError(
                message=f"Please enter a range between 1-{playlist_len}",
                cursor_position=len(document.text))  # Move cursor to end

3
class IndexValidator(Validator):
    def validate(self, document):
        user_values = re.findall(',?\d+,?', str(document.text))
        index = re.findall('\d+', str(document.text))
        other = re.findall('[^,\d\s]+', str(document.text))
        if not user_values:
            raise ValidationError(message=f"Please enter valid index (ex 1 or 1,2) (index < {playlist_len})",
                                  cursor_position=len(str(document.text)))  # Move cursor to end

        if other and user_values:
            raise ValidationError(
                message=f"Please enter valid index (ex 1 or 1,2) (index < {playlist_len})",
                cursor_position=len(str(document.text)))  # Move cursor to end

        elif index and user_values:
            greater_index = ""
            for i in index:
                if int(i) > playlist_len or int(i) == 0:
                    greater_index = greater_index + str(i)

                    raise ValidationError(
                        message=f"Please enter valid index ex 1 or 1,2 (index < {playlist_len})",
                        cursor_position=len(str(document.text)))  # Move cursor to end
                    break


def link_type(url):
    video = regex.search(r'v=[0-9a-zA-Z]*', url)
    playlist = regex.search(r'list=[0-9a-zA-Z\-_]*', url)

    if playlist:
        type = 'playlist'
        return type
    elif video:
        type = 'video'
        return type


def choices_video_quality(answers):
    choices = []
    if urlis == 'video':
        results = ifinal.option_with_filesize(link)
        if not results:
            sys.exit(1)
        choices = results['only_video']
        choices = choices
    else:
        choices = [{'name': '1080p HD', 'value': '137'}, {'name': '720p HD', 'value': '136'}, {'name': '480p', 'value': '135'}, {
            'name': '360p', 'value': '134'}, {'name': '240p', 'value': '133'}, {'name': '144p', 'value': '132'}]
    return choices


def choices_video_audio_quality(vid_aud_quality_ans):
    choices = []
    if urlis == 'video':
        results = ifinal.option_with_filesize(link)
        if not results:
            sys.exit(1)
        choices = results['video_audio']
        choices = choices
    else:
        choices = [{'name': '1080p HD', 'value': '137+bestaudio'}, {'name': '720p HD', 'value': '22/136+bestaudio'}, {'name': '480p', 'value': '135+bestaudio'}, {
            'name': '360p', 'value': '18/134+bestaudio'}, {'name': '240p', 'value': '133+bestaudio'}, {'name': '144p', 'value': '132+bestaudio/'}]
    return choices


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
                    'name': 'Single Video (ex 1) or Specify Videos (ex 1,2)',
                    'value': 'specific'
                },
                {
                    'name': 'Range (ex 1-2)',
                    'value': 'range'
                },

            ],

        },
        {
            'type': 'input',
            'name': 'playlist_items',
            'message': 'Enter range (ex 1-2):',
            'validate': RangeValidator,
            'when': lambda answers: answers['option'] == 'range'
        },
        {
            'type': 'input',
            'name': 'playlist_items',
            'message': 'Enter Video index (ex 1,2):',
            'validate': IndexValidator,
            'when': lambda answers: answers['option'] == 'specific'
        }
    ]
    playlist_option_ans = prompt(playlist_option_ques, style=style)
    if not playlist_option_ans:
        sys.exit(1)
    video_answers = video()
    post_answers = post_playlist_questions()
    final_type = {'type': 'playlist'}
    return(dict(final_type, **playlist_option_ans, **video_answers, **post_answers))


def video_audio_quality():
    vid_aud_quality_ques = {
        'type': 'list',
        'name': 'format',
        'message': 'Choose Quality',
        'choices': choices_video_audio_quality,
        # 'when': lambda answers: answers['want'] == 'video_audio'
    }
    vid_aud_quality_ans = prompt(vid_aud_quality_ques, style=style)
    if not vid_aud_quality_ans:
        sys.exit(1)
    return vid_aud_quality_ans


def video_quality():
    video_quality_que = {
        'type': 'list',
        'name': 'format',
        'message': 'Choose Quality',
        'choices': choices_video_quality,
        # 'when': lambda answers: answers['want'] == 'video'
    }
    vid_quality_ans = prompt(video_quality_que, style=style)
    if not vid_quality_ans:
        sys.exit(1)
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
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '',
            #'embed-thumbnail': True
        }]
    }
    a = prompt(audio_quality_que, style=style)
    if not a:
        sys.exit(1)
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
    video_want_answers = prompt(video_want_ques, style=style)
    if not video_want_answers:
        sys.exit(1)
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
            'message': 'Want numbering in Videos?',
            'default': False
        },
        {
            'type': 'confirm',
            'name': 'output2',
            'message': 'Playlist videos in separate directory?',
            'default': False
        }
    ]
    post_playlist_ans = prompt(post_playlist_que, style=style)
    if not post_playlist_ans:
        sys.exit(1)
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
    global link
    global urlis
    link = url

    validation = link_type(url)
    if validation == 'playlist':
        urlis = 'playlist'
        global playlist_len
        playlist_len = dummy.playlist_length(url)
        options = playlist()
        return clear_noise(options)

    elif validation == 'video':
        urlis = 'video'
        options = video()
        return clear_noise(options)
    else:
        options = video()
        return clear_noise(options)

