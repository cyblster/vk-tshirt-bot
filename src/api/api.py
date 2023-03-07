import requests


class Api:
    def __init__(self, user_token: str, group_token: str, version: str = '5.131'):
        self.user_token = user_token
        self.group_token = group_token
        self.version = version

        self.api_url = 'https://api.vk.com/method/{method}'
        self.common_params = {
            'access_token': self.user_token,
            'v': self.version
        }

    def create_comment(self, group_id, post_id, comment_id, photo):
        requests.get(self.api_url.format(method='wall.createComment'), params={
            'access_token': self.group_token, 'owner_id': -group_id, 'post_id': post_id,
            'reply_to_comment': comment_id, 'attachments': photo, "v": self.version
        })
