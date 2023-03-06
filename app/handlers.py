from flask import request

from app import app, config


@app.route('/', methods=['POST'])
def root():
    event = request.json

    if event['type'] == 'confirmation':
        return config.API_CONFIRM_STRING, 200

    if event['type'] == 'wall_post_new':
        if app.__group_id is None:
            app.group_id = event['group_id']

        if app.post_id is None:
            app.post_id = event['id']

        return '', 200

    if event['type'] == 'wall_reply_new':
        if not app.is_ready():
            return {'error': 'Need a new post on the wall before the bot works'}, 409

        if 'attachments' not in event['object']:
            app.reply_to_comment(app.group_id, app.post_id, event['object']['id'], 'Ответочка')
        if event['object']['attachments']['type'] != 'photo':
            return 'Unsupported media type', 415

        embed_url = event['object']['attachments']['photo']['sizes'][-1]['url']

