class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str

    def __init__(self, user_data):
        self.id = user_data.get('id')
        self.is_bot = user_data.get('is_bot')
        self.first_name = user_data.get('first_name')
        self.last_name = user_data.get('last_name')
        self.username = user_data.get('username')


class Chat:
    id: int
    username: str
    type: str

    def __init__(self, chat_data):
        self.id = chat_data.get('id')
        self.username = chat_data.get('username')
        self.type = chat_data.get('type')


class Message:
    id: int
    update_id: int
    user: User
    chat: Chat
    date: int
    text: str
    data: str
    document: dict
    photo: dict

    def __init__(self, content):
        self.update_id = content.get('update_id')
        key = 'callback_query' if 'callback_query' in content else 'message'
        if key in content:
            message_data = content[key]
            if message_data:
                self.id = message_data.get('message_id') or message_data['message']['message_id']
                self.date = message_data.get('date')
                self.text = message_data.get('text')
                self.data = message_data.get('data')
                self.photo = message_data.get('photo')
                self.document = message_data.get('document')
                self.user = User(message_data.get('from'))
                self.chat = Chat(message_data.get('chat') or message_data['message']['chat'])
