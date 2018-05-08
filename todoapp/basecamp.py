import json
import random
import requests


class BasecampConnection(object):
    BASECAMP_API_ENDPOINT = 'https://3.basecampapi.com/'
    AUTHORIZATION_URL = 'https://launchpad.37signals.com/authorization.json'
    CREATE_TODO_ENDPOINT = '/buckets/{}/todolists/{}/todos.json'
    UPLOAD_ATTACHMENT_ENDPOINT = '/attachments.json'

    def __init__(self, access_token):
        self.access_token = access_token
        self.PROJECT_ID = '1190341'
        self.TODO_LIST_ID = '657088489'
        self.ACCOUNT_ID = None

    def _get_auth_header(self):
        return {'Authorization': 'Bearer {}'.format(self.access_token)}

    def _get_account_id(self):
        if not self.ACCOUNT_ID:
            resp = requests.get(self.AUTHORIZATION_URL, headers=self._get_auth_header())
            resp = json.loads(resp.content)
            self.ACCOUNT_ID = resp['accounts'][0]['id']
        return self.ACCOUNT_ID

    def _get_account_endpoint(self):
        return '{}{}'.format(
            self.BASECAMP_API_ENDPOINT,
            self._get_account_id(),
        )

    def create_todo(self, title, attachable_sgid):
        url = '{}{}'.format(
            self._get_account_endpoint(),
            self.CREATE_TODO_ENDPOINT.format(self.PROJECT_ID, self.TODO_LIST_ID),
        )

        return requests.post(url, headers=self._get_auth_header(), json={
            'content': title,
            'description': '<bc-attachment sgid="{}"></bc-attachment>'.format(attachable_sgid)
        })

    def upload_attachment(self, audio_file):
        name = 'mz{}.m4a'.format(random.randint(0, 100))
        url = '{}{}?name={}'.format(
            self._get_account_endpoint(),
            self.UPLOAD_ATTACHMENT_ENDPOINT,
            name,
        )

        headers = self._get_auth_header()
        headers.update({
            'Content-Type': 'audio/x-m4a',
        })
        resp = requests.post(url, headers=headers, data=audio_file)
        return json.loads(resp.content)['attachable_sgid']

    def create_todo_with_attachment(self, title, audio_file):
        attachment_sgid = self.upload_attachment(audio_file)
        self.create_todo(title, attachment_sgid)
