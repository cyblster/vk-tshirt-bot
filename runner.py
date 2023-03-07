from src.api.api import Api
from src.api.longpoll import LongPoll
from src.api.upload import Upload
from src.image.image import TShirtImage

USER_TOKEN = 'vk1.a.4ok_ms5OarxM_6-3osLilXGYlOlCiBdvZMPSREuKqXqPDZEXuOPVu02sVvAiZAevQkASWNxehjuLZp7ydK3GXKJz8NO7IG_b6DmqNVSaTQrLt5k7Un9iVYSpts-Wr22St7bLR1weriTjh5C9qmEWAxnuqUZPjqVb0iEtFTK3wfy6o2KLAmg7WRThwfcOSp-JwOlXQd7eLhXbjbTadGMrcw'
GROUP_TOKEN = 'vk1.a.97Ss6DUgORk4wkAldQjNtNy-ogbjrY-4G_Wo7ZmRzuIS5j13LlN0SG0UZRxdJHgs-953PkpiTRy763hDK1xl-gP_iTsQIZIf04Susnwvm5O1SSTBvDDVDDo77px25cDgXziiV_P-jG8mqw00lD5r4xmyRYBph0ThQvdRrT6BnzarpJTIhVumqsbNAbNToIozzBf-GXcc1H_kiDzVsgotNA'

api = Api(USER_TOKEN, GROUP_TOKEN)
longpoll = LongPoll(api, group_id=219219396)
upload = Upload(api, group_id=219219396, album_id=293345255)

post_id = None

for event in longpoll.listen():
    if event['type'] == 'wall_post_new':
        if post_id is not None:
            continue
        post_id = event['object']['id']

    if event['type'] == 'wall_reply_new':
        if post_id is None:
            continue
        if event['object']['from_id'] == -219219396:
            continue
        if 'attachments' not in event['object']:
            continue
        if event['object']['attachments'][0]['type'] != 'photo':
            continue
        photo_url = event['object']['attachments'][0]['photo']['sizes'][-1]['url']

        photo = upload.photo(TShirtImage(photo_url).get_byte_arr())
        api.create_comment(group_id=219219396, post_id=post_id, comment_id=event['object']['id'], photo=photo)
