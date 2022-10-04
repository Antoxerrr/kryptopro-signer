from urllib.parse import urljoin

import requests
from urllib3.util import SKIP_HEADER

from signer.core.cert import sign_data


class GISMTApi:
    """API для авторизации в ГИС МТ."""

    HOST_URL = 'https://ismp.crpt.ru/api/v3/'
    # proxies = {'https': 'http://127.0.0.1:8888'}
    proxies = {}

    def request_token(self, certificate):
        data_to_sign = self._request_data_to_sign()
        signature = self._sign(data_to_sign['data'], certificate)
        return self._request_auth_token(signature, data_to_sign['uuid'])

    def _request_data_to_sign(self):
        path = 'auth/cert/key'
        url = urljoin(self.HOST_URL, path)
        response = requests.get(url)
        data = response.json()
        return data

    def _request_auth_token(self, signature, uuid):
        payload = dict(uuid=uuid, data=signature)
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Accept-Encoding': SKIP_HEADER,
            'Accept': 'application/json',
            'Connection': None
        }
        path = 'auth/cert/'
        url = urljoin(self.HOST_URL, path)
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        if response.status_code != 200:
            error_message = response_data.get('error_message')
            default_message = 'Сообщение об ошибке не найдено'
            raise TokenRequestError(error_message or default_message)
        return response_data.get('token')

    def _sign(self, data: str, certificate):
        try:
            return sign_data(data, certificate)
        except Exception as exc:
            raise SignatureError(str(exc))


class BaseError(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class TokenRequestError(BaseError): pass
class SignatureError(BaseError): pass
