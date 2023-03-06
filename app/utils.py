import requests
from PIL import Image
from io import BytesIO

import app.config as config


def get_image(embed_url: str):
    with Image.open(config.SOURCE_IMAGE_PATH).convert('RGBA') as source_image:
        with Image.open(BytesIO(requests.get(embed_url).content)).convert('RGBA') as embed_image:
            embed_image = embed_image.resize(config.EMBED_IMAGE_SIZE, Image.Resampling.LANCZOS)

            source_width, source_height = source_image.size
            embed_width, embed_height = embed_image.size
            source_image.paste(
                embed_image,
                (source_width // 2 - embed_width // 2, source_height // 2 - embed_height // 2),
                embed_image
            )

            source_image.save('result.png', format='png')
