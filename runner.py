from app import app, config


if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=int(config.APP_PORT))
