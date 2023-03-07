import requests
from PIL import Image
from io import BytesIO


class TShirtImage:
    def __init__(self, embed_url):
        self.embed_url = embed_url

        self.source = Image.open('src/image/static/source.jpg').convert('RGBA')
        self.embed = Image.open(BytesIO(requests.get(embed_url).content)).convert('RGBA')

        self.embed = self.embed.resize((256, 256), Image.Resampling.LANCZOS)
        self.source.paste(
            self.embed, (
                self.source.size[0] // 2 - self.embed.size[0] // 2 + 16,
                self.source.size[1] // 2 - self.embed.size[1] // 2
            )
        )

    def get_byte_arr(self):
        byte_arr = BytesIO()
        self.source.save(byte_arr, format='PNG')

        return byte_arr.getvalue()
