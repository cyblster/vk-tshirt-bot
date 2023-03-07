import requests


class LongPoll:
    def __init__(self, api, group_id, version='3'):
        self.api = api
        self.group_id = group_id

        self.server = None
        self.key = None
        self.ts = None
        self.version = version

        self._get_long_poll_server()

    def _get_long_poll_server(self):
        response = requests.get(self.api.api_url.format(method='groups.getLongPollServer'), params={
            **self.api.common_params, **{
                'group_id': self.group_id,
                'lp_version': self.version
            }
        }).json()['response']

        self.server = response['server']
        self.key = response['key']
        self.ts = response['ts']

    def _check(self, wait=25):
        response = requests.get(self.server, params={
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': wait,
            'version': self.version
        }).json()

        if 'failed' in response:
            return []

        self.ts = response['ts']

        return response['updates']

    def listen(self, wait=25):
        while True:
            for event in self._check(wait):
                yield event
