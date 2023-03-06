import requests
from flask import Flask

from app import config


class MyApp(Flask):
    def __init__(self, import_name: str):
        self.confirm_string = config.API_CONFIRM_STRING

        self.api_url = 'https://api.vk.com/method/{method}'
        self.api_token = config.API_TOKEN
        self.api_version = config.API_VERSION

        self.post_id = None

        super().__init__(import_name)

    def is_ready(self) -> bool:
        if None not in (self.group_id, self.post_id):
            return True
        return False

    def reply_to_comment(self, group_id: int, post_id: int, comment_id: int, message: str) -> None:
        requests.get(self.api_url.format(method='wall.createComment'), params={
            'access_token': self.api_token, 'owner_id': -group_id, 'post_id': post_id,
            'reply_to_comment': comment_id, 'message': message, 'v': self.api_version
        })


app = MyApp(__name__)


from . import handlers
