import datetime
import requests
from src.apiprotocol import ApiProtocol


class ApiClient:

    def __init__(self, app_id, app_secret):
        '''Fill the system's parameters which will not be changed in every invoking'''
        self.version = "1.0"
        self.api_entry = "https://open.koudaitong.com/api/entry?"
        self.format = "json"
        self.sign_method = "md5"
        self.default_useragent = "KdtApiSdk Client v0.1"

        self.app_id = app_id
        self.app_secret = app_secret

    def get(self, method, **params):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                           AppleWebKit/537.36 (KHTML, like Gecko) \
                           Chrome/47.0.2526.106 Safari/537.36'
        }
        url = self.api_entry + self.get_params(method, **params)
        # print('url: ', url)
        response = requests.get(url, headers=header)
        return response.text

    def get_params(self, method, **params):
        return self.build_param_str(
                self.build_complete_params(method, **params))

    def build_param_str(self, params):
        result = ''
        for index, key in enumerate(params):
            if index == 0:
                result += (key + '=' + str(params[key]))
            else:
                result += ('&' + key + '=' + str(params[key]))
        return result

    def build_complete_params(self, method, **params):
        common_params = self.get_common_params(method)
        for key in params:
            if key in common_params:
                raise ValueError()
            else:
                common_params[key] = params[key]
        common_params[ApiProtocol.SIGN_KEY] = ApiProtocol().sign(
                self.app_secret,**common_params)
        return common_params

    def get_common_params(self, method):
        common_dict = {
            ApiProtocol.APP_ID_KEY: self.app_id,
            ApiProtocol.METHOD_KEY: method,
            ApiProtocol.TIMESTAMP_KEY: str(
                    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            ApiProtocol.FORMAT_KEY: self.format,
            ApiProtocol.SIGN_METHOD_KEY: self.sign_method,
            ApiProtocol.VERSION_KEY: self.version
        }
        # print('get_common_params:',common_dict)
        return common_dict


