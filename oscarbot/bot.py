import json
import os
import re

from django.conf import settings
import requests


class Bot:
    token = None
    menu = None
    api_url = settings.TELEGRAM_URL

    def __init__(self, token):
        self.token = token

    def send_message(self, chat_id, message, photo=None, is_silent=False, is_background=False, reply_to_msg_id=None,
                     parse_mode='HTML', reply_keyboard=None):
        """
        @param chat_id:
        @param message:
        @param is_silent:
        @param is_background:
        @param reply_to_msg_id:
        @param reply_keyboard:
        @param parse_mode:
        @return: reply message json
        :param line_button:
        """
        params = {
            'chat_id': chat_id,
            'text': re.sub('<[^>]*>', '', message),  # TODO: todo something
            'parse_mode': parse_mode,
            'protect_content': True
        }
        if reply_keyboard is not None:
            params['reply_markup'] = reply_keyboard
        if is_silent:
            params['silent'] = True
            params['disable_notification'] = True
        if is_background:
            params['background'] = True
        if reply_to_msg_id:
            params['reply_to_msg_id'] = reply_to_msg_id

        params['disable_web_page_preview'] = True
        if photo:
            params['photo'] = f'{settings.BASE_URL}{settings.MEDIA_URL}{photo}'
            params['caption'] = params['text']
            result = requests.post(self.api_url + self.token + "/sendPhoto", data=params)
        else:
            result = requests.post(self.api_url + self.token + "/sendMessage", data=params)
        content = result.content.decode('utf-8')
        return content

    def send_photo(self, chat_id, photo_url):
        """
        @param chat_id:
        @param photo_url:
        @return: reply message json
        """
        params = {'chat_id': chat_id, 'photo': photo_url, 'parse_mode': 'Markdown'}
        result = requests.post(self.api_url + self.token + "/sendPhoto", data=params)
        content = result.content.decode('utf-8')
        return content

    def send_photos(self, chat_id, photos):
        photo_group = []
        for photo in photos:
            photo_group.append(
                {
                    'type': 'photo',
                    'media': photo
                }
            )
        params = {'chat_id': chat_id, 'media': json.dumps(photo_group)}
        result = requests.post(self.api_url + self.token + "/sendMediaGroup", data=params)
        content = result.content.decode('utf-8')
        return content

    def update_message(self, chat_id, message_id, message, photo=None, reply_keyboard=None):
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': re.sub('<[^>]*>', '', message),  # TODO: todo something
            'parse_mode': 'HTML'
        }
        if reply_keyboard is not None:
            params['reply_markup'] = reply_keyboard
        result = requests.post(self.api_url + self.token + "/editMessageText", data=params)
        return result.content.decode('utf-8')

    def delete_message(self, chat_id, message_id):
        params = {'chat_id': chat_id, 'message_id': message_id}
        response = requests.post(self.api_url + self.token + '/deleteMessage', data=params)
        return response

    def get_file(self, file_id):
        result = requests.get(self.api_url + self.token + f'/getFile?file_id={file_id}')
        json_result = result.json()
        if json_result['ok']:
            file_path = json_result['result']['file_path']

            return f"https://api.telegram.org/file/bot{self.token}/{file_path}"
        return None

    def get_user_photo(self, t_id):
        result = requests.get(self.api_url + self.token + '/getUserProfilePhotos', data={'user_id': t_id})
        json_result = result.json()
        if json_result['ok']:
            photos = json_result['result']['photos']
            if len(photos) > 0:
                smallest_photo = photos[0][0]['file_id']
                result = requests.get(self.api_url + self.token + f'/getFile?file_id={smallest_photo}')
                json_result = result.json()
                if json_result['ok']:
                    photo_path = json_result['result']['file_path']
                    result = requests.get(f"https://api.telegram.org/file/bot{self.token}/{photo_path}")
                    media_file = f'users/{t_id}.jpg'
                    with open(os.path.join(settings.BASE_DIR, f'media/{media_file}'), 'wb') as f:
                        f.write(result.content)
                    return media_file
        return None
