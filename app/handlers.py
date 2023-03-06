from flask import request

from app import app, config


@app.route('/', methods=['POST'])
def root():
    event = request.json

    print(event)

    if event['type'] == 'confirmation':
        return config.API_CONFIRM_STRING, 200

    if event['type'] == 'wall_post_new':
        if app.post_id is None:
            app.post_id = event['id']
            return {'error': False, 'message': 'Post has been successfully created'}, 200
        return {'error': True, 'message': 'Post already created'}, 200

    if event['type'] == 'wall_reply_new':
        if not app.is_ready():
            return {'error': True, 'message': 'Need a new post on the wall before the bot works'}, 200

        if 'attachments' not in event['object']:
            app.reply_to_comment(app.group_id, app.post_id, event['object']['id'], 'Ответочка')
        if event['object']['attachments']['type'] != 'photo':
            return {'error': True, 'message': 'Unsupported media type'}, 200

        embed_url = event['object']['attachments']['photo']['sizes'][-1]['url']

