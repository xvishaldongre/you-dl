import pyperclip
import regex
from youtubesearchpython import SearchVideos, SearchPlaylists
from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError


class queryValidator(Validator):
    def validate(self, document):
        query = document.text
        if query == '':
            raise ValidationError(
                message='Please enter something to search',
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
    answers = prompt(questions)
    return answers


def search_video(query):
    data = SearchVideos(query, offset=1, mode="dict", max_results=8)
    final_data = data.result()
    options = []
    for i in final_data['search_result']:
        temp_dict = {}
        temp_dict.update({'name': i['title'], 'value': i['link']})
        options.append(temp_dict)
    return options


def search_playlist(query):
    data = SearchPlaylists(query, offset=1, mode='dict', max_results=8)
    final_data = data.result()
    options = []
    for i in final_data['search_result']:
        temp_dict = {}
        temp_dict.update({'name': i['title'], 'value': i['link']})
        options.append(temp_dict)
    return options


def get_options(answers):
    options = [
        {
            'name': 'Enter link',
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
            'name': 'Enter other link',
            'value': 'manual'
        }
        options.insert(0, {
            'name': 'Link form clipboard',
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
    ans1 = prompt(ques1)

    if ans1['source'] == 'video_search':
        query = ans1['query']
        ques2 = {
            'type': 'list',
            'name': 'url',
            'message': 'Results (select):',
            'choices': search_video(query)
        }
        ans2 = prompt(ques2)
        return(ans2['url'])

    elif ans1['source'] == 'playlist_search':
        query = ans1['query']
        ques2 = {
            'type': 'list',
            'name': 'url',
            'message': 'Results (select):',
            'choices': search_playlist(query)
        }
        ans2 = prompt(ques2)
        return(ans2['url'])

    elif ans1['source'] == 'manual':
        ans2 = {}
        ans2['url'] = ans1['url']
        return(ans2['url'])

    elif ans1['source'] == 'clipboard':
        ans2 = {}
        ans2['url'] = pyperclip.paste()
        return(ans2['url'])
