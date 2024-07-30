import json
import os

import requests
from django.conf import settings


class Bot:
    token = None
    menu = None
    api_url = settings.TELEGRAM_URL

    def __init__(self, token):
        self.token = token

    def send_message(self, chat_id, message, photo=None, video=None, file=None, media_group=None, has_spoiler=False,
                     media_group_type='photo', is_silent=False, is_background=False, reply_to_msg_id=None,
                     parse_mode='HTML', reply_keyboard=None, protect_content=False, disable_web_page_preview=False):
        """
        @param file:
        @param disable_web_page_preview:
        @param chat_id:
        @param message:
        @param photo:
        @param video:
        @param media_group:
        @param has_spoiler:
        @param media_group_type:
        @param is_silent:
        @param is_background:
        @param reply_to_msg_id:
        @param parse_mode:
        @param reply_keyboard:
        @param protect_content:
        @return: reply message json
        :param line_button:
        """
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': parse_mode,
            'protect_content': protect_content
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

        params['disable_web_page_preview'] = disable_web_page_preview
        if photo:
            if 'https://' in photo:
                params['photo'] = f'{photo}'  # ?random=58&random=64
            else:
                params['photo'] = f'{settings.BASE_URL}{settings.MEDIA_URL}{photo}'  # ?random=58&random=64
            params['caption'] = params['text']
            result = requests.post(self.api_url + self.token + "/sendPhoto", data=params)
        elif video:
            if video.startswith('https://'):
                params['video'] = video
            else:
                params['video'] = f'{settings.BASE_URL}{settings.MEDIA_URL}{video}'
            params['caption'] = params['text']
            result = requests.post(self.api_url + self.token + "/sendVideo", data=params)
        elif file:
            if file.startswith('https://'):
                params['document'] = file
            else:
                params['document'] = f'{settings.BASE_URL}{settings.MEDIA_URL}{file}'
            params['caption'] = params['text']
            result = requests.post(self.api_url + self.token + "/sendDocument", data=params)
        elif media_group:
            data = []
            for file in media_group:
                media_data = {
                    'type': media_group_type,
                    'caption': message,
                    'parse_mode': parse_mode,
                    'has_spoiler': has_spoiler,
                    'media': file if file.startswith('https://') else f'{settings.BASE_URL}{settings.MEDIA_URL}{file}'
                }
                data.append(media_data)
            params['media'] = json.dumps(data)
            result = requests.post(self.api_url + self.token + "/sendMediaGroup", data=params)
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

    def send_video(self, chat_id, video_url):
        params = {
            'chat_id': chat_id,
            'video_note': video_url,
            'parse_mode': 'Markdown',
            'length': 100
        }
        result = requests.post(self.api_url + self.token + "/sendVideoNote", data=params)
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

    def update_message(self, chat_id, message, message_id, is_silent=False, is_background=False, reply_to_msg_id=None,
                       parse_mode='HTML', reply_keyboard=None, **kwargs):
        params = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': message,
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
        result = requests.post(self.api_url + self.token + "/editMessageText", data=params)
        content = result.content.decode('utf-8')
        return content

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

    def answer_callback_query(self, callback_query_id, text, url, show_alert, cache_time):
        """Answer callback query."""
        params = {
            'callback_query_id': callback_query_id,
            'show_alert': show_alert,
            'cache_time': cache_time,
        }
        if text:
            params['text'] = text
        if url:
            params['url'] = url
        result = requests.post(self.api_url + self.token + '/answerCallbackQuery', data=params)
        return result.content

    def get_me(self):
        """Get me."""
        result = requests.post(self.api_url + self.token + '/getMe')
        return result.json()
