import os
from dotenv import load_dotenv


load_dotenv()


APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')

API_TOKEN = os.getenv('API_TOKEN')
API_CONFIRM_STRING = os.getenv('API_CONFIRM_STRING')
API_VERSION = '5.131'

SOURCE_IMAGE_PATH = 'static/source.png'
EMBED_IMAGE_SIZE = 256, 256
