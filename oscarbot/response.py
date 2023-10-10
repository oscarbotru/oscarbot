from oscarbot.bot import Bot


class TGResponse:

    def __init__(self, message: str, menu=None, need_update=False, attache=None) -> None:
        # self.chat = chat
        self.message = message
        self.menu = menu
        self.attache = attache
        self.need_update = need_update

    def send(self, token, user):
        tg_bot = Bot(token)
        data_to_send = {
            'chat_id': user.t_id,
            'message': self.message,
            'reply_keyboard': self.menu
        }

        if self.need_update:
            response_content = tg_bot.update_message(
                **data_to_send,
                message_id=user.last_message_id,
            )
        else:
            response_content = tg_bot.send_message(
                **data_to_send
            )
        user.update_last_sent_message(response_content)

    def can_send(self):
        if self.chat is not None and self.message is not None:
            return True
        return False
