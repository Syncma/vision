import logging
import requests

from datetime import datetime, timedelta
from json import JSONDecodeError

from . import BaseAPI
from bottle import default_app

app = default_app()


class BaiduAIP(BaseAPI):
    access_token = None
    at_expire = datetime.now()

    def __init__(self, client_id=None, client_secret=None):
        super().__init__()
        if client_id is None:
            client_id = app.config['baidu.aip.client_id'],
        if client_secret is None:
            client_secret = app.config['baidu.aip.client_secret'],

        self.client_id = client_id
        self.client_secret = client_secret

    def before_request(self, kwargs):
        self.check_access_token()

        kwargs['url'] += '?access_token=' + BaiduFace.access_token
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 30

    def check_access_token(self):
        if BaiduFace.at_expire > datetime.now():
            return

        params = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }
        resp = requests.get('https://aip.baidubce.com/oauth/2.0/token', params)
        if not resp.ok:
            logging.error('baidu resp %s %s', resp.status_code, resp.text)
            raise RuntimeError('get baidu access token failed')

        resp_json = resp.json()
        expires_in = resp_json['expires_in']
        BaiduFace.at_expire = datetime.now() + timedelta(seconds=expires_in)
        BaiduFace.access_token = resp_json['access_token']

    @staticmethod
    def parse_response(resp):
        try:
            result = resp.json()
        except JSONDecodeError:
            result = {
                'error_code': -1,
                'error_msg': 'request failed',
            }
        if result["error_code"] == 0:
            is_ok = True
        else:
            is_ok = False

        return result, is_ok


class BaiduFace(BaiduAIP):
    def get_base_url(self):
        return 'https://aip.baidubce.com/rest/2.0/face/v3'

    def detect(self, image_content_b64):
        face_fields = 'age,beauty,expression,gender'
        resp = self.post(
            '/detect', {
                'image': image_content_b64,
                'image_type': "BASE64",
                'face_fields': face_fields,
            })
        result, is_ok = self.parse_response(resp)
        return result, is_ok
