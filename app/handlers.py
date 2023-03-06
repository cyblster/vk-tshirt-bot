from flask import request

from app import app, config


@app.route('/', methods=['POST'])
def root():
    event = request.json

    if event['type'] == 'confirmation':
        return config.APP_CONFIRM_STRING, 200

    print(event)
