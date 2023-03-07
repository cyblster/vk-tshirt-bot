import os
from dotenv import load_dotenv

from src.api.api import Api
from src.api.longpoll import LongPoll
from src.api.upload import Upload
from src.image.image import TShirtImage


load_dotenv()


USER_TOKEN = os.getenv('USER_TOKEN')
GROUP_TOKEN = os.getenv('GROUP_TOKEN')

GROUP_ID = int(os.getenv('GROUP_ID'))
ALBUM_ID = int(os.getenv('ALBUM_ID'))

api = Api(USER_TOKEN, GROUP_TOKEN)
longpoll = LongPoll(api, group_id=GROUP_ID)
upload = Upload(api, group_id=GROUP_ID, album_id=ALBUM_ID)

post_id = None

for event in longpoll.listen():
    if event['type'] == 'wall_post_new':
        if post_id is not None:
            continue
        post_id = event['object']['id']

    if event['type'] == 'wall_reply_new':
        if post_id is None:
            continue
        if event['object']['from_id'] == -GROUP_ID:
            continue
        if 'attachments' not in event['object']:
            continue
        if event['object']['attachments'][0]['type'] != 'photo':
            continue
        photo_url = event['object']['attachments'][0]['photo']['sizes'][-1]['url']

        photo = upload.photo(TShirtImage(photo_url).get_byte_arr())
        api.create_comment(group_id=GROUP_ID, post_id=post_id, comment_id=event['object']['id'], photo=photo)
