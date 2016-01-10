import datetime

import requests

from src import ApiProtocol


class ApiClient:

    def __init__(self, app_id, app_secret):
        self.version = "1.0"
        self.api_entry = "https://open.koudaitong.com/api/entry?"
        self.format = "json"
        self.sign_method = "md5"
        self.default_useragent = "KdtApiSdk Client v0.1"

        self.app_id = app_id
        self.app_secret = app_secret

    def get(self, method, **params):
        header = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
        }
        # url = self.api_entry + self.build_param_str(self.build_complete_params(method, **params))
        url = self.api_entry + self.get_params(method, **params)
        print('url: ', url)
        response = requests.get(url, headers=header)

        response_text = repr(response.text)
        result = response_text.split(',')
        # for i in result:
        #     print(i, sep='\n')

        # print(response.text)
        return response.text

    # def post(self, method, filekey, *filepath, **params):
    #     url = self.api_entry + self.get_params(method, **params)



    def get_params(self, method, **params):
        return self.build_param_str(self.build_complete_params(method, **params))

    def build_param_str(self, params):
        result = ''
        for index,key in enumerate(params):
            if index == 0:
                result += (key + '=' + str(params[key]))
            else:
                result += ('&' + key + '=' + str(params[key]))
        # print('result: ',result)

        # result1 = str(result.encode('utf-8')).replace("%3A", ":")\
        #             .replace("%2F", "/")\
        #             .replace("%26", "&")\
        #             .replace("%3D", "=")\
        #             .replace("%3F", "?")
        # print('result1: ', result1)
        return result



    def build_complete_params(self, method, **params):
        common_params = self.get_common_params(method)
        for key in params:
            if key in common_params:
                raise ValueError()
            else:
                common_params[key] = params[key]
        # c = ApiProtocol.ApiProtocol()
        # c.sign()
        common_params[ApiProtocol.ApiProtocol.SIGN_KEY] = ApiProtocol.ApiProtocol().sign(self.app_secret, **common_params)
        # print('build_complete_params: ',common_params)
        return common_params


    def get_common_params(self, method):
        common_dict = {
            ApiProtocol.ApiProtocol.APP_ID_KEY : self.app_id,
            ApiProtocol.ApiProtocol.METHOD_KEY : method,
            ApiProtocol.ApiProtocol.TIMESTAMP_KEY : str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            # ApiProtocol.ApiProtocol.TIMESTAMP_KEY : '2016-01-06 20:06:39',
            ApiProtocol.ApiProtocol.FORMAT_KEY : self.format,
            ApiProtocol.ApiProtocol.SIGN_METHOD_KEY : self.sign_method,
            ApiProtocol.ApiProtocol.VERSION_KEY : self.version
        }
        # print('get_common_params:',common_dict)
        return common_dict


if __name__ == '__main__':
    id = '290c00897561005101'
    test_dict = {
        # 'timestamp' : '2013-05-06 13:52:03',
        # 'format' : 'json',
        # 'app_id' : 'test',
        # 'v' : 1.0,
        # 'sign_method' : 'md5',
        'num_iid' : '203218118'
        }
    app_sert = '52813f143dbcc7854815a12043a48213'
    method = 'kdt.item.get'

    test = ApiClient(id, app_sert)
    # test.build_complete_params(method, **test_dict)
    # test.build_param_str(test.build_complete_params(method, **test_dict))
    # test.get_common_params('hello')
    test.get(method, **test_dict)
