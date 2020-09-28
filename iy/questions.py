from rich import print
from youtubesearchpython import SearchVideos, SearchPlaylists
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from halo import Halo
import regex
import re
import sys
import pyperclip
#

spinner = Halo(text='Searching', spinner='dots')

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#8B64CE bold',
    Token.Instruction: '#EBF2FA',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '#00ff00 bold',
})


# TODO search_video(query) in validator | and create two seprate vaildator of video query and playlist query


class queryValidator(Validator):
    def validate(self, document):
        query = document.text
        if len(query) >= 55:
            raise ValidationError(
                message='Please be concise. Query should be less than 50 characters.',
                cursor_position=len(document.text))  # Move cursor to end
        elif query == "":
            raise ValidationError(
                message='Please enter something.',
                cursor_position=len(document.text))  # Move cursor to end


class linkValidator(Validator):
    def validate(self, document):
        url = document.text
        if urlvalidator(url):
            return True
        else:
            raise ValidationError(
                message='Please enter a valid youtube link',
                cursor_position=len(document.text))  # Move cursor to end


def urlvalidator(url):
    if regex.match(r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+', url):
        return True
    else:
        return False


def check_clipboard():
    clipboard_content = pyperclip.paste()
    if urlvalidator(clipboard_content):
        return True
    else:
        return False


def search_query():
    questions = [
        {
            'type': 'input',
            'name': 'query',
            'message': 'Search:',
            'validate': queryValidator
        }]
    answers = prompt(questions, style=style)
    if not answers:
        pass

    return answers


def search_video(query):
    spinner.start()

    data = SearchVideos(query, offset=1, mode="dict", max_results=8)
    final_data = data.result()
    if not final_data:
        spinner.stop()
        print("[bold red]  Something went wrong. Try another query or check network connenctivity[bold red]")

    else:
        options = []
        for i in final_data['search_result']:
            temp_dict = {}
            temp_dict.update({'name': i['title'], 'value': i['link']})
            options.append(temp_dict)
        spinner.stop()

        return options


def search_playlist(query):
    spinner.start()

    data = SearchPlaylists(query, offset=1, mode='dict', max_results=8)
    final_data = data.result()
    if not final_data:
        spinner.stop()
        print("[bold red]  Something went wrong. Try another query or check network connenctivity[/bold red]")

    else:
        options = []
        for i in final_data['search_result']:
            temp_dict = {}
            temp_dict.update({'name': i['title'], 'value': i['link']})
            options.append(temp_dict)
        spinner.stop()

        return options


def get_options(answers):
    options = [
        {
            'name': 'Enter URL',
            'value': 'manual'
        },
        {
            'name': 'Search Video',
            'value': 'video_search'
        },
        {
            'name': 'Search Playlist',
            'value': 'playlist_search'
        }
    ]

    if check_clipboard():
        options[0] = {
            'name': 'Enter other URL',
            'value': 'manual'
        }
        options.insert(0, {
            'name': 'URL form clipboard',
            'value': 'clipboard',
        })
    return options


def start_1():
    ques1 = [
        {
            'type': 'list',
            'name': 'source',
            'message': 'Select:',
            'choices': get_options
        },
        {
            'type': 'input',
            'name': 'url',
            'message': 'Enter Link:',
            'validate': linkValidator,
            'when': lambda ans1: ans1['source'] == 'manual'
        },
        {
            'type': 'input',
            'name': 'query',
            'message': 'Search:',
            'validate': queryValidator,
            'when': lambda ans1: ans1['source'] == 'video_search' or ans1['source'] == 'playlist_search'

        }]
    ans1 = prompt(ques1, style=style)
    if not ans1:
        pass

    if ans1['source'] == 'video_search':
        query = ans1['query']
        ques2 = {
            'type': 'list',
            'name': 'url',
            'message': 'Results (select):',
            'choices': search_video(query)
        }
        ans2 = prompt(ques2, style=style)
        if not ans2:
            pass

        return(ans2['url'])

    elif ans1['source'] == 'playlist_search':
        query = ans1['query']
        ques2 = {
            'type': 'list',
            'name': 'url',
            'message': 'Results (select):',
            'choices': search_playlist(query)
        }
        ans2 = prompt(ques2, style=style)
        if not ans2:
            pass

        return(ans2['url'])

    elif ans1['source'] == 'manual':
        ans2 = {}
        ans2['url'] = ans1['url']
        return(ans2['url'])

    elif ans1['source'] == 'clipboard':
        ans2 = {}
        ans2['url'] = pyperclip.paste()
        return(ans2['url'])
