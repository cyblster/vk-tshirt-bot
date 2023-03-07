import requests
from io import BytesIO


class Upload:
    def __init__(self, api, group_id, album_id):
        self.api = api
        self.group_id = group_id
        self.album_id = album_id

        self.url = None

        self._get_upload_server()

    def _get_upload_server(self):
        response = requests.get(self.api.api_url.format(method='photos.getUploadServer'), params={
            **self.api.common_params, **{
                'group_id': self.group_id,
                'album_id': self.album_id
            }
        }).json()['response']

        self.url = response['upload_url']

    def _post(self, file):
        with FileOpener(file) as photo_file:
            response = requests.post(self.url, files=photo_file).json()

        return {'server': response['server'], 'photos_list': response['photos_list'], 'hash_': response['hash']}

    def _save(self, server, photos_list, hash_):
        response = requests.get(self.api.api_url.format(method='photos.save'), params={
            **self.api.common_params, **{
                'server': server,
                'photos_list': photos_list,
                'hash': hash_,
                'group_id': self.group_id,
                'album_id': self.album_id,
            }
        }).json()['response'][0]

        return 'photo{}_{}'.format(response['owner_id'], response['id'])

    def photo(self, byte_arr):
        return self._save(**self._post(byte_arr))


class FileOpener:
    def __init__(self, files, key_format='file{}'):
        if not isinstance(files, list):
            files = [files]

        self.files = files
        self.key_format = key_format
        self.opened_files = []

    def __enter__(self):
        return self.open_files()

    def __exit__(self, type_, value, traceback):
        self.close_files()

    def open_files(self):
        self.close_files()

        files = []

        for x, file in enumerate(self.files):
            if hasattr(file, 'read'):
                f = file

                if hasattr(file, 'name'):
                    filename = file.name
                else:
                    filename = '.png'
            else:
                filename = file
                f = BytesIO(filename)
                self.opened_files.append(f)

            files.append(
                (self.key_format.format(x), ('file{}.{}'.format(x, 'png'), f))
            )

        return files

    def close_files(self):
        for f in self.opened_files:
            f.close()

        self.opened_files = []
