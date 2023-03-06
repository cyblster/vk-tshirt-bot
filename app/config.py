import os
from dotenv import load_dotenv


load_dotenv()


APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')

API_TOKEN = os.getenv('APP_TOKEN')
API_CONFIRM_STRING = os.getenv('APP_CONFIRM_STRING')
API_VERSION = '5.131'

GROUP_ID = -67580761
POST_ID = 9131393

SOURCE_IMAGE_PATH = 'static/source.png'
EMBED_IMAGE_SIZE = 256, 256
